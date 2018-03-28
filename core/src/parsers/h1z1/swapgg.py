import json
import requests


def swapgg(wrapper_kwargs, scraper):
    
    # Get data
    data = scraper.post("https://swap.gg/api/inventory/bot", data={"refresh": "true"})
    r_items = json.loads(data.text)['result']

    # Filter
    r_items = filter(lambda x: x.get("appId") == '433850', r_items)

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Iterate items
    for item in r_items:
        
        # Extract info
        name = item['marketName']
        price = item['price'] / 100

        # Pass item if price is not number
        if not isinstance(price, (float, int)):
            continue
        
        # Cache update
        upd[wrapper_kwargs.get('game')][name] = {}
        upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
        upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = True
    
    return upd
