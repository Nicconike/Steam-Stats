"""Test Card Generation Script"""

# Disable pylint warnings for false positives
# pylint: disable=duplicate-code,redefined-outer-name,unused-argument,unused-variable
import asyncio
from unittest import mock
from unittest.mock import patch, MagicMock, AsyncMock
from playwright.async_api import Error as PlaywrightError
import pytest
from api.card import (
    handle_exception,
    get_element_bounding_box,
    html_to_png,
    convert_html_to_png,
    format_unix_time,
    generate_card_for_player_summary,
    format_playtime,
    generate_card_for_played_games,
    generate_card_for_steam_workshop,
)


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("GITHUB_REF_NAME", "main")


def test_handle_file_not_found_error(caplog):
    """Test handle_exception with FileNotFoundError"""
    exception = FileNotFoundError("Test File Not Found Error")
    handle_exception(exception)
    if len(caplog.records) != 1:
        pytest.fail("Expected one log record, found " + str(len(caplog.records)))
    if caplog.records[0].levelname != "ERROR":
        pytest.fail("Expected log level ERROR, found " + caplog.records[0].levelname)
    if caplog.records[0].message != "File Not Found Error: Test File Not Found Error":
        pytest.fail(
            "Expected log message 'File Not Found Error: Test File Not Found Error', found "
            + caplog.records[0].message
        )


def test_handle_playwright_error(caplog):
    """Test handle_exception with PlaywrightError"""
    exception = PlaywrightError("Test Playwright Error")
    handle_exception(exception)
    if len(caplog.records) != 1:
        pytest.fail("Expected one log record, found " + str(len(caplog.records)))
    if caplog.records[0].levelname != "ERROR":
        pytest.fail("Expected log level ERROR, found " + caplog.records[0].levelname)
    if caplog.records[0].message != "Playwright Error: Test Playwright Error":
        pytest.fail(
            "Expected log message 'Playwright Error: Test Playwright Error', found "
            + caplog.records[0].message
        )


def test_handle_key_error(caplog):
    """Test handle_exception with KeyError"""
    exception = KeyError("Test Key Error")
    handle_exception(exception)
    if len(caplog.records) != 1:
        pytest.fail("Expected one log record, found " + str(len(caplog.records)))
    if caplog.records[0].levelname != "ERROR":
        pytest.fail("Expected log level ERROR, found " + caplog.records[0].levelname)
    if caplog.records[0].message != "Key Error: 'Test Key Error'":
        pytest.fail(
            "Expected log message 'Key Error: Test Key Error', found "
            + caplog.records[0].message
        )


def test_handle_timeout_error(caplog):
    """Test handle_exception with asyncio.TimeoutError"""
    exception = asyncio.TimeoutError("Test Timeout Error")
    handle_exception(exception)
    if len(caplog.records) != 1:
        pytest.fail("Expected one log record, found " + str(len(caplog.records)))
    if caplog.records[0].levelname != "ERROR":
        pytest.fail("Expected log level ERROR, found " + caplog.records[0].levelname)
    if caplog.records[0].message != "Timeout Error: Test Timeout Error":
        pytest.fail(
            "Expected log message 'Timeout Error: Test Timeout Error', found "
            + caplog.records[0].message
        )


def test_handle_unexpected_error(caplog):
    """Test handle_exception with an unexpected error"""
    exception = Exception("Test Unexpected Error")
    handle_exception(exception)
    if len(caplog.records) != 1:
        pytest.fail("Expected one log record, found " + str(len(caplog.records)))
    if caplog.records[0].levelname != "ERROR":
        pytest.fail("Expected log level ERROR, found " + caplog.records[0].levelname)
    if caplog.records[0].message != "Unexpected Error: Test Unexpected Error":
        pytest.fail(
            "Expected log message 'Unexpected Error: Test Unexpected Error', found "
            + caplog.records[0].message
        )


async def _test_file_not_found_error(html_file, selector):
    """Helper function to test FileNotFoundError"""
    with mock.patch("os.path.exists", return_value=False):
        with mock.patch("api.card.logger") as mock_logger:
            result = await get_element_bounding_box(html_file, selector)
            if result is not None:
                raise AssertionError("Expected result to be None for FileNotFoundError")
            if not mock_logger.error.called:
                raise AssertionError(
                    "Expected logger.error to be called for FileNotFoundError"
                )
            if mock_logger.error.call_args[0][
                0
            ] != "File Not Found Error: %s" or "HTML file not found:" not in str(
                mock_logger.error.call_args[0][1]
            ):
                raise AssertionError(
                    "Expected logger.error to be called with 'File Not Found Error: %s',"
                    "'HTML file not found:'"
                )


