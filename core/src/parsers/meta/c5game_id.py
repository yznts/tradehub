# pylint: disable=E0401
import requests
import concurrent.futures
import logging
from bs4 import BeautifulSoup
from modules import nested_data
import data.dota2



def c5game_id(wrapper_kwargs, scraper):
    
    # Cache update
    upd = {
        wrapper_kwargs.get('game'): {
            wrapper_kwargs.get('market'): {}
        }
    }

    # ID scrapers
    upd = nested_data.merge(upd, dota2(wrapper_kwargs, scraper))

    return upd


def dota2(wrapper_kwargs, scraper):
    game = wrapper_kwargs.get('game')
    market = wrapper_kwargs.get('market')

    # Cache update
    upd = {game: {
        market: {}
    }}

    # Parse heroes
    for hero in data.dota2.heroes:
        # Extract pages count
        resp = scraper.get(data.dota2.c5_heroes_url.format(hero, 1))
        page = BeautifulSoup(resp.text, 'lxml')
        try:
            pcount = int(page.find('li', {'class': 'last'}).find('a').get('href').split('=')[-1])
        except:
            pcount = 1

        # Parse pages with futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=36) as executor:
            futures = [
                executor.submit(lambda page_num: scraper.get(data.dota2.c5_heroes_url.format(hero, page_num)).text, page_num) 
                for page_num in range(1, pcount+1)
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    # Parse html
                    page = future.result()
                    page = BeautifulSoup(page, 'lxml')
                    
                    # Iterate items
                    for item in page.find('div', {'class': 'tab-pane'}).find_all('li'):
                        name = item.find('p', {'class': 'name'}).find('span').get_text().strip()
                        link = item.find('p', {'class': 'name'}).find('a')['href']
                        item_id = link.split('/')[-1].split('-')[0]
                        
                        # Save item id
                        upd[game][market][item_id] = name

                except Exception as e:
                    print('some exception...')

    return upd