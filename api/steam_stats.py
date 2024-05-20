"""Retrieves Steam User Data using Steam Web API"""
import os
import requests
import svgwrite

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


def generate_svg(player_data, output_file):
    """Generate SVG for Steam Player Summary"""
    dwg = svgwrite.Drawing(output_file, profile='tiny',
                           size=('600px', '200px'))

    # Add background rectangle for the card
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'),
            rx=10, ry=10, class_='background'))

    # Access the player data
    player = player_data["response"]["players"][0]

    # Add avatar image with hyperlink
    avatarmedium = player["avatarmedium"]
    profileurl = player["profileurl"]
    avatar_group = dwg.g(class_='avatar-group')
    avatar_group.add(dwg.image(avatarmedium, insert=(
        20, 50), size=(64, 64), class_='avatar'))
    avatar_group.add(dwg.rect(insert=(20, 50), size=(64, 64),
                     fill='none', stroke='none', id='avatar-link'))
    dwg.add(avatar_group)

    # Add persona name in the middle
    personaname = player["personaname"]
    dwg.add(dwg.text(f'{personaname}', insert=('50%', 40), class_='name'))

    # Add location country code on the right side
    loccountrycode = player.get("loccountrycode", "N/A").lower()
    if loccountrycode != "n/a":
        flag_url = f"https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.0.0/flags/4x3/{
            loccountrycode}.svg"
        dwg.add(dwg.image(flag_url, insert=(520, 20),
                size=(64, 48), class_='location'))

    # Add JavaScript for hyperlink functionality
    dwg.script(content=f"""
        document.getElementById('avatar-link').addEventListener('click', function() {{
            window.open('{profileurl}', '_blank');
        }});
    """)

    dwg.save()
