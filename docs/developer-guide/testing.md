---
title: Testing Guidelines
description: How to run and write unit tests for Steam Stats
---

# Testing Guidelines :material-test-tube:

Steam Stats includes thorough testing to ensure code quality and reliability. This guide explains the testing structure and best practices.

!!! warning "Assert Keyword Usage"
    Due to security best practices and vulnerability analysis tools like Bandit, **do not use the `assert` keyword directly in tests**.
    Instead, raise `AssertionError` explicitly when validation fails, as this project’s standard ensures clear and secure failure semantics.

## Test Structure :material-puzzle-outline:

### Test Directory Layout

```sh
tests/                     # Test suite
├── test_card.py           # Card generation and PNG tests
├── test_main.py           # Main workflow integration tests
├── test_steam_stats.py    # Steam API integration tests
├── test_steam_workshop.py # Workshop scraping tests
├── test_utils.py          # Utility function tests
└── __init__.py            # Test package initialization
```

## Running Unit Tests :material-test-tube-empty:

Run tests with pytest:

```sh
pytest
pytest -v
pytest tests/test_steam_stats.py
pytest --cov=api --cov-report=xml --cov-report=term-missing
```

## Writing Unit Tests :octicons-pencil-24:

- Use clear, descriptive test function names
- Mock external dependencies such as API calls
- Follow the Arrange-Act-Assert pattern with explicit `AssertionError` raises
- Use fixtures for common setup

### Example :octicons-code-24:
```sh
def test_get_player_summaries_success(requests_mock):
result = get_player_summaries()
if result is None:
raise AssertionError("Expected result to be not None")
if "response" not in result:
raise AssertionError("Expected 'response' key in result")
```

## Fixtures and Mocking :material-test-tube-off:

Centralize mock responses and environment variable mocks in `conftest.py` for reuse.

## Continuous Integration :simple-githubactions:

Unit tests run automatically on GitHub Actions for pull requests and main branch pushes via [coverage.yml](https://github.com/Nicconike/Steam-Stats/blob/master/.github/workflows/coverage.yml).

---

*Return to [Developer Guide](index.md).*
