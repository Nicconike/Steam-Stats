"""Scrape Steam Workshop Data"""
import json
import requests
from bs4 import BeautifulSoup, Tag

# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (10, 15)


def fetch_workshop_item_links(steam_id):
    """Fetch each workshop item's link"""
    url = f"https://steamcommunity.com/id/{steam_id}/myworkshopfiles/"
    item_links = []

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        workshop_items = soup.find_all("div", class_="workshopItem")

        for item in workshop_items:
            link_tag = item.find("a", class_="ugc")
            if link_tag and "href" in link_tag.attrs:
                item_links.append(link_tag["href"])
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(
            f"An unexpected error occurred while fetching workshop item links: {e}")

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
                    stats[key] = int(value)
        else:
            print(f"Could not find stats table at {item_url}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(
            f"An unexpected error occurred while fetching individual workshop stats: {e}")

    return stats


def save_to_file(data, filename):
    """Save fetched data to a file in JSON format"""
    if data is not None:
        with open(filename, 'w', encoding='utf-8') as file:
            # Use json.dump to write the JSON data to the file
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    else:
        print("No data to save")


def fetch_all_workshop_stats(item_links):
    """Fetch Stats for all of the items in Steam User's Workshop"""
    all_stats = []
    for link in item_links:
        try:
            stats = fetch_individual_workshop_stats(link)
            if stats:
                all_stats.append(stats)
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {link}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while fetching stats for {
                  link}: {e}")
    return {"individual_stats": all_stats}


if __name__ == "__main__":
    links = fetch_workshop_item_links("gr1mmr3aper")
    workshop_data = fetch_all_workshop_stats(links)
    save_to_file(workshop_data, "workshop_data.json")
