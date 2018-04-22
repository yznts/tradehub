import json
import requests
import urllib.parse

def bitskins(wrapper_kwargs, scraper):

    # Token
    token = wrapper_kwargs['bs-token'].now()

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}
    
    # Get data
    resp = requests.get('https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key={0}&code={1}&app_id=578080'.format(
        wrapper_kwargs['bs-api-key'],
        token
    ))
    items = json.loads(resp.text)['data']['items']

    # Iterate items
    for item in items:
        name = item['market_hash_name']
        price = float(item['lowest_price'])
        av = bool(item['total_items'])

        # Cache update
        upd[wrapper_kwargs.get('game')][name] = {}
        upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
        upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = av
        upd[wrapper_kwargs.get('game')][name]['{0}|link'.format(wrapper_kwargs.get('market'))] = 'https://bitskins.com/?'+ \
            urllib.parse.urlencode({
                'market_hash_name': name,
                'appid': 578080,
                'sort_by': 'price',
                'order': 'asc'
            })

    return upd
