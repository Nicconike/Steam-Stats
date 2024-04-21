"""Scrape Workshop Data and embed it in Readme"""
import json
import os
import time
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup, Tag

# Load environment variables from .env file
load_dotenv()

# Secrets Configuration
STEAM_ID = os.getenv('STEAM_CUSTOM_ID')

# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (10, 15)


def fetch_workshop_item_links(steam_id):
    """Fetch each workshop item's link"""
    url = f"https://steamcommunity.com/id/{steam_id}/myworkshopfiles/"
    print(f"Fetching items from {steam_id}'s Workshop")

    # Start the timer
    start_time = time.time()

    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(response.content, 'html.parser')
    workshop_items = soup.find_all('div', class_='workshopItem')

    item_links = []
    for item in workshop_items:
        link_tag = item.find('a', class_='ugc')
        if link_tag and 'href' in link_tag.attrs:
            item_links.append(link_tag['href'])

    # End the timer
    end_time = time.time()
    # Calculate the total time taken
    total_time = end_time - start_time
    print(f"Total time taken to fetch the data: {total_time} seconds")

    return item_links


def fetch_workshop_item_link(steam_id):
    """Fetch each workshop item's link"""
    url = f"https://steamcommunity.com/id/{steam_id}/myworkshopfiles/?p=1"
    print(f"Fetching items from {steam_id}'s Workshop")
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(response.content, 'html.parser')
    workshop_items = soup.find_all("div", class_='workshopItem')
    pagination = soup.find_all("div", class_="workshopBrowsePagingControls")
    # pages = pagination.find_all("a", class_="pagelink")

    item_links = []
    pages = []
    for item in workshop_items:
        link_tag = item.find('a', class_='ugc')
        if link_tag and 'href' in link_tag.attrs:
            item_links.append(link_tag['href'])

    for item in pagination:
        page_tag = item.find("a", class_="pagelink")
        if page_tag and "href" in page_tag.attrs:
            pages.append(page_tag["href"])

    return item_links, pages


def fetch_individual_workshop_stats(item_url):
    """Fetch Author Stats from a Workshop Item"""
    response = requests.get(item_url, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(response.content, 'html.parser')
    stats_table = soup.find('table', class_='stats_table')
    stats = {}
    if isinstance(stats_table, Tag):
        for row in stats_table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                key = cells[1].text.strip().lower().replace(' ', '_')
                value = cells[0].text.strip().replace(',', '')
                stats[key] = int(value)
    else:
        print(f"Could not find stats table at {item_url}")
    return stats


def fetch_all_workshop_stats(item_links):
    """Fetch the Stats for all of the items in Steam User's Workshop"""
    all_stats = []
    for link in item_links:
        stats = fetch_individual_workshop_stats(link)
        all_stats.append(stats)
    return all_stats


def save_to_file(data, filename):
    """Save fetched data to a file in JSON format"""
    if data is not None:
        with open(filename, 'w', encoding='utf-8') as file:
            # Use json.dump to write the JSON data to the file
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    else:
        print("No data to save")


# Entry Code
if __name__ == "__main__":
    links = fetch_workshop_item_links(STEAM_ID)
    if links:  # Check if any links were found
        workshop_data = fetch_all_workshop_stats(links)
        save_to_file(links, "links.json")
        save_to_file(workshop_data, "workshop_data.json")
    else:
        print("No workshop item links were found")
