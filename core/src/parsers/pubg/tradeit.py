import json

items_quality = {
    "BS": "Battle-Scarred",
    "WW": "Well-Worn",
    "FT": "Field-Tested",
    "MW": "Minimal Wear",
    "FN": "Factory New",
}

def tradeit(wrapper_kwargs, scraper):

    # Get data
    resp = scraper.get('https://tradeit.gg/compressedstatic')
    data = json.loads(resp.text)
    items = data[0]['578080']['items']

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Iterate items
    for name, info in items.items():
        # Extract info
        name = name.split('_')[1]
        if 'e' in info:
            name = '{0} ({1})'.format(name, items_quality[info['e']])
        price = float(info.get("p"))/100
        # Cache update
        upd[wrapper_kwargs.get('game')][name] = {}
        upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
        upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = True
    
    return upd
