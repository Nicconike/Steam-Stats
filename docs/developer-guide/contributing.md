---
title: Contributing Guidelines
description: Code standards, PR workflow and contribution best practices
---

# Contributing Guidelines :material-television-guide:

Thanks for your interest in contributing to Steam Stats! This guide covers how to contribute code, documentation, tests, and bug reports.

## Ways to Contribute :material-handshake:

| Type             | Skills Needed         | Typical Time         |
|------------------|-----------------------|----------------------|
| Bug Reports      | User experience       | 5-15 minutes         |
| Documentation    | Markdown, clarity     | 30 minutes - 2 hours |
| Bug Fixes        | Python, debugging     | 1-4 hours            |
| New Features     | Python, APIs, testing | 4-20 hours           |
| Code Review      | Python knowledge      | 15-30 minutes        |

## Before You Start :material-clipboard-list:

- Check existing issues and pull requests to avoid duplication
- Review the [roadmap](https://github.com/Nicconike/Steam-Stats/projects)
- For major changes, open a proposal issue first

## Development Workflow :material-cog-clockwise:

### 1. Fork and Clone

```sh
git clone https://github.com/YOUR-USERNAME/Steam-Stats.git
cd Steam-Stats
git remote add upstream https://github.com/Nicconike/Steam-Stats.git
```

### 2. Create Feature Branch

```sh
git checkout -b feat/your-feature-name
```

### 3. Development Setup

Follow [Local Development](local-development.md) for environment setup.

### 4. Coding Standards

| Standard          | Tool    | Notes                   |
|-------------------|---------|-------------------------|
| Code formatting   | black   | 100-char line length    |
| Import sorting    | isort   | Compatible with black   |
| Linting           | pylint  | 10/10 score maintained  |
| Type checking     | mypy    | Strict mode on new code |
| Security scanning | bandit  | Vulnerability detection |

### 5. Commit Messages

Use [Conventional Commits](https://conventionalcommits.org/):

```sh
git commit -m "feat(api): add new Steam API endpoint"
git commit -m "fix(cards): resolve PNG generation bug"
git commit -m "docs(contributing): update guidelines"
```

### 6. Testing

- Add or update tests for any new or fixed functionality
- Run all tests locally before pushing

### 7. Pull Requests

- Rebase on upstream main before creating PR
- Fill out PR description clearly explaining changes
- Link to any issues fixed or related

## Reporting Bugs :material-bug-stop: :material-bug-stop-outline:

Use the [bug report template](https://github.com/Nicconike/Steam-Stats/issues/new?assignees=nicconike&labels=bug&template=bug-report.yml) and provide steps to reproduce, logs, and expected behavior.

## Requesting Features :material-rocket:

Use the [feature request template](https://github.com/Nicconike/Steam-Stats/issues/new?assignees=nicconike&labels=enhancement&template=feature-request.yml) and clearly describe your idea and motivation.

## Recognition :material-trophy:

Contributors to Steam Stats get recognition in:

- The contributors section of the README
- Release notes for major features or fixes
- GitHub contributor graph

---

*Return to [Developer Guide](index.md).*
