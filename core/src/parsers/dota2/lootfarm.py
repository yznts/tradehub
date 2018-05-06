import json


def lootfarm(wrapper_kwargs, scraper):
    
    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Get data
    resp = scraper.get('https://loot.farm/fullpriceDOTA.json')
    r_items = json.loads(resp.text)

    # Iterate items
    for item in r_items:
        
        # Extract info
        name = item['name']
        price = item['price']/100
        av = bool(item['have'])
        
        # Cache update
        upd[wrapper_kwargs.get('game')][name] = {}
        upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
        upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = av
    
    return upd
