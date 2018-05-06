from data import dota2
import json
import requests
import logging


data_url = 'https://open.c5game.com/v1/store'
item_url = 'https://www.c5game.com/dota/{0}-{1}.html'
base_params = {
    'appid': 570,
    'limit': 1000,
    'page': 1,
    'sort': 'price',
    'only': 0,
}


def c5game(wrapper_kwargs, scraper):

    sp = {
        'S': '{0}(sale)'.format(wrapper_kwargs.get('market')),
        'P': '{0}(purchase)'.format(wrapper_kwargs.get('market'))
    }
    
    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}

    # Get CNY rate
    CNY = json.loads(requests.get(
        'http://{0}:{1}/get'.format(
            wrapper_kwargs.get('storage').conf.cl_host,
            wrapper_kwargs.get('storage').conf.cl_port
        ),
        params={
            'api_key': wrapper_kwargs.get('storage').conf.cl_api_key,
            'path': 'meta:currencies'
        }
    ).text).get('CNY')

    # c5game ids
    c5game_id_name = json.loads(requests.get(
        'http://{0}:{1}/get'.format(
            wrapper_kwargs.get('storage').conf.cl_host,
            wrapper_kwargs.get('storage').conf.cl_port
        ),
        params={
            'api_key': wrapper_kwargs.get('storage').conf.cl_api_key,
            'path': 'meta:c5game.com(id)'
        }
    ).text)

    # Return if needed params not exists yet
    if not CNY or not c5game_id_name:
        raise Exception('One of needed params is None')


    # Parse by heroes
    for hero in dota2.heroes:
        try:
            resp = scraper.get(data_url, params={**base_params, **{
                'hero': hero
            }})
            items = json.loads(resp.text)
            items = items.get('data')
            items = items.get('list')
        except Exception as e:
            pass
        
        if not items:
            continue
            
        for item in items:
            # Extract params
            name = c5game_id_name.get(str(item.get('item_id')))
            price = float(item.get('price')) / CNY
            # Pass if id not parsed
            if not name:
                continue
            
            # Init dict for item
            if name not in upd[wrapper_kwargs.get('game')]:
                upd[wrapper_kwargs.get('game')][name] = {}
            # Write price and av state
            upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(sp[item.get('product_type')])] = price
            upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(sp[item.get('product_type')])] = True
            upd[wrapper_kwargs.get('game')][name]['{0}|link'.format(sp[item.get('product_type')])] = item_url.format(
                item.get('item_id'),
                item.get('product_type')
            )

    return upd
