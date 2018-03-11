#!/usr/bin/python3
import json
import logging
from collections import namedtuple

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='res/log.txt',
    level=logging.DEBUG
)


if __name__ == '__main__':

    logging.info('Start')
    

    # -------------------------
    # Config
    # -------------------------

    with open('res/config.json') as f:
        config = json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    


    # -------------------------
    # Parsers
    # -------------------------

    from processes.parsers_legacy.csgo.opskins import CsgoOpskinsParserProcess
    from processes.parsers_legacy.csgo.csmoney import CsgoCsmoneyParserProcess
    from processes.parsers_legacy.csgo.tradeit import CsgoTradeitParserProcess
    from processes.parsers_legacy.pubg.opskins import PubgOpskinsParserProcess
    from processes.parsers_legacy.pubg.tradeit import PubgTradeitParserProcess
    from processes.parsers_legacy.h1z1.opskins import H1z1OpskinsParserProcess
    from processes.parsers_legacy.h1z1.tradeit import H1z1TradeitParserProcess

    parsers = [
        CsgoOpskinsParserProcess,
        CsgoCsmoneyParserProcess,
        CsgoTradeitParserProcess,
        PubgOpskinsParserProcess,
        PubgTradeitParserProcess,
        H1z1OpskinsParserProcess,
        H1z1TradeitParserProcess,
    ]



    # -------------------------
    # Run
    # -------------------------

    processes = []
    for parser in parsers:
        proc = parser(config)
        proc.start()
        processes.append(proc)
    for p in processes:
        p.join()
