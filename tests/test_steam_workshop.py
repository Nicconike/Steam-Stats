"""Test Steam Workshop Script"""
from unittest.mock import MagicMock, patch
import pytest
import requests
from api.steam_workshop import (
    get_server_info,
    is_server_online,
    extract_links,
    has_next_page,
    handle_request_exception,
    fetch_workshop_item_links,
    fetch_individual_workshop_stats,
    fetch_all_workshop_stats
)


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("INPUT_STEAM_API_KEY", "dummy_api_key")
    monkeypatch.setenv("INPUT_STEAM_CUSTOM_ID", "dummy_custom_id")


def test_get_server_info_success(requests_mock):
    """Test successful retrieval of server info"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        json={"servertime": 1234567890}
    )
    result = get_server_info("dummy_api_key")
    assert result is not None
    assert "servertime" in result


def test_get_server_info_http_error(requests_mock):
    """Test HTTP error handling for server info"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        status_code=404
    )
    result = get_server_info("dummy_api_key")
    assert result is None


def test_get_server_info_request_exception(requests_mock):
    """Test request exception handling for server info"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        exc=requests.exceptions.RequestException
    )
    result = get_server_info("dummy_api_key")
    assert result is None


def test_is_server_online_success(requests_mock):
    """Test server online check"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        json={"servertime": 1234567890}
    )
    result = is_server_online("dummy_api_key")
    assert result is True


def test_is_server_online_http_error(requests_mock):
    """Test server online check with HTTP error"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        status_code=404
    )
    result = is_server_online("dummy_api_key")
    assert result is False


def test_is_server_online_request_exception(requests_mock):
    """Test server online check with request exception"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        exc=requests.exceptions.RequestException
    )
    result = is_server_online("dummy_api_key")
    assert result is False


def test_extract_links():
    """Test link extraction from workshop items"""
    mock_item = MagicMock()
    mock_link_tag = MagicMock()
    mock_link_tag.attrs = {
        "href": "https://steamcommunity.com/id/nicconike/myworkshopfiles/"}
    mock_item.find.return_value = mock_link_tag
    mock_link_tag.__getitem__.return_value = (
        "https://steamcommunity.com/id/nicconike/myworkshopfiles/")
    result = extract_links([mock_item])
    assert result == [
        "https://steamcommunity.com/id/nicconike/myworkshopfiles/"]


def test_has_next_page():
    """Test next page detection"""
    mock_soup = MagicMock()
    mock_soup.find.return_value = MagicMock(find=MagicMock(return_value=True))
    result = has_next_page(mock_soup)
    assert result is True


def test_handle_request_exception():
    """Test request exception handling"""
    with patch('api.steam_workshop.logger') as mock_logger:
        handle_request_exception(requests.exceptions.ConnectionError())
        mock_logger.error.assert_called_with(
            "Connection error occurred. Please check your network connection")


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
    result = fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")
    assert result == [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"]


def test_fetch_individual_workshop_stats_success(requests_mock):
    """Test successful fetching of individual workshop stats"""
    requests_mock.get(
        'http://example.com',
        text='<table class="stats_table"><tr><td>1,000</td><td>Unique Visitors</td></tr></table>'
    )
    result = fetch_individual_workshop_stats("http://example.com")
    assert result == {"unique_visitors": 1000,
                      "current_subscribers": 0, "current_favorites": 0}


def test_fetch_all_workshop_stats_success(requests_mock):
    """Test successful fetching of all workshop stats"""
    requests_mock.get(
        'http://example.com',
        text='<table class="stats_table"><tr><td>1,000</td><td>Unique Visitors</td></tr></table>'
    )
    result = fetch_all_workshop_stats(["http://example.com"])
    assert result["total_unique_visitors"] == 1000
    assert result["total_current_subscribers"] == 0
    assert result["total_current_favorites"] == 0
    assert len(result["individual_stats"]) == 1
