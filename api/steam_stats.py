"""Retrieves Steam User Data using Steam Web API"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Secrets Configuration
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

# Verify that the environment variables are loaded correctly
if not STEAM_API_KEY or not STEAM_ID:
    raise ValueError(
        "Missing STEAM_API_KEY or STEAM_ID in environment variables")

# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (10, 15)

# Steam Web API endpoints
PLAYER_SUMMARIES = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
RECENTLY_PLAYED_GAMES = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/"


def get_player_summaries():
    """Get Player Summaries from Steam
    Fetch basic profile information for a list of 64-bit Steam IDs"""
    # Construct the URL with all parameters
    url = f"{PLAYER_SUMMARIES}?key={STEAM_API_KEY}&steamids={STEAM_ID}"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None


def get_recently_played_games():
    """Fetch a list of games a player has played in the last two weeks"""
    url = f"{RECENTLY_PLAYED_GAMES}?key={
        STEAM_API_KEY}&steamid={STEAM_ID}&format=json"
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    try:
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None
