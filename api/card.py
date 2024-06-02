"""Generate Cards for Steam Stats"""
import datetime
import math
import os
import asyncio
import time
import zipfile
from pyppeteer import launch
import requests
from steam_stats import get_player_summaries, get_recently_played_games
from steam_workshop import fetch_workshop_item_links, fetch_all_workshop_stats
from dotenv import load_dotenv

load_dotenv()

# Secrets Configuration
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")
STEAM_CUSTOM_ID = os.getenv("STEAM_CUSTOM_ID")
REQUEST_TIMEOUT = (10, 15)

CHROMIUM_ZIP_URL = "https://commondatastorage.googleapis.com/chromium-browser-snapshots/Win_x64/1309077/chrome-win.zip"
CHROMIUM_DIR = os.path.join(os.getcwd(), 'chromium')
CHROMIUM_EXECUTABLE = os.path.join(CHROMIUM_DIR, 'chrome-win', 'chrome.exe')
MARGIN = 5


def download_and_extract_chromium():
    """Download and extract Chromium from the provided URL"""
    if not os.path.exists(CHROMIUM_DIR):
        os.makedirs(CHROMIUM_DIR)
    zip_path = os.path.join(CHROMIUM_DIR, 'chrome-win.zip')
    if not os.path.exists(zip_path):
        print("Downloading Chromium...")
        response = requests.get(
            CHROMIUM_ZIP_URL, stream=True, timeout=REQUEST_TIMEOUT)
        with open(zip_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print("Chromium downloaded successfully.")
    if not os.path.exists(CHROMIUM_EXECUTABLE):
        print("Extracting Chromium...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(CHROMIUM_DIR)
        print("Chromium extracted successfully.")


async def get_element_bounding_box(html_file, selector):
    """Get the bounding box of the specified element using pyppeteer"""
    browser = await launch(headless=True, executablePath=CHROMIUM_EXECUTABLE)
    page = await browser.newPage()
    await page.goto(f'file://{os.path.abspath(html_file)}')
    bounding_box = await page.evaluate(f'''() => {{
        var element = document.querySelector('{selector}');
        var rect = element.getBoundingClientRect();
        return {{x: rect.x, y: rect.y, width: rect.width, height: rect.height}};
    }}''')
    await browser.close()
    # Add margin to the bounding box
    bounding_box['x'] = max(bounding_box['x'] - MARGIN, 0)
    bounding_box['y'] = max(bounding_box['y'] - MARGIN, 0)
    bounding_box['width'] += 2 * MARGIN
    bounding_box['height'] += 2 * MARGIN
    return bounding_box


async def html_to_png(html_file, output_file, selector):
    """Convert HTML file to PNG using pyppeteer with clipping"""
    bounding_box = await get_element_bounding_box(html_file, selector)
    browser = await launch(headless=True, executablePath=CHROMIUM_EXECUTABLE)
    page = await browser.newPage()
    await page.goto(f'file://{os.path.abspath(html_file)}')
    await page.screenshot({
        'path': output_file,
        'clip': {
            'x': bounding_box['x'],
            'y': bounding_box['y'],
            'width': bounding_box['width'],
            'height': bounding_box['height']
        }
    })
    await browser.close()


def convert_html_to_png(html_file, output_file, selector):
    """Convert HTML file to PNG using pyppeteer with clipping"""
    download_and_extract_chromium()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(html_to_png(html_file, output_file, selector))


def format_unix_time(unix_time):
    """Convert Unix time to human-readable format"""
    return datetime.datetime.fromtimestamp(unix_time).strftime("%d/%m/%Y")


def generate_card_for_player_summary(player_data):
    """Generate HTML content based on Steam Player Summary Data"""
    if not player_data:
        return None
    summary_data = player_data["response"]["players"][0]
    personaname = summary_data["personaname"]
    personastate = summary_data["personastate"]
    avatarfull = summary_data["avatarfull"]
    loccountrycode = summary_data["loccountrycode"]
    lastlogoff = summary_data["lastlogoff"]
    timecreated = summary_data["timecreated"]
    gameextrainfo = summary_data.get("gameextrainfo", None)

    # Convert lastlogoff & timecreated from Unix time to human-readable format
    lastlogoff_str = format_unix_time(lastlogoff)
    timecreated_str = format_unix_time(timecreated)

    personastate_map = {
        0: "Offline",
        1: "Online",
        2: "Busy",
        3: "Away",
        4: "Snooze",
        5: "Looking to trade",
        6: "Looking to play"
    }
    personastate_value = personastate_map.get(personastate, "Unknown")

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Steam Player Summary</title>
    <style>
        .card {{
            width: 100%;
            max-width: 500px;
            margin: auto;
            border: 2px solid #000;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            background-color: #fff;
        }}
        .avatar {{
            width: 100px;
            height: 100px;
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
    </style>
</head>
<body>
    <div class="card">
        <div class="content">
            <img id="avatar" class="avatar" src="{avatarfull}" alt="Avatar">
            <h2 id="name">Name: {personaname}</h2>
            <p id="status">Status: {personastate_value}</p>
            <p id="country">Country: <span id="country-code">{loccountrycode}</span>
                <img id="flag" class="flag"
                src="https://flagcdn.com/w320/{loccountrycode.lower()}.png" alt="Flag">
            </p>
            <p id="lastlogoff">Last Logoff: {lastlogoff_str}</p>
            <p id="lastlogoff">Gaming Since: {timecreated_str}</p>
            {"<p id='game'>Currently Playing: <span id='game-info'>" +
             gameextrainfo + "</span></p>" if gameextrainfo else ""}
        </div>
    </div>
</body>
</html>
    """
    with open("../assets/steam_summary.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    convert_html_to_png("../assets/steam_summary.html",
                        "../assets/steam_summary.png", ".card")

    return (
        "![Steam Summary]"
        "(https://github.com/Nicconike/Steam-Stats/blob/master/assets/steam_summary.png)\n"
    )


def generate_card_for_played_games(games_data):
    """Generate HTML Card for recently played games in last 2 weeks"""
    if not games_data:
        return None

    max_playtime = games_data["response"]["games"][0]["playtime_2weeks"]

    # Generate the progress bars with repeating styles
    progress_bars = ""
    for i, game in enumerate(games_data["response"]["games"]):
        if "name" in game and "playtime_2weeks" in game:
            name = game["name"]
            playtime = game["playtime_2weeks"]
            img_icon_url = f"https://media.steampowered.com/steamcommunity/public/images/apps/{
                game["appid"]}/{game["img_icon_url"]}.jpg"
            normalized_playtime = (playtime / max_playtime) * 100
            normalized_playtime = math.log1p(playtime) / math.log1p(
                max(game["playtime_2weeks"] for game in games_data["response"]["games"])) * 100

            normalized_playtime = round(normalized_playtime)
            display_time = f"{playtime} mins" if playtime < 60 else f"{
                playtime / 60:.2f} hrs"
            progress_bars += f"""
            <div class="bar-container">
                <img src="{img_icon_url}" alt="{name}" class="game-icon">
                <progress class="progress-style-{(i % 6) + 1}" value="{normalized_playtime}"
                max="100"></progress>
                <span class="game-info"><b>{name} ({display_time})</b></span>
            </div>
            """

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
    <div class="card">
        <div class="content">
            <h2>Recently Played Games</h2>
            {progress_bars}
        </div>
    </div>
</body>
</html>
    """

    with open("../assets/recently_played_games.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    convert_html_to_png("../assets/recently_played_games.html",
                        "../assets/recently_played_games.png", ".card")

    return (
        "![Steam Summary]"
        "(https://github.com/Nicconike/Steam-Stats/blob/master/assets/recently_played_games.png)"
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
            background-color: #4CAF50;
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
    with open("../assets/steam_workshop_stats.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    convert_html_to_png("../assets/steam_workshop_stats.html",
                        "../assets/steam_workshop_stats.png", ".card")

    return (
        "![Steam Summary]"
        "(https://github.com/Nicconike/Steam-Stats/blob/master/assets/steam_workshop_stats.png"
        "?sanitize=true)\n"
    )


if __name__ == "__main__":
    start_time = time.time()
    player_summary = get_player_summaries()
    recently_played_games = get_recently_played_games()
    links = fetch_workshop_item_links(STEAM_CUSTOM_ID)
    workshop_data = fetch_all_workshop_stats(links)
    generate_card_for_player_summary(player_summary)
    generate_card_for_played_games(recently_played_games)
    generate_card_for_steam_workshop(workshop_data)
    end_time = time.time()  # End the timer
    total_time = end_time-start_time
    total_time = round(total_time, 3)  # Total time
    print(f"Total Execution Time: {total_time} seconds")
