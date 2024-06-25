"""Test Main Runner Script"""
from unittest.mock import patch
import pytest
from api import main


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("INPUT_STEAM_ID", "dummy_steam_id")
    monkeypatch.setenv("INPUT_STEAM_API_KEY", "dummy_api_key")
    monkeypatch.setenv("INPUT_STEAM_CUSTOM_ID", "dummy_custom_id")
    monkeypatch.setenv("INPUT_WORKSHOP_STATS", "true")


@pytest.fixture
def mock_requests_get(requests_mock):
    """Mock requests.get"""
    requests_mock.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
                      json={"response": {"players": []}})
    requests_mock.get('http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
                      json={"response": {"games": []}})
    requests_mock.get('https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1',
                      text='<div class="workshopItem"><a class="ugc"'
                      'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065">'
                      '</a></div>')


@pytest.fixture
def mock_functions():
    """Mock functions from steam modules"""
    with patch('api.main.get_player_summaries',
               return_value={"response": {"players": []}}) as mock_get_player_summaries, \
            patch('api.main.get_recently_played_games',
                  return_value={"response": {"games": []}}) as mock_get_recently_played_games, \
            patch('api.main.fetch_workshop_item_links',
                  return_value=[
                      "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"]
                  ) as mock_fetch_workshop_item_links, \
            patch('api.main.fetch_all_workshop_stats',
                  return_value={"total_unique_visitors": 1000, "total_current_subscribers": 0,
                                "total_current_favorites": 0, "individual_stats": []}
                  ) as mock_fetch_all_workshop_stats, \
            patch('api.main.generate_card_for_player_summary',
                  return_value="Player Summary Card") as mock_generate_card_for_player_summary, \
            patch('api.main.generate_card_for_played_games',
                  return_value="Played Games Card") as mock_generate_card_for_played_games, \
            patch('api.main.generate_card_for_steam_workshop',
                  return_value="Workshop Stats Card") as mock_generate_card_for_steam_workshop, \
            patch('api.main.update_readme') as mock_update_readme:
        yield {
            "get_player_summaries": mock_get_player_summaries,
            "get_recently_played_games": mock_get_recently_played_games,
            "fetch_workshop_item_links": mock_fetch_workshop_item_links,
            "fetch_all_workshop_stats": mock_fetch_all_workshop_stats,
            "generate_card_for_player_summary": mock_generate_card_for_player_summary,
            "generate_card_for_played_games": mock_generate_card_for_played_games,
            "generate_card_for_steam_workshop": mock_generate_card_for_steam_workshop,
            "update_readme": mock_update_readme
        }


def test_main_script(mock_requests_get, mock_functions):
    """Test the main script execution"""
    with patch('builtins.print') as mock_print:
        main.main()
        mock_print.assert_any_call("Retrieved Steam User Stats")
        mock_print.assert_any_call(
            "README.md has been successfully updated with Steam Stats")
        mock_print.assert_any_call("Retrieved Workshop Stats")
        mock_print.assert_any_call(
            "README.md has been successfully updated with Workshop Stats")
