---
title: Local Development
description: Set up your development environment to contribute to Steam Stats
---

# Local Development Setup :material-laptop:

This guide helps you set up a local development environment for Steam Stats contributions.

## Prerequisites :material-hammer-wrench:

| Requirement       | Minimum Version | Purpose                                               |
|-------------------|-----------------|-------------------------------------------------------|
| **Python**        | 3.9+            | Core application runtime                              |
| **Docker Desktop**| 4.0+            | Container testing and builds, publishing to Docker Hub|
| **Git**           | 2.49+           | Version control                                       |
| **Playwright**    | 1.52+           | Browser automation for PNG generation                 |

### Determining Minimum Versions :octicons-versions-24:
- **Python 3.9+**: Required for modern type hints and async features used in the codebase
- **Docker Desktop 4.0+**: Supports BuildKit and multi-platform builds needed for the project
- **Git 2.49+**: Supports modern workflow features and security updates
- **Playwright 1.52+**: Stable API for Chromium browser automation

## Environment Setup :material-rocket-launch-outline:

### 1. Clone and Install :octicons-repo-clone-24:

```sh
# Clone your fork
git clone https://github.com/YOUR-USERNAME/Steam-Stats.git
cd Steam-Stats

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
OR
& {path-to-where-you-created-venv}>/venv/Scripts/Activate.ps1
& F:/CodeBase/Steam-Stats/venv/Scripts/Activate.ps1

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

### 2. Install Playwright Browsers :octicons-browser-24:

```sh
# Install browser binaries for PNG generation
python -m playwright install --with-deps chromium
playwright install --with-deps chromium

# Verify installation
playwright --version
```

### 3. Environment Variables :material-file-cog:

Create a `.env` file in the project root:

```sh
# Required for API testing
INPUT_STEAM_API_KEY=YOUR_32_CHARACTER_STEAM_API_KEY
INPUT_STEAM_ID=YOUR_17_DIGIT_STEAM_ID
INPUT_STEAM_CUSTOM_ID=YOUR_CUSTOM_STEAM_ID

# Optional
INPUT_WORKSHOP_STATS=True
INPUT_LOG_SCALE=False
```

!!! warning "Keep .env Private"
    Never commit your `.env` file, it's already in `.gitignore`. Use test credentials, not your production Steam API key

## Development Workflow :octicons-workflow-24:

### Running Locally :material-source-commit-local:

```sh
# Run the full workflow
python -m api.main

# Run specific components
python -c "from steam_stats import get_player_summaries; print(get_player_summaries())"
python -c "from api.card import generate_card_for_steam_user; generate_card_for_steam_user(data)"
```

### Testing Changes :material-test-tube:

```sh
# Run all tests
pytest

# Run specific test file
pytest tests/test_steam_stats.py

# Run with coverage
pytest --cov=api --cov=steam_stats

# Run tests with verbose output
pytest -v
```

### Code Quality  :octicons-code-24:

```sh
# Format code
black api/ tests/

# Lint code
flake8 api/ tests/

# Type checking
mypy api/
```

## Docker Development :simple-docker:

### Build and Test Container :octicons-container-24:

```sh
# Build the Docker image
docker build -t steam-stats-dev .

# Run with environment variables
docker run --env-file .env steam-stats-dev

# Interactive debugging
docker run -it --env-file .env steam-stats-dev /bin/sh

# Test with Docker Desktop
# View logs and container status in Docker Desktop GUI
```

## Documentation Development :material-book-open-outline:

### MkDocs Setup :simple-materialformkdocs:

```sh
# Install MkDocs and theme
pip install mkdocs-material mkdocs-mermaid2-plugin mkdocstrings[python]

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

Access at: `http://localhost:8000` or `http://127.0.0.1:8000`

## Debugging Common Issues :material-bug-outline:

### Steam API Issues :material-steam:

```python
# Debug API responses
import requests
import json

response = requests.get(
    "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/",
    params={"key": "YOUR_API_KEY", "steamids": "YOUR_STEAM_ID"}
)
print(json.dumps(response.json(), indent=2))
```

### Playwright/PNG Issues :material-file-png-box:

```python
# Debug HTML generation
from api.card import generate_card_for_player_summary

# This creates HTML files you can open in browser
html_content = generate_card_for_player_summary(your_data)
with open("debug_card.html", "w") as f:
    f.write(html_content)
```

