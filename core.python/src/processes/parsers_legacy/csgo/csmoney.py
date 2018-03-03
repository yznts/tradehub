import multiprocessing
import cfscrape
import time
import json
import redis
import logging


class CsgoCsmoneyParserProcess(multiprocessing.Process):
    
    def __init__(self, config):
        multiprocessing.Process.__init__(self)
        self.config = config
        self.http = cfscrape.create_scraper()
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
            db=rconf.map.csgo,
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
                    bulk.hset(name, 'csmoney-available', 0)
                
                # Request new data
                resp = self.http.get('http://cs.money/load_bots_inventory')
                items = json.loads(resp.text)

                # Iterate items
                for item in items:
                    # Name fix
                    name = item['m'] if 'e' not in item else '{0} ({1})'.format(item['m'], self.items_quality[item['e']])
                    # Pass if not in full list
                    if name not in i_list:
                        continue
                    # Pass if with overprice
                    if 'ar' in item:
                        continue
                    # Update data
                    bulk.hset(name, 'csmoney-price', float(item['p']))
                    bulk.hset(name, 'csmoney-available', 1)
                
                # Save
                bulk.execute()

                # Write last update time
                self.r_meta.hset("last-updates", "{0}-{1}".format('csgo', 'csmoney'), int(time.time()))

                # Log
                logging.info('({0:.2f}) CS:GO csmoney updated'.format(time.time() - start_time))
                time.sleep(self.config.delays.parsers.csgo.opskins)

            except Exception as e:
                print(e)
