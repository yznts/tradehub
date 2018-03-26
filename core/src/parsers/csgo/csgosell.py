import json
import requests


def csgosell(wrapper_kwargs, scraper):
    
    # Get data
    data = scraper.post("https://csgosell.com/phpLoaders/forceBotUpdate/all.txt", data={
        "stage": "botAll",
        "steamId": 76561198364873979,
        "hasBonus": False,
        "coins": 0
    })
    r_items = json.loads(data.text)

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Iterate items
    for item in r_items:
        
        # Extract info
        name = item['h']
        price = item['p']
        
        # Cache update
        upd[wrapper_kwargs.get('game')][name] = {}
        upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
        upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = True
    
    return upd
