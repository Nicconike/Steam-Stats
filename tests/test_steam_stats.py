"""Test Steam Stats Script"""
import pytest
import requests
from api.steam_stats import get_player_summaries, get_recently_played_games


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("INPUT_STEAM_API_KEY", "dummy_api_key")
    monkeypatch.setenv("INPUT_STEAM_ID", "dummy_steam_id")


def test_get_player_summaries_success(requests_mock):
    """Test successful retrieval of player summaries"""
    requests_mock.get(
        'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
        json={"response": {"players": []}}
    )
    result = get_player_summaries()
    assert result is not None
    assert "response" in result
    assert "players" in result["response"]


def test_get_player_summaries_http_error(requests_mock):
    """Test HTTP error handling for player summaries"""
    requests_mock.get(
        'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
        status_code=404
    )
    result = get_player_summaries()
    assert result is None


def test_get_player_summaries_request_exception(requests_mock):
    """Test request exception handling for player summaries"""
    requests_mock.get(
        'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
        exc=requests.exceptions.RequestException
    )
    result = get_player_summaries()
    assert result is None


def test_get_recently_played_games_success(requests_mock):
    """Test successful retrieval of recently played games"""
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 1, "games": [
            {"name": "TestGame", "playtime_2weeks": 120}]}}
    )
    result = get_recently_played_games()
    assert result is not None
    assert "response" in result
    assert "games" in result["response"]


def test_get_recently_played_games_no_games(requests_mock):
    """Test retrieval of recently played games with no games played"""
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 0}}
    )
    result = get_recently_played_games()
    assert result is None


def test_get_recently_played_games_http_error(requests_mock):
    """Test HTTP error handling for recently played games"""
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        status_code=404
    )
    result = get_recently_played_games()
    assert result is None


def test_get_recently_played_games_request_exception(requests_mock):
    """Test request exception handling for recently played games"""
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        exc=requests.exceptions.RequestException
    )
    result = get_recently_played_games()
    assert result is None
