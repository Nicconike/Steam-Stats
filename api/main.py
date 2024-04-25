"""Main Runner Script"""
import os
import time
from steam_stats import get_recently_played_games
from steam_workshop import fetch_workshop_item_links, fetch_all_workshop_stats
import pygal

# Secrets Configuration
STEAM_ID = os.getenv("STEAM_CUSTOM_ID")

# def generate_markdown(summary_data, recently_played_data):
#     """Generate combined Markdown content for player data, achievements, recently played games"""

#     # Generate Steam User Summary Markdown
#     personastate_str = summary_data["personastate"]
#     summary_markdown = f"""
# ## Steam User Summary for {summary_data["personaname"]}

# - **Steam Status:** {personastate_str}
# - **Last Logoff (IST):** {summary_data["lastlogoff"]}
# - **Profile URL:** [Visit Profile]({summary_data["profileurl"]})
# - **Avatar:** ![Avatar]({summary_data["avatarmedium"]})
# """

#     # Add game status if the user is in-game
#     if "gameid" in summary_data and summary_data["gameid"]:
#         summary_markdown += f"\n- **Currently In-Game:** {
#             summary_data["gameid"]}"

#     # Generate Recently Played Games Markdown
#     total_count = recently_played_data["response"]["total_count"]
#     games_markdown = f"## Recently Played Games (Total: {total_count})\n"
#     for game in recently_played_data["response"]["games"]:
#         playtime_2weeks = game["playtime_2weeks"]
#         playtime_forever = game["playtime_forever"]

#         # Format playtime for the last 2 weeks
#         if playtime_2weeks >= 60:
#             playtime_2weeks_hours = playtime_2weeks // 60
#             playtime_2weeks_minutes = playtime_2weeks % 60
#             playtime_2weeks_str = f"{playtime_2weeks_hours} hrs {
#                 playtime_2weeks_minutes} mins"
#         else:
#             playtime_2weeks_str = f"{playtime_2weeks} mins"

#         # Format total playtime
#         if playtime_forever >= 60:
#             playtime_forever_hours = playtime_forever // 60
#             playtime_forever_minutes = playtime_forever % 60
#             playtime_forever_str = f"{playtime_forever_hours} hrs {
#                 playtime_forever_minutes} mins"
#         else:
#             playtime_forever_str = f"{playtime_forever} mins"

#         games_markdown += f"- {game["name"]}: Playtime last 2 weeks: {
#             playtime_2weeks_str}, Total playtime: {playtime_forever_str}\n"

#     # Combine all Markdown sections
#     combined_markdown = summary_markdown + "\n" + games_markdown
#     return combined_markdown


# def generate_svg_for_steam_summary(player_data):
#     """Generates SVG Card for retrieved Steam Summary Data"""
#     # Create an SVG drawing instance
#     dwg = svgwrite.Drawing(size=('500px', '150px'), profile='full')

#     # Set up styles
#     styles = """
#     .header { font: bold 16px sans-serif; fill: #333; }
#     .info { font: 12px sans-serif; fill: #666; }
#     """
#     dwg.defs.add(dwg.style(styles))

#     # Add background
#     dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))

#     # Add avatar image on the left side
#     if 'avatarmedium' in player_data:
#         dwg.add(dwg.image(player_data['avatarmedium'], insert=(
#             10, 10), size=('100px', '100px')))

#     # Add personaname and hyperlink to profileurl
#     if 'personaname' in player_data and 'profileurl' in player_data:
#         link = dwg.add(dwg.a(href=player_data['profileurl']))
#         link.add(dwg.text(player_data['personaname'], insert=(
#             '120px', '30px'), class_='header'))

#     # Add personastate and gameextrainfo on the right side
#     personastate_text = PERSONASTATE_MAPPING.get(
#         player_data.get('personastate', 0), "Unknown")
#     dwg.add(dwg.text(f"State: {personastate_text}",
#             insert=('120px', '60px'), class_='info'))

#     if 'gameextrainfo' in player_data:
#         dwg.add(dwg.text(f"Playing: {player_data['gameextrainfo']}", insert=(
#             '120px', '80px'), class_='info'))

#     # Return SVG content as a string
#     return dwg.tostring()

def generate_svg_for_recently_played_games(player_data):
    """Generate SVG for Recently Played Games in Steam in the last 2 weeks"""
    bar_chart = pygal.HorizontalBar(
        legend_at_bottom=True, rounded_bars=15, explicit_size=True)
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
    # bar_chart.render_to_file("assets/recently_played_games.svg")

    return bar_chart.render(is_unicode=True)


def generate_svg_for_steam_workshop(total_stats):
    """Generates SVG Card for retrieved Workshop Data using Pygal Multi-series Pie Chart"""
    # Create a multi-series pie chart instance
    pie_chart = pygal.Pie(legend_at_bottom=True, explicit_size=True)
    pie_chart.title = "Steam Workshop Stats"

    # Extract all element values from individual_stats and add them as a series
    unique_visitors = [stat["unique_visitors"]
                       for stat in total_stats["individual_stats"]]
    current_subscribers = [stat["current_subscribers"]
                           for stat in total_stats["individual_stats"]]
    current_favorites = [stat["current_favorites"]
                         for stat in total_stats["individual_stats"]]

    pie_chart.add("Subscribers", current_subscribers)
    pie_chart.add("Unique Visitors", unique_visitors)
    pie_chart.add("Favorites", current_favorites)

    # Render the chart to an SVG file
    # pie_chart.render_to_file("assets/steam_workshop_stats.svg")

    # Return the SVG data as a string to embed directly in Markdown
    return pie_chart.render(is_unicode=True)


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
        print("Failed to fetch steam data")

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
