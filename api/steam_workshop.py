"""Scrape Steam Workshop Data"""

import logging
import requests
from bs4 import BeautifulSoup, Tag

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (25, 30)

GET_SERVER_INFO_URL = "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/"


def get_server_info(api_key):
    """Fetch server information from the Steam Web API"""
    try:
        response = requests.get(
            GET_SERVER_INFO_URL, params={"key": api_key}, timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching server info: %s", str(e))
        return None


def is_server_online(api_key):
    """Check if the server is online based on the GetServerInfo response"""
    serverinfo = get_server_info(api_key)
    if serverinfo and "servertime" in serverinfo:
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
        next_page_link = paging_controls.find("a", class_="pagebtn", string=">")
        return next_page_link is not None
    return False


def handle_request_exception(e):
    """Handle request exceptions"""
    if isinstance(e, requests.exceptions.ConnectionError):
        logger.error("Connection error occurred. Please check your network connection")
    elif isinstance(e, requests.exceptions.Timeout):
        logger.error("Request timed out. Please try again later")
    elif isinstance(e, requests.exceptions.TooManyRedirects):
        logger.error("Too many redirects. Check the URL and try again")
    elif isinstance(e, requests.exceptions.HTTPError):
        logger.error(
            "HTTP error occurred: %s - %s",
            str(e.response.status_code),
            str(e.response.reason),
        )
    else:
        logger.error("An error occurred: %s", str(e))


def fetch_workshop_item_links(steam_id, api_key):
    """Fetch each workshop item's link, navigating through all pages"""
    if not is_server_online(api_key):
        raise ConnectionError(
            "Steam Community is currently offline. Please try again later"
        )

    base_url = "https://steamcommunity.com/id/" + str(steam_id) + "/myworkshopfiles/"
    item_links = []
    page_number = 1

    while True:
        url = str(base_url) + "?p=" + str(page_number)
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            workshop_items = soup.find_all("div", class_="workshopItem")

            if not workshop_items:
                logger.info("No workshop items found on page %d", page_number)
                break

            item_links.extend(extract_links(workshop_items))

            if not has_next_page(soup):
                break

            page_number += 1

        except requests.exceptions.RequestException as e:
            handle_request_exception(e)
            break
        except AttributeError as e:
            logger.error(
                "Parsing error: %s. The structure of the page might have changed",
                str(e),
            )
            break

    if not item_links and page_number == 1:
        raise ValueError("No items were found in your Steam Workshop")

    return item_links


def parse_stats_table(stats_table):
    """Parse the stats table and return a dictionary of stats"""
    stats = {}
    if not isinstance(stats_table, Tag):
        return stats
    for row in stats_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 2:
            key = cells[1].text.strip().lower().replace(" ", "_")
            value = cells[0].text.strip().replace(",", "")
            try:
                stats[key] = int(value) if value else 0
            except ValueError:
                logger.error("Could not convert value to int: %s", str(value))
                stats[key] = 0
    return stats


def fetch_individual_workshop_stats(item_url):
    """Fetch Author Stats from a Workshop Item"""
    stats = {}

    try:
        response = requests.get(item_url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        stats_table = soup.find("table", class_="stats_table")

        if isinstance(stats_table, Tag):
            stats = parse_stats_table(stats_table)
        else:
            logger.info("Could not find stats table at %s", str(item_url))
    except (requests.exceptions.RequestException, AttributeError) as e:
        handle_request_exception(e)
        return {}

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
        except (requests.exceptions.RequestException, AttributeError) as e:
            handle_request_exception(e)

    total_unique_visitors = sum(item.get("unique_visitors", 0) for item in all_stats)
    total_current_subscribers = sum(
        item.get("current_subscribers", 0) for item in all_stats
    )
    total_current_favorites = sum(
        item.get("current_favorites", 0) for item in all_stats
    )

    return {
        "total_unique_visitors": total_unique_visitors,
        "total_current_subscribers": total_current_subscribers,
        "total_current_favorites": total_current_favorites,
        "individual_stats": all_stats,
    }
