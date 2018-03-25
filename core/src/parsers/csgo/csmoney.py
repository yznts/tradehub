import json
import requests

items_quality = {
    "BS": "Battle-Scarred",
    "WW": "Well-Worn",
    "FT": "Field-Tested",
    "MW": "Minimal Wear",
    "FN": "Factory New",
}

def csmoney(wrapper_kwargs, scraper):
    
    # Get data
    resp = scraper.get('https://cs.money/load_bots_inventory', timeout=60)
    r_items = json.loads(resp.text)

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Iterate items
    for item in r_items:

        # Extract info
        name = item['m'] if 'e' not in item else '{0} ({1})'.format(item['m'], items_quality[item['e']])
        price = item['p']

        # Pass if overpiced
        if 'ar' in item:
            continue
        
        # Cache update
        upd[wrapper_kwargs.get('game')][name] = {}
        upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
        upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = True

    return upd