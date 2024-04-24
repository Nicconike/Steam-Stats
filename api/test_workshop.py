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


if __name__ == "__main__":
    links = fetch_workshop_item_links(STEAM_ID)
    workshop_data = fetch_all_workshop_stats(links)
    generate_svg_for_steam_workshop_funnel(workshop_data)
