"""Main Runner Script"""
import os
import time
from steam_stats import get_player_summaries, get_recently_played_games
from steam_workshop import fetch_workshop_item_links, fetch_all_workshop_stats
from card import (
    generate_card_for_player_summary,
    generate_card_for_played_games,
    generate_card_for_steam_workshop
)

# Required Secrets Configuration
STEAM_ID = os.environ["INPUT_STEAM_ID"]
STEAM_API_KEY = os.environ["INPUT_STEAM_API_KEY"]
STEAM_CUSTOM_ID = os.environ["INPUT_STEAM_CUSTOM_ID"]

# Optional Feature Flags
WORKSHOP_STATS = os.getenv("INPUT_WORKSHOP_STATS", "false").lower() == "true"

# Version Identifier for Changelog
__version__ = "0.1.4"


def update_readme(markdown_data, start_marker, end_marker, readme_path="README.md"):
    """Updates the README.md file with the provided Markdown content within specified markers"""
    # Read the current README content
    with open(readme_path, "r", encoding="utf-8") as file:
        readme_content = file.read()

    # Find the start and end index for the section to update
    start_index = readme_content.find(start_marker)
    if start_index == -1:
        print("Error: Start marker not found in README.md")
        return

    end_index = readme_content.find(end_marker, start_index)
    if end_index == -1:
        print("Error: End marker not found in README.md")
        return

    # Construct the new README content with the updated section
    new_readme_content = (
        readme_content[:start_index + len(start_marker)] + "\n" +
        markdown_data + "\n" + readme_content[end_index:]
    )

    # Write the updated content back to the README file
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(new_readme_content)


# Entry Code
if __name__ == "__main__":
    # Start the timer
    start_time = time.time()

    player_summary = get_player_summaries()
    recently_played_games = get_recently_played_games()
    links = fetch_workshop_item_links(STEAM_CUSTOM_ID, STEAM_API_KEY)

    USER_MARKDOWN_CONTENT = ""
    if player_summary and recently_played_games:
        summary_content = generate_card_for_player_summary(player_summary)
        recent_games = generate_card_for_played_games(
            recently_played_games)

        if summary_content and recent_games:
            USER_MARKDOWN_CONTENT += summary_content
            USER_MARKDOWN_CONTENT += recent_games
            print("Retrieved Steam User Stats")
        else:
            print(
                "Failed to generate card data for Steam Summary & Recently Played Games")

        if USER_MARKDOWN_CONTENT:
            update_readme(USER_MARKDOWN_CONTENT,
                          "<!-- Steam-Stats start -->", "<!-- Steam-Stats end -->")
            print("README.md has been successfully updated with Steam Stats")
        else:
            print("Failed to update README with latest Steam Stats")
    else:
        print("Failed to fetch Steam User Summary & Games Data")

    if WORKSHOP_STATS is True:
        WORKSHOP_MARKDOWN_CONTENT = ""
        if links:
            workshop_data = fetch_all_workshop_stats(links)
            WORKSHOP_MARKDOWN_CONTENT += generate_card_for_steam_workshop(
                workshop_data)
            print("Retrieved Workshop Stats")
            if WORKSHOP_MARKDOWN_CONTENT:
                update_readme(WORKSHOP_MARKDOWN_CONTENT,
                              "<!-- Steam-Workshop start -->", "<!-- Steam-Workshop end -->")
                print("README.md has been successfully updated with Workshop Stats")
        else:
            print("No workshop content was found")

    end_time = time.time()  # End the timer
    total_time = round(end_time-start_time, 3)  # Total time
    if total_time > 60:
        minutes = total_time // 60
        seconds = total_time % 60
        print("Total Execution Time: " + str(int(minutes)) +
              " minutes and " + str(seconds) + " seconds")
    else:
        print("Total Execution Time: " + str(total_time) + " seconds")
