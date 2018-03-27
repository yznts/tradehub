# pylint: disable=E1136
# pylint: disable=E1101

import multiprocessing
import bottle
import requests
import json
import logging


def legacy_api(**kwargs):
    la = _LegacyAPI(kwargs.get('storage'))
    la.run()



# For making fields compatible with old codenames
legacy_codenames = {
    'csgo': {
        'cs.money': 'csmoney',
        'loot.farm': 'lootfarm',
        'cs.deals': 'csdeals',
        'opskins.com': 'opskins',
        'beefun.shop': 'beefun',
        'tradeit.gg': 'tradeitgg',
        'csgosell.com': 'csgosell',
        'skinsjar.com': 'skinsjar',
        'swap.gg': 'swapgg',
        'tradeskinsfast.com': 'tradeskinsfast',
        'c5game.com(sale)': 'c5game-s',
        'c5game.com(purchase)': 'c5game-p'
    },
    'pubg': {
        'opskins.com': 'opskins',
        'tradeit.gg': 'tradeitgg',
        'loot.farm': 'lootfarm',
        'c5game.com(sale)': 'c5game-s',
        'c5game.com(purchase)': 'c5game-p'
    },
    'h1z1': {
        'c5game.com(sale)': 'c5game-s',
        'c5game.com(purchase)': 'c5game-p',
        'opskins.com': 'opskins',
        'tradeit.gg': 'tradeitgg'
    }
}

bottle.hook


