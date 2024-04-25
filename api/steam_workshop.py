"""Scrape Steam Workshop Data"""
import requests
from bs4 import BeautifulSoup, Tag

# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (10, 15)


def fetch_workshop_item_links(steam_id):
    """Fetch each workshop item's link"""
    url = f"https://steamcommunity.com/id/{steam_id}/myworkshopfiles/"

    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(response.content, "html.parser")
    workshop_items = soup.find_all("div", class_="workshopItem")

    item_links = []
    for item in workshop_items:
        link_tag = item.find("a", class_="ugc")
        if link_tag and "href" in link_tag.attrs:
            item_links.append(link_tag["href"])

    return item_links


def fetch_individual_workshop_stats(item_url):
    """Fetch Author Stats from a Workshop Item"""
    response = requests.get(item_url, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(response.content, "html.parser")
    stats_table = soup.find("table", class_="stats_table")
    stats = {}
    if isinstance(stats_table, Tag):
        for row in stats_table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) == 2:
                key = cells[1].text.strip().lower().replace(' ', '_')
                value = cells[0].text.strip().replace(',', '')
                stats[key] = int(value)
    else:
        print(f"Could not find stats table at {item_url}")
    return stats


def fetch_all_workshop_stats(item_links):
    """Fetch Stats for all of the items in Steam User's Workshop and sum them up"""
    all_stats = []
    for link in item_links:
        stats = fetch_individual_workshop_stats(link)
        all_stats.append(stats)

    # Calculate the totals
    total_unique_visitors = sum(item["unique_visitors"] for item in all_stats)
    total_current_subscribers = sum(
        item["current_subscribers"] for item in all_stats)
    total_current_favorites = sum(
        item["current_favorites"] for item in all_stats)

    return {
        "total_unique_visitors": total_unique_visitors,
        "total_current_subscribers": total_current_subscribers,
        "total_current_favorites": total_current_favorites,
        "individual_stats": all_stats
    }
