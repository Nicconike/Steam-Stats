"""Test Main Runner Script"""

# Disable pylint warnings for false positives
# pylint: disable=redefined-outer-name, unused-argument
import logging
from unittest import TestCase
from unittest.mock import patch, MagicMock
import time
from pytest import approx
import pytest
from api.main import (
    update_readme,
    generate_steam_stats,
    generate_workshop_stats,
    commit_to_github,
    update_readme_sections,
    update_section,
    collect_files_to_update,
    log_execution_time,
    main,
    logger,
)


@pytest.fixture
def mock_repo():
    """Mock Repo"""
    return MagicMock()


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("GITHUB_TOKEN", "fake_token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "fake/repo")
    monkeypatch.setenv("INPUT_STEAM_ID", "fake_steam_id")
    monkeypatch.setenv("INPUT_STEAM_API_KEY", "fake_steam_api_key")
    monkeypatch.setenv("INPUT_STEAM_CUSTOM_ID", "fake_steam_custom_id")
    monkeypatch.setenv("INPUT_WORKSHOP_STATS", "true")


@pytest.fixture
def mock_dependencies(mocker):
    """Fixtures for mocking dependencies"""
    fixtures = {}
    fixtures["initialize_github"] = mocker.patch("api.main.initialize_github")
    fixtures["get_readme_content"] = mocker.patch("api.main.get_readme_content")
    fixtures["update_readme_sections"] = mocker.patch("api.main.update_readme_sections")
    fixtures["collect_files_to_update"] = mocker.patch(
        "api.main.collect_files_to_update"
    )
    fixtures["commit_to_github"] = mocker.patch("api.main.commit_to_github")
    fixtures["log_execution_time"] = mocker.patch("api.main.log_execution_time")
    return fixtures


def test_update_readme(mock_repo):
    """Test Update readme Function"""
    markdown_data = "New Content"
    start_marker = "<!--START-->"
    end_marker = "<!--END-->"
    mock_repo.get_contents.return_value.decoded_content = (
        b"<!--START-->\nOld Content\n<!--END-->"
    )
    result = update_readme(mock_repo, markdown_data, start_marker, end_marker)
    TestCase().assertEqual(result, "<!--START-->\nNew Content\n<!--END-->")

    mock_repo.get_contents.return_value.decoded_content = (
        b"Some content without markers"
    )
    result = update_readme(mock_repo, markdown_data, start_marker, end_marker)
    TestCase().assertIsNone(result)

    mock_repo.get_contents.side_effect = FileNotFoundError
    result = update_readme(mock_repo, markdown_data, start_marker, end_marker)
    TestCase().assertIsNone(result)

    mock_repo.get_contents.return_value.decoded_content = (
        b"<!--START-->\nNew Content\n<!--END-->"
    )
    result = update_readme(mock_repo, markdown_data, start_marker, end_marker)
    TestCase().assertIsNone(result)


def test_update_readme_no_change(mock_repo):
    """Test update_readme returns None if content is already up to date"""
    markdown_data = "Same Content"
    start_marker = "<!--START-->"
    end_marker = "<!--END-->"

    existing_content = start_marker + "\n" + markdown_data + "\n" + end_marker
    mock_repo.get_contents.return_value.decoded_content = existing_content.encode(
        "utf-8"
    )

    result = update_readme(mock_repo, markdown_data, start_marker, end_marker)

    TestCase().assertIsNone(result)


@patch("api.main.get_player_summaries")
@patch("api.main.generate_card_for_player_summary")
@patch("api.main.get_recently_played_games")
@patch("api.main.generate_card_for_played_games")
@patch("api.main.logger")
def test_generate_steam_stats(
    mock_logger,
    mock_generate_card_played,
    mock_get_recently_played,
    mock_generate_card_summary,
    mock_get_player_summaries,
):
    """Test Generating Steam Stats"""
    mock_get_player_summaries.return_value = {"player": "summary"}
    mock_generate_card_summary.return_value = "Player Summary Card"
    mock_get_recently_played.return_value = {"games": "data"}
    mock_generate_card_played.return_value = "Played Games Card"

    result = generate_steam_stats()

    TestCase().assertIn("Player Summary Card", result)
    TestCase().assertIn("Played Games Card", result)
    mock_logger.info.assert_any_call("Retrieved Steam User Data")
    mock_logger.info.assert_any_call("Generated Card for Steam User Data")
    mock_logger.info.assert_any_call("Retrieved Recently Played Games Data")
    mock_logger.info.assert_any_call("Generated Card for Recently Played Games")

    mock_get_player_summaries.return_value = None
    mock_get_recently_played.return_value = {"games": "data"}
    mock_generate_card_played.return_value = "Played Games Card"
    result = generate_steam_stats()
    TestCase().assertIn("Played Games Card", result)
    TestCase().assertEqual(result, "Played Games Card")
    mock_logger.info.assert_any_call("No Steam User Summary data found")

    mock_get_player_summaries.return_value = {"player": "summary"}
    mock_generate_card_summary.return_value = "Player Summary Card"
    mock_get_recently_played.return_value = None
    result = generate_steam_stats()
    TestCase().assertIn("Player Summary Card", result)
    TestCase().assertEqual(result, "Player Summary Card")
    mock_logger.info.assert_any_call("No Recently Played Games data found")

    mock_get_player_summaries.return_value = {"player": "summary"}
    mock_generate_card_summary.return_value = None
    mock_get_recently_played.return_value = {"games": "data"}
    mock_generate_card_played.return_value = "Played Games Card"
    result = generate_steam_stats()
    TestCase().assertIn("Played Games Card", result)
    TestCase().assertEqual(result, "Played Games Card")
    mock_logger.error.assert_any_call("Failed to generate card for Steam Summary")

    mock_get_player_summaries.return_value = {"player": "summary"}
    mock_generate_card_summary.return_value = "Player Summary Card"
    mock_get_recently_played.return_value = {"games": "data"}
    mock_generate_card_played.return_value = None
    result = generate_steam_stats()
    TestCase().assertIn("Player Summary Card", result)
    TestCase().assertEqual(result, "Player Summary Card")
    mock_logger.info.assert_any_call("No Games data found, skipping card generation")


@patch("api.main.fetch_workshop_item_links")
@patch("api.main.fetch_all_workshop_stats")
@patch("api.main.generate_card_for_steam_workshop")
@patch("api.main.logger")
def test_generate_workshop_stats(
    mock_logger, mock_generate_card, mock_fetch_all_stats, mock_fetch_links
):
    """Test Generating Steam Workshop Stats"""
    mock_fetch_links.return_value = ["link1", "link2"]
    mock_fetch_all_stats.return_value = {"workshop": "stats"}
    mock_generate_card.return_value = "Workshop Stats Card"
    result = generate_workshop_stats()
    TestCase().assertIn("Workshop Stats Card", result)

    mock_fetch_links.return_value = None
    result = generate_workshop_stats()
    TestCase().assertEqual(result, "")
    mock_logger.error.assert_any_call("No workshop content was found")

    mock_fetch_links.return_value = ["link1", "link2"]
    mock_generate_card.return_value = None
    result = generate_workshop_stats()
    TestCase().assertEqual(result, "")
    mock_logger.error.assert_any_call("Failed to generate card data for Workshop Stats")


@patch("api.utils.create_tree_elements")
@patch("api.main.logger")
def test_commit_to_github(mock_logger, mock_create_tree_elements, mock_repo):
    """Test Committing to Github Repo"""
    fake_blob = MagicMock()
    fake_blob.sha = "fake_blob_sha"
    mock_repo.create_git_blob.return_value = fake_blob

    mock_repo.get_branch.return_value.commit.sha = "fake_sha"
    mock_repo.create_git_tree.return_value = MagicMock()
    mock_repo.create_git_commit.return_value = MagicMock(sha="new_commit_sha")
    mock_repo.get_git_ref.return_value.edit.return_value = None

    result = commit_to_github(mock_repo, {"README.md": "New Content"})
    TestCase().assertTrue(result)

    result = commit_to_github(mock_repo, {})
    TestCase().assertTrue(result)

    mock_repo.get_branch.side_effect = ValueError("Test ValueError")
    result = commit_to_github(mock_repo, {"README.md": "New Content"})
    TestCase().assertFalse(result)
    mock_logger.error.assert_any_call(
        "Error occurred while committing to GitHub: %s", "Test ValueError"
    )

    mock_repo.get_branch.side_effect = IOError("Test IOError")
    result = commit_to_github(mock_repo, {"README.md": "New Content"})
    TestCase().assertFalse(result)
    mock_logger.error.assert_any_call(
        "Error occurred while committing to GitHub: %s", "Test IOError"
    )


@patch("api.main.generate_steam_stats")
@patch("api.main.generate_workshop_stats")
@patch("api.main.update_section")
@patch("api.main.logger")
def test_update_readme_sections(
    mock_logger,
    mock_update_section,
    mock_generate_workshop,
    mock_generate_steam,
    mock_repo,
):
    """Test Updating Readme with marker sections"""
    mock_generate_steam.return_value = "Steam Stats Content"
    mock_generate_workshop.return_value = "Workshop Stats Content"
    mock_update_section.side_effect = (
        lambda repo, content, new_content, start_marker, end_marker: content
        + start_marker
        + new_content
        + end_marker
    )

    updated_content = update_readme_sections(mock_repo, "Original Content")

    TestCase().assertIn("Steam Stats Content", updated_content)
    TestCase().assertIn("Workshop Stats Content", updated_content)
    TestCase().assertIn("<!-- Steam-Stats start -->", updated_content)
    TestCase().assertIn("<!-- Steam-Stats end -->", updated_content)
    TestCase().assertIn("<!-- Steam-Workshop start -->", updated_content)
    TestCase().assertIn("<!-- Steam-Workshop end -->", updated_content)

    mock_generate_steam.return_value = None
    updated_content = update_readme_sections(mock_repo, "Original Content")
    TestCase().assertIn("Original Content", updated_content)
    mock_logger.info.assert_any_call("No Steam stats content generated")

    mock_generate_steam.return_value = "Steam Stats Content"
    mock_generate_workshop.return_value = None
    updated_content = update_readme_sections(mock_repo, "Original Content")
    TestCase().assertIn("Steam Stats Content", updated_content)
    TestCase().assertIn(
        "<!-- Steam-Stats start -->Steam Stats Content<!-- Steam-Stats end -->",
        updated_content,
    )
    mock_logger.info.assert_any_call("No Workshop stats content generated")


@patch("api.main.update_readme")
def test_update_section(mock_update_readme, mock_repo):
    """Test Updating marker sections"""
    mock_update_readme.return_value = "Updated Section"
    updated_content = update_section(
        mock_repo, "Original Content", "New Content", "<!--START-->", "<!--END-->"
    )
    TestCase().assertIn("Updated Section", updated_content)

    mock_update_readme.return_value = None
    updated_content = update_section(
        mock_repo, "Original Content", "New Content", "<!--START-->", "<!--END-->"
    )
    TestCase().assertEqual(updated_content, "Original Content")


def test_collect_files_to_update():
    """Test Collecting files to update for Github Repo"""
    current_readme = "New README Content"
    original_readme = "Original README Content"

    with patch("os.path.exists") as mock_exists, patch(
        "builtins.open", new_callable=MagicMock
    ) as mock_open:
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b"binary content"
        )

        files_to_update = collect_files_to_update(current_readme, original_readme)

        TestCase().assertIn("README.md", files_to_update)
        TestCase().assertIn("assets/steam_summary.png", files_to_update)


