"""Test Main Runner Script"""
# Disable pylint warnings for false positives
# pylint: disable=redefined-outer-name
from unittest import mock
from unittest.mock import patch, ANY
import pytest
from api.main import (main, update_readme, get_player_summaries, get_recently_played_games,
                      fetch_workshop_item_links, generate_steam_stats, generate_workshop_stats)


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("INPUT_STEAM_API_KEY", "dummy_api_key")
    monkeypatch.setenv("INPUT_STEAM_CUSTOM_ID", "dummy_custom_id")


@pytest.fixture
def readme_content():
    """Fixture to provide initial README content"""
    return "Some initial content\n<!-- START -->\nOld content\n<!-- END -->\nSome final content"


@pytest.fixture
def updated_readme_content():
    """Fixture to provide expected updated README content"""
    return "Some initial content\n<!-- START -->\nNew content\n<!-- END -->\nSome final content"


def test_update_readme_success(readme_content, updated_readme_content, tmp_path):
    """Test successful update of README.md"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")

    with mock.patch("api.main.logger") as mock_logger:
        update_readme("New content", "<!-- START -->",
                      "<!-- END -->", readme_path=str(readme_path))

        result = readme_path.read_text(encoding="utf-8")
        if result != updated_readme_content:
            raise AssertionError("Expected README content to be updated")

        if mock_logger.error.called:
            raise AssertionError("Expected no errors to be logged")


def test_update_readme_start_marker_not_found(readme_content, tmp_path):
    """Test when start marker is not found in README.md"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")

    with mock.patch("api.main.logger") as mock_logger:
        update_readme("New content", "<!-- NON_EXISTENT_START -->",
                      "<!-- END -->", readme_path=str(readme_path))

        result = readme_path.read_text(encoding="utf-8")
        if result != readme_content:
            raise AssertionError("Expected README content to remain unchanged")

        if not mock_logger.error.called:
            raise AssertionError(
                "Expected an error to be logged for missing start marker")


def test_update_readme_end_marker_not_found(readme_content, tmp_path):
    """Test when end marker is not found in README.md"""
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")

    with mock.patch("api.main.logger") as mock_logger:
        update_readme("New content", "<!-- START -->",
                      "<!-- NON_EXISTENT_END -->", readme_path=str(readme_path))

        result = readme_path.read_text(encoding="utf-8")
        if result != readme_content:
            raise AssertionError("Expected README content to remain unchanged")

        if not mock_logger.error.called:
            raise AssertionError(
                "Expected an error to be logged for missing end marker")


def test_update_readme_no_markers(tmp_path):
    """Test when neither start nor end markers are found in README.md"""
    readme_content = "Some initial content\nSome final content"
    readme_path = tmp_path / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")

    with mock.patch("api.main.logger") as mock_logger:
        update_readme("New content", "<!-- START -->",
                      "<!-- END -->", readme_path=str(readme_path))

        result = readme_path.read_text(encoding="utf-8")
        if result != readme_content:
            raise AssertionError("Expected README content to remain unchanged")

        if not mock_logger.error.called:
            raise AssertionError(
                "Expected errors to be logged for missing markers")


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
    result = get_player_summaries()
    if result is None:
        raise AssertionError("Expected result to be not None")
    if result is None or "response" not in result:
        raise AssertionError("Expected 'response' to be in result")
    if "players" not in result["response"]:
        raise AssertionError("Expected 'players' to be in result['response']")


def test_get_recently_played_games_success(requests_mock):
    """Test successful retrieval of recently played games"""
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 1, "games": [
            {"name": "TestGame", "playtime_2weeks": 120,
                "appid": 12345, "img_icon_url": "icon.jpg"}
        ]}}
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
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 0}}
    )
    result = get_recently_played_games()
    if result is not None:
        raise AssertionError("Expected result to be None")


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
    expected_result = [
        "https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065"]
    if result != expected_result:
        raise AssertionError(f"Result should be {expected_result}")


