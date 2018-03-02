import multiprocessing
import json
import requests
import logging
import redis
import time


class H1z1OpskinsParserProcess(multiprocessing.Process):

    def __init__(self, config):
        multiprocessing.Process.__init__(self)
        self.config = config
        self.http = requests.session()
        rconf = self.config.redis_debug if self.config.debug else self.config.redis
        self.r_meta = redis.StrictRedis(
            host=rconf.host,
            port=rconf.port,
            db=rconf.map.meta,
            decode_responses=True
        )
        self.r_data = redis.StrictRedis(
            host=rconf.host,
            port=rconf.port,
            db=rconf.map.h1z1,
            decode_responses=True
        )

    
    def run(self):
        while True:
            try:
                start_time = time.time()

                i_list = self.r_data.keys('*')

                # Bulk for transaction
                bulk = self.r_data.pipeline()

                # Drop old
                for name in self.r_data.keys('*'):
                    bulk.hset(name, 'opskins-available', 0)

                # Request new data
                resp = self.http.get('https://api.opskins.com/IPricing/GetAllLowestListPrices/v1?appid=433850')
                items = json.loads(resp.text)['response']

                # Pass if no items
                if len(items) == 0:
                    logging.info('CSGO opskins zero length')
                    time.sleep(self.config.delays.error)
                
                # Iterate items
                for name, info in items.items():
                    # Pass if not in full list
                    if name not in i_list:
                        continue
                    # Update info
                    bulk.hset(name, 'opskins-price', info['price']/100)
                    bulk.hset(name, 'opskins-available', 1)
                
                # Save
                bulk.execute()

                # Write last update time
                self.r_meta.hset("last-updates", "{0}-{1}".format('h1z1', 'opskins'), int(time.time()))

                # Log
                logging.info('({0:.2f}) H1Z1 opskins updated'.format(time.time() - start_time))
                time.sleep(self.config.delays.parsers.h1z1.opskins)
                    
            except Exception as e:
                logging.info('CS:GO opskins error: {0}'.format(e))
