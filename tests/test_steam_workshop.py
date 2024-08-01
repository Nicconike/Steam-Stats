"""Test Steam Workshop Script"""
# Disable pylint warnings for false positives
# pylint: disable=duplicate-code, unused-argument, redefined-outer-name
from unittest.mock import MagicMock, patch, Mock
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
    fetch_all_workshop_stats, BeautifulSoup
)


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("INPUT_STEAM_API_KEY", "dummy_api_key")
    monkeypatch.setenv("INPUT_STEAM_CUSTOM_ID", "dummy_custom_id")


@pytest.fixture
def mock_requests_get(mocker):
    """Mock requests.get"""
    return mocker.patch('requests.get')


@pytest.fixture
def mock_beautifulsoup(mocker):
    """Mock BeautifulSoup"""
    return mocker.patch('api.steam_workshop.BeautifulSoup')


@pytest.fixture
def mock_dependencies(mocker):
    """Mock dependencies"""
    return {
        'is_server_online': mocker.patch('api.steam_workshop.is_server_online'),
        'extract_links': mocker.patch('api.steam_workshop.extract_links'),
        'has_next_page': mocker.patch('api.steam_workshop.has_next_page'),
        'handle_request_exception': mocker.patch('api.steam_workshop.handle_request_exception')
    }


def test_get_server_info_success(requests_mock):
    """Test successful retrieval of server info"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        json={"servertime": 1234567890}
    )
    result = get_server_info("dummy_api_key")
    if result is None:
        pytest.fail("Expected result to be not None")
    if "servertime" not in result:
        pytest.fail("Expected 'servertime' to be in result")


def test_get_server_info_http_error(requests_mock):
    """Test HTTP error handling for server info"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        status_code=404
    )
    result = get_server_info("dummy_api_key")
    if result is not None:
        pytest.fail("Expected result to be None")


def test_get_server_info_request_exception(requests_mock):
    """Test request exception handling for server info"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        exc=requests.exceptions.RequestException
    )
    result = get_server_info("dummy_api_key")
    if result is not None:
        pytest.fail("Expected result to be None")


def test_is_server_online_success(requests_mock):
    """Test server online check"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        json={"servertime": 1234567890}
    )
    result = is_server_online("dummy_api_key")
    if not result:
        pytest.fail("Expected result to be True")


