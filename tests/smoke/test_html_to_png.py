"""Verify full HTML to PNG conversion flow"""

import os
import tempfile
import pytest
from playwright.sync_api import sync_playwright


def test_html_to_png_basic():
    """Verify HTML can be converted to PNG using Playwright"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial; padding: 20px; background: #1b2838; color: #c7d5e0; }
            .card { background: #171a21; padding: 20px; border-radius: 5px; }
            h1 { color: #66c0f4; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Steam Stats Test</h1>
            <p>Test card for smoke testing</p>
        </div>
    </body>
    </html>
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_content)
        html_file = f.name

    output_file = html_file.replace(".html", ".png")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 800, "height": 400})
            page.goto(f"file://{os.path.abspath(html_file)}")
            page.wait_for_selector(".card")
            page.screenshot(path=output_file, full_page=False)
            browser.close()

        if not os.path.exists(output_file):
            pytest.fail(f"PNG file was not created at {output_file}")

        file_size = os.path.getsize(output_file)
        if file_size <= 0:
            pytest.fail("PNG file is empty")
        print(f"Generated PNG file size: {file_size} bytes")

    finally:
        if os.path.exists(html_file):
            os.unlink(html_file)
        if os.path.exists(output_file):
            os.unlink(output_file)


def test_playwright_screenshot_element():
    """Verify specific element can be captured as screenshot"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><style>
        body { margin: 0; background: #1b2838; }
        .outer-card { background: #171a21; padding: 40px; }
        .inner { color: #66c0f4; font-size: 24px; }
    </style></head>
    <body>
        <div class="outer-card">
            <div class="inner">Element Screenshot Test</div>
        </div>
    </body>
    </html>
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_content)
        html_file = f.name

    output_file = html_file.replace(".html", "_element.png")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"file://{os.path.abspath(html_file)}")

            element = page.query_selector(".outer-card")
            if element is None:
                pytest.fail("Element .outer-card not found")

            element.screenshot(path=output_file)
            browser.close()

        if not os.path.exists(output_file):
            pytest.fail("Element screenshot was not created")

    finally:
        if os.path.exists(html_file):
            os.unlink(html_file)
        if os.path.exists(output_file):
            os.unlink(output_file)


def test_multiple_screenshots():
    """Verify multiple screenshots can be taken in sequence"""
    html_content = """
    <!DOCTYPE html>
    <html><body style="background: #1b2838; color: white;">
        <h1>Multiple Test</h1>
    </body></html>
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_content)
        html_file = f.name

    output_files = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"file://{os.path.abspath(html_file)}")

            for i in range(3):
                output_file = html_file.replace(".html", f"_shot{i}.png")
                output_files.append(output_file)
                page.screenshot(path=output_file)
                if not os.path.exists(output_file):
                    pytest.fail(f"Screenshot {i} not created")

            browser.close()

    finally:
        for f in output_files:
            if os.path.exists(f):
                os.unlink(f)
        if os.path.exists(html_file):
            os.unlink(html_file)