class _LegacyAPI:

    def __init__(self, storage):
        self.storage = storage
        
        self.app = bottle.Bottle()

        self.app.add_hook('after_request', self.hook_cors)

        self.app.route('/services/games', 'GET', callback=self.handler_s_games)
        self.app.route('/services/available/<game>', 'GET', callback=self.handler_s_available)
        self.app.route('/services/items_count/<game>', 'GET', callback=self.handler_s_items_count)
        self.app.route('/services/last_updates/<game>', 'GET', callback=self.handler_s_last_updates)

        self.app.route('/currencies/<currency>', 'GET', self.hanlder_currencies)

        self.app.route('/items/all/<game>', 'GET', self.handler_items_all)

        self.app.route('/rates/all/<game>', 'GET', self.handler_rates_all)
        self.app.route('/rates/by_names/<game>', 'POST', self.handler_rates_by_names)

        self.app.route('/ping', 'GET', self.handler_ping)
        self.app.route('/version', 'GET', self.handler_ver)
        self.app.route('/test', 'POST', self.test)

    def test(self):
        return 'test'

    def hook_cors(self):
        """
        You need to add some headers to each request.
        Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
        """
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        bottle.response.headers['Access-Control-Allow-Headers'] = '*'

    def handler_s_games(self):
        bottle.response.content_type = 'application/json'
        return json.dumps([
            'csgo',
            'pubg',
            'h1z1'
        ])
    
    def handler_s_available(self, game):
        return legacy_codenames[game]

    
    def handler_s_items_count(self, game):
        items = json.loads(requests.get(
            'http://{0}:{1}/get'.format(
                self.storage.conf.cl_host,
                self.storage.conf.cl_port,
            ),
            params={
                'api_key': self.storage.conf.cl_api_key,
                'path': game
            }
        ).text)
        resp = {}
        for name, info in items.items():
            for field in info:
                if 'available' in field and info[field]:
                    if not field.split('|')[0] in resp:
                        resp[field.split('|')[0]] = 0
                    resp[field.split('|')[0]] += 1
        return resp
        
    
    def handler_s_last_updates(self, game):
        bottle.response.content_type = 'application/json'
        return requests.get(
            'http://{0}:{1}/get'.format(
                self.storage.conf.cl_host,
                self.storage.conf.cl_port,
            ),
            params={
                'api_key': self.storage.conf.cl_api_key,
                'path': 'meta:last_updates:{0}'.format(game)
            }
        ).text
    
    
    def hanlder_currencies(self, currency):
        currencies = json.loads(requests.get(
            'http://{0}:{1}/get'.format(
                self.storage.conf.cl_host,
                self.storage.conf.cl_port,
            ),
            params={
                'api_key': self.storage.conf.cl_api_key,
                'path': 'meta:currencies'
            }
        ).text)
        return str(currencies.get(currency))
    

    def handler_items_all(self, game):
        items = json.loads(requests.get(
            'http://{0}:{1}/get'.format(
                self.storage.conf.cl_host,
                self.storage.conf.cl_port,
            ),
            params={
                'api_key': self.storage.conf.cl_api_key,
                'path': game
            }
        ).text)
        litems = {}
        for name, info in items.items():
            litems[name] = {}
            for field in info:
                new_field = field
                for lfname, lcname in legacy_codenames[game].items():
                    if lfname in new_field:
                        new_field = new_field.replace(lfname, lcname)
                        break
                new_field = new_field.replace('|', '-')
                litems[name][new_field] = items[name][field]
        return litems
    

    def handler_rates_all(self, game):
        s1_name = bottle.request.query["s1_name"]
        s2_name = bottle.request.query["s2_name"]
        s1_commission = bottle.request.query["s1_commission"]
        s2_commission = bottle.request.query["s2_commission"]

        resp = {}
        
        s1_commission = 1-(float(s1_commission)/100)
        s2_commission = 1-(float(s2_commission)/100)

        items = json.loads(requests.get(
            'http://{0}:{1}/get'.format(
                self.storage.conf.cl_host,
                self.storage.conf.cl_port,
            ),
            params={
                'api_key': self.storage.conf.cl_api_key,
                'path': game
            }
        ).text)

        for name, info in items.items():
            s1_av = info.get('{0}|available'.format(s1_name))
            s2_av = info.get('{0}|available'.format(s2_name))

            s1_price = info.get('{0}|price'.format(s1_name))
            s2_price = info.get('{0}|price'.format(s2_name))

            if s1_price:
                s1_price = float(s1_price)
                s1_price_after_commission = s1_price * s1_commission
            else:
                s1_price = 0
                s1_price_after_commission = 0
            
            if s2_price:
                s2_price = float(s2_price)
                s2_price_after_commission = s2_price * s2_commission
            else:
                s2_price = 0
                s2_price_after_commission = 0
            
            resp[name] = {
                "s1-av": s1_av,
                "s2-av": s2_av,
                "s1-price": s1_price,
                "s2-price": s2_price,
                "s1-s2-rate": 100-((s1_price/s2_price_after_commission)*100) if s1_price and s2_price else 0,
                "s2-s1-rate": ((s1_price_after_commission/s2_price)*100)-100 if s1_price and s2_price else 0
            }
        
        return resp



    
    def handler_rates_by_names(self, game):
        s1_name = bottle.request.forms.get("s1_name")
        s2_name = bottle.request.forms.get("s2_name")
        s1_commission = bottle.request.forms.get("s1_commission")
        s2_commission = bottle.request.forms.get("s2_commission")
        names = bottle.request.forms.get("names")
        # Fix JS issues
        names = names.replace("â", "★")
        names = names.replace("â¢", "™")
        # Format
        names = names.split(",")

        resp = {}
        
        s1_commission = 1-(float(s1_commission)/100)
        s2_commission = 1-(float(s2_commission)/100)

        items = json.loads(requests.get(
            'http://{0}:{1}/get'.format(
                self.storage.conf.cl_host,
                self.storage.conf.cl_port,
            ),
            params={
                'api_key': self.storage.conf.cl_api_key,
                'path': game
            }
        ).text)

        for name in names:
            info = items.get(name)
            if not info:
                continue

            s1_av = info.get('{0}|available'.format(s1_name))
            s2_av = info.get('{0}|available'.format(s2_name))

            s1_price = info.get('{0}|price'.format(s1_name))
            s2_price = info.get('{0}|price'.format(s2_name))

            if s1_price:
                s1_price = float(s1_price)
                s1_price_after_commission = s1_price * s1_commission
            else:
                s1_price = 0
                s1_price_after_commission = 0
            
            if s2_price:
                s2_price = float(s2_price)
                s2_price_after_commission = s2_price * s2_commission
            else:
                s2_price = 0
                s2_price_after_commission = 0
            
            resp[name] = {
                "s1-av": s1_av,
                "s2-av": s2_av,
                "s1-price": s1_price,
                "s2-price": s2_price,
                "s1-s2-rate": 100-((s1_price/s2_price_after_commission)*100) if s1_price and s2_price else 0,
                "s2-s1-rate": ((s1_price_after_commission/s2_price)*100)-100 if s1_price and s2_price else 0
            }
        
        print(resp)
        
        return resp

    

    def handler_ver(self):
        return 'legacy'

    def handler_ping(self):
        return 'pong'

    def run(self):
        self.app.run(host=self.storage.conf.legacy_api_host, port=self.storage.conf.legacy_api_port)