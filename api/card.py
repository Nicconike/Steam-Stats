"""Generate Cards for Steam Stats"""

import datetime
import logging
import math
import os
import asyncio
from typing import Optional, TypedDict
from playwright.async_api import async_playwright, Error as PlaywrightError
from api.utils import get_asset_paths

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


MARGIN = 10
CARD_SELECTOR = ".card"


class FloatRect(TypedDict):
    """Define FloatRect type for compatibility with Playwright"""

    x: float
    y: float
    width: float
    height: float


# Get GitHub Repo's Details where the action is being run
repo_owner, repo_name = os.getenv("GITHUB_REPOSITORY", "owner/repo").split("/")
branch_name = os.getenv("GITHUB_REF_NAME", "main")

# Persona state mapping for Steam Profile Status
personastate_map = {
    0: "Offline",
    1: "Online",
    2: "Busy",
    3: "Away",
    4: "Snooze",
    5: "Looking to trade",
    6: "Looking to play",
}


def handle_exception(e):
    """Handle exceptions and log appropriate error messages"""
    if isinstance(e, FileNotFoundError):
        logger.error("File Not Found Error: %s", e)
    elif isinstance(e, PlaywrightError):
        logger.error("Playwright Error: %s", e)
    elif isinstance(e, KeyError):
        logger.error("Key Error: %s", e)
    elif isinstance(e, asyncio.TimeoutError):
        logger.error("Timeout Error: %s", e)
    elif isinstance(e, ValueError):
        logger.error("Value Error: %s", e)
    else:
        logger.error("Unexpected Error: %s", e)


async def get_element_bounding_box(
    html_file: str, selector: str, margin: int = MARGIN
) -> Optional[FloatRect]:
    """Get the bounding box of the specified element using Playwright"""
    browser = None
    try:
        # Check if the HTML file exists
        if not os.path.exists(html_file):
            raise FileNotFoundError("HTML file not found: " + html_file)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                await page.goto("file://" + os.path.abspath(html_file))
            except TimeoutError as e:
                raise asyncio.TimeoutError("Timeout error while loading page") from e

            # Find element and get its bounding box
            element = await page.query_selector(selector)
            if not element:
                raise ValueError("Element not found for selector: " + selector)

            try:
                bounding_box = await element.bounding_box()
            except KeyError as e:
                raise KeyError("Key error while retrieving bounding box") from e

            if not bounding_box:
                raise ValueError(
                    "Could not retrieve bounding box for selector: " + selector
                )

            # Add margin to the bounding box
            bounding_box_with_margin: FloatRect = {
                "x": max(bounding_box["x"] - margin, 0),
                "y": max(bounding_box["y"] - margin, 0),
                "width": bounding_box["width"] + 2 * margin,
                "height": bounding_box["height"] + 2 * margin,
            }

            await browser.close()
            return bounding_box_with_margin

    except (
        FileNotFoundError,
        PlaywrightError,
        ValueError,
        KeyError,
        asyncio.TimeoutError,
    ) as e:
        handle_exception(e)
        return None
    finally:
        if browser:
            await browser.close()


async def html_to_png(
    html_file: str, output_file: str, selector: str, margin: int = MARGIN
) -> bool:
    """Convert an HTML file to a PNG using Playwright with clipping"""
    bounding_box = await get_element_bounding_box(html_file, selector, margin)
    if not bounding_box:
        logger.error("Bounding box could not be determined")
        return False

    clip: FloatRect = {
        "x": float(bounding_box["x"]),
        "y": float(bounding_box["y"]),
        "width": float(bounding_box["width"]),
        "height": float(bounding_box["height"]),
    }

    browser = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("file://" + os.path.abspath(html_file))

            # Take screenshot with clipping
            await page.screenshot(path=output_file, clip=clip)
            return True

    except (PlaywrightError, asyncio.TimeoutError) as e:
        handle_exception(e)
        return False

    finally:
        if browser:
            await browser.close()


def convert_html_to_png(html_file, output_file, selector):
    """Synchronous wrapper to convert HTML to PNG"""
    try:
        return asyncio.run(html_to_png(html_file, output_file, selector))
    except (FileNotFoundError, PlaywrightError, KeyError, asyncio.TimeoutError) as e:
        handle_exception(e)
        return False


