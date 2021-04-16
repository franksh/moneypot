""" Methods to access the API programmatically """
from urllib import request
import json

import moneypot
from moneypot.exchange import Session
    
EXCHANGE_PORT = moneypot.config['exchange']['port'] 

def get_stocks_list(format=None):
    """ Return a list of all stocks 
    
    Parameters:
    -----------
     - format: str
        - 'dict': as dict
        - 'df': as DataFrame
    """
    # url = f"http://localhost:{EXCHANGE_PORT}/stock/"
    # response = _get_url_response(url)
    # return response
    from moneypot.models import Stock

    session = Session()
    stocks = session.query(Stock).all()

    if format == 'dict':
        stocks_dict = [stock.to_dict() for stock in stocks]
        return stocks_dict
    else:
        return stocks


def get_stock_id_by_symbol(symbol):
    """ Get ID of stock """
    from moneypot.models import Stock

    session = Session()
    stock = session.query(Stock).filter(Stock.symbol==symbol).first()
    return stock.id

# def get_stock_label_by_symbol(symbol):
#     """ Get ID of stock """
#     from moneypot.models import Stock

#     session = Session()
#     stock = session.query(Stock).filter(Stock.symbol==symbol).first()
#     return stock.id

def get_ticker(id, format=None):
    """ Return a ticker for a stock
    
    Parameters:
    -----------
     - format: str
        - 'dict': as dict
        - 'df': as DataFrame
    """
    # url = f"http://localhost:{EXCHANGE_PORT}/stock/"
    # response = _get_url_response(url)
    # return response
    from moneypot.models import Ticker

    id = int(id)
    session = Session()
    ticks = session.query(Ticker).filter(Ticker.stock_id==id).all()

    if format == 'dict':
        ticks_dict = [tick.to_dict() for tick in ticks]
        return ticks_dict
    else:
        return ticks


def _get_url_response(url):
    """ Load a generic URL response json """
    req = request.urlopen(url)
    response = json.loads(req.read())
    return response


if __name__ == '__main__':
    stocks = get_stocks_list()