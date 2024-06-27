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
    assert result is not None
    assert "response" in result
    assert "players" in result["response"]


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
    assert result is not None
    assert "response" in result
    assert "games" in result["response"]


def test_get_recently_played_games_no_games(requests_mock):
    """Test retrieval of recently played games with no games played"""
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 0}}
    )
    result = main.get_recently_played_games()
    assert result is None


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
    assert result == [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"]


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
    assert "![Steam Summary]" in result
    assert "![Recently Played Games]" in result


def test_generate_workshop_stats(requests_mock):
    """Test generating Workshop stats"""
    # Mock the initial request to fetch workshop item links
    requests_mock.get(
        'https://steamcommunity.com/id/nicconike/myworkshopfiles/?p=1',
        text='<div class="workshopItem"><a class="ugc"'
        'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"></a></div>'
    )
    # Mock the server info request
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        json={"servertime": 1234567890}
    )
    # Mock the request to fetch individual workshop stats
    requests_mock.get(
        'https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065',
        text='<table class="stats_table"><tr><td>1,000</td><td>Unique Visitors</td></tr></table>'
    )
    # Mock the next page request if applicable
    requests_mock.get(
        'https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=2',
        text=''
    )
    result = main.generate_workshop_stats()
    assert "![Steam Workshop Stats]" in result


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