### Workshop Scraping Issues :octicons-issue-draft-24:

```python
# Debug scraping
from api.steam_workshop import fetch_all_workshop_stats
import pprint

data = fetch_all_workshop_stats()
pprint.pprint(data)
```

## Continuous Integration :simple-githubactions:

### Pre-commit Hooks :material-hook:

```sh
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### GitHub Actions Testing :material-ab-testing:

All PRs run through these automated workflows:

- **Security Scanning** `(bandit.yml)`: Vulnerability detection in Python code
- **Code Quality** `(codeql.yml)`: Static analysis and security scanning
- **Test Coverage** `(coverage.yml)`: Code coverage reporting and enforcement
- **Dependency Security** `(dependency-review.yml)`: Check for vulnerable dependencies
- **Container Build**: Ensures Docker image builds successfully
- **Security Scorecard** `(scorecard.yml)`: OpenSSF security best practices assessment

### Release Automation

- **Automated Releases**: `release.yml` - Semantic versioning and changelog generation
- **Package Publishing**: Automated PyPI and Docker Hub publishing

## Making Changes :material-pencil:

### 1. Create Feature Branch :octicons-git-branch-24:

```sh
git checkout -b feature/your-feature-name
```

### 2. Development Cycle :material-recycle-variant:

```sh
# Make changes
# Run tests
pytest

# Format code
black .
pylint .

# Commit changes
git add .
git commit -m "feat: add new feature description"
```

### 3. Test Full Workflow :material-test-tube:

```sh
# Test end-to-end
python -m api.main

# Verify generated files
ls -la assets/

# Test Docker build
docker build .
```

### 4. Submit PR :octicons-git-pull-request-24:

```sh
git push origin feature/your-feature-name
# Create PR on GitHub
```

## VS Code Configuration :material-microsoft-visual-studio-code:

### Recommended Extensions :simple-gitextensions:
Based on the project's tech stack, these extensions enhance development:

#### Core Development
- `ms-python.python` - Python language support
- `ms-python.pylint` - Pylint integration
- `ms-python.black-formatter` - Code formatting
- `ms-python.vscode-pylance` - Enhanced Python IntelliSense

#### Code Quality & Security
- `sonarsource.sonarlint-vscode` - Code quality analysis
- `shardulm94.trailing-spaces` - Whitespace management

#### Development Productivity
- `github.copilot` - AI-powered code completion
- `github.copilot-chat` - AI assistant
- `wakatime.vscode-wakatime` - Time tracking

#### File Handling & Formatting
- `redhat.vscode-yaml` - YAML language support
- `tamasfe.even-better-toml` - TOML file support
- `samuelcolvin.jinjahtml` - Jinja template support
- `mechatroner.rainbow-csv` - CSV file visualization

#### Additional Tools
- `ms-azuretools.vscode-containers` - Docker container support
- `vscode-icons-team.vscode-icons` - Enhanced file icons
- `ms-vscode.live-server` - Local development server

#### Installation Command
You can install all recommended extensions at once using:

```sh
code --install-extension ms-python.python
--install-extension ms-python.pylint
--install-extension ms-python.black-formatter
--install-extension ms-python.vscode-pylance
--install-extension sonarsource.sonarlint-vscode
--install-extension shardulm94.trailing-spaces
--install-extension redhat.vscode-yaml
--install-extension tamasfe.even-better-toml
--install-extension samuelcolvin.jinjahtml
--install-extension mechatroner.rainbow-csv
```

| Extension              | Purpose                     |
|------------------------|-----------------------------|
| **Python**             | Python language support     |
| **Pylance**            | Advanced Python IntelliSense|
| **Black Formatter**    | Code formatting             |
| **Docker**             | Docker container management |
| **GitLens**            | Enhanced Git capabilities   |
| **YAML**               | YAML file support           |
| **Markdown All in One**| Documentation editing       |

### VS Code Settings :material-cog:

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.testing.pytestEnabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true
    },
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### Launch Configuration :material-launch:

Create .vscode/launch.json for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Steam Stats",
            "type": "python",
            "request": "launch",
            "module": "api.main",
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env"
        },
        {
            "name": "Debug Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["-v"],
            "console": "integratedTerminal"
        }
    ]
}
```

---

*Next: [Contributing Guidelines](contributing.md) for code standards and PR workflow*
