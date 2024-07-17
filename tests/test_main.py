"""Test Main Runner Script"""
# Disable pylint warnings for false positives
# pylint: disable=redefined-outer-name, unused-argument
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock
import time
import pytest
from api.main import (update_readme, generate_steam_stats, generate_workshop_stats,
                      get_github_token, get_repo, create_tree_elements, commit_to_github,
                      initialize_github, get_readme_content, update_readme_sections, update_section,
                      collect_files_to_update, log_execution_time, main, logger)


@pytest.fixture
def mock_repo():
    """Mock Repo"""
    return MagicMock()


@pytest.fixture
def mock_github():
    """Mock Github Repo"""
    with patch("api.main.Github") as mock_github:
        yield mock_github


@pytest.fixture
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
    fixtures['initialize_github'] = mocker.patch('api.main.initialize_github')
    fixtures['get_readme_content'] = mocker.patch(
        'api.main.get_readme_content')
    fixtures['update_readme_sections'] = mocker.patch(
        'api.main.update_readme_sections')
    fixtures['collect_files_to_update'] = mocker.patch(
        'api.main.collect_files_to_update')
    fixtures['commit_to_github'] = mocker.patch('api.main.commit_to_github')
    fixtures['log_execution_time'] = mocker.patch(
        'api.main.log_execution_time')
    fixtures['logger_info'] = mocker.patch.object(logger, 'info')
    fixtures['logger_error'] = mocker.patch.object(logger, 'error')
    return fixtures


def test_update_readme(mock_repo):
    """Test Update readme Function"""
    markdown_data = "New Content"
    start_marker = "<!--START-->"
    end_marker = "<!--END-->"
    mock_repo.get_contents.return_value.decoded_content = b"<!--START-->\nOld Content\n<!--END-->"
    result = update_readme(mock_repo, markdown_data, start_marker, end_marker)
    TestCase().assertEqual(result, "<!--START-->\nNew Content\n<!--END-->")

    mock_repo.get_contents.return_value.decoded_content = b"Some content without markers"
    result = update_readme(mock_repo, markdown_data, start_marker, end_marker)
    TestCase().assertIsNone(result)

    mock_repo.get_contents.side_effect = FileNotFoundError
    result = update_readme(mock_repo, markdown_data, start_marker, end_marker)
    TestCase().assertIsNone(result)

    mock_repo.get_contents.return_value.decoded_content = b"<!--START-->\nNew Content\n<!--END-->"
    result = update_readme(mock_repo, markdown_data, start_marker, end_marker)
    TestCase().assertIsNone(result)


@patch("api.main.get_player_summaries")
@patch("api.main.generate_card_for_player_summary")
@patch("api.main.get_recently_played_games")
@patch("api.main.generate_card_for_played_games")
@patch("api.main.logger")
def test_generate_steam_stats(mock_logger, mock_generate_card_played, mock_get_recently_played,
                              mock_generate_card_summary, mock_get_player_summaries):
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
    mock_logger.info.assert_any_call(
        "Generated Card for Recently Played Games")

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
    mock_logger.error.assert_any_call(
        "Failed to generate card for Steam Summary")

    mock_get_player_summaries.return_value = {"player": "summary"}
    mock_generate_card_summary.return_value = "Player Summary Card"
    mock_get_recently_played.return_value = {"games": "data"}
    mock_generate_card_played.return_value = None
    result = generate_steam_stats()
    TestCase().assertIn("Player Summary Card", result)
    TestCase().assertEqual(result, "Player Summary Card")
    mock_logger.info.assert_any_call(
        "No Games data found, skipping card generation")


@patch("api.main.fetch_workshop_item_links")
@patch("api.main.fetch_all_workshop_stats")
@patch("api.main.generate_card_for_steam_workshop")
@patch("api.main.logger")
def test_generate_workshop_stats(mock_logger, mock_generate_card,
                                 mock_fetch_all_stats, mock_fetch_links):
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
    mock_logger.error.assert_any_call(
        "Failed to generate card data for Workshop Stats")


