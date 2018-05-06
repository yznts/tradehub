# pylint: disable=E0401
import json

from modules import nested_data


def tradeit(wrapper_kwargs, scraper):

    # Get data
    resp = scraper.get('https://tradeit.gg/compressedstatic')
    data = json.loads(resp.text)
    items = {}
    for bot in data:
        items = nested_data.merge(items, bot['570']['items'])

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Iterate items
    for name, info in items.items():
        # Extract info
        name = name.split('_')[1]
        price = float(info.get("p"))/100
        # Cache update
        upd[wrapper_kwargs.get('game')][name] = {}
        upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
        upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = True
    
    return upd
