"""Utility functions for the API"""

import base64
import logging
import os
from pathlib import Path
from github import Github, InputGitTreeElement, Auth

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / "assets"
README = "README.md"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_steam_credentials():
    """Fetch Steam credentials using environment variables"""
    return {
        "steam_id": os.environ["INPUT_STEAM_ID"],
        "api_key": os.environ["INPUT_STEAM_API_KEY"],
        "custom_id": os.environ["INPUT_STEAM_CUSTOM_ID"],
    }


def get_github_token():
    """Get GitHub token from environment variables"""
    token = (
        os.environ.get("GITHUB_TOKEN")
        or os.environ.get("GH_TOKEN")
        or os.environ.get("INPUT_GH_TOKEN")
    )
    if not token:
        raise ValueError(
            "No GitHub token found in env vars (GITHUB_TOKEN, GH_TOKEN or INPUT_GH_TOKEN"
        )
    return token


def get_repo(g):
    """Get Repo object"""
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    if not repo_name:
        raise ValueError("GITHUB_REPOSITORY environment variable not set")
    return g.get_repo(repo_name)


def initialize_github():
    """Initialize GitHub client and get repo"""
    token = get_github_token()
    g = Github(auth=Auth.Token(token))
    return get_repo(g)


def get_readme_content(repo):
    """Get current README content"""
    readme_file = repo.get_contents(README)
    if isinstance(readme_file, list):
        readme_file = readme_file[0]
    return readme_file.decoded_content.decode("utf-8")


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
            path=file_path, mode="100644", type="blob", sha=blob.sha
        )
        tree_elements.append(element)
    return tree_elements


def get_asset_paths(filename_base: str) -> tuple[Path, Path, str]:
    """Returns the absolute HTML, PNG & relative PNG path for embedding in markdown"""
    html_path = ASSETS_DIR / f"{filename_base}.html"
    png_path = ASSETS_DIR / f"{filename_base}.png"
    relative_png_path = png_path.relative_to(REPO_ROOT).as_posix()
    return html_path, png_path, relative_png_path
