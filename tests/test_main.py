"""Test Main Runner Script"""
# Disable pylint warnings for false positives
# pylint: disable=redefined-outer-name, unused-argument
from unittest.mock import Mock, patch
import pytest
from api.main import (
    update_readme, generate_steam_stats, generate_workshop_stats,
    get_github_token, get_repo, create_tree_elements, commit_to_github,
    initialize_github, get_readme_content, update_readme_sections,
    update_section, collect_files_to_update
)


@pytest.fixture
def mock_dependencies(mocker):
    """Mock all the function dependencies"""
    mocks = {
        'get_player_summaries': mocker.patch('main.get_player_summaries',
                                             return_value={'response': {'players': [{'personaname':
                                                                                     'TestUser'
                                                                                     }]}}),
        'get_recently_played_games': mocker.patch('main.get_recently_played_games',
                                                  return_value={'response': {'games': []}}),
        'generate_card_for_player_summary': mocker.patch('main.generate_card_for_player_summary',
                                                         return_value='Player Summary Card'),
        'generate_card_for_played_games': mocker.patch('main.generate_card_for_played_games',
                                                       return_value='Recently Played Games Card'),
        'fetch_workshop_item_links': mocker.patch('main.fetch_workshop_item_links',
                                                  return_value=['link1', 'link2']),
        'fetch_all_workshop_stats': mocker.patch('main.fetch_all_workshop_stats',
                                                 return_value={'stats': 'data'}),
        'generate_card_for_steam_workshop': mocker.patch('main.generate_card_for_steam_workshop',
                                                         return_value='Workshop Stats Card'),
        'Github': mocker.patch('main.Github'),
        'get_repo': mocker.patch('main.get_repo'),
    }

    mocker.patch.dict('os.environ', {
        'INPUT_STEAM_ID': 'test_steam_id',
        'INPUT_STEAM_API_KEY': 'test_api_key',
        'INPUT_STEAM_CUSTOM_ID': 'test_custom_id',
        'INPUT_WORKSHOP_STATS': 'true',
        'GITHUB_REPOSITORY': 'test/repo'
    })

    return mocks


def test_update_readme(mock_dependencies):
    """Test Update Readme"""
    mock_repo = Mock()
    mock_repo.get_contents.return_value.decoded_content = (
        b'<!-- Start -->\n'
        b'Old content\n'
        b'<!-- End -->'
    )
    result = update_readme(mock_repo, 'New content',
                           '<!-- Start -->', '<!-- End -->')
    expected = '<!-- Start -->\nNew content\n<!-- End -->'
    if result != expected:
        pytest.fail(f"Expected '{expected}', but got '{result}'")


def test_generate_steam_stats(mock_dependencies):
    """Test Generating Steam Stats"""
    result = generate_steam_stats()
    expected = 'Player Summary CardRecently Played Games Card'
    if result != expected:
        pytest.fail(f"Expected '{expected}', but got '{result}'")


def test_generate_workshop_stats(mock_dependencies):
    """Test Generating Steam Workshop Stats"""
    result = generate_workshop_stats()
    expected = 'Workshop Stats Card'
    if result != expected:
        pytest.fail(f"Expected '{expected}', but got '{result}'")


def test_get_github_token():
    """Test fetching Github Token"""
    with patch.dict('os.environ', {'GITHUB_TOKEN': 'test_token'}):
        token = get_github_token()
        if token != 'test_token':
            pytest.fail(f"Expected 'test_token', but got '{token}'")


def test_get_repo():
    """Test fetching Github Repo"""
    mock_github = Mock()
    with patch.dict('os.environ', {'GITHUB_REPOSITORY': 'test/repo'}):
        get_repo(mock_github)
        mock_github.get_repo.assert_called_once_with('test/repo')


def test_create_tree_elements():
    """Test Creating Tree Elements for Git"""
    mock_repo = Mock()
    files_to_update = {'test.txt': 'content'}
    create_tree_elements(mock_repo, files_to_update)
    mock_repo.create_git_blob.assert_called_once()


def test_commit_to_github():
    """Test committing to Github"""
    mock_repo = Mock()
    files_to_update = {'test.txt': 'content'}
    result = commit_to_github(mock_repo, files_to_update)
    if not result:
        pytest.fail("Expected True, but got False")


def test_initialize_github(mock_dependencies):
    """Test Initializing Github"""
    with patch('main.get_github_token', return_value='test_token'):
        initialize_github()
        mock_dependencies['Github'].assert_called_once_with('test_token')


def test_get_readme_content():
    """Test fetching readme content"""
    mock_repo = Mock()
    mock_repo.get_contents.return_value.decoded_content = b'README content'
    result = get_readme_content(mock_repo)
    if result != 'README content':
        pytest.fail(f"Expected 'README content', but got '{result}'")


def test_update_readme_sections(mock_dependencies):
    """Test updating readme sections with markers"""
    mock_repo = Mock()
    current_content = '<!-- Steam-Stats start -->Old<!-- Steam-Stats end -->'
    result = update_readme_sections(mock_repo, current_content)
    expected = (
        '<!-- Steam-Stats start -->\n'
        'Player Summary CardRecently Played Games Card\n'
        '<!-- Steam-Stats end -->'
    )
    if result != expected:
        pytest.fail(f"Expected '{expected}', but got '{result}'")


def test_update_section():
    """Test updating section in Readme"""
    mock_repo = Mock()
    current_content = '<!-- Start -->Old<!-- End -->'
    new_content = 'New'
    result = update_section(mock_repo, current_content,
                            new_content, '<!-- Start -->', '<!-- End -->')
    expected = '<!-- Start -->\nNew\n<!-- End -->'
    if result != expected:
        pytest.fail(f"Expected '{expected}', but got '{result}'")


def test_collect_files_to_update():
    """Test collection of files to update to Github"""
    with patch('os.path.exists', return_value=True), \
            patch('builtins.open', Mock()):
        current_readme = 'New content'
        original_readme = 'Old content'
        result = collect_files_to_update(current_readme, original_readme)
        if len(result) != 4:
            pytest.fail(f"Expected 4 files to update, but got {len(result)}")
