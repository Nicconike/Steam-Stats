"""Main Runner Script"""
import os
import time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from steam_stats import get_recently_played_games
from steam_workshop import fetch_workshop_item_links, fetch_all_workshop_stats
import pygal

# Secrets Configuration
STEAM_ID = os.getenv("STEAM_CUSTOM_ID")


def generate_svg_for_recently_played_games(player_data):
    """Generate SVG for Recently Played Games in Steam in the last 2 weeks"""
    bar_chart = pygal.HorizontalBar(
        legend_at_bottom=True, rounded_bars=15, explicit_size=True, width=800, height=400)
    bar_chart.title = "Playtime in the Last Two Weeks (hours)"

    # Add data to the chart
    if player_data and "response" in player_data and "games" in player_data["response"]:
        for game in player_data["response"]["games"]:
            if "name" in game and "playtime_2weeks" in game:
                playtime_minutes = game["playtime_2weeks"]
                playtime_hours = playtime_minutes / 60  # for plotting

                # Determine the label based on the original playtime in minutes
                if playtime_minutes >= 60:
                    # Display in hours if 60 mins or more
                    label = f"{game["name"]} ({playtime_hours:.2f} hrs)"
                else:
                    # Display in minutes if less than 60
                    label = f"{game["name"]} ({playtime_minutes} mins)"

                # Add to chart using the hours value for consistency in scaling
                bar_chart.add(label, playtime_hours)
    else:
        print("No game data available to display")

    # Render the chart to an SVG file
    bar_chart.render_to_file("assets/recently_played_games.svg")

    return "![Steam Games Stats](https://github.com/Nicconike/Steam-Stats/blob/master/assets/recently_played_games.svg?sanitize=true)"


def generate_svg_for_steam_workshop(workshop_stats):
    """Generates SVG Card for retrieved Workshop Data using Plotly for table creation"""
    # Create the table data
    header_values = ["Workshop Stats", "Total"]
    data = {
        "Workshop_Stats": ["Unique Visitors", "Current Subscribers", "Current Favorites"],
        "Total": [
            workshop_stats["total_unique_visitors"],
            workshop_stats["total_current_subscribers"],
            workshop_stats["total_current_favorites"]
        ]
    }
    df = pd.DataFrame(data)
    # Generate random colors for each row
    colors = [f'rgb({np.random.randint(0, 256)}, {np.random.randint(0, 256)}, {
        np.random.randint(0, 256)})' for _ in range(len(df))]

    # Create the table figure
    fig = go.Figure(data=[go.Table(
        header=dict(values=header_values, line_color="paleturquoise",
                    fill_color="paleturquoise", align="center", font=dict(color='black', size=16)),
        cells=dict(values=[df[col].tolist() for col in df.columns],
                   line_color=[colors],
                   fill_color=[colors],
                   align="center",
                   font=dict(color='black', size=14)))
    ])
    # Adjust layout to fit the table size
    fig.update_layout(
        # Set all the margins to 0
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=True
    )
    fig.write_image("assets/steam_workshop_stats.svg")

    return "![Steam Games Stats](https://github.com/Nicconike/Steam-Stats/blob/master/assets/steam_workshop_stats.svg?sanitize=true)"


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


# Entry Code
if __name__ == "__main__":
    # Start the timer
    start_time = time.time()
    recently_played_games = get_recently_played_games()
    links = fetch_workshop_item_links(STEAM_ID)

    USER_MARKDOWN_CONTENT = ""
    if recently_played_games:
        USER_MARKDOWN_CONTENT += generate_svg_for_recently_played_games(
            recently_played_games)
        print("Successfully retrieved Steam User Data")
    else:
        print("Failed to fetch Steam data for Recently Played Games")

    WORKSHOP_MARKDOWN_CONTENT = ""
    if links:
        workshop_data = fetch_all_workshop_stats(links)
        WORKSHOP_MARKDOWN_CONTENT += generate_svg_for_steam_workshop(
            workshop_data)
        print("Retrieved all Workshop Stats")
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