def test_get_github_token(mock_env_vars):
    """Test fetching github token"""
    token = get_github_token()
    TestCase().assertEqual(token, "fake_token")

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="No GitHub token found in env vars"):
            get_github_token()


def test_get_repo(mock_github):
    """Test fetching GitHub repo"""
    mock_repo = MagicMock()
    mock_github.return_value.get_repo.return_value = mock_repo

    with patch.dict(os.environ, {"GITHUB_REPOSITORY": "fake/repo"}):
        repo = get_repo(mock_github.return_value)
        TestCase().assertEqual(repo, mock_repo)

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GITHUB_REPOSITORY environment variable not set"):
            get_repo(mock_github.return_value)


def test_initialize_github(mock_github, mock_env_vars):
    """Test Initializing Github Repo"""
    mock_repo = MagicMock()
    mock_github.return_value.get_repo.return_value = mock_repo

    repo = initialize_github()
    TestCase().assertEqual(repo, mock_repo)


@patch("api.main.InputGitTreeElement")
def test_create_tree_elements(mock_input_git_tree_element, mock_repo):
    """Test Create Tree elements"""
    files_to_update = {
        "README.md": "New Content",
        "image.png": b"binary content"
    }
    mock_repo.create_git_blob.side_effect = lambda content, encoding: MagicMock(
        sha="fake_sha")
    mock_input_git_tree_element.side_effect = lambda path, mode, type, sha: MagicMock(
        path=path)

    tree_elements = create_tree_elements(mock_repo, files_to_update)

    TestCase().assertEqual(len(tree_elements), 2)
    TestCase().assertEqual(tree_elements[0].path, "README.md")
    TestCase().assertEqual(tree_elements[1].path, "image.png")


@patch("api.main.create_tree_elements")
@patch("api.main.logger")
def test_commit_to_github(mock_logger, mock_create_tree_elements, mock_repo):
    """Test Committing to Github Repo"""
    mock_create_tree_elements.return_value = [MagicMock()]
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
        "Error occurred while committing to GitHub: %s", "Test ValueError")

    mock_repo.get_branch.side_effect = IOError("Test IOError")
    result = commit_to_github(mock_repo, {"README.md": "New Content"})
    TestCase().assertFalse(result)
    mock_logger.error.assert_any_call(
        "Error occurred while committing to GitHub: %s", "Test IOError")


def test_get_readme_content(mock_repo):
    """Test fetching Readme Content"""
    mock_repo.get_contents.return_value = MagicMock(
        decoded_content=b"README content")
    content = get_readme_content(mock_repo)
    TestCase().assertEqual(content, "README content")

    mock_repo.get_contents.return_value = [
        MagicMock(decoded_content=b"README content")]
    content = get_readme_content(mock_repo)
    TestCase().assertEqual(content, "README content")


@patch("api.main.generate_steam_stats")
@patch("api.main.generate_workshop_stats")
@patch("api.main.update_section")
@patch("api.main.logger")
def test_update_readme_sections(mock_logger, mock_update_section, mock_generate_workshop,
                                mock_generate_steam, mock_repo):
    """Test Updating Readme with marker sections"""
    mock_generate_steam.return_value = "Steam Stats Content"
    mock_generate_workshop.return_value = "Workshop Stats Content"
    mock_update_section.side_effect = (
        lambda repo, content, new_content, start_marker, end_marker:
        content + start_marker + new_content + end_marker
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
        "<!-- Steam-Stats start -->Steam Stats Content<!-- Steam-Stats end -->", updated_content)
    mock_logger.info.assert_any_call("No Workshop stats content generated")


@patch("api.main.update_readme")
def test_update_section(mock_update_readme, mock_repo):
    """Test Updating marker sections"""
    mock_update_readme.return_value = "Updated Section"
    updated_content = update_section(
        mock_repo, "Original Content", "New Content", "<!--START-->", "<!--END-->")
    TestCase().assertIn("Updated Section", updated_content)

    mock_update_readme.return_value = None
    updated_content = update_section(
        mock_repo, "Original Content", "New Content", "<!--START-->", "<!--END-->")
    TestCase().assertEqual(updated_content, "Original Content")