def test_is_server_online_http_error(requests_mock):
    """Test server online check with HTTP error"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        status_code=404
    )
    result = is_server_online("dummy_api_key")
    if result:
        pytest.fail("Expected result to be False")


def test_is_server_online_request_exception(requests_mock):
    """Test server online check with request exception"""
    requests_mock.get(
        'https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/',
        exc=requests.exceptions.RequestException
    )
    result = is_server_online("dummy_api_key")
    if result:
        pytest.fail("Expected result to be False")


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
    expected_result = [
        "https://steamcommunity.com/id/nicconike/myworkshopfiles/"]
    if result != expected_result:
        pytest.fail(f"Result should be {expected_result}")


def test_has_next_page():
    """Test next page detection"""
    mock_soup = MagicMock()
    mock_soup.find.return_value = MagicMock(find=MagicMock(return_value=True))
    result = has_next_page(mock_soup)
    if not result:
        pytest.fail("Expected result to be True")


def test_has_next_page_no_paging_controls():
    """Test next page detection with no paging controls"""
    mock_soup = MagicMock()
    mock_soup.find.return_value = None
    result = has_next_page(mock_soup)
    if result:
        pytest.fail("Expected result to be False")


def test_handle_request_exception():
    """Test request exception handling"""
    with patch('api.steam_workshop.logger') as mock_logger:
        handle_request_exception(requests.exceptions.ConnectionError())
        mock_logger.error.assert_called_with(
            "Connection error occurred. Please check your network connection")

        handle_request_exception(requests.exceptions.Timeout())
        mock_logger.error.assert_called_with(
            "Request timed out. Please try again later")

        handle_request_exception(requests.exceptions.TooManyRedirects())
        mock_logger.error.assert_called_with(
            "Too many redirects. Check the URL and try again")

        response_mock = Mock()
        response_mock.status_code = 404
        response_mock.reason = "Not Found"
        handle_request_exception(
            requests.exceptions.HTTPError(response=response_mock))
        mock_logger.error.assert_called_with(
            "HTTP error occurred: %s - %s", "404", "Not Found")

        handle_request_exception(Exception("Some error"))
        mock_logger.error.assert_called_with(
            "An error occurred: %s", "Some error")


def test_fetch_workshop_item_links_success(mock_dependencies, requests_mock):
    """Test successful fetching of workshop item links"""
    mock_dependencies['is_server_online'].return_value = True
    mock_dependencies['extract_links'].return_value = [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"
    ]
    mock_dependencies['has_next_page'].return_value = False
    requests_mock.get(
        'https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1',
        text=(
            '<div class="workshopItem"><a class="ugc" '
            'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"></a></div>'
        )
    )

    result = fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")
    expected_result = [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"
    ]
    if result != expected_result:
        pytest.fail("Result should be " + str(expected_result))


def test_fetch_workshop_item_links_server_offline(mock_dependencies):
    """Test fetching workshop item links when server is offline"""
    mock_dependencies['is_server_online'].return_value = False
    with pytest.raises(ConnectionError,
                       match="Steam Community is currently offline. Please try again later"):
        fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")


def test_fetch_workshop_item_links_no_items(mock_dependencies, requests_mock):
    """Test fetching workshop item links with no items found"""
    mock_dependencies['is_server_online'].return_value = True
    mock_dependencies['extract_links'].return_value = []
    mock_dependencies['has_next_page'].return_value = False
    requests_mock.get(
        'https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1',
        text='<div class="noItems"></div>'
    )

    with pytest.raises(ValueError, match="No items were found in your Steam Workshop"):
        fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")


def test_fetch_workshop_item_links_parsing_error(mock_dependencies, requests_mock):
    """Test fetching workshop item links with parsing error"""
    mock_dependencies['is_server_online'].return_value = True
    mock_dependencies['extract_links'].side_effect = AttributeError(
        "Parsing error")
    requests_mock.get(
        'https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1',
        text='<div class="workshopItem"></div>'
    )

    with patch('api.steam_workshop.logger') as mock_logger:
        with pytest.raises(ValueError, match="No items were found in your Steam Workshop"):
            fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")
        mock_logger.error.assert_called_with(
            "Parsing error: %s. The structure of the page might have changed", "Parsing error"
        )


def test_fetch_workshop_item_links_multiple_pages(mock_dependencies, requests_mock):
    """Test fetching workshop item links with multiple pages"""
    mock_dependencies['is_server_online'].return_value = True
    mock_dependencies['extract_links'].side_effect = [
        ["https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"],
        ["https://steamcommunity.com/sharedfiles/filedetails/?id=2984474066"]
    ]
    mock_dependencies['has_next_page'].side_effect = [True, False]
    requests_mock.get(
        'https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1',
        text=(
            '<div class="workshopItem"><a class="ugc" '
            'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"></a></div>'
        )
    )
    requests_mock.get(
        'https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=2',
        text=(
            '<div class="workshopItem"><a class="ugc" '
            'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474066"></a></div>'
        )
    )

    result = fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")
    expected_result = [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065",
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474066"
    ]
    if result != expected_result:
        pytest.fail("Result should be " + str(expected_result))


# def test_fetch_workshop_item_links_request_exception(mock_dependencies, requests_mock, caplog):
#     """Test fetching workshop item links with request exception"""
#     mock_dependencies['is_server_online'].return_value = True
#     mock_dependencies['extract_links'].return_value = [
#         "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"
#     ]
#     mock_dependencies['has_next_page'].return_value = True
#     requests_mock.get('https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1',
#                       exc=requests.exceptions.RequestException)

#     with pytest.raises(ValueError, match="No items were found in your Steam Workshop"):
#         fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")

#     mock_dependencies['handle_request_exception'].assert_called_once()

#     error_logs = [
#         record for record in caplog.records if record.levelname == "ERROR"]
#     if len(error_logs) != 1:
#         pytest.fail("Expected one error log, found " + str(len(error_logs)))


def test_fetch_individual_workshop_stats_success(mock_requests_get, mock_beautifulsoup):
    """Test successful fetching of individual workshop stats"""
    mock_requests_get.return_value = Mock(
        status_code=200,
        content='<table class="stats_table"><tr><td>100</td><td>unique_visitors</td></tr></table>')
    mock_soup = BeautifulSoup(
        '<table class="stats_table"><tr><td>100</td><td>unique_visitors</td></tr></table>',
        'html.parser')
    mock_beautifulsoup.return_value = mock_soup

    result = fetch_individual_workshop_stats('http://example.com')

    if result['unique_visitors'] != 100:
        raise AssertionError("Expected unique_visitors to be 100")
    if result['current_subscribers'] != 0:
        raise AssertionError("Expected current_subscribers to be 0")
    if result['current_favorites'] != 0:
        raise AssertionError("Expected current_favorites to be 0")


def test_fetch_individual_workshop_stats_no_table(mock_requests_get, mock_beautifulsoup):
    """Test fetching of individual workshop stats with no stats table"""
    mock_requests_get.return_value = Mock(
        status_code=200, content='<div>No stats table</div>')
    mock_soup = BeautifulSoup('<div>No stats table</div>', 'html.parser')
    mock_beautifulsoup.return_value = mock_soup

    result = fetch_individual_workshop_stats('http://example.com')

    if result['unique_visitors']:
        raise AssertionError("Expected unique_visitors to be 0")
    if result['current_subscribers']:
        raise AssertionError("Expected current_subscribers to be 0")
    if result['current_favorites']:
        raise AssertionError("Expected current_favorites to be 0")


def test_fetch_individual_workshop_stats_request_exception(mock_requests_get):
    """Test request exception handling for individual workshop stats"""
    mock_requests_get.side_effect = requests.exceptions.RequestException

    result = fetch_individual_workshop_stats('http://example.com')

    if result:
        raise AssertionError("Expected result to be an empty dictionary")


def test_fetch_all_workshop_stats_success(mock_requests_get, mock_beautifulsoup):
    """Test successful fetching of all workshop stats"""
    mock_requests_get.side_effect = [
        Mock(status_code=200,
             content=(
                 '<table class="stats_table"><tr><td>100</td><td>unique_visitors</td></tr></table>'
             )),
        Mock(status_code=200,
             content=(
                 '<table class="stats_table"><tr><td>200</td><td>unique_visitors</td></tr></table>'
             ))
    ]
    mock_soup1 = BeautifulSoup(
        '<table class="stats_table"><tr><td>100</td><td>unique_visitors</td></tr></table>',
        'html.parser')
    mock_soup2 = BeautifulSoup(
        '<table class="stats_table"><tr><td>200</td><td>unique_visitors</td></tr></table>',
        'html.parser')
    mock_beautifulsoup.side_effect = [mock_soup1, mock_soup2]

    result = fetch_all_workshop_stats(
        ['http://example.com/item1', 'http://example.com/item2'])

    if result['total_unique_visitors'] != 300:
        raise AssertionError("Expected total_unique_visitors to be 300")
    if result['total_current_subscribers'] != 0:
        raise AssertionError("Expected total_current_subscribers to be 0")
    if result['total_current_favorites'] != 0:
        raise AssertionError("Expected total_current_favorites to be 0")


def test_fetch_all_workshop_stats_request_exception(mock_requests_get):
    """Test request exception handling for all workshop stats"""
    mock_requests_get.side_effect = [
        requests.exceptions.RequestException,
        Mock(status_code=200,
             content=(
                 '<table class="stats_table"><tr><td>200</td><td>unique_visitors</td></tr></table>'
             ))
    ]
    mock_soup = BeautifulSoup(
        '<table class="stats_table"><tr><td>200</td><td>unique_visitors</td></tr></table>',
        'html.parser')
    with patch('api.steam_workshop.BeautifulSoup', return_value=mock_soup):
        result = fetch_all_workshop_stats(
            ['http://example.com/item1', 'http://example.com/item2'])

    if result['total_unique_visitors'] != 200:
        raise AssertionError("Expected total_unique_visitors to be 200")
    if result['total_current_subscribers'] != 0:
        raise AssertionError("Expected total_current_subscribers to be 0")
    if result['total_current_favorites'] != 0:
        raise AssertionError("Expected total_current_favorites to be 0")
