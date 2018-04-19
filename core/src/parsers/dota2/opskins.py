import json


def opskins(wrapper_kwargs, scraper):

    # Get data
    resp = scraper.get('https://api.opskins.com/IPricing/GetAllLowestListPrices/v1?appid=570')
    r_items = json.loads(resp.text)['response']

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Iterate items
    for name, info in r_items.items():
        
        # Extract info
        price = info['price']/100
        
        # Cache update
        upd[wrapper_kwargs.get('game')][name] = {}
        upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
        upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = True
    
    return upd
