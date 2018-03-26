import json
import requests


def skinsjar(wrapper_kwargs, scraper):
    
    # Get data
    data = scraper.get('https://skinsjar.com/api/v3/load/bots?refresh=1&v=0')
    r_items = json.loads(data.text)['items']

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Iterate items
    for item in r_items:
        
        # Extract info
        name = item['name']
        price = item['price']

        # Pass item if price is not number
        if not isinstance(price, (float, int)):
            continue
        
        # Cache update
        upd[wrapper_kwargs.get('game')][name] = {}
        upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
        upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = True
    
    return upd
