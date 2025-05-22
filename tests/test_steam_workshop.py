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
    parse_stats_table,
    fetch_individual_workshop_stats,
    fetch_all_workshop_stats,
    BeautifulSoup,
)


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("INPUT_STEAM_API_KEY", "dummy_api_key")
    monkeypatch.setenv("INPUT_STEAM_CUSTOM_ID", "dummy_custom_id")


@pytest.fixture
def mock_requests_get(mocker):
    """Mock requests.get"""
    return mocker.patch("requests.get")


@pytest.fixture
def mock_beautifulsoup(mocker):
    """Mock BeautifulSoup"""
    return mocker.patch("api.steam_workshop.BeautifulSoup")


@pytest.fixture
def mock_dependencies(mocker):
    """Mock dependencies"""
    return {
        "is_server_online": mocker.patch("api.steam_workshop.is_server_online"),
        "extract_links": mocker.patch("api.steam_workshop.extract_links"),
        "has_next_page": mocker.patch("api.steam_workshop.has_next_page"),
        "handle_request_exception": mocker.patch(
            "api.steam_workshop.handle_request_exception"
        ),
    }


def test_get_server_info_success(requests_mock):
    """Test successful retrieval of server info"""
    requests_mock.get(
        "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/",
        json={"servertime": 1234567890},
    )
    result = get_server_info("dummy_api_key")
    if result is None:
        pytest.fail("Expected result to be not None")
    if "servertime" not in result:
        pytest.fail("Expected 'servertime' to be in result")


def test_get_server_info_http_error(requests_mock):
    """Test HTTP error handling for server info"""
    requests_mock.get(
        "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/",
        status_code=404,
    )
    result = get_server_info("dummy_api_key")
    if result is not None:
        pytest.fail("Expected result to be None")


def test_get_server_info_request_exception(requests_mock):
    """Test request exception handling for server info"""
    requests_mock.get(
        "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/",
        exc=requests.exceptions.RequestException,
    )
    result = get_server_info("dummy_api_key")
    if result is not None:
        pytest.fail("Expected result to be None")


def test_is_server_online_success(requests_mock):
    """Test server online check"""
    requests_mock.get(
        "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/",
        json={"servertime": 1234567890},
    )
    result = is_server_online("dummy_api_key")
    if not result:
        pytest.fail("Expected result to be True")


def test_is_server_online_http_error(requests_mock):
    """Test server online check with HTTP error"""
    requests_mock.get(
        "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/",
        status_code=404,
    )
    result = is_server_online("dummy_api_key")
    if result:
        pytest.fail("Expected result to be False")


def test_is_server_online_request_exception(requests_mock):
    """Test server online check with request exception"""
    requests_mock.get(
        "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/",
        exc=requests.exceptions.RequestException,
    )
    result = is_server_online("dummy_api_key")
    if result:
        pytest.fail("Expected result to be False")


def test_extract_links():
    """Test link extraction from workshop items"""
    mock_item = MagicMock()
    mock_link_tag = MagicMock()
    mock_link_tag.attrs = {
        "href": "https://steamcommunity.com/id/nicconike/myworkshopfiles/"
    }
    mock_item.find.return_value = mock_link_tag
    mock_link_tag.__getitem__.return_value = (
        "https://steamcommunity.com/id/nicconike/myworkshopfiles/"
    )
    result = extract_links([mock_item])
    expected_result = ["https://steamcommunity.com/id/nicconike/myworkshopfiles/"]
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
    with patch("api.steam_workshop.logger") as mock_logger:
        handle_request_exception(requests.exceptions.ConnectionError())
        mock_logger.error.assert_called_with(
            "Connection error occurred. Please check your network connection"
        )

        handle_request_exception(requests.exceptions.Timeout())
        mock_logger.error.assert_called_with(
            "Request timed out. Please try again later"
        )

        handle_request_exception(requests.exceptions.TooManyRedirects())
        mock_logger.error.assert_called_with(
            "Too many redirects. Check the URL and try again"
        )

        response_mock = Mock()
        response_mock.status_code = 404
        response_mock.reason = "Not Found"
        handle_request_exception(requests.exceptions.HTTPError(response=response_mock))
        mock_logger.error.assert_called_with(
            "HTTP error occurred: %s - %s", "404", "Not Found"
        )

        handle_request_exception(Exception("Some error"))
        mock_logger.error.assert_called_with("An error occurred: %s", "Some error")


def test_fetch_workshop_item_links_success(mock_dependencies, requests_mock):
    """Test successful fetching of workshop item links"""
    mock_dependencies["is_server_online"].return_value = True
    mock_dependencies["extract_links"].return_value = [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"
    ]
    mock_dependencies["has_next_page"].return_value = False
    requests_mock.get(
        "https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1",
        text=(
            '<div class="workshopItem"><a class="ugc" '
            'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"></a></div>'
        ),
    )

    result = fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")
    expected_result = [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"
    ]
    if result != expected_result:
        pytest.fail("Result should be " + str(expected_result))


