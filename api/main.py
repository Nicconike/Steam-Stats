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

# Secrets Configuration
STEAM_ID = os.getenv("STEAM_CUSTOM_ID")

# Verify that the environment variables are loaded correctly
if not STEAM_ID:
    raise ValueError(
        "Missing STEAM_ID in environment variables")


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
    player_summary = get_player_summaries()
    recently_played_games = get_recently_played_games()
    links = fetch_workshop_item_links(STEAM_ID)

    USER_MARKDOWN_CONTENT = ""
    if player_summary and recently_played_games:
        summary_content = generate_card_for_player_summary(player_summary)
        recent_games = generate_card_for_played_games(
            recently_played_games)

        if summary_content and recent_games:
            USER_MARKDOWN_CONTENT += summary_content
            USER_MARKDOWN_CONTENT += recent_games
            print("Successfully retrieved Steam User Data")
        else:
            print(
                "Failed to generate HTML content for Steam Summary or Recently Played Games")
    else:
        print("Failed to fetch Steam Summary & Games Data")

    WORKSHOP_MARKDOWN_CONTENT = ""
    if links:
        workshop_data = fetch_all_workshop_stats(links)
        WORKSHOP_MARKDOWN_CONTENT += generate_card_for_steam_workshop(
            workshop_data)
        print("Retrieved all Workshop Stats")
    else:
        print("No workshop content was found")

    if USER_MARKDOWN_CONTENT and WORKSHOP_MARKDOWN_CONTENT:
        update_readme(USER_MARKDOWN_CONTENT,
                      "<!-- Steam-Stats start -->", "<!-- Steam-Stats end -->")
        update_readme(WORKSHOP_MARKDOWN_CONTENT,
                      "<!-- Steam-Workshop start -->", "<!-- Steam-Workshop end -->")
        print("README.md has been successfully updated")
    else:
        print("Failed to fetch or process data")

    end_time = time.time()  # End the timer
    total_time = end_time-start_time
    total_time = round(total_time, 3)  # Total time
    print(f"Total Execution Time: {total_time} seconds")
