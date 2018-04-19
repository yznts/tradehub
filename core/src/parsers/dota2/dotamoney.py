import json
import requests

def dotamoney(wrapper_kwargs, scraper):
    
    # Get data
    resp = scraper.get('http://dota.money/load_all_bots_inventory', timeout=60)
    resp = json.loads(resp.text)

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Iterate bots
    for _, items in resp.items():
        for item in items:
            name = item['m']
            price = item['p']

            # Cache update
            upd[wrapper_kwargs.get('game')][name] = {}
            upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
            upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = True

    return upd
