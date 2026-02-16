"""Verify Chromium browser launches successfully"""

import os
import tempfile
import pytest
from playwright.sync_api import sync_playwright


def test_browser_launch():
    """Verify Chromium browser can launch and close successfully"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        if browser is None:
            pytest.fail("Browser failed to launch")
        browser.close()


def test_browser_new_page():
    """Verify browser can create a new page"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        if page is None:
            pytest.fail("Failed to create new page")
        page.close()
        browser.close()


def test_browser_navigate_to_file():
    """Verify browser can navigate to a local file"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write("<html><body><h1>Test</h1></body></html>")
            temp_file = f.name

        try:
            file_path = os.path.abspath(temp_file)
            page.goto(f"file://{file_path}")
            content = page.content()
            if "Test" not in content:
                pytest.fail("Page content does not contain expected text")
        finally:
            os.unlink(temp_file)
            page.close()
            browser.close()