async def _test_playwright_error(html_file, selector):
    """Helper function to test PlaywrightError"""
    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("api.card.async_playwright") as mock_playwright:
            mock_playwright.return_value.__aenter__.side_effect = PlaywrightError(
                "Playwright error"
            )
            with mock.patch("api.card.logger") as mock_logger:
                result = await get_element_bounding_box(html_file, selector)
                if result is not None:
                    raise AssertionError(
                        "Expected result to be None for PlaywrightError"
                    )
                if not mock_logger.error.called:
                    raise AssertionError(
                        "Expected logger.error to be called for PlaywrightError"
                    )
                if mock_logger.error.call_args[0][
                    0
                ] != "Playwright Error: %s" or "Playwright error" not in str(
                    mock_logger.error.call_args[0][1]
                ):
                    raise AssertionError(
                        "Expected logger.error to be called with 'Playwright Error: %s',"
                        "'Playwright error'"
                    )


async def _test_key_error(html_file, selector):
    """Helper function to test KeyError"""
    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("api.card.async_playwright") as mock_playwright:
            mock_browser = mock.AsyncMock()
            mock_page = mock.AsyncMock()
            mock_element = mock.AsyncMock()
            mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = (
                mock_browser
            )
            mock_browser.new_page.return_value = mock_page
            mock_page.query_selector.return_value = mock_element
            mock_element.bounding_box.side_effect = KeyError(
                "Key error while retrieving bounding box"
            )
            with mock.patch("api.card.logger") as mock_logger:
                result = await get_element_bounding_box(html_file, selector)
                if result is not None:
                    raise AssertionError("Expected result to be None for KeyError")
                if not mock_logger.error.called:
                    raise AssertionError(
                        "Expected logger.error to be called for KeyError"
                    )
                if mock_logger.error.call_args[0][
                    0
                ] != "Key Error: %s" or "Key error while retrieving bounding box" not in str(
                    mock_logger.error.call_args[0][1]
                ):
                    raise AssertionError(
                        "Expected logger.error to be called with "
                        "'Key Error: %s', 'Key error while retrieving bounding box'"
                    )


async def _test_timeout_error(html_file, selector):
    """Helper function to test asyncio.TimeoutError"""
    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("api.card.async_playwright") as mock_playwright:
            mock_browser = mock.AsyncMock()
            mock_page = mock.AsyncMock()
            mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = (
                mock_browser
            )
            mock_browser.new_page.return_value = mock_page
            mock_page.goto.side_effect = asyncio.TimeoutError(
                "Timeout error while loading page"
            )
            with mock.patch("api.card.logger") as mock_logger:
                result = await get_element_bounding_box(html_file, selector)
                if result is not None:
                    raise AssertionError("Expected result to be None for TimeoutError")
                if not mock_logger.error.called:
                    raise AssertionError(
                        "Expected logger.error to be called for TimeoutError"
                    )
                if mock_logger.error.call_args[0][
                    0
                ] != "Timeout Error: %s" or "Timeout error while loading page" not in str(
                    mock_logger.error.call_args[0][1]
                ):
                    raise AssertionError(
                        "Expected logger.error to be called with "
                        "'Timeout Error: %s', 'Timeout error while loading page'"
                    )


async def _test_element_not_found(html_file, selector):
    """Helper function to test ValueError when element is not found"""
    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("api.card.async_playwright") as mock_playwright:
            mock_browser = mock.AsyncMock()
            mock_page = mock.AsyncMock()
            mock_page.query_selector.return_value = None  # Element not found
            mock_browser.new_page.return_value = mock_page
            mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = (
                mock_browser
            )

            with mock.patch("api.card.logger") as mock_logger:
                result = await get_element_bounding_box(html_file, selector)

                if result is not None:
                    raise AssertionError(
                        "Expected result to be None for ValueError when element not found"
                    )

                if not mock_logger.error.called:
                    raise AssertionError(
                        "Expected logger.error to be called for ValueError (element not found)"
                    )

                log_call_args = mock_logger.error.call_args[0]

                expected_msg = "Value Error: %s"
                expected_detail = f"Element not found for selector: {selector}"

                if log_call_args[0] != expected_msg:
                    raise AssertionError(
                        f"Expected logger format '{expected_msg}', got '{log_call_args[0]}'"
                    )

                if expected_detail not in str(log_call_args[1]):
                    raise AssertionError(
                        f"Expected exception message to contain '{expected_detail}', got '{
                            log_call_args[1]}'"
                    )


