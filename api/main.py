"""Main Runner Script"""
import json
import os
import time
import svgwrite
from steam_stats import get_player_summaries, get_recently_played_games, process_player_summary_data
from steam_workshop import fetch_workshop_item_links, fetch_all_workshop_stats

# Secrets Configuration
STEAM_ID = os.getenv("STEAM_CUSTOM_ID")


def generate_markdown(summary_data, recently_played_data):
    """Generate combined Markdown content for player data, achievements, recently played games"""

    # Generate Steam User Summary Markdown
    personastate_str = summary_data["personastate"]
    summary_markdown = f"""
## Steam User Summary for {summary_data["personaname"]}

- **Steam Status:** {personastate_str}
- **Last Logoff (IST):** {summary_data["lastlogoff"]}
- **Profile URL:** [Visit Profile]({summary_data["profileurl"]})
- **Avatar:** ![Avatar]({summary_data["avatarmedium"]})
"""

    # Add game status if the user is in-game
    if "gameid" in summary_data and summary_data["gameid"]:
        summary_markdown += f"\n- **Currently In-Game:** {
            summary_data["gameid"]}"

    # Generate Recently Played Games Markdown
    total_count = recently_played_data["response"]["total_count"]
    games_markdown = f"## Recently Played Games (Total: {total_count})\n"
    for game in recently_played_data["response"]["games"]:
        playtime_2weeks = game["playtime_2weeks"]
        playtime_forever = game["playtime_forever"]

        # Format playtime for the last 2 weeks
        if playtime_2weeks >= 60:
            playtime_2weeks_hours = playtime_2weeks // 60
            playtime_2weeks_minutes = playtime_2weeks % 60
            playtime_2weeks_str = f"{playtime_2weeks_hours} hrs {
                playtime_2weeks_minutes} mins"
        else:
            playtime_2weeks_str = f"{playtime_2weeks} mins"

        # Format total playtime
        if playtime_forever >= 60:
            playtime_forever_hours = playtime_forever // 60
            playtime_forever_minutes = playtime_forever % 60
            playtime_forever_str = f"{playtime_forever_hours} hrs {
                playtime_forever_minutes} mins"
        else:
            playtime_forever_str = f"{playtime_forever} mins"

        games_markdown += f"- {game["name"]}: Playtime last 2 weeks: {
            playtime_2weeks_str}, Total playtime: {playtime_forever_str}\n"

    # Combine all Markdown sections
    combined_markdown = summary_markdown + "\n" + games_markdown
    return combined_markdown


def generate_svg_card(total_stats):
    """Generates SVG Card for retrieved Workshop Data"""

    # Create an SVG drawing instance
    dwg = svgwrite.Drawing(size=('300px', '150px'))

    # Set up styles and background
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
    styles = """
    .title { font: bold 20px sans-serif; }
    .stat { font: normal 16px sans-serif; }
    """
    dwg.defs.add(dwg.style(styles))

    # Add title and stats
    dwg.add(dwg.text("Steam Workshop Stats", insert=(10, 30), class_='title'))
    dwg.add(dwg.text(f'Total Unique Visitors: {
            total_stats["total_unique_visitors"]}', insert=(10, 60), class_='stat'))
    dwg.add(dwg.text(f'Total Subscribers: {
            total_stats["total_current_subscribers"]}', insert=(10, 80), class_='stat'))
    dwg.add(dwg.text(f'Total Favorites: {
            total_stats["total_current_favorites"]}', insert=(10, 100), class_='stat'))

    # Return SVG content as a string
    return dwg.tostring()


def update_readme(markdown_data, start_marker, end_marker, readme_path="README.md"):
    """Updates the README.md file with the provided Markdown content within specified markers."""
    # Read the current README content
    with open(readme_path, "r", encoding="utf-8") as file:
        readme_content = file.read()

    # Find the start and end index for the section to update
    start_index = readme_content.find(start_marker) + len(start_marker)
    end_index = readme_content.find(end_marker)

    # Check if both markers are found
    if start_index == -1 or end_index == -1 or start_index >= end_index:
        print("Error: Markers not found in README.md")
        return

    # Construct the new README content with the updated section
    new_readme_content = (
        readme_content[:start_index] + "\n" +
        markdown_data + "\n" + readme_content[end_index:]
    )

    # Write the updated content back to the README file
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(new_readme_content)


def save_to_file(data, filename):
    """Save fetched data to a file in JSON format"""
    if data is not None:
        with open(filename, 'w', encoding='utf-8') as file:
            # Use json.dump to write the JSON data to the file
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    else:
        print("No data to save")


# Entry Code
if __name__ == "__main__":
    # Start the timer
    start_time = time.time()
    player_summary = get_player_summaries()
    recently_played_games = get_recently_played_games()

    USER_MARKDOWN_CONTENT = ""
    if player_summary and recently_played_games and player_summary["response"]["players"]:
        steam_player_data = player_summary["response"]["players"][0]
        processed_data = process_player_summary_data(steam_player_data)
        USER_MARKDOWN_CONTENT += generate_markdown(
            processed_data, recently_played_games)
        print("Successfully retrieved Steam User Data")
    else:
        print("Failed to fetch steam data")

    WORKSHOP_MARKDOWN_CONTENT = ""
    links = fetch_workshop_item_links(STEAM_ID)
    if links:
        workshop_data = fetch_all_workshop_stats(links)
        WORKSHOP_MARKDOWN_CONTENT = generate_svg_card(workshop_data)
        print("Retrieved all workshop stats and created svg")
    else:
        print("No workshop content was found")

    if USER_MARKDOWN_CONTENT and WORKSHOP_MARKDOWN_CONTENT:
        update_readme(USER_MARKDOWN_CONTENT,
                      "<!-- Steam-Stats start -->", "<!-- Steam-Stats end -->")
        update_readme(WORKSHOP_MARKDOWN_CONTENT,
                      "<!-- Steam-Workshop start -->", "<!-- Steam-Workshop end -->")
        print("README.md has been successfully updated.")
    else:
        print("Failed to fetch or process data")

    end_time = time.time()  # End the timer
    total_time = end_time-start_time
    total_time = round(total_time, 3)  # Total time
    print(f"Total Execution Time: {total_time} seconds")
