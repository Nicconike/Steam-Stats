"""Test Card Generation Script"""
# Disable pylint warnings for false positives
# pylint: disable=duplicate-code
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from api.card import (
    get_element_bounding_box,
    html_to_png,
    convert_html_to_png,
    format_unix_time,
    generate_card_for_player_summary,
    generate_card_for_played_games,
    generate_card_for_steam_workshop
)


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("GITHUB_REF_NAME", "main")


@pytest.mark.asyncio
async def test_get_element_bounding_box():
    """Test get_element_bounding_box function"""
    html_file = "test.html"
    selector = ".test-element"
    bounding_box = {"x": 10, "y": 20, "width": 100, "height": 200}

    with patch("os.path.exists", return_value=True), \
            patch("api.card.async_playwright") as mock_playwright:
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value=bounding_box)
        mock_page.goto = AsyncMock()
        mock_page.close = AsyncMock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_browser.close = AsyncMock()
        mock_playwright.return_value.__aenter__.return_value.firefox.launch = AsyncMock(
            return_value=mock_browser)

        result = await get_element_bounding_box(html_file, selector)
        if result != bounding_box:
            raise AssertionError(f"Expected result to be {bounding_box}")


@pytest.mark.asyncio
async def test_html_to_png():
    """Test html_to_png function"""
    html_file = "test.html"
    output_file = "output.png"
    selector = ".test-element"
    bounding_box = {"x": 10, "y": 20, "width": 100, "height": 200}

    with patch("os.path.exists", return_value=True), \
            patch("api.card.get_element_bounding_box", new_callable=AsyncMock,
                  return_value=bounding_box), \
            patch("api.card.async_playwright") as mock_playwright:
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_page.goto = AsyncMock()
        mock_page.screenshot = AsyncMock()
        mock_page.close = AsyncMock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_browser.close = AsyncMock()
        mock_playwright.return_value.__aenter__.return_value.firefox.launch = AsyncMock(
            return_value=mock_browser)

        await html_to_png(html_file, output_file, selector)
        mock_page.screenshot.assert_called_once_with(
            path=output_file, clip=bounding_box)


def test_convert_html_to_png():
    """Test convert_html_to_png function"""
    html_file = "test.html"
    output_file = "output.png"
    selector = ".test-element"

    with patch("api.card.html_to_png", new_callable=AsyncMock) as mock_html_to_png:
        convert_html_to_png(html_file, output_file, selector)
        mock_html_to_png.assert_called_once_with(
            html_file, output_file, selector)


def test_format_unix_time():
    """Test format_unix_time function"""
    unix_time = 1609459200  # 01/01/2021 @ 12:00am (UTC)
    expected = "01/01/2021"
    result = format_unix_time(unix_time)
    if result != expected:
        raise AssertionError(f"Expected result to be {expected}")


def test_generate_card_for_player_summary():
    """Test generate_card_for_player_summary function"""
    player_data = {
        "response": {
            "players": [{
                "personaname": "TestUser",
                "personastate": 1,
                "avatarfull": "http://example.com/avatar.jpg",
                "loccountrycode": "US",
                "lastlogoff": 1609459200,
                "timecreated": 1609459200,
                "gameextrainfo": "TestGame"
            }]
        }
    }
    result = generate_card_for_player_summary(player_data)
    if result is None:
        raise AssertionError("Result should not be None")
    if "![Steam Summary]" not in result:
        raise AssertionError("Result should contain '![Steam Summary]'")


def test_generate_card_for_played_games():
    """Test generate_card_for_played_games function"""
    games_data = {
        "response": {
            "games": [{
                "name": "TestGame",
                "playtime_2weeks": 120,
                "appid": 12345,
                "img_icon_url": "icon.jpg"
            }]
        }
    }
    result = generate_card_for_played_games(games_data)
    if result is None:
        raise AssertionError("Result should not be None")
    if "![Recently Played Games]" not in result:
        raise AssertionError(
            "Result should contain '![Recently Played Games]'")


def test_generate_card_for_steam_workshop():
    """Test generate_card_for_steam_workshop function"""
    workshop_stats = {
        "total_unique_visitors": 1000,
        "total_current_subscribers": 500,
        "total_current_favorites": 200
    }
    result = generate_card_for_steam_workshop(workshop_stats)
    if result is None:
        raise AssertionError("Result should not be None")
    if "![Steam Workshop Stats]" not in result:
        raise AssertionError("Result should contain '![Steam Workshop Stats]'")