async def _test_bounding_box_none_error(html_file, selector):
    """Helper function to test ValueError when bounding box is None"""
    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("api.card.async_playwright") as mock_playwright:
            mock_browser = mock.AsyncMock()
            mock_page = mock.AsyncMock()
            mock_element = mock.AsyncMock()

            mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = (
                mock_browser
            )
            mock_browser.new_page.return_value = mock_page
            mock_page.query_selector.return_value = mock_element

            # Simulate bounding_box returning None
            mock_element.bounding_box.return_value = None

            with mock.patch("api.card.logger") as mock_logger:
                result = await get_element_bounding_box(html_file, selector)

                if result is not None:
                    raise AssertionError(
                        "Expected result to be None when bounding box is None"
                    )

                if not mock_logger.error.called:
                    raise AssertionError(
                        "Expected logger.error to be called when bounding box is None"
                    )

                if mock_logger.error.call_args[0][0] != "Value Error: %s" or (
                    "Could not retrieve bounding box for selector"
                    not in str(mock_logger.error.call_args[0][1])
                ):
                    raise AssertionError(
                        "Expected logger.error to be called with "
                        "'Value Error: %s', 'Could not retrieve bounding box for selector...'"
                    )


def test_get_element_bounding_box():
    """Test get_element_bounding_box function"""
    html_file = "test.html"
    selector = ".test-element"
    asyncio.run(_test_file_not_found_error(html_file, selector))
    asyncio.run(_test_playwright_error(html_file, selector))
    asyncio.run(_test_key_error(html_file, selector))
    asyncio.run(_test_timeout_error(html_file, selector))
    asyncio.run(_test_element_not_found(html_file, selector))
    asyncio.run(_test_bounding_box_none_error(html_file, selector))


@pytest.mark.asyncio
async def test_html_to_png():
    """Test html_to_png function"""
    html_file = "test.html"
    output_file = "output.png"
    selector = ".test-element"
    bounding_box = {"x": 10, "y": 20, "width": 100, "height": 200}

    with patch("os.path.exists", return_value=True), patch(
        "api.card.get_element_bounding_box",
        new_callable=AsyncMock,
        return_value=bounding_box,
    ), patch("api.card.async_playwright") as mock_playwright:
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_page.goto = AsyncMock()
        mock_page.screenshot = AsyncMock()
        mock_page.close = AsyncMock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_browser.close = AsyncMock()
        mock_playwright.return_value.__aenter__.return_value.chromium.launch = (
            AsyncMock(return_value=mock_browser)
        )

        await html_to_png(html_file, output_file, selector)
        mock_page.screenshot.assert_called_once_with(
            path=output_file, clip=bounding_box
        )


@pytest.mark.asyncio
async def test_html_to_png_bounding_box_none():
    """Test html_to_png when get_element_bounding_box returns None"""
    html_file = "test.html"
    output_file = "output.png"
    selector = ".invalid-element"

    with patch(
        "api.card.get_element_bounding_box", new_callable=AsyncMock, return_value=None
    ), patch("api.card.logger") as mock_logger:
        result = await html_to_png(html_file, output_file, selector)
        if result:
            pytest.fail("Expected False when bounding box is None")
        if mock_logger.error.call_count != 1:
            pytest.fail("Expected logger.error to be called once")
        if mock_logger.error.call_args[0][0] != "Bounding box could not be determined":
            pytest.fail("Incorrect error message logged")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception", [PlaywrightError("Failed to launch"), asyncio.TimeoutError()]
)
async def test_html_to_png_exceptions(exception):
    """Test html_to_png when PlaywrightError or TimeoutError is raised"""
    html_file = "test.html"
    output_file = "output.png"
    selector = ".test-element"
    bbox = {"x": 0, "y": 0, "width": 100, "height": 100}

    with patch(
        "api.card.get_element_bounding_box", new_callable=AsyncMock, return_value=bbox
    ), patch("api.card.async_playwright") as mock_playwright, patch(
        "api.card.handle_exception"
    ) as mock_handle:

        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_page.goto = AsyncMock(side_effect=exception)
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_browser.close = AsyncMock()
        mock_playwright.return_value.__aenter__.return_value.chromium.launch = (
            AsyncMock(return_value=mock_browser)
        )

        result = await html_to_png(html_file, output_file, selector)
        if result:
            pytest.fail(f"Expected False due to exception: {exception}")
        if mock_handle.call_count != 1:
            pytest.fail("handle_exception should be called once")
        if mock_handle.call_args[0][0] != exception:
            pytest.fail("handle_exception called with incorrect exception")