def format_unix_time(unix_time):
    """Convert Unix time to human-readable format with ordinal day"""
    dt = datetime.datetime.fromtimestamp(unix_time)
    day = dt.day
    suffix = (
        "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    )
    return f"{day}{suffix} {dt.strftime('%b %Y')}"


def generate_card_for_player_summary(player_data):
    """Generate HTML content based on Steam Player Summary Data"""
    if not player_data:
        return None

    summary = player_data["response"]["players"][0]
    player = {
        "name": summary.get("personaname", "Unknown"),
        "status": personastate_map.get(summary.get("personastate", 0), "Unknown"),
        "avatar": summary.get("avatarfull", ""),
        "country": summary.get("loccountrycode", ""),
        "lastlogoff": format_unix_time(summary.get("lastlogoff", 0)),
        "timecreated": format_unix_time(summary.get("timecreated", 0)),
        "game": summary.get("gameextrainfo"),
    }

    country_section = (
        f"""
        <p id="country">Country: <span id="country-code">{player['country']}</span>
            <img id="flag" class="flag"
            src="https://flagcdn.com/w320/{player['country'].lower()}.png" alt="Flag">
        </p>
        """
        if player["country"]
        else ""
    )

    game_section = (
        f"<p id='game'>Currently Playing: <span id='game-info'>{player['game']}</span></p>"
        if player["game"]
        else ""
    )

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Steam Profile Summary</title>
        <style>
            .card {{
                width: 100%;
                max-width: 400px;
                margin: auto;
                border: 2px solid #000;
                padding: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                background-color: #fff;
            }}
            .avatar {{
                width: 80px;
                height: 80px;
                border-radius: 50%;
                margin: auto;
            }}
            .content {{
                text-align: center;
            }}
            .flag {{
                width: 32px;
                height: 24px;
                vertical-align: middle;
            }}
            .info-container {{
                display: flex;
                justify-content: space-between;
                margin-top: 10px;
            }}
            .info-left, .info-right {{
                width: 48%;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="content">
                <h2>Steam Profile Summary</h2>
                <img id="avatar" class="avatar" src="{player['avatar']}" alt="Avatar">
                <h2 id="name">{player['name']}</h2>
                <div class="info-container">
                    <div class="info-left">
                        <p id="status">Status: {player['status']}</p>
                        {country_section}
                    </div>
                    <div class="info-right">
                        <p id="lastlogoff">Last Logoff: {player['lastlogoff']}</p>
                        <p id="timecreated">PC Gaming Since: {player['timecreated']}</p>
                    </div>
                </div>
                {game_section}
            </div>
        </div>
    </body>
    </html>
    """

    html_path, png_path, relative_png_path = get_asset_paths("steam_summary")
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    convert_html_to_png(html_path, png_path, CARD_SELECTOR)

    return (
        f"![Steam Summary](https://github.com/{repo_owner}/"
        f"{repo_name}/blob/{branch_name}/{relative_png_path})\n"
    )


def format_playtime(playtime):
    """Format playtime into human-readable format"""
    if playtime < 60:
        unit = "min" if playtime == 1 else "mins"
        return f"{playtime} {unit}"
    hours, minutes = divmod(playtime, 60)
    if minutes == 0:
        return f"{hours} hrs"
    unit = "min" if minutes == 1 else "mins"
    return f"{hours} hrs and {minutes} {unit}"


def generate_progress_bar(game, index, max_playtime, log_scale, placeholder_image):
    """Generate progress bar HTML for a single game"""
    name = game.get("name", "Unknown Game")
    playtime = game.get("playtime_2weeks", 0)
    img_icon_url = (
        placeholder_image
        if name == "Spacewar"
        else (
            f"https://media.steampowered.com/steamcommunity/public/images/apps/"
            f"{game.get('appid')}/{game.get('img_icon_url')}.jpg"
        )
    )
    normalized_playtime = (
        round(math.log1p(playtime) / math.log1p(max_playtime) * 100)
        if log_scale
        else round((playtime / max_playtime) * 100)
    )
    display_time = format_playtime(playtime)
    style_class = f"progress-style-{(index % 6) + 1}"

    return f"""
    <div class="bar-container">
        <img src="{img_icon_url}" alt="{name}" class="game-icon">
        <progress class="{style_class}" value="{normalized_playtime}" max="100"></progress>
        <div class="game-info">
            <span class="game-name">{name}</span><br>
            <span class="game-time">{display_time}</span>
        </div>
    </div>
    """


def generate_card_for_played_games(games_data):
    """Generate HTML Card for recently played games in last 2 weeks"""
    if not games_data:
        return None

    placeholder_image = "https://i.imgur.com/DBnVqet.jpg"
    log_scale = os.getenv("INPUT_LOG_SCALE", "false").lower() in ("true", "1", "t")
    watermark = '<div class="watermark">Log Scale Enabled</div>' if log_scale else ""

    num_games = len(games_data["response"]["games"])
    min_canvas_height = num_games * 60 + 70
    max_playtime = (
        max(game["playtime_2weeks"] for game in games_data["response"]["games"]) or 1
    )

    progress_bars = "".join(
        generate_progress_bar(game, i, max_playtime, log_scale, placeholder_image)
        for i, game in enumerate(games_data["response"]["games"])
        if "name" in game and "playtime_2weeks" in game
    )

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recently Played Games in Last 2 Weeks</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="card" style="height: {min_canvas_height}px; position: relative; ">
            <div class="content" style="position: relative; text-align: center;">
                <h2>Recently Played Games (Last 2 Weeks)</h2>
                {progress_bars}
            </div>
            {watermark}
        </div>
    </body>
    </html>
    """

    html_path, png_path, relative_png_path = get_asset_paths("recently_played_games")
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    convert_html_to_png(html_path, png_path, CARD_SELECTOR)

    return (
        f"![Recently Played Games](https://github.com/{repo_owner}/"
        f"{repo_name}/blob/{branch_name}/{relative_png_path})"
    )


def generate_card_for_steam_workshop(workshop_stats):
    """Generates HTML content for retrieved Workshop Data"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Steam Workshop Stats</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-color: #f0f0f0;
                margin: 0;
            }}
            .card {{
                width: 100%;
                max-width: 400px;
                margin: auto;
                border: 2px solid #000;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                background-color: #fff;
                text-align: center;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #6495ED;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Steam Workshop Stats</h2>
            <table>
                <thead>
                    <tr>
                        <th>Workshop Stats</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Unique Visitors</td>
                        <td>{workshop_stats.get("total_unique_visitors", 0)}</td>
                    </tr>
                    <tr>
                        <td>Current Subscribers</td>
                        <td>{workshop_stats.get("total_current_subscribers", 0)}</td>
                    </tr>
                    <tr>
                        <td>Current Favorites</td>
                        <td>{workshop_stats.get("total_current_favorites", 0)}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    html_path, png_path, relative_png_path = get_asset_paths("steam_workshop_stats")
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    convert_html_to_png(html_path, png_path, CARD_SELECTOR)

    return (
        f"![Steam Workshop Stats](https://github.com/{repo_owner}/"
        f"{repo_name}/blob/{branch_name}/{relative_png_path})"
    )
