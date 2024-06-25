"""Test Steam Workshop Script"""
import os
from unittest.mock import patch, MagicMock
import pytest
import requests
from api import steam_workshop
from dotenv import load_dotenv

load_dotenv()

STEAM_ID = os.environ["INPUT_STEAM_ID"]
STEAM_API_KEY = os.environ["INPUT_STEAM_API_KEY"]


@pytest.fixture
def mock_requests_get():
    """Mock requests.get"""
    with patch('api.steam_workshop.requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_server_info_response(mock_requests_get):
    """Mock the response to simulate a successful API call for server info"""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"servertime": 1234567890}
    mock_requests_get.return_value = mock_response
    return mock_requests_get


@pytest.fixture
def mock_http_error_response(mock_requests_get):
    """Mock the response to simulate an HTTP error"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "HTTP Error")
    mock_requests_get.return_value = mock_response
    return mock_requests_get


@pytest.fixture
def mock_request_exception_response(mock_requests_get):
    """Mock the response to simulate a request exception"""
    mock_requests_get.side_effect = requests.exceptions.RequestException(
        "Request Exception")
    return mock_requests_get


def test_get_server_info_success(mock_server_info_response):
    """Test successful retrieval of server info"""
    result = steam_workshop.get_server_info("dummy_api_key")
    assert result is not None
    assert "servertime" in result


def test_get_server_info_http_error(mock_http_error_response):
    """Test HTTP error handling for server info"""
    result = steam_workshop.get_server_info("dummy_api_key")
    assert result is None


def test_get_server_info_request_exception(mock_request_exception_response):
    """Test request exception handling for server info"""
    result = steam_workshop.get_server_info("dummy_api_key")
    assert result is None


def test_is_server_online_success(mock_server_info_response):
    """Test server online check"""
    result = steam_workshop.is_server_online("dummy_api_key")
    assert result is True


def test_is_server_online_http_error(mock_http_error_response):
    """Test server online check with HTTP error"""
    result = steam_workshop.is_server_online("dummy_api_key")
    assert result is False


def test_is_server_online_request_exception(mock_request_exception_response):
    """Test server online check with request exception"""
    result = steam_workshop.is_server_online("dummy_api_key")
    assert result is False


def test_extract_links():
    """Test link extraction from workshop items"""
    mock_item = MagicMock()
    mock_link_tag = MagicMock()
    mock_link_tag.attrs = {
        "href": "https://steamcommunity.com/sharedfiles/filedetails/?id=2986231133"}
    mock_item.find.return_value = mock_link_tag
    result = steam_workshop.extract_links([mock_item])
    assert result == [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2986231133"]


def test_has_next_page():
    """Test next page detection"""
    mock_soup = MagicMock()
    mock_soup.find.return_value = MagicMock(find=MagicMock(return_value=True))
    result = steam_workshop.has_next_page(mock_soup)
    assert result is True


def test_handle_request_exception():
    """Test request exception handling"""
    with patch('api.steam_workshop.logger') as mock_logger:
        steam_workshop.handle_request_exception(
            requests.exceptions.ConnectionError())
        mock_logger.error.assert_called_with(
            "Connection error occurred. Please check your network connection")


def test_fetch_workshop_item_links_success(mock_server_info_response, mock_requests_get):
    """Test successful fetching of workshop item links"""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.content = (
        b'<div class="workshopItem"><a class="ugc"'
        b'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"></a></div>'
    )
    mock_requests_get.return_value = mock_response

    result = steam_workshop.fetch_workshop_item_links(
        "dummy_id", "dummy_api_key")
    assert result == [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"]


def test_fetch_individual_workshop_stats_success(mock_requests_get):
    """Test successful fetching of individual workshop stats"""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.content = (
        b'<table class="stats_table"><tr><td>1,000</td><td>Unique Visitors</td></tr></table>')
    mock_requests_get.return_value = mock_response

    result = steam_workshop.fetch_individual_workshop_stats(
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065")
    assert result == {"unique_visitors": 1000,
                      "current_subscribers": 0, "current_favorites": 0}


def test_fetch_all_workshop_stats_success(mock_requests_get):
    """Test successful fetching of all workshop stats"""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.content = (
        b'<table class="stats_table"><tr><td>1,000</td><td>Unique Visitors</td></tr></table>')
    mock_requests_get.return_value = mock_response

    result = steam_workshop.fetch_all_workshop_stats(
        ["https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"])
    assert result["total_unique_visitors"] == 1000
    assert result["total_current_subscribers"] == 0
    assert result["total_current_favorites"] == 0
    assert len(result["individual_stats"]) == 1