def test_log_execution_time():
    """Test Log execution time"""
    start_time = time.time() - 65
    with patch("api.main.logger") as mock_logger:
        log_execution_time(start_time)
        mock_logger.info.assert_any_call(
            "Total Execution Time: %d minutes and %.3f seconds", 1, approx(5.0, abs=0.1)
        )

    start_time = time.time() - 30
    with patch("api.main.logger") as mock_logger:
        log_execution_time(start_time)
        mock_logger.info.assert_any_call(
            "Total Execution Time: %.3f seconds", approx(30.0, abs=0.1)
        )


def test_main_successful_commit(caplog, mock_dependencies):
    """Test Main Function for Successful Commit"""
    mock_repo = MagicMock(name="MockGitHubRepo")
    mock_dependencies["initialize_github"].return_value = mock_repo
    mock_dependencies["get_readme_content"].return_value = "original_readme"
    mock_dependencies["update_readme_sections"].return_value = "current_readme"
    mock_dependencies["collect_files_to_update"].return_value = ["file1", "file2"]
    mock_dependencies["commit_to_github"].return_value = True

    with caplog.at_level(logging.INFO):
        main()

    info_logs = [
        record.message for record in caplog.records if record.levelname == "INFO"
    ]
    if not any("Successfully committed to GitHub" in msg for msg in info_logs):
        raise AssertionError(
            "Expected 'Successfully committed to GitHub' info log not found"
        )