def test_fetch_workshop_item_links_server_offline(mock_dependencies):
    """Test fetching workshop item links when server is offline"""
    mock_dependencies["is_server_online"].return_value = False
    with pytest.raises(
        ConnectionError,
        match="Steam Community is currently offline. Please try again later",
    ):
        fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")


def test_fetch_workshop_item_links_no_items(mock_dependencies, requests_mock):
    """Test fetching workshop item links with no items found"""
    mock_dependencies["is_server_online"].return_value = True
    mock_dependencies["extract_links"].return_value = []
    mock_dependencies["has_next_page"].return_value = False
    requests_mock.get(
        "https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1",
        text='<div class="noItems"></div>',
    )

    with pytest.raises(ValueError, match="No items were found in your Steam Workshop"):
        fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")


def test_fetch_workshop_item_links_parsing_error(mock_dependencies, requests_mock):
    """Test fetching workshop item links with parsing error"""
    mock_dependencies["is_server_online"].return_value = True
    mock_dependencies["extract_links"].side_effect = AttributeError("Parsing error")
    requests_mock.get(
        "https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1",
        text='<div class="workshopItem"></div>',
    )

    with patch("api.steam_workshop.logger") as mock_logger:
        with pytest.raises(
            ValueError, match="No items were found in your Steam Workshop"
        ):
            fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")
        mock_logger.error.assert_called_with(
            "Parsing error: %s. The structure of the page might have changed",
            "Parsing error",
        )


def test_fetch_workshop_item_links_multiple_pages(mock_dependencies, requests_mock):
    """Test fetching workshop item links with multiple pages"""
    mock_dependencies["is_server_online"].return_value = True
    mock_dependencies["extract_links"].side_effect = [
        ["https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"],
        ["https://steamcommunity.com/sharedfiles/filedetails/?id=2984474066"],
    ]
    mock_dependencies["has_next_page"].side_effect = [True, False]
    requests_mock.get(
        "https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=1",
        text=(
            '<div class="workshopItem"><a class="ugc" '
            'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"></a></div>'
        ),
    )
    requests_mock.get(
        "https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=2",
        text=(
            '<div class="workshopItem"><a class="ugc" '
            'href="https://steamcommunity.com/sharedfiles/filedetails/?id=2984474066"></a></div>'
        ),
    )

    result = fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")
    expected_result = [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065",
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474066",
    ]
    if result != expected_result:
        pytest.fail("Result should be " + str(expected_result))


def test_fetch_workshop_item_links_request_exception(mock_dependencies):
    """Test fetch_workshop_item_links when a request exception occurs"""
    mock_dependencies["is_server_online"].return_value = True

    with patch(
        "api.steam_workshop.requests.get",
        side_effect=requests.exceptions.ConnectionError,
    ):
        with patch("api.steam_workshop.handle_request_exception") as mock_handle:
            with pytest.raises(
                ValueError, match="No items were found in your Steam Workshop"
            ):
                fetch_workshop_item_links("dummy_custom_id", "dummy_api_key")
            mock_handle.assert_called_once()


@pytest.mark.parametrize(
    "html_input, is_tag, expected, should_log_error, error_value",
    [
        (
            "<table>"
            + "<tr><td>1,234</td><td>Subscribers</td></tr>"
            + "<tr><td>56</td><td>Favorites</td></tr>"
            + "</table>",
            True,
            {"subscribers": 1234, "favorites": 56},
            False,
            None,
        ),
        (
            "not_a_tag",
            False,
            {},
            False,
            None,
        ),
        (
            "<table></table>",
            True,
            {},
            False,
            None,
        ),
        (
            "<table><tr><td>abc</td><td>Downloads</td></tr></table>",
            True,
            {"downloads": 0},
            True,
            "abc",
        ),
    ],
)
def test_parse_stats_table_combined(
    html_input, is_tag, expected, should_log_error, error_value
):
    """Test parse_stats_table with various inputs"""
    if is_tag:
        soup = BeautifulSoup(html_input, "html.parser")
        stats_table = soup.find("table")
    else:
        stats_table = html_input

    if should_log_error:
        with patch("api.steam_workshop.logger") as mock_logger:
            result = parse_stats_table(stats_table)
            if result != expected:
                pytest.fail(f"Expected {expected}, got {result}")
            if mock_logger.error.call_count != 1:
                pytest.fail("Expected logger.error to be called once")
            if (
                mock_logger.error.call_args[0][0]
                != "Could not convert value to int: %s"
            ):
                pytest.fail("Incorrect error message format")
            if mock_logger.error.call_args[0][1] != error_value:
                pytest.fail(
                    f"Expected error value '{error_value}', got '{
                        mock_logger.error.call_args[0][1]}'"
                )
    else:
        result = parse_stats_table(stats_table)
        if result != expected:
            pytest.fail(f"Expected {expected}, got {result}")


