import json


def csdeals(wrapper_kwargs, scraper):

    # Headers for request
    headers = {
        "X-Requested-With": "XMLHttpRequest",
		"Referer": "https://cs.deals/",
    }

    # Get data
    resp = scraper.get('https://cs.deals/ajax/botsinventory', headers=headers)
    r_items = json.loads(resp.text)['response']

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Iterate items
    for item in r_items:

        # Pass item if name is not string
        if not isinstance(item['m'], str):
            continue
        
        # Extract info
        name = item['m']
        price = item['v']
        
        # Cache update
        upd[wrapper_kwargs.get('game')][name] = {}
        upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
        upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = True
    
    return upd
