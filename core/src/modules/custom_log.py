import logging
import time

def info(msg, game=None, market=None, tt=None):
    logging.info('{0:.3f} \t {1}:{2} {3}'.format(
        time.time()-tt if tt else 0,
        game,
        market,
        msg
    ))