"""Scrape Steam Workshop Data"""
import requests
from bs4 import BeautifulSoup, Tag

# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (10, 15)


def fetch_workshop_item_links(steam_id):
    """Fetch each workshop item's link, navigating through all pages"""
    base_url = f"https://steamcommunity.com/id/{steam_id}/myworkshopfiles/"
    item_links = []
    page_number = 1

    while True:
        url = f"{base_url}?p={page_number}"
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            workshop_items = soup.find_all("div", class_="workshopItem")

            # If no items are found, break the loop
            if not workshop_items:
                print(f"No workshop items found on page {page_number}")
                break

            for item in workshop_items:
                link_tag = item.find("a", class_="ugc")
                if link_tag and "href" in link_tag.attrs:
                    item_links.append(link_tag["href"])

            # Check for the next page link
            paging_controls = soup.find(
                "div", class_="workshopBrowsePagingControls")
            if paging_controls:
                next_page_link = paging_controls.find(
                    "a", class_="pagebtn", string=">")
                if not next_page_link:
                    break  # No more pages
            else:
                break  # No pagination controls found

            page_number += 1

        except requests.exceptions.ConnectionError:
            print("Connection error occurred. Please check your network connection")
            break
        except requests.exceptions.Timeout:
            print("Request timed out. Please try again later")
            break
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects. Check the URL and try again")
            break
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {
                  e.response.status_code} - {e.response.reason}")
            break
        except AttributeError as e:
            print(f"Parsing error: {
                  e}. The structure of the page might have changed")
            break

    if not item_links and page_number == 1:
        raise ValueError("No items were found in your Steam Workshop")

    return item_links


def fetch_individual_workshop_stats(item_url):
    """Fetch Author Stats from a Workshop Item"""
    stats = {}

    try:
        response = requests.get(item_url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        stats_table = soup.find("table", class_="stats_table")

        if isinstance(stats_table, Tag):
            for row in stats_table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) == 2:
                    key = cells[1].text.strip().lower().replace(' ', '_')
                    value = cells[0].text.strip().replace(',', '')
                    try:
                        stats[key] = int(value) if value else 0
                    except ValueError:
                        print(f"Could not convert value to int: {value}")
                        stats[key] = 0
        else:
            print(f"Could not find stats table at {item_url}")
    except requests.exceptions.ConnectionError:
        print("Connection error occurred. Please check your network connection")
    except requests.exceptions.Timeout:
        print("Request timed out. Please try again later")
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects. Check the URL and try again")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {
              e.response.status_code} - {e.response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except AttributeError as e:
        print(f"Parsing error: {
              e}. The structure of the page might have changed")

    # Ensure all expected stats are present, even if they are zero
    stats['unique_visitors'] = stats.get('unique_visitors', 0)
    stats['current_subscribers'] = stats.get('current_subscribers', 0)
    stats['current_favorites'] = stats.get('current_favorites', 0)

    return stats


def fetch_all_workshop_stats(item_links):
    """Fetch Stats for all of the items in Steam User's Workshop"""
    all_stats = []

    for link in item_links:
        try:
            stats = fetch_individual_workshop_stats(link)
            if stats:
                all_stats.append(stats)
        except requests.exceptions.ConnectionError:
            print(f"Connection error occurred while fetching stats for {
                  link}. Please check your network connection.")
        except requests.exceptions.Timeout:
            print(f"Request timed out while fetching stats for {
                  link}. Please try again later.")
        except requests.exceptions.TooManyRedirects:
            print(f"Too many redirects while fetching stats for {
                  link}. Check the URL and try again.")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred while fetching stats for {
                  link}: {e.response.status_code} - {e.response.reason}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {link}: {e}")

    # Calculate the totals
    total_unique_visitors = sum(item.get("unique_visitors", 0)
                                for item in all_stats)
    total_current_subscribers = sum(
        item.get("current_subscribers", 0) for item in all_stats)
    total_current_favorites = sum(
        item.get("current_favorites", 0) for item in all_stats)

    return {
        "total_unique_visitors": total_unique_visitors,
        "total_current_subscribers": total_current_subscribers,
        "total_current_favorites": total_current_favorites,
        "individual_stats": all_stats
    }
