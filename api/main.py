"""Main Runner Script"""
# Disable pylint warnings for false positives
# pylint: disable=duplicate-code
import base64
import logging
import os
import time
from api.steam_stats import get_player_summaries, get_recently_played_games
from api.steam_workshop import fetch_workshop_item_links, fetch_all_workshop_stats
from api.card import (
    generate_card_for_player_summary,
    generate_card_for_played_games,
    generate_card_for_steam_workshop
)
from github import Github, InputGitTreeElement

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Required Secrets Configuration
STEAM_ID = os.environ["INPUT_STEAM_ID"]
STEAM_API_KEY = os.environ["INPUT_STEAM_API_KEY"]
STEAM_CUSTOM_ID = os.environ["INPUT_STEAM_CUSTOM_ID"]

# Optional Feature Flag
WORKSHOP_STATS = os.getenv("INPUT_WORKSHOP_STATS",
                           "false").lower() in ("true", "1", "t")

# Version Identifier for Changelog
__version__ = "1.0.0"


def update_readme(repo, markdown_data, start_marker, end_marker):
    """Updates the README.md file with the provided Markdown content within specified markers"""
    try:
        readme_file = repo.get_contents("README.md")
        readme_content = readme_file.decoded_content.decode("utf-8")

        start_index = readme_content.find(start_marker)
        end_index = readme_content.find(end_marker, start_index)

        if start_index == -1 or end_index == -1:
            logger.error("Markers not found: %s", start_marker)
            return None

        new_section_content = start_marker + "\n" + markdown_data + "\n" + end_marker

        if new_section_content != readme_content[start_index:end_index + len(end_marker)]:
            return new_section_content

        return None

    except (FileNotFoundError, PermissionError, IOError) as e:
        logger.error("Error occurred while updating README: %s", str(e))
        return None


def generate_steam_stats():
    """Generate Steam Stats and return markdown content"""
    user_markdown_content = ""
    player_summary = get_player_summaries()
    if player_summary:
        logger.info("Retrieved Steam User Data")
        summary_content = generate_card_for_player_summary(player_summary)
        if summary_content:
            user_markdown_content += summary_content
            logger.info("Generated Card for Steam User Data")
        else:
            logger.error("Failed to generate card for Steam Summary")
    else:
        logger.info("No Steam User Summary data found")

    recently_played_games = get_recently_played_games()
    if recently_played_games:
        logger.info("Retrieved Recently Played Games Data")
        recent_games = generate_card_for_played_games(recently_played_games)
        if recent_games:
            user_markdown_content += recent_games
            logger.info("Generated Card for Recently Played Games")
        else:
            logger.info("No Games data found, skipping card generation")
    else:
        logger.info("No Recently Played Games data found")

    return user_markdown_content


def generate_workshop_stats():
    """Generate Workshop Stats and return markdown content"""
    workshop_markdown_content = ""
    links = fetch_workshop_item_links(STEAM_CUSTOM_ID, STEAM_API_KEY)
    if links:
        workshop_data = fetch_all_workshop_stats(links)
        workshop_content = generate_card_for_steam_workshop(workshop_data)
        if workshop_content:
            workshop_markdown_content += workshop_content
            logger.info("Generated Card for Workshop Stats")
        else:
            logger.error("Failed to generate card data for Workshop Stats")
    else:
        logger.error("No workshop content was found")

    return workshop_markdown_content


def get_github_token():
    """Get GitHub token from environment variables"""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get(
        "GH_TOKEN") or os.environ.get("INPUT_GH_TOKEN")
    if not token:
        raise ValueError(
            "No GitHub token found in env vars (GITHUB_TOKEN, GH_TOKEN or INPUT_GH_TOKEN")
    return token


def get_repo(g):
    """Get Repo object"""
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    if not repo_name:
        raise ValueError("GITHUB_REPOSITORY environment variable not set")
    return g.get_repo(repo_name)


def create_tree_elements(repo, files_to_update):
    """Create tree elements for GitHub commit"""
    tree_elements = []
    for file_path, file_content in files_to_update.items():
        if isinstance(file_content, bytes):
            content = base64.b64encode(file_content).decode("utf-8")
            encoding = "base64"
        else:
            content = file_content
            encoding = "utf-8"

        blob = repo.create_git_blob(content, encoding)
        element = InputGitTreeElement(
            path=file_path, mode="100644", type="blob", sha=blob.sha)
        tree_elements.append(element)
    return tree_elements


