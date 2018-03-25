import requests
from fixerio import Fixerio


def currencies(wrapper_kwargs, scraper):
    
    # Get data
    f = Fixerio(base='USD')
    upd = {
        'meta': {
            'currencies': f.latest().get('rates')
        }
    }

    # Save data
    return upd
