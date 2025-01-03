"""Generate Cards for Steam Stats"""

import datetime
import logging
import math
import os
import asyncio
from playwright.async_api import async_playwright, Error as PlaywrightError

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

MARGIN = 10

# Get Github Repo's Details where the action is being ran
repo_owner, repo_name = os.environ["GITHUB_REPOSITORY"].split("/")
branch_name = os.environ["GITHUB_REF_NAME"]

# Personastate mapping for Steam Profile Status
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
        logger.error("File Not Found Error: %s", str(e))
    elif isinstance(e, PlaywrightError):
        logger.error("Playwright Error: %s", str(e))
    elif isinstance(e, KeyError):
        logger.error("Key Error: %s", str(e))
    elif isinstance(e, asyncio.TimeoutError):
        logger.error("Timeout Error: %s", str(e))
    else:
        logger.error("Unexpected Error: %s", str(e))


async def get_element_bounding_box(html_file, selector):
    """Get the bounding box of the specified element using Playwright"""
    browser = None
    try:
        # Check if the HTML file exists
        if not os.path.exists(html_file):
            raise FileNotFoundError("HTML file not found:" + str(html_file))
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()
            await page.goto("file://" + os.path.abspath(html_file))
            bounding_box = await page.evaluate(
                "() => {"
                ' var element = document.querySelector("' + selector + '");'
                " if (!element) {"
                ' throw new Error("Element not found: ' + selector + '");'
                " }"
                " var rect = element.getBoundingClientRect();"
                " return {x: rect.x, y: rect.y, width: rect.width, height: rect.height};"
                "}"
            )
            await page.close()
        # Add margin to the bounding box
        bounding_box["x"] = max(bounding_box["x"] - MARGIN, 0)
        bounding_box["y"] = max(bounding_box["y"] - MARGIN, 0)
        bounding_box["width"] += 2 * MARGIN
        bounding_box["height"] += 2 * MARGIN
        return bounding_box
    except (FileNotFoundError, PlaywrightError, KeyError, asyncio.TimeoutError) as e:
        handle_exception(e)
    finally:
        if browser:
            await browser.close()


async def html_to_png(html_file, output_file, selector):
    """Convert HTML file to PNG using Playwright with clipping"""
    browser = None
    try:
        bounding_box = await get_element_bounding_box(html_file, selector)
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()
            await page.goto("file://" + os.path.abspath(html_file))
            await page.screenshot(path=output_file, clip=bounding_box)
            await page.close()
    except (FileNotFoundError, PlaywrightError, KeyError, asyncio.TimeoutError) as e:
        handle_exception(e)
    finally:
        if browser:
            await browser.close()


def convert_html_to_png(html_file, output_file, selector):
    """Convert HTML file to PNG using Playwright with clipping"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(html_to_png(html_file, output_file, selector))
    except (FileNotFoundError, PlaywrightError, KeyError, asyncio.TimeoutError) as e:
        handle_exception(e)


def format_unix_time(unix_time):
    """Convert Unix time to human-readable format with ordinal day"""
    dt = datetime.datetime.fromtimestamp(unix_time)
    day = dt.day

    if 11 <= day <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    return str(day) + suffix + " " + dt.strftime("%b %Y")


def generate_card_for_player_summary(player_data):
    """Generate HTML content based on Steam Player Summary Data"""
    if not player_data:
        return None
    summary_data = player_data["response"]["players"][0]
    personaname = summary_data["personaname"]
    personastate = summary_data["personastate"]
    avatarfull = summary_data["avatarfull"]
    loccountrycode = summary_data.get("loccountrycode", "")
    lastlogoff = summary_data["lastlogoff"]
    timecreated = summary_data["timecreated"]
    gameextrainfo = summary_data.get("gameextrainfo", None)

    # Convert lastlogoff & timecreated from Unix time to human-readable format
    lastlogoff_str = format_unix_time(lastlogoff)
    timecreated_str = format_unix_time(timecreated)

    personastate_value = personastate_map.get(personastate, "Unknown")

    # Create country section only if loccountrycode exists
    country_section = ""
    if loccountrycode:
        country_section = f"""
            <p id="country">Country: <span id="country-code">{loccountrycode}</span>
                <img id="flag" class="flag"
                src="https://flagcdn.com/w320/{loccountrycode.lower()}.png" alt="Flag">
            </p>
        """

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
            .info-left {{
                width: 45%;
            }}
            .info-right {{
                width: 55%;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="content">
                <h2>Steam Profile Summary</h2>
                <img id="avatar" class="avatar" src="{avatarfull}" alt="Avatar">
                <h2 id="name">{personaname}</h2>
                <div class="info-container">
                    <div class="info-left">
                        <p id="status">Status: {personastate_value}</p>
                        {country_section}
                    </div>
                    <div class="info-right">
                        <p id="lastlogoff">Last Logoff: {lastlogoff_str}</p>
                        <p id="timecreated">PC Gaming Since: {timecreated_str}</p>
                    </div>
                </div>
                {"<p id='game'>Currently Playing: <span id='game-info'>" +
                gameextrainfo + "</span></p>" if gameextrainfo else ""}
            </div>
        </div>
    </body>
    </html>
    """
    with open("assets/steam_summary.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    convert_html_to_png(
        "assets/steam_summary.html", "assets/steam_summary.png", ".card"
    )

    return (
        "![Steam Summary]"
        "(https://github.com/"
        + repo_owner
        + "/"
        + repo_name
        + "/blob/"
        + branch_name
        + "/assets/steam_summary.png)\n"
    )


