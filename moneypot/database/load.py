
import pandas as pd
from typing import List

from moneypot.database import Session
from moneypot.database import DBStock, DBTickerStock
from moneypot.database import DBCoin, DBTickerCoin

from moneypot.models import TickerStock, TickerCoin

# StockList = list[Stock]

def get_all_stocks() -> pd.DataFrame:
    """ Return a list of all stocks 
    """
    session = Session()
    stocks_query = session.query(DBStock).statement
    dfstocks = pd.read_sql(stocks_query, session.connection())
    return dfstocks

def get_all_coins() -> pd.DataFrame:
    """ Return a list of all coins 
    """
    session = Session()
    coins_query = session.query(DBCoin).statement
    dfcoins = pd.read_sql(coins_query, session.connection())
    return dfcoins


def get_ticker_stock(stock_id) -> TickerStock:
    """ Return a ticker for a stock
    
    Parameters:
    -----------
     - stock_id: int
        
    Returns:
    --------
     - ticker: moneypot.models.TickerStock
    """
    stock_id = int(stock_id)
    session = Session()

    query = session.query(DBTickerStock).filter(DBTickerStock.stock_id==stock_id).statement
    dfticker = pd.read_sql(query, session.connection())
    ticker = TickerStock(dfticker)
    return ticker

def get_ticker_coin(symbol) -> TickerCoin:
    """ Return a ticker for a coin
    
    Parameters:
    -----------
     - symbol: str
        
    Returns:
    --------
     - ticker: moneypot.models.TickerCoin
    """
    # stock_id = int(stock_id)
    session = Session()

    query = session.query(DBTickerCoin).filter(DBTickerCoin.symbol==symbol).statement
    dfticker = pd.read_sql(query, session.connection())
    ticker = TickerCoin(dfticker)
    return ticker