def test_collect_files_to_update():
    """Test Collecting files to update for Github Repo"""
    current_readme = "New README Content"
    original_readme = "Original README Content"

    with patch("os.path.exists") as mock_exists, patch("builtins.open",
                                                       new_callable=MagicMock) as mock_open:
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = b"binary content"

        files_to_update = collect_files_to_update(
            current_readme, original_readme)

        TestCase().assertIn("README.md", files_to_update)
        TestCase().assertIn("assets/steam_summary.png", files_to_update)


def test_log_execution_time():
    """Test Log execution time"""
    start_time = time.time() - 65
    with patch("api.main.logger") as mock_logger:
        log_execution_time(start_time)
        mock_logger.info.assert_any_call(
            "Total Execution Time: %d minutes and %.3f seconds", 1, 5.0)

    start_time = time.time() - 30
    with patch("api.main.logger") as mock_logger:
        log_execution_time(start_time)
        mock_logger.info.assert_any_call(
            "Total Execution Time: %.3f seconds", 30.0)


def test_main_successful_commit(mock_dependencies):
    """Test Main Function for Successful Commit"""
    mock_dependencies['initialize_github'].return_value = "repo"
    mock_dependencies['get_readme_content'].return_value = "original_readme"
    mock_dependencies['update_readme_sections'].return_value = "current_readme"
    mock_dependencies['collect_files_to_update'].return_value = [
        "file1", "file2"]
    mock_dependencies['commit_to_github'].return_value = True

    main()

    if mock_dependencies['logger_info'].call_count != 1:
        raise AssertionError(
            "Expected logger.info to be called once for successful commit")
    if mock_dependencies['logger_error'].call_count != 0:
        raise AssertionError("Expected logger.error to not be called")


def test_main_no_changes(mock_dependencies):
    """Test Main Function for No Changes"""
    mock_dependencies['initialize_github'].return_value = "repo"
    mock_dependencies['get_readme_content'].return_value = "original_readme"
    mock_dependencies['update_readme_sections'].return_value = "current_readme"
    mock_dependencies['collect_files_to_update'].return_value = []

    main()

    if mock_dependencies['logger_info'].call_count != 1:
        raise AssertionError(
            "Expected logger.info to be called once for no changes")
    if mock_dependencies['logger_error'].call_count != 0:
        raise AssertionError("Expected logger.error to not be called")


def test_main_commit_failure(mock_dependencies):
    """Test Main Function for Commit Failure"""
    mock_dependencies['initialize_github'].return_value = "repo"
    mock_dependencies['get_readme_content'].return_value = "original_readme"
    mock_dependencies['update_readme_sections'].return_value = "current_readme"
    mock_dependencies['collect_files_to_update'].return_value = [
        "file1", "file2"]
    mock_dependencies['commit_to_github'].return_value = False

    main()

    if mock_dependencies['logger_info'].call_count != 0:
        raise AssertionError(
            "Expected logger.info to not be called for commit failure")
    if mock_dependencies['logger_error'].call_count != 1:
        raise AssertionError(
            "Expected logger.error to be called once for commit failure")


def test_main_value_error(mock_dependencies):
    """Test Main Function for ValueError"""
    mock_dependencies['initialize_github'].side_effect = ValueError(
        "Test ValueError")

    main()

    if mock_dependencies['logger_info'].call_count != 0:
        raise AssertionError("Expected logger.info to not be called")
    if mock_dependencies['logger_error'].call_count != 1:
        raise AssertionError("Expected logger.error to be called once")


def test_main_io_error(mock_dependencies):
    """Test Main Function for IOError"""
    mock_dependencies['initialize_github'].side_effect = IOError(
        "Test IOError")

    main()

    if mock_dependencies['logger_info'].call_count != 0:
        raise AssertionError("Expected logger.info to not be called")
    if mock_dependencies['logger_error'].call_count != 1:
        raise AssertionError("Expected logger.error to be called once")


if __name__ == "__main__":
    pytest.main()
