"""Retrieves Steam User Stats using Steam Web API"""
# Disable pylint warnings for false positives
# pylint: disable=duplicate-code
import os
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Required Secrets Configuration
STEAM_ID = os.environ["INPUT_STEAM_ID"]
STEAM_API_KEY = os.environ["INPUT_STEAM_API_KEY"]

# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (25, 30)

# Steam Web API endpoints
PLAYER_SUMMARIES = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
RECENTLY_PLAYED_GAMES = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/"


def get_player_summaries():
    """Get Player Summaries from Steam
    Fetch basic profile information for a list of 64-bit Steam IDs"""
    # Construct the URL with all parameters
    url = PLAYER_SUMMARIES + "?key=" + STEAM_API_KEY + "&steamids=" + STEAM_ID
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as err:
        logger.error("HTTP error occurred: %s", err)
        return None
    except requests.exceptions.RequestException as err:
        logger.error("An error occurred: %s", err)
        return None


def get_recently_played_games():
    """Fetch a list of games a player has played in the last two weeks"""
    url = RECENTLY_PLAYED_GAMES + "?key=" + STEAM_API_KEY + \
        "&steamid=" + STEAM_ID + "&format=json"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if data["response"].get("total_count", 0) == 0:
            return None
        logger.info("Successfully fetched recently played games")
        return data
    except requests.exceptions.HTTPError as err:
        logger.error("HTTP error occurred: %s", err)
        return None
    except requests.exceptions.RequestException as err:
        logger.error("An error occurred: %s", err)
        return None