def test_main_no_changes(caplog, mock_dependencies):
    """Test Main Function for No Changes"""
    mock_repo = MagicMock(name="MockGitHubRepo")
    mock_dependencies["initialize_github"].return_value = mock_repo
    mock_dependencies["get_readme_content"].return_value = "original_readme"
    mock_dependencies["update_readme_sections"].return_value = "current_readme"
    mock_dependencies["collect_files_to_update"].return_value = []

    with caplog.at_level(logging.INFO):
        main()

    info_logs = [
        record.message for record in caplog.records if record.levelname == "INFO"
    ]
    if not any("No changes to commit" in msg for msg in info_logs):
        raise AssertionError("Expected 'No changes to commit' info log not found")


def test_main_commit_failure(caplog, mock_dependencies):
    """Test Main Function for Commit Failure"""
    mock_repo = MagicMock(name="MockGitHubRepo")
    mock_dependencies["initialize_github"].return_value = mock_repo
    mock_dependencies["get_readme_content"].return_value = "original_readme"
    mock_dependencies["update_readme_sections"].return_value = "current_readme"
    mock_dependencies["collect_files_to_update"].return_value = ["file1", "file2"]
    mock_dependencies["commit_to_github"].return_value = False

    with caplog.at_level(logging.ERROR):
        main()

    error_logs = [
        record.message for record in caplog.records if record.levelname == "ERROR"
    ]
    if not any("Failed to commit changes to GitHub" in msg for msg in error_logs):
        raise AssertionError(
            "Expected 'Failed to commit changes to GitHub' error log not found"
        )


@pytest.mark.parametrize(
    "exception_type, expected_message",
    [
        (ValueError("Test ValueError"), "ValueError error occurred: Test ValueError"),
        (IOError("Test IOError"), "OSError error occurred: Test IOError"),
    ],
)
def test_main_exception_handling(caplog, mocker, exception_type, expected_message):
    """Test exception block in main() logs correct error message"""
    caplog.set_level(logging.ERROR, logger=logger.name)

    mocker.patch("api.main.initialize_github", side_effect=exception_type)
    mocker.patch("api.utils.get_readme_content")
    mocker.patch("api.main.update_readme_sections")
    mocker.patch("api.main.collect_files_to_update")
    mocker.patch("api.main.commit_to_github")
    mocker.patch("api.main.log_execution_time")

    main()

    messages = [
        record.message for record in caplog.records if record.levelname == "ERROR"
    ]
    if expected_message not in messages:
        raise AssertionError(
            f"Expected error log '{expected_message}' not found. Got: {messages}"
        )


if __name__ == "__main__":
    pytest.main()
