import requests
import json


def beefun(wrapper_kwargs, scraper):

    # Get data
    resp = scraper.post(
        'https://beefun.shop/api/graphql',
        json={
            'query': '{ robots { id name csgoInventory { id asset { id assetid ownerId class { id name nameColor marketHashName iconUrl inspectId stattrak type exterior nameTag stickers { name iconUrl __typename } allowTradeNumber __typename } paint { id index wear __typename } priceForRobot __typename } reserved __typename } __typename } }',
            'variables': {},
            'operationName': None
        },
        timeout=60
    )
    data = json.loads(resp.text)
    data = data["data"]
    robots = data["robots"]
    
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

    # Cache update
    upd = {wrapper_kwargs.get('game'): {}}
    
    # Iterate bots
    for robot in robots:
        inv = robot["csgoInventory"]
        # Iterate items
        for item in inv:
            # Extract data
            name = item["asset"]["class"]["marketHashName"]
            price = (float(item["asset"]["priceForRobot"])/100) / CNY
            # Cache update
            upd[wrapper_kwargs.get('game')][name] = {}
            upd[wrapper_kwargs.get('game')][name]['{0}|price'.format(wrapper_kwargs.get('market'))] = price
            upd[wrapper_kwargs.get('game')][name]['{0}|available'.format(wrapper_kwargs.get('market'))] = True
    
    return upd