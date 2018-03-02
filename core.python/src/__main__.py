#!/usr/bin/python3
import json
import logging
from collections import namedtuple

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='res/log.txt',
    level=logging.DEBUG
)
logging.getLogger('requests').setLevel(logging.CRITICAL)


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
    from processes.parsers_legacy.pubg.opskins import PubgOpskinsParserProcess
    from processes.parsers_legacy.h1z1.opskins import H1z1OpskinsParserProcess

    parsers = [
        CsgoOpskinsParserProcess,
        PubgOpskinsParserProcess,
        H1z1OpskinsParserProcess
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
