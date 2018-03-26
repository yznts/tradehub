# pylint: disable=E1101
# pylint: disable=E0401

import cfscrape
import time
import json
import requests
import logging

from modules import custom_log


def parser_wrapper(**kwargs):

    time.sleep(0.3)
    
    storage = kwargs.get('storage')
    proxy = kwargs.get('proxy')
    game = kwargs.get('game')
    market = kwargs.get('market')
    parser = kwargs.get('parser')

    drop_av = kwargs.get('drop_av') or True
    update_cache = kwargs.get('update_cache') or True
    update_time = kwargs.get('update_time') or True
    sale_purchase = kwargs.get('sale_purchase') or False

    scraper = cfscrape.create_scraper()

    if proxy:
        scraper.proxies = {
            'http': 'http://{0}'.format(proxy),
            'https': 'https://{0}'.format(proxy),
        }
    
    while True:

        try:
            # Get upd
            tt = time.time()
            upd = parser(kwargs, scraper)
            custom_log.info('upd loaded', game=game, market=market, tt=tt)

            # Get full items list
            filist = json.loads(requests.get(
                'http://{0}:{1}/get'.format(
                    storage.conf.cl_host,
                    storage.conf.cl_port
                ),
                params={
                    'api_key': storage.conf.cl_api_key,
                    'path': game
                }
            ).text)

            # Drop items av state that not in upd
            if drop_av:

                tt = time.time()

                # For usual parsers
                if not sale_purchase:
                    # For cache items
                    for item_name in filist:
                        # Check item name in upd
                        if item_name not in upd[game]:
                            upd[game][item_name] = {}
                            upd[game][item_name]['{0}|available'.format(market)] = False

                # For sale/purchase
                else:
                    # For cache items
                    for item_name in filist:
                        # Check item name in upd
                        if item_name not in upd[game]:
                            upd[game][item_name] = {}
                            upd[game][item_name]['{0}(sale)|available'.format(market)] = False
                            upd[game][item_name]['{0}(purchase)|available'.format(market)] = False
                        # Check sale/purchase fields
                        if not upd[game][item_name].get('{0}(sale)|available'.format(market)):
                            upd[game][item_name]['{0}(sale)|available'.format(market)] = False
                        if not upd[game][item_name].get('{0}(purchase)|available'.format(market)):
                            upd[game][item_name]['{0}(purchase)|available'.format(market)] = False
            
                custom_log.info('av dropped', game=game, market=market, tt=tt)
            

            # Update server cache
            if update_cache:
                
                tt = time.time()

                requests.put(
                    'http://{0}:{1}/set'.format(
                        storage.conf.cl_host,
                        storage.conf.cl_port
                    ),
                    params={
                        'api_key': storage.conf.cl_api_key
                    },
                    json=upd
                )
                
                custom_log.info('server cache updated', game=game, market=market, tt=tt)
            

            # Update last update time
            if update_time:
                
                tt = time.time()

                if not sale_purchase:
                    lu = {
                        market: int(time.time())
                    }
                else:
                    lu = {
                        '{0}(sale)'.format(market): int(time.time()),
                        '{0}(purchase)'.format(market): int(time.time()),
                    }
                
                requests.put(
                    'http://{0}:{1}/set'.format(
                        storage.conf.cl_host,
                        storage.conf.cl_port
                    ),
                    params={
                        'api_key': storage.conf.cl_api_key
                    },
                    json={
                        'meta': {
                            'last_updates': {
                                game: lu
                            }
                        }
                    }
                )

                custom_log.info('last time updated', game=game, market=market, tt=tt)
            
            # Delay
            time.sleep(storage.conf.delays[game][market])

        except Exception as e:
            logging.exception(e)
            time.sleep(storage.conf.delays.error)
