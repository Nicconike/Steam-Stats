# TESTING PHASE
"""Retrieves and displays Steam User Data in README using Steam Web API"""
import svgwrite
from zoneinfo import ZoneInfo  # Python 3.9 and newer
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Secrets Configuration
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
STEAM_ID = os.getenv('STEAM_ID')
STEAM_APP_ID = os.getenv('STEAM_APP_ID')

# A reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (10, 15)

# Steam Web API endpoint
PLAYER_SUMMARIES_URL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
PLAYER_ACHIEVEMENTS_URL = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
USER_STATS_FOR_GAME_URL = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
RECENTLY_PLAYED_GAMES_URL = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/"

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
    url = f"{PLAYER_SUMMARIES_URL}?key={STEAM_API_KEY}&steamids={STEAM_ID}"
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


def get_player_achievements():
    """Fetch a list of achievements for a user by app id"""
    url = f"{PLAYER_ACHIEVEMENTS_URL}?appid={
        STEAM_APP_ID}&key={STEAM_API_KEY}&steamid={STEAM_ID}"
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


def get_user_stats_for_game():
    """Fetch user stats for a game by app id"""
    url = f"{PLAYER_ACHIEVEMENTS_URL}?appid={
        STEAM_APP_ID}&key={STEAM_API_KEY}&steamid={STEAM_ID}"
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


def get_recently_played_games():
    """Fetch a list of games a player has played in the last two weeks"""
    url = f"{RECENTLY_PLAYED_GAMES_URL}?key={
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
    # Convert Unix timestamp to IST timezone and format it
    lastlogoff_ist = datetime.fromtimestamp(
        player_data['lastlogoff'], tz=timezone.utc).astimezone(ZoneInfo("Asia/Kolkata"))
    lastlogoff_str = lastlogoff_ist.strftime('%d/%m/%Y %H:%M:%S')

    # Extract other fields
    processed_data = {
        'personaname': player_data['personaname'],
        'profileurl': player_data['profileurl'],
        'avatarmedium': player_data['avatarmedium'],
        'lastlogoff': lastlogoff_str,
        'personastate': player_data['personastate'],
        'gameid': player_data.get('gameid')
    }
    return processed_data


def generate_markdown(processed_data):
    """Generate Markdown content for the player data."""
    # Map the personastate number to its string representation
    personastate_str = PERSONASTATE_MAPPING.get(
        processed_data['personastate'], "Unknown")

    # Initialize markdown content
    markdown_content = f"""
## Steam User Summary for {processed_data['personaname']}

- **Persona State:** {personastate_str}
- **Last Logoff (IST):** {processed_data['lastlogoff']}
- **Profile URL:** [Visit Profile]({processed_data['profileurl']})
- **Avatar:** ![Avatar]({processed_data['avatarmedium']})
"""

    # Add game status if the user is in-game
    if 'gameid' in processed_data and processed_data['gameid']:
        markdown_content += f"\n- **Currently In-Game:** {
            processed_data['gameid']}"

    return markdown_content


def generate_markdown_for_achievements(achievements_data):
    """Generate Markdown content for player achievements."""
    game_name = achievements_data['playerstats']['gameName']
    achievements = achievements_data['playerstats']['achievements']

    markdown_content = f"## Achievements for {game_name}\n"
    for achievement in achievements:
        markdown_content += f"- {achievement['apiname']}: Achieved at {datetime.fromtimestamp(
            achievement['unlocktime'], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}\n"
    return markdown_content


def generate_markdown_for_recently_played_games(recently_played_data):
    """Generate Markdown content for recently played games."""
    total_count = recently_played_data['response']['total_count']
    games = recently_played_data['response']['games']

    markdown_content = f"## Recently Played Games (Total: {total_count})\n"
    for game in games:
        markdown_content += f"- {game['name']}: Playtime last 2 weeks: {
            game['playtime_2weeks']} mins, Total playtime: {game['playtime_forever']} mins\n"
    return markdown_content


""" def generate_svg_for_recently_played_games(recently_played_games):
    # Create an SVG drawing instance
    dwg = svgwrite.Drawing()

    # Set up the title for the card
    dwg.add(dwg.text('Steam\'s Recently Played Games',
            insert=(0, 20), fill='black'))

    # Calculate the maximum playtime in the last two weeks for scaling the bars
    max_playtime_2weeks = max(game['playtime_2weeks']
                              for game in recently_played_games['response']['games'])

    # Add the game names and playtime bars to the SVG
    for index, game in enumerate(recently_played_games['response']['games']):
        game_name = game['name']
        playtime_2weeks = game['playtime_2weeks']
        playtime_forever = game['playtime_forever']

        # Scale the playtime to fit the bar width
        # Example scaling factor
        bar_width_2weeks = (playtime_2weeks / max_playtime_2weeks) * 200

        # Add game name text
        dwg.add(dwg.text(f'{game_name}', insert=(
            0, 40 + index * 30), fill='black'))

        # Add bars for playtime in the last two weeks
        dwg.add(dwg.rect(insert=(100, 30 + index * 30),
                size=(bar_width_2weeks, 10), fill='blue'))

        # Add text for playtime
        dwg.add(dwg.text(f'{playtime_2weeks} hrs', insert=(
            bar_width_2weeks + 110, 40 + index * 30), fill='black'))

    # Return the SVG content as a string
    return dwg.tostring() """


def update_readme_with_markdown(markdown_content, readme_path="../README.md"):
    """Updates the README.md file with the provided Markdown content."""
    start_marker = "<!-- Steam-Stats start -->"
    end_marker = "<!-- Steam-Stats end -->"

    # Read the current README content
    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.read()

    # Find the start and end index for the section to update
    start_index = readme_content.find(start_marker) + len(start_marker)
    end_index = readme_content.find(end_marker)

    # Check if both markers are found
    if start_index == -1 or end_index == -1 or start_index >= end_index:
        print("Error: Markers not found in README.md")
        return

    # Construct the new README content with the updated section
    new_readme_content = (
        readme_content[:start_index] + "\n" +
        markdown_content + "\n" + readme_content[end_index:]
    )

    # Write the updated content back to the README file
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(new_readme_content)


# Entry Code
if __name__ == "__main__":
    player_summary = get_player_summaries()
    player_achievements = get_player_achievements()
    user_stats = get_user_stats_for_game()
    recently_played_games = get_recently_played_games()

    markdown_content = ""
    if player_summary and player_summary['response']['players']:
        player_data = player_summary['response']['players'][0]
        processed_data = process_player_summary_data(player_data)
        markdown_content += generate_markdown(processed_data)

    if player_achievements:
        markdown_content += generate_markdown_for_achievements(
            player_achievements)

    if recently_played_games:
        markdown_content += generate_markdown_for_recently_played_games(
            recently_played_games)

    if markdown_content:
        update_readme_with_markdown(markdown_content)
        print("README.md has been successfully updated.")
    else:
        print("Failed to fetch or process data.")