def generate_card_for_played_games(games_data):
    """Generate HTML Card for recently played games in last 2 weeks"""
    if not games_data:
        return None

    # Placeholder image for Spacewar
    placeholder_image = "https://i.imgur.com/DBnVqet.jpg"

    # Check if LOG_SCALE is enabled (Optional Feature Flag)
    log_scale = os.getenv("INPUT_LOG_SCALE", "false").lower() in ("true", "1", "t")
    watermark = '<div class="watermark">Log Scale Enabled</div>' if log_scale else ""

    # Calculate dynamic height
    num_games = games_data["response"]["total_count"]
    min_canvas_height = num_games * 60 + 70

    # Get max playtime for normalization
    max_playtime = games_data["response"]["games"][0]["playtime_2weeks"]

    def format_playtime(playtime):
        """Format playtime into human-readable format"""
        if playtime < 60:
            unit = " min" if playtime == 1 else " mins"
            return str(playtime) + unit

        hours, minutes = divmod(playtime, 60)
        if minutes == 0:
            return str(hours) + " hrs"

        unit = " min" if minutes == 1 else " mins"
        return str(hours) + " hrs and " + str(minutes) + unit

    def generate_progress_bar(game, index):
        """Generate progress bar HTML for a single game"""
        name = game["name"]
        playtime = game["playtime_2weeks"]
        img_icon_url = (
            placeholder_image
            if name == "Spacewar"
            else "https://media.steampowered.com/steamcommunity/public/images/apps/"
            + str(game["appid"])
            + "/"
            + game["img_icon_url"]
            + ".jpg"
        )
        normalized_playtime = (
            round(
                math.log1p(playtime)
                / math.log1p(
                    max(
                        game["playtime_2weeks"]
                        for game in games_data["response"]["games"]
                    )
                )
                * 100
            )
            if log_scale
            else round((playtime / max_playtime) * 100)
        )
        display_time = format_playtime(playtime)

        return (
            """
        <div class="bar-container">
            <img src="{img}" alt="{name}" class="game-icon">
            <progress class="progress-style-{style}" value="{value}" max="100"></progress>
            <div class="game-info">
                <span class="game-name">{name}</span><br>
                <span class="game-time">{time}</span>
            </div>
        </div>
        """.replace(
                "{img}", img_icon_url
            )
            .replace("{name}", name)
            .replace("{style}", str((index % 6) + 1))
            .replace("{value}", str(normalized_playtime))
            .replace("{time}", display_time)
        )

    # Generate progress bars for all games
    progress_bars = "".join(
        generate_progress_bar(game, i)
        for i, game in enumerate(games_data["response"]["games"])
        if "name" in game and "playtime_2weeks" in game
    )

    # Generate HTML content
    html_content = (
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recently Played Games in Last 2 Weeks</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="card" style="height: {height}px; position: relative; ">
            <div class="content" style="position: relative; text-align: center;">
                <h2>Recently Played Games (Last 2 Weeks)</h2>
                {bars}
            </div>
            {watermark}
        </div>
    </body>
    </html>
    """.replace(
            "{height}", str(min_canvas_height)
        )
        .replace("{bars}", progress_bars)
        .replace("{watermark}", watermark)
    )

    with open("assets/recently_played_games.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    convert_html_to_png(
        "assets/recently_played_games.html", "assets/recently_played_games.png", ".card"
    )

    return (
        "![Recently Played Games]"
        "(https://github.com/"
        + repo_owner
        + "/"
        + repo_name
        + "/blob/"
        + branch_name
        + "/assets/recently_played_games.png)"
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
        <div class="card" style="text-align: center;">
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
                        <td>{workshop_stats["total_unique_visitors"]}</td>
                    </tr>
                    <tr>
                        <td>Current Subscribers</td>
                        <td>{workshop_stats["total_current_subscribers"]}</td>
                    </tr>
                    <tr>
                        <td>Current Favorites</td>
                        <td>{workshop_stats["total_current_favorites"]}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    with open("assets/steam_workshop_stats.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    convert_html_to_png(
        "assets/steam_workshop_stats.html", "assets/steam_workshop_stats.png", ".card"
    )

    return (
        "![Steam Workshop Stats]"
        "(https://github.com/"
        + repo_owner
        + "/"
        + repo_name
        + "/blob/"
        + branch_name
        + "/assets/steam_workshop_stats.png)"
    )
