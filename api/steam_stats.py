"""Retrieves Steam User Data using Steam Web API"""
from zoneinfo import ZoneInfo  # Python 3.9 and newer
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Secrets Configuration
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")
STEAM_APP_ID = os.getenv("STEAM_APP_ID")

# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (10, 15)

# Steam Web API endpoints
PLAYER_SUMMARIES = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
RECENTLY_PLAYED_GAMES = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/"

# Steam Account Status Mapping
PERSONASTATE_MAPPING = {
    0: "Offline",
    1: "Online",
    2: "Busy",
    3: "Away",
    4: "Snooze",
    5: "Looking to Trade",
    6: "Looking to Play"
}


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


def process_player_summary_data(player_data):
    """Process the retrieved summary data"""
    # Convert Unix timestamp to IST timezone and format it
    lastlogoff_ist = datetime.fromtimestamp(
        player_data["lastlogoff"], tz=timezone.utc).astimezone(ZoneInfo("Asia/Kolkata"))
    lastlogoff_str = lastlogoff_ist.strftime("%d/%m/%Y %H:%M:%S")

    # Extract other fields
    process_data = {
        "personaname": player_data["personaname"],
        "profileurl": player_data["profileurl"],
        "avatarmedium": player_data["avatarmedium"],
        "lastlogoff": lastlogoff_str,
        "personastate": PERSONASTATE_MAPPING.get(player_data["personastate"], "Unknown"),
        "gameid": player_data.get("gameid")
    }
    return process_data
