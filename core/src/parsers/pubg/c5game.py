import concurrent.futures
from bs4 import BeautifulSoup
import requests
import json
import logging
import time

# pylint: disable=E0401

import modules.nested_data
import modules.custom_log


url_template = "https://www.c5game.com/market.html?appid=578080&sort=price.desc&page={0}"

def c5game(wrapper_kwargs, scraper):

    # upd obj for cache
    upd = {wrapper_kwargs.get('game'): {}}

    # Update local CNY rate
    wrapper_kwargs['CNY'] = json.loads(requests.get(
        'http://{0}:{1}/get'.format(
            wrapper_kwargs.get('storage').conf.cl_host,
            wrapper_kwargs.get('storage').conf.cl_port
        ),
        params={
            'api_key': wrapper_kwargs.get('storage').conf.cl_api_key,
            'path': 'meta:currencies'
        }
    ).text).get('CNY')

    # Wait for next loop if no CNY
    if not wrapper_kwargs['CNY']:
        logging.info("No CNY")
        return upd

    # Pack scraper to wrapper kwargs for using in another threads
    wrapper_kwargs['scraper'] = scraper

    # Generate all pages links
    tt = time.time()
    pages_links = _generate_pages(wrapper_kwargs)
    modules.custom_log.info('pages links generated', game=wrapper_kwargs.get('game'), market=wrapper_kwargs.get('market'), tt=tt)
    
    # Pages processing
    with concurrent.futures.ThreadPoolExecutor(15) as tpe:
        args = zip([wrapper_kwargs]*len(pages_links), pages_links)
        for res in tpe.map(_parse_page, args):
            upd[wrapper_kwargs.get('game')] = modules.nested_data.merge(upd[wrapper_kwargs.get('game')], res)

    return upd

def _generate_pages(wrapper_kwargs):

    pages_links = []

    # Get page
    resp = wrapper_kwargs['scraper'].get(url_template.format(1), timeout=120)
    page = BeautifulSoup(resp.content, 'lxml')

    # Extract pages count
    try:
        pages_count = int(page.find('li', {'class': 'last'}).find('a').get('href').split('=')[-1])
    except:
        pages_count = 1
    
    # Generate links
    for num in range(1, pages_count+1):
        pages_links.append(url_template.format(num))
    
    return pages_links


def _parse_page(args, retries=0):
    wrapper_kwargs, link = args
    if retries > 3:
        return {}
    try:
        upd = {}

        # Get page
        res = wrapper_kwargs['scraper'].get(link, timeout=120)
        if res.status_code != 200:
            return _parse_page(args, retries=retries+1)
        page = BeautifulSoup(res.content, 'lxml')

        # Iterate items on page
        for item in page.find('div', {'class': 'tab-pane'}).find_all('li'):

            # Extract info
            name = item.find('p', {'class': 'name'}).find('span').get_text().strip()
            price = float(item.find('span', {'class': 'price'}).get_text().replace('￥', '').strip())
            direction = item['class'][0].strip()

            # Set fields
            if name not in upd:
                upd[name] = {}
            if direction == 'selling':
                upd[name]['c5game.com(sale)|price'] = price / wrapper_kwargs.get('CNY')
                upd[name]['c5game.com(sale)|available'] = True
            elif direction == 'purchaseing':
                upd[name]['c5game.com(purchase)|price'] = price / wrapper_kwargs.get('CNY')
                upd[name]['c5game.com(purchase)|available'] = True
        
        return upd

    except Exception as e:
        logging.exception(e)
        _parse_page(args, retries=retries+1)
