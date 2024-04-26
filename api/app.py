"""Flask Application"""
from flask import Flask, jsonify
from steam_stats import get_player_summaries, get_recently_played_games
from steam_workshop import fetch_workshop_item_links, fetch_all_workshop_stats
app = Flask(__name__)


@app.route("/player-summaries")
def player_summaries():
    """Endpoint to fetch player summaries"""
    data = get_player_summaries()
    return jsonify(data)


@app.route("/recently-played-games")
def recently_played_games():
    """Endpoint to fetch recently played games"""
    data = get_recently_played_games()
    return jsonify(data)


@app.route("/workshop-stats/<steam_id>")
def workshop_stats(steam_id):
    """Endpoint to fetch workshop stats for a given Steam ID"""
    links = fetch_workshop_item_links(steam_id)
    data = fetch_all_workshop_stats(links)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
