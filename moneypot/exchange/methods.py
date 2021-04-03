""" Methods to access the API programmatically """
from urllib import request
import json

import moneypot
    
EXCHANGE_PORT = moneypot.config['exchange']['port'] 

def get_stocks_list():
    """ Return a list of all stocks """
    url = f"http://localhost:{EXCHANGE_PORT}/stock/"
    response = _get_url_response(url)
    return response


def _get_url_response(url):
    """ Load a generic URL response json """
    req = request.urlopen(url)
    response = json.loads(req.read())
    return response


if __name__ == '__main__':
    stocks = get_stocks_list()