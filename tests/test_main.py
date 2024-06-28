"""Test Main Runner Script"""
# Disable pylint warnings for false positives
# pylint: disable=duplicate-code
from unittest.mock import patch, ANY
import pytest
from api import main


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("INPUT_STEAM_API_KEY", "dummy_api_key")
    monkeypatch.setenv("INPUT_STEAM_CUSTOM_ID", "dummy_custom_id")


def test_get_player_summaries_success(requests_mock):
    """Test successful retrieval of player summaries"""
    requests_mock.get(
        'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
        json={"response": {"players": [{
            "personaname": "TestUser", "personastate": 1, "avatarfull":
            "http://example.com/avatar.jpg", "loccountrycode": "US",
            "lastlogoff": 1609459200, "timecreated": 1609459200
        }]}}
    )
    result = main.get_player_summaries()
    if result is None:
        raise AssertionError("Expected result to be not None")
    if result is None or "response" not in result:
        raise AssertionError("Expected 'response' to be in result")
    if "players" not in result["response"]:
        raise AssertionError("Expected 'players' to be in result['response']")


def test_get_recently_played_games_success(requests_mock):
    """Test successful retrieval of recently played games"""
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 1, "games": [
            {"name": "TestGame", "playtime_2weeks": 120,
                "appid": 12345, "img_icon_url": "icon.jpg"}
        ]}}
    )
    result = main.get_recently_played_games()
    if result is None:
        raise AssertionError("Expected result to be not None")
    if result is None or "response" not in result:
        raise AssertionError("Expected 'response' to be in result")
    if "games" not in result["response"]:
        raise AssertionError("Expected 'games' to be in result['response']")


def test_get_recently_played_games_no_games(requests_mock):
    """Test retrieval of recently played games with no games played"""
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 0}}
    )
    result = main.get_recently_played_games()
    if result is not None:
        raise AssertionError("Expected result to be None")


def test_fetch_workshop_item_links_success(requests_mock):
    """Test successful fetching of workshop item links"""
    requests_mock.get(
        'https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1',
        text='<div class="workshopItem"><a class="ugc"'
        'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"></a></div>'
    )
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        json={"servertime": 1234567890}
    )
    result = main.fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")
    expected_result = [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"]
    if result != expected_result:
        raise AssertionError(f"Result should be {expected_result}")


def test_generate_steam_stats(requests_mock):
    """Test generating Steam stats"""
    requests_mock.get(
        'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
        json={"response": {"players": [{
            "personaname": "TestUser", "personastate": 1, "avatarfull":
            "http://example.com/avatar.jpg", "loccountrycode": "US",
            "lastlogoff": 1609459200, "timecreated": 1609459200}
        ]}}
    )
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 1, "games": [
            {"name": "TestGame", "playtime_2weeks": 120,
                "appid": 12345, "img_icon_url": "icon.jpg"}
        ]}}
    )
    result = main.generate_steam_stats()
    if "![Steam Summary]" not in result:
        raise AssertionError("Expected '![Steam Summary]' to be in result")
    if "![Recently Played Games]" not in result:
        raise AssertionError(
            "Expected '![Recently Played Games]' to be in result")


def test_generate_workshop_stats(requests_mock):
    """Test generating Workshop stats"""
    requests_mock.get(
        'https://steamcommunity.com/id/nicconike/myworkshopfiles/?p=1',
        text='<div class="workshopItem"><a class="ugc"'
        'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"></a></div>'
    )
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        json={"servertime": 1234567890}
    )
    requests_mock.get(
        'https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065',
        text='<table class="stats_table"><tr><td>1,000</td><td>Unique Visitors</td></tr></table>'
    )
    requests_mock.get(
        'https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=2',
        text=''
    )
    result = main.generate_workshop_stats()
    if "![Steam Workshop Stats]" not in result:
        raise AssertionError(
            "Expected '![Steam Workshop Stats]' to be in result")


def test_main(requests_mock):
    """Test the main function execution"""
    requests_mock.get(
        'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
        json={"response": {"players": [{
            "personaname": "TestUser", "personastate": 1, "avatarfull":
            "http://example.com/avatar.jpg", "loccountrycode": "US",
            "lastlogoff": 1609459200, "timecreated": 1609459200}
        ]}}
    )
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 1, "games": [
            {"name": "TestGame", "playtime_2weeks": 120,
                "appid": 12345, "img_icon_url": "icon.jpg"}
        ]}}
    )
    requests_mock.get(
        'https://steamcommunity.com/id/nicconike/myworkshopfiles/?p=1',
        text='<div class="workshopItem"><a class="ugc"'
        'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"></a></div>'
    )
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        json={"servertime": 1234567890}
    )
    requests_mock.get(
        'https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065',
        text='<table class="stats_table"><tr><td>1,000</td><td>Unique Visitors</td></tr></table>'
    )
    with patch('api.main.update_readme') as mock_update_readme:
        main.main()
        mock_update_readme.assert_any_call(
            ANY, "<!-- Steam-Stats start -->", "<!-- Steam-Stats end -->")
        mock_update_readme.assert_any_call(
            ANY, "<!-- Steam-Workshop start -->", "<!-- Steam-Workshop end -->")