def commit_to_github(repo, files_to_update):
    """Commit files to GitHub Repo"""
    if not files_to_update:
        logger.info("No changes to commit")
        return True

    try:
        branch = repo.get_branch(repo.default_branch)
        last_commit_sha = branch.commit.sha

        tree_elements = create_tree_elements(repo, files_to_update)
        new_tree = repo.create_git_tree(
            tree_elements, repo.get_git_tree(last_commit_sha))

        new_commit = repo.create_git_commit(
            message="chore: Update Steam Stats",
            tree=new_tree,
            parents=[repo.get_git_commit(last_commit_sha)]
        )

        ref = repo.get_git_ref("heads/" + branch.name)
        ref.edit(sha=new_commit.sha)
        return True

    except (ValueError, IOError) as e:
        logger.error("Error occurred while committing to GitHub: %s", str(e))
        return False


def initialize_github():
    """Initialize GitHub client and get repo"""
    token = get_github_token()
    g = Github(token)
    return get_repo(g)


def get_readme_content(repo):
    """Get current README content"""
    readme_file = repo.get_contents("README.md")
    if isinstance(readme_file, list):
        readme_file = readme_file[0]
    return readme_file.decoded_content.decode("utf-8")


def update_readme_sections(repo, current_content):
    """Update README sections with Steam and Workshop stats"""
    updated_content = current_content

    steam_stats_content = generate_steam_stats()
    if steam_stats_content:
        updated_content = update_section(repo, updated_content, steam_stats_content,
                                         "<!-- Steam-Stats start -->", "<!-- Steam-Stats end -->")
        logger.info("Steam stats updated")
    else:
        logger.info("No Steam stats content generated")

    if WORKSHOP_STATS:
        workshop_content = generate_workshop_stats()
        if workshop_content:
            updated_content = update_section(repo, updated_content, workshop_content,
                                             "<!-- Steam-Workshop start -->",
                                             "<!-- Steam-Workshop end -->")
            logger.info("Workshop stats updated")
        else:
            logger.info("No Workshop stats content generated")

    return updated_content


def update_section(repo, current_content, new_content, start_marker, end_marker):
    """Update a section of the README using markers"""
    updated_section = update_readme(
        repo, new_content, start_marker, end_marker)
    if updated_section:
        start_index = current_content.find(start_marker)
        end_index = current_content.find(
            end_marker, start_index) + len(end_marker)
        return current_content[:start_index] + updated_section + current_content[end_index:]
    return current_content


def collect_files_to_update(current_readme, original_readme):
    """Collect files that needs to be updated"""
    files_to_update = {}
    if current_readme != original_readme:
        files_to_update["README.md"] = current_readme.encode("utf-8")

    for png_file in ["steam_summary.png", "recently_played_games.png", "steam_workshop_stats.png"]:
        png_path = "assets/" + png_file
        if os.path.exists(png_path):
            with open(png_path, "rb") as file:
                files_to_update["assets/" + png_file] = file.read()

    return files_to_update


def log_execution_time(start_time):
    """Log the total execution time"""
    total_time = round(time.time() - start_time, 3)
    if total_time > 60:
        minutes, seconds = divmod(total_time, 60)
        logger.info(
            "Total Execution Time: %d minutes and %.3f seconds", minutes, seconds)
    else:
        logger.info("Total Execution Time: %.3f seconds", total_time)


def main():
    """Main function to run the script"""
    start_time = time.time()

    try:
        repo = initialize_github()
        original_readme = get_readme_content(repo)
        current_readme = update_readme_sections(repo, original_readme)
        files_to_update = collect_files_to_update(
            current_readme, original_readme)

        if files_to_update:
            if commit_to_github(repo, files_to_update):
                logger.info("Successfully committed to GitHub")
            else:
                logger.error("Failed to commit changes to GitHub")
        else:
            logger.info("No changes to commit")

    except (ValueError, IOError) as e:
        logger.error("%s error occurred: %s", type(e).__name__, str(e))

    log_execution_time(start_time)


if __name__ == "__main__":
    main()
