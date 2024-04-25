import json
from steam_workshop import fetch_workshop_item_links, fetch_all_workshop_stats
from main import STEAM_ID
import pygal


def generate_svg_for_steam_workshop(total_stats):
    """Generates SVG Card for retrieved Workshop Data using Pygal Radar Chart"""
    # Create a Radar chart instance
    radar_chart = pygal.Radar(
        fill=True, show_legend=True, legend_at_bottom=True)
    radar_chart.title = 'Steam Workshop Stats'

    # Define the fields and their respective values

    # Set the labels for the axes
    radar_chart.x_labels = ['Total Favorites',
                            'Total Subscribers', 'Total Unique Visitors']

    # Add data to the radar chart
    radar_chart.add('Total Favorites', total_stats["total_current_favorites"])
    radar_chart.add('Total Subscribers',
                    total_stats["total_current_subscribers"])
    radar_chart.add('Total Unique Visitors',
                    total_stats["total_unique_visitors"])

    # Render the chart to an SVG file
    radar_chart.render_to_file('steam_workshop_stats.svg')

    # Optionally, return the SVG data as a string to embed directly in HTML or Markdown
    return radar_chart.render(is_unicode=True)


def generate_svg_for_steam_workshop_funnel(total_stats):
    """Generates SVG Card for retrieved Workshop Data using Pygal Funnel Chart"""
    # Create a Funnel chart instance
    funnel_chart = pygal.Funnel(legend_at_bottom=True)
    funnel_chart.title = 'Steam Workshop Stats'

    # funnel_chart.x_labels = ['Total Favorites','Total Subscribers', 'Total Unique Visitors']

    # Add data to the radar chart
    funnel_chart.add('Total Subscribers',
                     total_stats["total_current_subscribers"])
    funnel_chart.add('Total Favorites', total_stats["total_current_favorites"])
    funnel_chart.add('Total Unique Visitors',
                     total_stats["total_unique_visitors"])

    # Render the chart to an SVG file
    funnel_chart.render_to_file('steam_workshop_stats.svg')

    # Optionally, return the SVG data as a string to embed directly in HTML or Markdown
    return funnel_chart.render(is_unicode=True)


def generate_svg_for_steam_workshop_pyramid(total_stats):
    """Generates SVG Card for retrieved Workshop Data using Pygal Pyramid Chart"""
    # Create a Pyramid chart instance
    pyramid_chart = pygal.Pyramid(
        legend_at_bottom=True, explicit_size=True, human_readable=True)
    pyramid_chart.title = 'Steam Workshop Stats'

    # Add data to the pyramid chart
    pyramid_chart.add('Total Subscribers',
                      total_stats["total_current_subscribers"])
    pyramid_chart.add('Total Favorites',
                      total_stats["total_current_favorites"])
    pyramid_chart.add('Total Unique Visitors',
                      total_stats["total_unique_visitors"])

    # Render the chart to an SVG file
    pyramid_chart.render_to_file("../assets/steam_workshop_stats.svg")

    return pyramid_chart.render(is_unicode=True)


def generate_svg_for_steam_workshop_pie(total_stats):
    """Generates SVG Card for retrieved Workshop Data using Pygal Multi-series Pie Chart"""
    # Create a multi-series pie chart instance
    pie_chart = pygal.Pie(legend_at_bottom=True)
    pie_chart.title = "Steam Workshop Stats"

    # Extract all element values from individual_stats and add them as a series
    unique_visitors = [stat['unique_visitors']
                       for stat in total_stats['individual_stats']]
    current_subscribers = [stat['current_subscribers']
                           for stat in total_stats['individual_stats']]
    current_favorites = [stat['current_favorites']
                         for stat in total_stats['individual_stats']]

    pie_chart.add("Subscribers", current_subscribers)
    pie_chart.add("Unique Visitors", unique_visitors)
    pie_chart.add("Favorites", current_favorites)

    # Render the chart to an SVG file
    pie_chart.render_to_file("../assets/steam_workshop_stats.svg")

    # Return the SVG data as a string to embed directly in Markdown
    return pie_chart.render(is_unicode=True)


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
    links = fetch_workshop_item_links(STEAM_ID)
    workshop_data = fetch_all_workshop_stats(links)
    generate_svg_for_steam_workshop_pie(workshop_data)
