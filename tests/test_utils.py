"""Test Utility functions for the API"""

# Disable pylint warnings for false positives
# pylint: disable=redefined-outer-name, unused-argument, unused-import
import os
from unittest import TestCase
from unittest.mock import MagicMock, patch
import pytest
from api.utils import (
    get_github_token,
    get_repo,
    create_tree_elements,
    initialize_github,
    get_readme_content,
)
from tests.test_main import mock_repo, mock_dependencies


@pytest.fixture
def mock_github():
    """Mock Github Repo"""
    with patch("api.utils.Github") as mock_github:
        yield mock_github


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("GITHUB_TOKEN", "fake_token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "fake/repo")
    monkeypatch.setenv("INPUT_STEAM_ID", "fake_steam_id")
    monkeypatch.setenv("INPUT_STEAM_API_KEY", "fake_steam_api_key")
    monkeypatch.setenv("INPUT_STEAM_CUSTOM_ID", "fake_steam_custom_id")
    monkeypatch.setenv("INPUT_WORKSHOP_STATS", "true")


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
        with pytest.raises(
            ValueError, match="GITHUB_REPOSITORY environment variable not set"
        ):
            get_repo(mock_github.return_value)


def test_initialize_github(mock_github, mock_env_vars):
    """Test Initializing Github Repo"""
    mock_repo = MagicMock()
    mock_github.return_value.get_repo.return_value = mock_repo

    repo = initialize_github()
    TestCase().assertEqual(repo, mock_repo)


@patch("api.utils.InputGitTreeElement")
def test_create_tree_elements(mock_input_git_tree_element, mock_repo):
    """Test Create Tree elements"""
    files_to_update = {"README.md": "New Content", "image.png": b"binary content"}
    mock_repo.create_git_blob.side_effect = lambda content, encoding: MagicMock(
        sha="fake_sha"
    )
    mock_input_git_tree_element.side_effect = lambda path, mode, type, sha: MagicMock(
        path=path
    )

    tree_elements = create_tree_elements(mock_repo, files_to_update)

    TestCase().assertEqual(len(tree_elements), 2)
    TestCase().assertEqual(tree_elements[0].path, "README.md")
    TestCase().assertEqual(tree_elements[1].path, "image.png")


def test_get_readme_content(mock_repo):
    """Test fetching Readme Content"""
    mock_repo.get_contents.return_value = MagicMock(decoded_content=b"README content")
    content = get_readme_content(mock_repo)
    TestCase().assertEqual(content, "README content")

    mock_repo.get_contents.return_value = [MagicMock(decoded_content=b"README content")]
    content = get_readme_content(mock_repo)
    TestCase().assertEqual(content, "README content")
