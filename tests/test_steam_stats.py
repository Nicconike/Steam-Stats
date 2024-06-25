"""Test Steam Stats Script"""
from unittest.mock import patch, MagicMock
import pytest
import requests
from api import steam_stats


@pytest.fixture
def mock_requests_get():
    """Mock requests.get"""
    with patch('api.steam_stats.requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_summary_response(mock_requests_get):
    """Mock the response to simulate a successful API call for player summaries"""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"response": {"players": []}}
    mock_requests_get.return_value = mock_response
    return mock_requests_get


@pytest.fixture
def mock_http_error_response(mock_requests_get):
    """Mock the response to simulate an HTTP error for player summaries"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "HTTP Error")
    mock_requests_get.return_value = mock_response
    return mock_requests_get


@pytest.fixture
def mock_request_exception_response(mock_requests_get):
    """Mock the response to simulate a request exception for player summaries"""
    mock_requests_get.side_effect = requests.exceptions.RequestException(
        "Request Exception")
    return mock_requests_get


@pytest.fixture
def mock_games_response(mock_requests_get):
    """Mock the response to simulate a successful API call for recently played games"""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"response": {"games": []}}
    mock_requests_get.return_value = mock_response
    return mock_requests_get


@pytest.fixture
def mock_games_http_error_response(mock_requests_get):
    """Mock the response to simulate an HTTP error for recently played games"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "HTTP Error")
    mock_requests_get.return_value = mock_response
    return mock_requests_get


@pytest.fixture
def mock_games_request_exception_response(mock_requests_get):
    """Mock the response to simulate a request exception for recently played games"""
    mock_requests_get.side_effect = requests.exceptions.RequestException(
        "Request Exception")
    return mock_requests_get


def test_get_player_summaries_success(mock_summary_response):
    """Test successful retrieval of player summaries"""
    result = steam_stats.get_player_summaries()
    assert result is not None
    assert "response" in result
    assert "players" in result["response"]


def test_get_player_summaries_http_error(mock_http_error_response):
    """Test HTTP error handling for player summaries"""
    result = steam_stats.get_player_summaries()
    assert result is None


def test_get_player_summaries_request_exception(mock_request_exception_response):
    """Test request exception handling for player summaries"""
    result = steam_stats.get_player_summaries()
    assert result is None


def test_get_recently_played_games_success(mock_games_response):
    """Test successful retrieval of recently played games"""
    result = steam_stats.get_recently_played_games()
    assert result is not None
    assert "response" in result
    assert "games" in result["response"]


def test_get_recently_played_games_http_error(mock_games_http_error_response):
    """Test HTTP error handling for recently played games"""
    result = steam_stats.get_recently_played_games()
    assert result is None


def test_get_recently_played_games_request_exception(mock_games_request_exception_response):
    """Test request exception handling for recently played games"""
    result = steam_stats.get_recently_played_games()
    assert result is None
