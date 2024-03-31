"""Retrieves and displays Steam User Data in README using Steam Web API"""
import os
from base64 import b64decode
import requests
from github import Github, GithubException

# Configuration
STEAM_API_KEY = os.getenv('STEAM_WEB_API_KEY')
STEAM_ID = os.getenv('STEAM_ID')
GH_TOKEN = os.getenv('GH_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')  # Format: "username/repo"

# Steam Web API endpoints
PLAYER_SUMMARIES_URL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
PLAYER_ACHIEVEMENTS_URL = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
USER_STATS_FOR_GAME_URL = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
RECENTLY_PLAYED_GAMES_URL = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/"

# Reasonable timeout for the request (connection and read timeout)
REQUEST_TIMEOUT = (10, 15)


def fetch_steam_data(endpoint, params):
    """Fetch Steam Stats as JSON dictionary"""
    try:
        response = requests.get(endpoint, params=params,
                                timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("The request to Steam Web API timed out.")
        return None
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None


def get_player_summaries():
    """Fetch basic profile information for a list of 64-bit Steam IDs"""
    params = {"key": STEAM_API_KEY, "steamids": STEAM_ID}
    data = fetch_steam_data(PLAYER_SUMMARIES_URL, params)
    if data is not None and 'response' in data and 'players' in data['response']:
        return data['response']['players'][0]
    else:
        print("Failed to fetch player summaries.")
        return None


def get_player_achievements(app_id):
    """Fetch a list of achievements for a user by app id"""
    params = {"appid": app_id, "key": STEAM_API_KEY, "steamid": STEAM_ID}
    data = fetch_steam_data(PLAYER_ACHIEVEMENTS_URL, params)
    if data is not None and 'playerstats' in data and 'achievements' in data['playerstats']:
        return data['playerstats']['achievements']
    else:
        print(f"Failed to fetch player achievements for app ID {app_id}.")
        return None


def get_user_stats_for_game(app_id):
    """Fetch a list of achievements for a user by app id"""
    params = {"appid": app_id, "key": STEAM_API_KEY, "steamid": STEAM_ID}
    data = fetch_steam_data(USER_STATS_FOR_GAME_URL, params)
    if data is not None and 'playerstats' in data and 'stats' in data['playerstats']:
        return data['playerstats']['stats']
    else:
        print(f"Failed to fetch user stats for game with app ID {app_id}.")
        return None


def get_recently_played_games():
    """Fetch a list of games a player has played in the last two weeks"""
    params = {"key": STEAM_API_KEY, "steamid": STEAM_ID, "format": "json"}
    data = fetch_steam_data(RECENTLY_PLAYED_GAMES_URL, params)
    if data is not None and 'response' in data and 'games' in data['response']:
        return data['response']['games']
    else:
        print("Failed to fetch recently played games.")
        return None


def update_readme_section(content, start_marker, end_marker):
    """Function to update the readme file"""
    if REPO_NAME is None:
        print("Repository name is not set.")
        return

    try:
        g = Github(GH_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("README.md")

        # Ensure contents is a single ContentFile object
        if isinstance(contents, list):
            print("Expected a single ContentFile but got a list.")
            return
        readme = contents

        decoded_content = b64decode(readme.content).decode('utf-8')

        start_index = decoded_content.find(start_marker) + len(start_marker)
        end_index = decoded_content.find(end_marker, start_index)

        if start_index == -1 or end_index == -1 or start_index >= end_index:
            raise ValueError(
                "Start or end marker not found, or in the wrong order")

        new_readme_content = decoded_content[:start_index] + \
            content + decoded_content[end_index:]
        repo.update_file(readme.path, "Update Steam stats",
                         new_readme_content, readme.sha)
    except GithubException as e:
        print(f"GitHub API exception occurred: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


class SteamFetchError(Exception):
    """Custom exception for errors fetching data from the Steam Web API."""
    pass


def main():
    """Entry Point for the Python Script"""
    try:
        player_info = get_player_summaries()
        if player_info is None:
            raise SteamFetchError(
                "Failed to fetch player summaries from Steam.")

        recently_played = get_recently_played_games()
        if recently_played is None:
            raise SteamFetchError(
                "Failed to fetch recently played games from Steam.")

        # Format the fetched data into Markdown
        steam_stats_md = f"""
        ### Steam Profile
        - Name: {player_info['personaname']}
        - Profile URL: {player_info['profileurl']}

        ### Recently Played Games
        {"".join([f"- {game['name']} - {game['playtime_2weeks']
                                        } minutesinthelast 2 weeks\n" for game in recently_played])}
        """

        # Update the README.md file within the Steam stats section
        update_readme_section(
            steam_stats_md, "<!-- Steam-Stats start -->", "<!-- Steam-Stats end -->")

    except SteamFetchError as e:
        print(f"Steam data fetch error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
