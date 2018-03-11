import multiprocessing
import json
import requests
import logging
import redis
import time


class H1z1TradeitParserProcess(multiprocessing.Process):

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

        self.items_quality = {
            "BS": "Battle-Scarred",
            "WW": "Well-Worn",
            "FT": "Field-Tested",
            "MW": "Minimal Wear",
            "FN": "Factory New",
        }

    def run(self):
        while True:
            try:
                start_time = time.time()

                i_list = self.r_data.keys('*')

                # Bulk for transaction
                bulk = self.r_data.pipeline()

                # Drop old
                for name in self.r_data.keys('*'):
                    bulk.hset(name, 'tradeitgg-available', 0)

                # Request new data
                resp = self.http.get('https://tradeit.gg/compressedstatic')
                data = json.loads(resp.text)
                items = data[0]['433850']['items']

                # Iterate items
                for name, info in items.items():
                    name = name.split('_')[1]
                    if name not in i_list:
                        continue
                    # Write to bulk
                    bulk.hset(name, 'tradeitgg-price', float(info.get("p"))/100)
                    bulk.hset(name, 'tradeitgg-available', 1)

                # Save
                bulk.execute()

                # Write last update time
                self.r_meta.hset("last-updates", "{0}-{1}".format('h1z1', 'tradeitgg'), int(time.time()))

                # Log
                logging.info('({0:.2f}) H1Z1 tradeit updated'.format(time.time() - start_time))
                time.sleep(self.config.delays.parsers.h1z1.tradeit)

            except Exception as e:
                logging.info('H1Z1 tradeit error: {0}'.format(e))
