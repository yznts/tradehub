from flask import Blueprint, render_template
import requests
import json
from collections import OrderedDict

from src.modules.config import config

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # Get cache
    r = requests.get('{0}/get'.format(config.cache_layer_address), params={
        'api_key': config.cache_layer_api_key,
        'path': ''
    })
    cache = json.loads(r.text)

    # Extract games with markets counters
    games = {}
    for game, items in cache.items():
        if game == 'meta': continue
        games[game] = {}
        for item_name, item_fields in items.items():
            for field, value in item_fields.items():
                if '|available' in field:
                    market = field.replace('|available', '')
                    if market not in games[game]: games[game][market] = 0
                    if value is True: games[game][market] += 1
    # Extract last update times
    last_updates = cache['meta']['last_updates']

    # Sort
    for game in games:
        games[game] = OrderedDict(sorted(games[game].items()))
    games = OrderedDict(sorted(games.items()))

    return render_template('index.html', games=games, last_updates=last_updates)
