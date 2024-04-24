"""Testing"""
from steam_stats import get_recently_played_games
import pygal


def generate_svg_for_recently_played_games(player_data):
    """Generate SVG for Recently Played Games in Steam in the last 2 weeks"""
    bar_chart = pygal.HorizontalBar(
        legend_at_bottom=True, rounded_bars=15, show_legend=True)
    bar_chart.title = "Playtime in the Last Two Weeks (hours)"

    # Add data to the chart
    if player_data and "response" in player_data and "games" in player_data["response"]:
        for game in player_data["response"]["games"]:
            if "name" in game and "playtime_2weeks" in game:
                playtime_minutes = game["playtime_2weeks"]
                playtime_hours = playtime_minutes / 60  # Convert minutes to hours for plotting

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

    bar_chart.render_to_file('recently_played_games.svg')

    # Optionally, return the SVG data as a string to embed directly in HTML or Markdown
    return bar_chart.render(is_unicode=True)


if __name__ == "__main__":
    steam_player_data = get_recently_played_games()
    generate_svg_for_recently_played_games(steam_player_data)
