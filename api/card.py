"""Generate Card for Steam Stats"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Secrets Configuration
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")


def get_player_summaries(api_key, steam_id):
    """Get Player Summaries from Steam"""
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={
        api_key}&steamids={steam_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["response"]["players"][0]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player summaries: {e}")
        return None


def generate_card_for_player_summary(api_key, steam_id):
    """Generate HTML content based on player data"""
    player_data = get_player_summaries(api_key, steam_id)
    if not player_data:
        return None

    personaname = player_data["personaname"]
    personastate = player_data["personastate"]
    avatarfull = player_data["avatarfull"]
    loccountrycode = player_data["loccountrycode"]
    gameextrainfo = player_data.get("gameextrainfo", None)

    personastate_map = {
        0: 'Offline',
        1: 'Online',
        2: 'Busy',
        3: 'Away',
        4: 'Snooze',
        5: 'Looking to trade',
        6: 'Looking to play'
    }
    personastate_text = personastate_map.get(personastate, 'Unknown')

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive SVG Card</title>
    <style>
        .card {{
            width: 100%;
            max-width: 600px;
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
            <p id="status">Status: {personastate_text}</p>
            <p id="country">Country: <span id="country-code">{loccountrycode}</span>
                <img id="flag" class="flag"
                src="https://flagcdn.com/w320/{loccountrycode.lower()}.png" alt="Flag">
            </p>
            {"<p id='game'>Currently Playing: <span id='game-info'>" +
             gameextrainfo + "</span></p>" if gameextrainfo else ""}</div></div>
</body>
</html>
    """
    return html_content