def test_convert_html_to_png():
    """Test convert_html_to_png function"""
    html_file = "test.html"
    output_file = "output.png"
    selector = ".test-element"

    with patch("api.card.html_to_png", new_callable=AsyncMock) as mock_html_to_png:
        convert_html_to_png(html_file, output_file, selector)
        mock_html_to_png.assert_called_once_with(html_file, output_file, selector)


@pytest.mark.parametrize(
    "raised_exception",
    [
        FileNotFoundError("File not found"),
        PlaywrightError("Playwright failed"),
        KeyError("Missing key"),
        asyncio.TimeoutError(),
    ],
)
def test_convert_html_to_png_exceptions(raised_exception):
    """Test convert_html_to_png when various exceptions are raised"""
    html_file = "test.html"
    output_file = "output.png"
    selector = ".test-element"

    with patch("api.card.html_to_png", side_effect=raised_exception), patch(
        "api.card.handle_exception"
    ) as mock_handle:
        result = convert_html_to_png(html_file, output_file, selector)
        if result:
            pytest.fail(f"Expected False for exception: {raised_exception}")
        if mock_handle.call_count != 1:
            pytest.fail("handle_exception should be called once")
        if mock_handle.call_args[0][0] != raised_exception:
            pytest.fail("handle_exception called with wrong exception")


def test_format_unix_time():
    """Test format_unix_time function"""
    unix_time = 1609459200  # 01/01/2021 @ 12:00am (UTC)
    expected = "1st Jan 2021"
    result = format_unix_time(unix_time)
    if result != expected:
        raise AssertionError(f"Expected result to be {expected}, but got {result}")


def test_generate_card_for_player_summary():
    """Test generate_card_for_player_summary function"""
    player_data = {
        "response": {
            "players": [
                {
                    "personaname": "TestUser",
                    "personastate": 1,
                    "avatarfull": "https://example.com/avatar.jpg",
                    "loccountrycode": "US",
                    "lastlogoff": 1609459200,
                    "timecreated": 1609459200,
                    "gameextrainfo": "TestGame",
                }
            ]
        }
    }
    result = generate_card_for_player_summary(player_data)
    if result is None:
        raise AssertionError("Result should not be None")
    if "![Steam Summary]" not in result:
        raise AssertionError("Result should contain '![Steam Summary]'")

    result_none = generate_card_for_player_summary(None)
    if result_none is not None:
        raise AssertionError("Expected None when player_data is None")

    result_empty = generate_card_for_player_summary({})
    if result_empty is not None:
        raise AssertionError("Expected None when player_data is empty")


@pytest.mark.parametrize(
    "playtime,expected",
    [
        (1, "1 min"),  # less than 60 mins, singular
        (45, "45 mins"),  # less than 60 mins, plural
        (60, "1 hrs"),  # exactly 60 mins, no leftover minutes
        (120, "2 hrs"),  # multiple hours, no leftover minutes
        (121, "2 hrs and 1 min"),  # multiple hours, singular leftover minute
        (135, "2 hrs and 15 mins"),  # multiple hours, plural leftover minutes
    ],
)
def test_format_playtime(playtime, expected):
    """Test format_playtime function with various playtime inputs."""
    actual = format_playtime(playtime)
    if actual != expected:
        pytest.fail(f"Expected '{expected}', got '{actual}' for playtime={playtime}")


def test_generate_card_for_played_games():
    """Test generate_card_for_played_games function"""
    games_data = {
        "response": {
            "games": [
                {
                    "name": "TestGame",
                    "playtime_2weeks": 120,
                    "appid": 12345,
                    "img_icon_url": "icon.jpg",
                }
            ]
        }
    }
    result = generate_card_for_played_games(games_data)
    if result is None:
        raise AssertionError("Result should not be None")
    if "![Recently Played Games]" not in result:
        raise AssertionError("Result should contain '![Recently Played Games]'")

    result_none = generate_card_for_played_games(None)
    if result_none is not None:
        raise AssertionError("Result should be None when games_data is None")

    result_empty = generate_card_for_played_games({})
    if result_empty is not None:
        raise AssertionError("Result should be None when games_data is empty")


def test_generate_card_for_steam_workshop():
    """Test generate_card_for_steam_workshop function"""
    workshop_stats = {
        "total_unique_visitors": 1000,
        "total_current_subscribers": 500,
        "total_current_favorites": 200,
    }
    result = generate_card_for_steam_workshop(workshop_stats)
    if result is None:
        raise AssertionError("Result should not be None")
    if "![Steam Workshop Stats]" not in result:
        raise AssertionError("Result should contain '![Steam Workshop Stats]'")
