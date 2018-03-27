# pylint: disable=E1101
# pylint: disable=E0401

import bottle

from modules import nested_data


def cache_layer(**kwargs):
    cl = _CacheLayer(kwargs.get('storage'))
    cl.run()


class _CacheLayer:

    def __init__(self, storage):
        self.storage = storage
        
        self.app = bottle.Bottle()
        self.api_key = self.storage.conf.cl_api_key
        self.cache = {}

        # Settings
        bottle.Request.MEMFILE_MAX = bottle.Request.MEMFILE_MAX * 1000

        # Routes
        self.app.add_hook('before_request', self.hanlder_before)
        self.app.route('/401', 'GET', self.handler_401)
        self.app.route('/ping', 'GET', self.handler_ping)
        self.app.route('/set', 'PUT', self.handler_set)
        self.app.route('/get', 'GET', self.handler_get)

        self.app.add_hook('after_request', self.hook_cors)

    def hook_cors(self):
        """
        You need to add some headers to each request.
        Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
        """
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        bottle.response.headers['Access-Control-Allow-Headers'] = '*'
    
    def hanlder_before(self):
        if bottle.request.query.get('api_key') != self.api_key:
            bottle.request.environ['PATH_INFO'] = '/401'
    
    def handler_401(self):
        return bottle.HTTPResponse(status=401)

    def handler_ping(self):
        return 'pong'
    
    def handler_set(self):
        data = bottle.request.json
        self.cache = nested_data.merge(self.cache, data)
    
    def handler_get(self):
        try:
            if bottle.request.query.get('path'):
                return nested_data.get(self.cache, bottle.request.query.get('path').split(':')) or {}
            else:
                return self.cache
        except Exception as e:
            return {}
        

    def run(self):
        self.app.run(host=self.storage.conf.cl_host, port=self.storage.conf.cl_port)
