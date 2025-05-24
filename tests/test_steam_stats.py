"""Test Steam Stats Script"""

# Disable pylint warnings for false positives
# pylint: disable=duplicate-code
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
    url = (
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
        "key=dummy_api_key&steamids=dummy_steam_id"
    )
    requests_mock.get(url, json={"response": {"players": []}}, status_code=200)

    result = get_player_summaries()
    if result is None:
        raise AssertionError("Expected result to be not None")
    if "response" not in result:
        raise AssertionError("Expected 'response' key in result")
    if "players" not in result["response"]:
        raise AssertionError("Expected 'players' key in result['response']")


def test_get_player_summaries_429_then_success(requests_mock):
    """Test retry on 429 then success"""
    url = (
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
        "key=dummy_api_key&steamids=dummy_steam_id"
    )
    requests_mock.get(
        url,
        [
            {"status_code": 429, "headers": {"Retry-After": "1"}},
            {"status_code": 200, "json": {"response": {"players": []}}},
        ],
    )

    result = get_player_summaries()
    if result is None:
        raise AssertionError("Expected result to be not None after retry")
    if "response" not in result or "players" not in result["response"]:
        raise AssertionError("Expected 'players' in 'response' after retry")


def test_get_player_summaries_429_max_retries(monkeypatch, requests_mock):
    """Test 429 on all attempts results in None"""
    url = (
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
        "key=dummy_api_key&steamids=dummy_steam_id"
    )
    requests_mock.get(url, status_code=429, headers={"Retry-After": "1"})

    # avoid sleep delay
    monkeypatch.setattr("time.sleep", lambda x: None)

    result = get_player_summaries()
    if result is not None:
        raise AssertionError("Expected None after exhausting retries on 429")


def test_get_player_summaries_http_error(requests_mock):
    """Test HTTPError handling"""
    url = (
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
        "key=dummy_api_key&steamids=dummy_steam_id"
    )
    requests_mock.get(url, status_code=404)

    result = get_player_summaries()
    if result is not None:
        raise AssertionError("Expected None for HTTP 404 error")


def test_get_player_summaries_request_exception(monkeypatch):
    """Test RequestException handling"""

    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Connection failed")

    monkeypatch.setattr("requests.get", mock_get)

    result = get_player_summaries()
    if result is not None:
        raise AssertionError("Expected None on RequestException")


def test_get_recently_played_games_success(requests_mock):
    """Test successful retrieval of recently played games"""
    requests_mock.get(
        "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/",
        json={
            "response": {
                "total_count": 1,
                "games": [{"name": "TestGame", "playtime_2weeks": 120}],
            }
        },
    )
    result = get_recently_played_games()
    if result is None:
        raise AssertionError("Expected result to be not None")
    if result is None or "response" not in result:
        raise AssertionError("Expected 'response' to be in result")
    if "games" not in result["response"]:
        raise AssertionError("Expected 'games' to be in result['response']")


def test_get_recently_played_games_no_games(requests_mock):
    """Test retrieval of recently played games with no games played"""
    requests_mock.get(
        "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/",
        json={"response": {"total_count": 0}},
    )
    result = get_recently_played_games()
    if result is not None:
        raise AssertionError("Expected result to be None")


def test_get_recently_played_games_http_error(requests_mock):
    """Test HTTP error handling for recently played games"""
    requests_mock.get(
        "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/",
        status_code=404,
    )
    result = get_recently_played_games()
    if result is not None:
        raise AssertionError("Expected result to be None")


def test_get_recently_played_games_request_exception(requests_mock):
    """Test request exception handling for recently played games"""
    requests_mock.get(
        "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/",
        exc=requests.exceptions.RequestException,
    )
    result = get_recently_played_games()
    if result is not None:
        raise AssertionError("Expected result to be None")