def test_fetch_individual_workshop_stats_success(mock_requests_get, mock_beautifulsoup):
    """Test successful fetching of individual workshop stats"""
    mock_requests_get.return_value = Mock(
        status_code=200,
        content='<table class="stats_table"><tr><td>100</td><td>unique_visitors</td></tr></table>',
    )
    mock_soup = BeautifulSoup(
        '<table class="stats_table"><tr><td>100</td><td>unique_visitors</td></tr></table>',
        "html.parser",
    )
    mock_beautifulsoup.return_value = mock_soup

    result = fetch_individual_workshop_stats("https://example.com")

    if result["unique_visitors"] != 100:
        raise AssertionError("Expected unique_visitors to be 100")
    if result["current_subscribers"] != 0:
        raise AssertionError("Expected current_subscribers to be 0")
    if result["current_favorites"] != 0:
        raise AssertionError("Expected current_favorites to be 0")


def test_fetch_individual_workshop_stats_no_table(
    mock_requests_get, mock_beautifulsoup
):
    """Test fetching of individual workshop stats with no stats table"""
    mock_requests_get.return_value = Mock(
        status_code=200, content="<div>No stats table</div>"
    )
    mock_soup = BeautifulSoup("<div>No stats table</div>", "html.parser")
    mock_beautifulsoup.return_value = mock_soup

    result = fetch_individual_workshop_stats("https://example.com")

    if result["unique_visitors"]:
        raise AssertionError("Expected unique_visitors to be 0")
    if result["current_subscribers"]:
        raise AssertionError("Expected current_subscribers to be 0")
    if result["current_favorites"]:
        raise AssertionError("Expected current_favorites to be 0")


def test_fetch_individual_workshop_stats_request_exception(mock_requests_get):
    """Test request exception handling for individual workshop stats"""
    mock_requests_get.side_effect = requests.exceptions.RequestException

    result = fetch_individual_workshop_stats("https://example.com")

    if result:
        raise AssertionError("Expected result to be an empty dictionary")


def test_fetch_all_workshop_stats_all_success():
    """Test fetch_all_workshop_stats with all successful responses"""
    mock_stats_1 = {
        "unique_visitors": 100,
        "current_subscribers": 50,
        "current_favorites": 25,
    }
    mock_stats_2 = {
        "unique_visitors": 200,
        "current_subscribers": 75,
        "current_favorites": 35,
    }

    with patch("api.steam_workshop.fetch_individual_workshop_stats") as mock_fetch:
        mock_fetch.side_effect = [mock_stats_1, mock_stats_2]
        result = fetch_all_workshop_stats(
            ["https://example.com/item1", "https://example.com/item2"]
        )

    if result["total_unique_visitors"] != 300:
        raise AssertionError("Expected total_unique_visitors to be 300")
    if result["total_current_subscribers"] != 125:
        raise AssertionError("Expected total_current_subscribers to be 125")
    if result["total_current_favorites"] != 60:
        raise AssertionError("Expected total_current_favorites to be 60")
    if len(result["individual_stats"]) != 2:
        raise AssertionError("Expected two individual stat entries")


def test_fetch_all_workshop_stats_partial_failure():
    """Test fetch_all_workshop_stats with one failure and one success"""
    mock_stats = {
        "unique_visitors": 200,
        "current_subscribers": 75,
        "current_favorites": 35,
    }

    with patch("api.steam_workshop.fetch_individual_workshop_stats") as mock_fetch:
        mock_fetch.side_effect = [
            requests.exceptions.RequestException("Network failed"),
            mock_stats,
        ]
        result = fetch_all_workshop_stats(
            ["https://example.com/item1", "https://example.com/item2"]
        )

    if result["total_unique_visitors"] != 200:
        raise AssertionError("Expected total_unique_visitors to be 200")
    if result["total_current_subscribers"] != 75:
        raise AssertionError("Expected total_current_subscribers to be 75")
    if result["total_current_favorites"] != 35:
        raise AssertionError("Expected total_current_favorites to be 35")
    if len(result["individual_stats"]) != 1:
        raise AssertionError("Expected one individual stat entry")


def test_fetch_all_workshop_stats_all_failures():
    """Test fetch_all_workshop_stats with all requests failing"""
    with patch("api.steam_workshop.fetch_individual_workshop_stats") as mock_fetch:
        mock_fetch.side_effect = [
            requests.exceptions.RequestException("Boom"),
            AttributeError("Missing attribute"),
        ]
        result = fetch_all_workshop_stats(
            ["https://example.com/item1", "https://example.com/item2"]
        )

    if result["total_unique_visitors"] != 0:
        raise AssertionError("Expected total_unique_visitors to be 0")
    if result["total_current_subscribers"] != 0:
        raise AssertionError("Expected total_current_subscribers to be 0")
    if result["total_current_favorites"] != 0:
        raise AssertionError("Expected total_current_favorites to be 0")
    if len(result["individual_stats"]) != 0:
        raise AssertionError("Expected no individual stat entries")
