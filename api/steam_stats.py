"""Retrieves and displays Steam User Data in README using Steam Web API"""
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
        player_data['lastlogoff'], tz=timezone.utc).astimezone(ZoneInfo("Asia/Kolkata"))
    lastlogoff_str = lastlogoff_ist.strftime('%d/%m/%Y %H:%M:%S')

    # Extract other fields
    process_data = {
        'personaname': player_data['personaname'],
        'profileurl': player_data['profileurl'],
        'avatarmedium': player_data['avatarmedium'],
        'lastlogoff': lastlogoff_str,
        'personastate': PERSONASTATE_MAPPING.get(player_data['personastate'], "Unknown"),
        'gameid': player_data.get('gameid')
    }
    return process_data


def generate_markdown(summary_data, recently_played_data):
    """Generate combined Markdown content for player data, achievements, recently played games"""

    # Generate Steam User Summary Markdown
    personastate_str = summary_data['personastate']
    summary_markdown = f"""
## Steam User Summary for {summary_data['personaname']}

- **Steam Status:** {personastate_str}
- **Last Logoff (IST):** {summary_data['lastlogoff']}
- **Profile URL:** [Visit Profile]({summary_data['profileurl']})
- **Avatar:** ![Avatar]({summary_data['avatarmedium']})
"""

    # Add game status if the user is in-game
    if 'gameid' in summary_data and summary_data['gameid']:
        summary_markdown += f"\n- **Currently In-Game:** {
            summary_data['gameid']}"

    # Generate Recently Played Games Markdown
    total_count = recently_played_data['response']['total_count']
    games_markdown = f"## Recently Played Games (Total: {total_count})\n"
    for game in recently_played_data['response']['games']:
        playtime_2weeks = game['playtime_2weeks']
        playtime_forever = game['playtime_forever']

        # Format playtime for the last 2 weeks
        if playtime_2weeks >= 60:
            playtime_2weeks_hours = playtime_2weeks // 60
            playtime_2weeks_minutes = playtime_2weeks % 60
            playtime_2weeks_str = f"{playtime_2weeks_hours} hrs {
                playtime_2weeks_minutes} mins"
        else:
            playtime_2weeks_str = f"{playtime_2weeks} mins"

        # Format total playtime
        if playtime_forever >= 60:
            playtime_forever_hours = playtime_forever // 60
            playtime_forever_minutes = playtime_forever % 60
            playtime_forever_str = f"{playtime_forever_hours} hrs {
                playtime_forever_minutes} mins"
        else:
            playtime_forever_str = f"{playtime_forever} mins"

        games_markdown += f"- {game['name']}: Playtime last 2 weeks: {
            playtime_2weeks_str}, Total playtime: {playtime_forever_str}\n"

    # Combine all Markdown sections
    combined_markdown = summary_markdown + "\n" + games_markdown
    return combined_markdown


def update_readme(markdown_data, readme_path="../README.md"):
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
        markdown_data + "\n" + readme_content[end_index:]
    )

    # Write the updated content back to the README file
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(new_readme_content)


# Entry Code
if __name__ == "__main__":
    player_summary = get_player_summaries()
    recently_played_games = get_recently_played_games()

    MARKDOWN_CONTENT = ""
    # generate_markdown(player_summary, recently_played_games)
    if player_summary and recently_played_games and player_summary['response']['players']:
        steam_player_data = player_summary['response']['players'][0]
        processed_data = process_player_summary_data(steam_player_data)
        MARKDOWN_CONTENT += generate_markdown(
            processed_data, recently_played_games)

    if MARKDOWN_CONTENT:
        update_readme(MARKDOWN_CONTENT)
        print("README.md has been successfully updated.")
    else:
        print("Failed to fetch or process data.")
