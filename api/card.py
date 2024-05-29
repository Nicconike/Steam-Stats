"""Generate Cards for Steam Stats"""
import datetime


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
    <title>Responsive SVG Card</title>
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
    with open("assets/steam_summary.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    return (
        "![Steam Summary]("
        "https://github.com/Nicconike/Steam-Stats/blob/master/assets/steam_summary.html"
        "?sanitize=true)\n"
    )


def generate_card_for_played_games(games_data):
    """Generate HTML content for recently played games with a horizontal bar graph"""
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
            display_time = f"{playtime} mins" if playtime < 60 else f"{
                playtime / 60:.2f} hrs"
            progress_bars += f"""
            <div class="bar-container">
                <img src="{img_icon_url}" alt="{name}" class="game-icon">
                <progress id="p{i}" value="{normalized_playtime}" max="100"
                class="bar-{(i % 6) + 1}"></progress>
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
    <link rel="stylesheet" href="assets/style.css">
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

    with open("assets/recently_played_games.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    return (
        "![Steam Games Stats]("
        "https://github.com/Nicconike/Steam-Stats/blob/master/assets/recently_played_games.html"
        "?sanitize=true)"
    )
