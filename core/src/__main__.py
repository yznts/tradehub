import json
import box
import multiprocessing
import logging
import time
import pyotp


# Config logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='res/log.txt',
    level=logging.INFO,
    filemode='w'
)
logging.getLogger('requests').setLevel(logging.CRITICAL)


if __name__ == '__main__':

    logging.info('Start')
    
    # Load config
    with open('res/conf.json') as f:
        temp = json.load(f)
        conf = box.Box(temp['configs'][temp['conf_name']])


    # Shared info for processes
    storage = multiprocessing.Manager().dict()
    storage.conf = conf


    # Bitskins specific
    import pyotp

    bs_secret = 'SULLU4WD7RXCGPGU'
    bs_token = pyotp.TOTP(bs_secret)


    # Processes declaration

    from processes.parser_wrapper import parser_wrapper
    from processes.cache_layer import cache_layer
    from processes.legacy_api import legacy_api

    import parsers.meta.currencies
    import parsers.meta.c5game_id

    import parsers.csgo.beefun
    import parsers.csgo.c5game
    import parsers.csgo.csdeals
    import parsers.csgo.csmoney
    import parsers.csgo.lootfarm
    import parsers.csgo.opskins
    import parsers.csgo.tradeit
    import parsers.csgo.csgosell
    import parsers.csgo.skinsjar
    import parsers.csgo.swapgg
    import parsers.csgo.tradeskinsfast

    import parsers.dota2.opskins
    import parsers.dota2.dotamoney
    import parsers.dota2.bitskins
    import parsers.dota2.lootfarm
    import parsers.dota2.tradeit
    import parsers.dota2.c5game

    import parsers.pubg.c5game
    import parsers.pubg.lootfarm
    import parsers.pubg.opskins
    import parsers.pubg.tradeit
    import parsers.pubg.swapgg
    import parsers.pubg.bitskins
    

    import parsers.h1z1.c5game
    import parsers.h1z1.opskins
    import parsers.h1z1.tradeit
    import parsers.h1z1.swapgg

    procs = [

        (cache_layer, {
            'storage': storage,
        }) if conf.enabled.cl else None,
        (legacy_api, {
            'storage': storage,
        }) if conf.enabled.la else None,


        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'meta',
            'market': 'currencies',
            'drop_av': False,
            'parser': parsers.meta.currencies.currencies,
        }) if conf.enabled.meta.currencies else None,
        (parser_wrapper, {
            'storage': storage,
            'game': 'meta',
            'market': 'c5game.com(id)',
            'drop_av': False,
            'parser': parsers.meta.c5game_id.c5game_id,
            'proxy': 'Dqjyqm:aDHhft@185.232.171.109:9137',
        }) if conf.enabled.meta['c5game.com(id)'] else None,

        # ---------------------
        # CSGO
        # ---------------------

        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'beefun.shop',
            'parser': parsers.csgo.beefun.beefun,
        }) if conf.enabled.csgo['beefun.shop'] else None,
        (parser_wrapper, {
            'storage': storage,
            'game': 'csgo',
            'market': 'c5game.com',
            'parser': parsers.csgo.c5game.c5game,
            'sale_purchase': True,
            'proxy': 'Dqjyqm:aDHhft@185.232.171.109:9137',
        }) if conf.enabled.csgo['c5game.com'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'cs.deals',
            'parser': parsers.csgo.csdeals.csdeals,
        }) if conf.enabled.csgo['cs.deals'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'cs.money',
            'parser': parsers.csgo.csmoney.csmoney,
        }) if conf.enabled.csgo['cs.money'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'loot.farm',
            'parser': parsers.csgo.lootfarm.lootfarm,
        }) if conf.enabled.csgo['loot.farm'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'opskins.com',
            'parser': parsers.csgo.opskins.opskins,
        }) if conf.enabled.csgo['opskins.com'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'tradeit.gg',
            'parser': parsers.csgo.tradeit.tradeit,
        }) if conf.enabled.csgo['tradeit.gg'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'csgosell.com',
            'parser': parsers.csgo.csgosell.csgosell,
        }) if conf.enabled.csgo['csgosell.com'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'skinsjar.com',
            'parser': parsers.csgo.skinsjar.skinsjar,
        }) if conf.enabled.csgo['skinsjar.com'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'swap.gg',
            'parser': parsers.csgo.swapgg.swapgg,
        }) if conf.enabled.csgo['swap.gg'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'tradeskinsfast.com',
            'parser': parsers.csgo.tradeskinsfast.tradeskinsfast,
        }) if conf.enabled.csgo['tradeskinsfast.com'] else None,
        
        # ---------------------
        # Dota 2
        # ---------------------

        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'dota2',
            'market': 'opskins.com',
            'parser': parsers.dota2.opskins.opskins
        }) if conf.enabled.dota2['opskins.com'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'dota2',
            'market': 'dota.money',
            'parser': parsers.dota2.dotamoney.dotamoney
        }) if conf.enabled.dota2['dota.money'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'bs-token': bs_token,
            'bs-api-key': conf['bitskins-api-key'],
            'game': 'dota2',
            'market': 'bitskins.com',
            'sale_purchase': False,
            'parser': parsers.dota2.bitskins.bitskins
        }) if conf.enabled.dota2['bitskins.com'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'dota2',
            'market': 'loot.farm',
            'parser': parsers.dota2.lootfarm.lootfarm,
        }) if conf.enabled.dota2['loot.farm'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'dota2',
            'market': 'tradeit.gg',
            'parser': parsers.dota2.tradeit.tradeit,
        }) if conf.enabled.dota2['tradeit.gg'] else None,
        (parser_wrapper, {
            'storage': storage,
            'game': 'dota2',
            'market': 'c5game.com',
            'parser': parsers.dota2.c5game.c5game,
            'sale_purchase': True,
            'proxy': 'Dqjyqm:aDHhft@185.232.171.109:9137',
        }) if conf.enabled.dota2['c5game.com'] else None,


        # ---------------------
        # PUBG
        # ---------------------

        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'pubg',
            'market': 'loot.farm',
            'parser': parsers.pubg.lootfarm.lootfarm,
        }) if conf.enabled.pubg['loot.farm'] else None,
        (parser_wrapper, {
            'storage': storage,
            'game': 'pubg',
            'market': 'c5game.com',
            'parser': parsers.pubg.c5game.c5game,
            'sale_purchase': True,
            'proxy': 'Dqjyqm:aDHhft@185.232.171.109:9137',
        }) if conf.enabled.pubg['c5game.com'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'pubg',
            'market': 'opskins.com',
            'parser': parsers.pubg.opskins.opskins,
        }) if conf.enabled.pubg['opskins.com'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'pubg',
            'market': 'tradeit.gg',
            'parser': parsers.pubg.tradeit.tradeit,
        }) if conf.enabled.pubg['tradeit.gg'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'pubg',
            'market': 'swap.gg',
            'parser': parsers.pubg.swapgg.swapgg,
        }) if conf.enabled.pubg['swap.gg'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'bs-token': bs_token,
            'bs-api-key': conf['bitskins-api-key'],
            'game': 'pubg',
            'market': 'bitskins.com',
            'sale_purchase': False,
            'parser': parsers.pubg.bitskins.bitskins
        }) if conf.enabled.pubg['bitskins.com'] else None,

        # ---------------------
        # H1Z1
        # ---------------------

        (parser_wrapper, {
            'storage': storage,
            'game': 'h1z1',
            'market': 'c5game.com',
            'parser': parsers.h1z1.c5game.c5game,
            'sale_purchase': True,
            'proxy': 'Dqjyqm:aDHhft@185.232.171.109:9137',
        }) if conf.enabled.h1z1['c5game.com'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'h1z1',
            'market': 'opskins.com',
            'parser': parsers.h1z1.opskins.opskins,
        }) if conf.enabled.h1z1['opskins.com'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'h1z1',
            'market': 'tradeit.gg',
            'parser': parsers.h1z1.tradeit.tradeit,
        }) if conf.enabled.h1z1['tradeit.gg'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'h1z1',
            'market': 'swap.gg',
            'parser': parsers.h1z1.swapgg.swapgg,
        }) if conf.enabled.h1z1['swap.gg'] else None,
        
    ]

    # Start processes
    monitor = []
    for p in procs:
        if not p:
            continue
        new_process = multiprocessing.Process(target=p[0], kwargs=p[1])
        new_process.start()
        monitor.append({
            'process': new_process,
            'func': p[0],
            'kwargs': p[1]
        })
    
    # Monitor processes status
    while True:
        for i, m in enumerate(monitor):
            logging.info('STATUS {0}:{1} {2} {3}'.format(i+1, m['process'].is_alive(), m['func'].__name__, m['kwargs']))
        for i, m in enumerate(monitor):
            if not m['process'].is_alive():
                logging.error('Process died! Restarting...')
                monitor[i]['process'] = multiprocessing.Process(target=m['func'], kwargs=m['kwargs'])
                monitor[i]['process'].start()
        time.sleep(30)