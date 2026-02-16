"""Verify Playwright installs and imports work correctly"""

import subprocess
import sys
import pytest


def test_playwright_package_installed():
    """Verify Playwright package is installed and importable"""
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.fail(f"Failed to run playwright: {result.stderr}")
    print(f"Playwright version: {result.stdout.strip()}")


def test_playwright_browser_installed():
    """Verify Playwright browsers are installed"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from playwright.sync_api import sync_playwright; print('OK')",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.fail(f"Failed to import playwright.sync_api: {result.stderr}")
    if "OK" not in result.stdout:
        pytest.fail("Playwright sync_api did not return OK")


def test_playwright_api_available():
    """Verify Playwright async API is available"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from playwright.async_api import async_playwright; print('OK')",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.fail(f"Failed to import playwright.async_api: {result.stderr}")
    if "OK" not in result.stdout:
        pytest.fail("Playwright async_api did not return OK")
