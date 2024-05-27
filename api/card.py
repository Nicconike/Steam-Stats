"""Generate Card for Steam Stats"""
import json
import os
from dotenv import load_dotenv
from steam_stats import get_player_summaries

load_dotenv()

# Secrets Configuration
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")


def generate_card_for_player_summary(player_data):
    """Generate HTML content based on Steam Player Summary Data"""
    summary_data = player_data["response"]["players"][0]
    personaname = summary_data["personaname"]
    personastate = summary_data["personastate"]
    avatarfull = summary_data["avatarfull"]
    loccountrycode = summary_data["loccountrycode"]
    gameextrainfo = summary_data.get("gameextrainfo", None)

    personastate_map = {
        0: 'Offline',
        1: 'Online',
        2: 'Busy',
        3: 'Away',
        4: 'Snooze',
        5: 'Looking to trade',
        6: 'Looking to play'
    }
    personastate_value = personastate_map.get(personastate, 'Unknown')

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
            <p id="status">Status: {personastate_value}</p>
            <p id="country">Country: <span id="country-code">{loccountrycode}</span>
                <img id="flag" class="flag"
                src="https://flagcdn.com/w320/{loccountrycode.lower()}.png" alt="Flag">
            </p>
            {"<p id='game'>Currently Playing: <span id='game-info'>" +
             gameextrainfo + "</span></p>" if gameextrainfo else ""}</div>
    </div>
</body>
</html>
    """
    return html_content


def save_to_file(data, filename):
    """Save fetched data to a file in JSON format"""
    if data is not None:
        with open(filename, 'w', encoding='utf-8') as file:
            # Use json.dump to write the JSON data to the file
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    else:
        print("No data to save")


if __name__ == "__main__":
    summary = get_player_summaries()
    html = generate_card_for_player_summary(summary)
    print(html)
