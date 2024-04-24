"""Retrieves Steam User Data using Steam Web API"""
import json
from zoneinfo import ZoneInfo  # Python 3.9 and newer
from datetime import datetime, timezone
import os
import pygal
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


def generate_svg_for_recently_played_games(player_data):
    """Generate SVG for Recently Played Games in Steam in the last 2 weeks"""
    bar_chart = pygal.HorizontalBar(
        legend_at_bottom=True, rounded_bars=15, show_legend=True)
    bar_chart.title = "Playtime in the Last Two Weeks (hours)"

    # Add data to the chart
    if player_data and "response" in player_data and "games" in player_data["response"]:
        for game in player_data["response"]["games"]:
            if "name" in game and "playtime_2weeks" in game:
                playtime_minutes = game["playtime_2weeks"]
                playtime_hours = playtime_minutes / 60  # Convert minutes to hours for plotting

                # Determine the label based on the original playtime in minutes
                if playtime_minutes >= 60:
                    # Display in hours if 60 mins or more
                    label = f"{game["name"]} ({playtime_hours:.2f} hrs)"
                else:
                    # Display in minutes if less than 60
                    label = f"{game["name"]} ({playtime_minutes} mins)"

                # Add to chart using the hours value for consistency in scaling
                bar_chart.add(label, playtime_hours)
    else:
        print("No game data available to display")

    # Return the SVG data as a string to embed directly in Markdown
    return bar_chart.render(is_unicode=True)


def save_to_file(data, filename):
    """Save fetched data to a file in JSON format"""
    if data is not None:
        with open(filename, 'w', encoding='utf-8') as file:
            # Use json.dump to write the JSON data to the file
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    else:
        print("No data to save")


if __name__ == "__main__":
    player_summary = get_player_summaries()
    recently_played_games = get_recently_played_games()

    generate_svg_for_recently_played_games(recently_played_games)
    print(generate_svg_for_recently_played_games)
    save_to_file(player_summary, "player_summaries.json")
    save_to_file(recently_played_games, "recently_played_games.json")
