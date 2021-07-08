""" Methods to access the API programmatically """
import json
import pandas as pd
from urllib import request

import moneypot
from moneypot.database import Session
from moneypot.database import Base, engine
from moneypot.database import DBStock, DBTickerStock
from moneypot.database import DBCoin, DBTickerCoin

from sqlalchemy import func
    
EXCHANGE_PORT = moneypot.config['exchange']['port'] 


def drop_stock_tables():
    """ Drops the stock tables from the database """

    tables_to_drop = [DBStock.__table__, DBTickerStock.__table__]
    Base.metadata.drop_all(bind=engine, tables=tables_to_drop)


def drop_coin_tables():
    """ Drops the coin tables from the database """
    tables_to_drop = [DBCoin.__table__, DBTickerCoin.__table__]
    Base.metadata.drop_all(bind=engine, tables=tables_to_drop)


def get_stock_id_by_symbol(symbol):
    """ Get ID of stock """
    from moneypot.database import DBStock

    session = Session()
    
    stock = session.query(DBStock).filter(DBStock.symbol==symbol).first()
    return stock.id

# def get_stock_label_by_symbol(symbol):
#     """ Get ID of stock """
#     from moneypot.models import Stock

#     session = Session()
#     stock = session.query(Stock).filter(Stock.symbol==symbol).first()
#     return stock.id



def _get_url_response(url):
    """ Load a generic URL response json """
    req = request.urlopen(url)
    response = json.loads(req.read())
    return response


if __name__ == '__main__':
    pass