def test_generate_steam_stats(requests_mock):
    """Test generating Steam Stats"""
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
    with mock.patch('api.main.generate_card_for_player_summary', return_value="![Steam Summary]"):
        with mock.patch('api.main.generate_card_for_played_games',
                        return_value="![Recently Played Games]"):
            result = generate_steam_stats()
            if "![Steam Summary]" not in result:
                raise AssertionError(
                    "Expected '![Steam Summary]' to be in result")
            if "![Recently Played Games]" not in result:
                raise AssertionError(
                    "Expected '![Recently Played Games]' to be in result")

    requests_mock.get(
        'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
        json={"response": {"players": []}}
    )
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 1, "games": [
            {"name": "TestGame", "playtime_2weeks": 120,
                "appid": 12345, "img_icon_url": "icon.jpg"}
        ]}}
    )
    with mock.patch('api.main.generate_card_for_player_summary', return_value=None):
        with mock.patch('api.main.generate_card_for_played_games',
                        return_value="![Recently Played Games]"):
            result = generate_steam_stats()
            if "![Steam Summary]" in result:
                raise AssertionError(
                    "Expected '![Steam Summary]' not to be in result")
            if "![Recently Played Games]" not in result:
                raise AssertionError(
                    "Expected '![Recently Played Games]' to be in result")

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
        json={"response": {"total_count": 0}}
    )
    with mock.patch('api.main.generate_card_for_player_summary', return_value="![Steam Summary]"):
        with mock.patch('api.main.generate_card_for_played_games', return_value=None):
            result = generate_steam_stats()
            if "![Steam Summary]" not in result:
                raise AssertionError(
                    "Expected '![Steam Summary]' to be in result")
            if "![Recently Played Games]" in result:
                raise AssertionError(
                    "Expected '![Recently Played Games]' not to be in result")

    requests_mock.get(
        'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
        json={"response": {"players": []}}
    )
    requests_mock.get(
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/',
        json={"response": {"total_count": 0}}
    )
    with mock.patch('api.main.generate_card_for_player_summary', return_value=None):
        with mock.patch('api.main.generate_card_for_played_games', return_value=None):
            result = generate_steam_stats()
            if result:
                raise AssertionError("Expected result to be empty")

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
    with mock.patch('api.main.generate_card_for_player_summary', return_value=None):
        with mock.patch('api.main.generate_card_for_played_games', return_value=None):
            result = generate_steam_stats()
            if result:
                raise AssertionError("Expected result to be empty")

    with mock.patch('api.main.get_player_summaries', return_value=None):
        with mock.patch('api.main.get_recently_played_games',
                        return_value={"response": {"total_count": 1, "games": [
                            {"name": "TestGame", "playtime_2weeks": 120,
                             "appid": 12345, "img_icon_url": "icon.jpg"}
                        ]}}):
            with mock.patch('api.main.generate_card_for_played_games',
                            return_value="![Recently Played Games]"):
                result = generate_steam_stats()
                if "![Steam Summary]" in result:
                    raise AssertionError(
                        "Expected '![Steam Summary]' not to be in result")
                if "![Recently Played Games]" not in result:
                    raise AssertionError(
                        "Expected '![Recently Played Games]' to be in result")


def test_generate_workshop_stats(requests_mock):
    """Test generating Workshop stats"""
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
    requests_mock.get(
        'https://steamcommunity.com/id/dummy_custom_id/myworkshopfiles/?p=2',
        text=''
    )
    with mock.patch('api.main.generate_card_for_steam_workshop',
                    return_value="![Steam Workshop Stats]"):
        result = generate_workshop_stats()
        if "![Steam Workshop Stats]" not in result:
            raise AssertionError(
                "Expected '![Steam Workshop Stats]' to be in result")

    with mock.patch('api.main.fetch_workshop_item_links', return_value=None):
        result = generate_workshop_stats()
        if result:
            raise AssertionError(
                "Expected result to be empty when no workshop item links are found")

    with mock.patch('api.main.fetch_workshop_item_links',
                    return_value=[
                        'https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065'
                    ]):
        with mock.patch('api.main.fetch_all_workshop_stats',
                        return_value={
                            "total_unique_visitors": 1000, "total_current_subscribers": 500,
                            "total_current_favorites": 250, "individual_stats": []
                        }):
            with mock.patch('api.main.generate_card_for_steam_workshop', return_value=None):
                result = generate_workshop_stats()
                if result:
                    raise AssertionError(
                        "Expected result to be empty when card generation fails")

    with mock.patch('api.main.fetch_workshop_item_links', return_value=[]):
        result = generate_workshop_stats()
        if result:
            raise AssertionError(
                "Expected result to be empty when no workshop item links are found")

    with mock.patch('api.main.fetch_workshop_item_links',
                    return_value=[
                        'https://steamcommunity.com/sharedfiles/filedetails/?id=2984474065'
                    ]):
        with mock.patch('api.main.fetch_all_workshop_stats', return_value={}):
            with mock.patch('api.main.generate_card_for_steam_workshop', return_value=None):
                result = generate_workshop_stats()
                if result:
                    raise AssertionError(
                        "Expected result to be empty when no workshop stats are found")


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

    with patch('api.main.WORKSHOP_STATS', True):
        with patch('api.main.update_readme') as mock_update_readme:
            main()
            mock_update_readme.assert_any_call(
                ANY, "<!-- Steam-Stats start -->", "<!-- Steam-Stats end -->")
            mock_update_readme.assert_any_call(
                ANY, "<!-- Steam-Workshop start -->", "<!-- Steam-Workshop end -->")

    with patch('api.main.generate_steam_stats', return_value=""):
        with patch('api.main.logger') as mock_logger:
            main()
            mock_logger.error.assert_called_with(
                "Failed to update README with latest Steam Stats")

    with patch('api.main.WORKSHOP_STATS', True):
        with patch('api.main.generate_workshop_stats', return_value=""):
            with patch('api.main.logger') as mock_logger:
                main()
                mock_logger.error.assert_called_with(
                    "Failed to update README with latest Workshop Stats")
