import json
import box
import multiprocessing
import cfscrape
import logging
import time

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

    # Processes declaration

    from processes.parser_wrapper import parser_wrapper
    from processes.cache_layer import cache_layer
    from processes.legacy_api import legacy_api

    import parsers.meta.currencies

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

    import parsers.pubg.c5game
    import parsers.pubg.lootfarm
    import parsers.pubg.opskins
    import parsers.pubg.tradeit
    

    import parsers.h1z1.c5game
    import parsers.h1z1.opskins
    import parsers.h1z1.tradeit
    

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
            'parser': parsers.meta.currencies.currencies,
        }) if conf.enabled.meta.currencies else None,


        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'csgo',
            'market': 'beefun.shop',
            'parser': parsers.csgo.beefun.beefun,
        }) if conf.enabled.csgo['beefun.shop'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
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

        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
            'game': 'pubg',
            'market': 'loot.farm',
            'parser': parsers.pubg.lootfarm.lootfarm,
        }) if conf.enabled.pubg['loot.farm'] else None,
        (parser_wrapper, {
            'storage': storage,
            'proxy': None,
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