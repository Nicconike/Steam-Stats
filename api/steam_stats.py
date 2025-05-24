"""Retrieves Steam User Stats using Steam Web API"""

import logging
import time
import requests
from api.utils import get_steam_credentials

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (25, 30)
MAX_RETRIES = 5

# Steam Web API endpoints
PLAYER_SUMMARIES = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
RECENTLY_PLAYED_GAMES = (
    "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/"
)


def get_player_summaries():
    """Get Player Summaries from Steam
    Fetch basic profile information for a list of 64-bit Steam IDs"""
    creds = get_steam_credentials()
    steam_id = creds["steam_id"]
    api_key = creds["api_key"]

    url = f"{PLAYER_SUMMARIES}?key={api_key}&steamids={steam_id}"
    for _ in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 2))
                logger.warning("Rate limited. Sleeping for %s seconds", retry_after)
                time.sleep(retry_after)
                continue
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error("HTTP error: %s", err)
            return None
        except requests.exceptions.RequestException as err:
            logger.error("Request error: %s", err)
            return None
    logger.error("Max retries reached. Failed to fetch player summaries.")
    return None


def get_recently_played_games():
    """Fetch a list of games a player has played in the last two weeks"""
    creds = get_steam_credentials()
    steam_id = creds["steam_id"]
    api_key = creds["api_key"]

    url = f"{RECENTLY_PLAYED_GAMES}?key={api_key}&steamid={steam_id}&format=json"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if data["response"].get("total_count", 0) == 0:
            return None
        return data
    except requests.exceptions.HTTPError as err:
        logger.error("HTTP error occurred: %s", err)
        return None
    except requests.exceptions.RequestException as err:
        logger.error("An error occurred: %s", err)
        return None
