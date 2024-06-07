"""Scrape Steam Workshop Data"""
import os
import requests
from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv

load_dotenv()

# Required Secrets Configuration
STEAM_API_KEY = os.environ["INPUT_STEAM_API_KEY"]
STEAM_CUSTOM_ID = os.environ["INPUT_STEAM_CUSTOM_ID"]


# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (25, 30)

GET_SERVER_INFO_URL = 'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/'


def get_server_info(api_key):
    """Fetch server information from the Steam Web API"""
    try:
        response = requests.get(GET_SERVER_INFO_URL, params={
                                'key': api_key}, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching server info: {e}")
        return None


def is_server_online(api_key):
    """Check if the server is online based on the GetServerInfo response"""
    serverinfo = get_server_info(api_key)
    if serverinfo and 'servertime' in serverinfo:
        return True
    return False


def extract_links(workshop_items):
    """Extract links from workshop items"""
    links = []
    for item in workshop_items:
        link_tag = item.find("a", class_="ugc")
        if link_tag and "href" in link_tag.attrs:
            links.append(link_tag["href"])
    return links


def has_next_page(soup):
    """Check if there is a next page"""
    paging_controls = soup.find("div", class_="workshopBrowsePagingControls")
    if paging_controls:
        next_page_link = paging_controls.find(
            "a", class_="pagebtn", string=">")
        return next_page_link is not None
    return False


def handle_request_exception(e):
    """Handle request exceptions"""
    if isinstance(e, requests.exceptions.ConnectionError):
        print("Connection error occurred. Please check your network connection")
    elif isinstance(e, requests.exceptions.Timeout):
        print("Request timed out. Please try again later")
    elif isinstance(e, requests.exceptions.TooManyRedirects):
        print("Too many redirects. Check the URL and try again")
    elif isinstance(e, requests.exceptions.HTTPError):
        print(f"HTTP error occurred: {
              e.response.status_code} - {e.response.reason}")
    else:
        print(f"An error occurred: {e}")


def fetch_workshop_item_links(steam_id, api_key):
    """Fetch each workshop item's link, navigating through all pages"""
    if not is_server_online(api_key):
        raise ConnectionError(
            "Steam Community is currently offline. Please try again later")

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

            if not workshop_items:
                print(f"No workshop items found on page {page_number}")
                break

            item_links.extend(extract_links(workshop_items))

            if not has_next_page(soup):
                break

            page_number += 1

        except requests.exceptions.RequestException as e:
            handle_request_exception(e)
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
                    key = cells[1].text.strip().lower().replace(" ", "_")
                    value = cells[0].text.strip().replace(",", "")
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
    stats["unique_visitors"] = stats.get("unique_visitors", 0)
    stats["current_subscribers"] = stats.get("current_subscribers", 0)
    stats["current_favorites"] = stats.get("current_favorites", 0)

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
