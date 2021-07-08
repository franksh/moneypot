
""" Methods to access the API programmatically """

import moneypot
from moneypot.database import Session
from moneypot.database import engine
from moneypot.database import DBStock, DBTickerStock
from moneypot.database import DBCoin, DBTickerCoin
    
def populate_stocks(symbols, broker):
    """ Populate stocks for list of symbols """

    print(" - populating stocks ")
    session = Session()
    DBStock.__table__.create(engine)

    # Load data for symbols
    for symbol in symbols:
        print(symbol)
        stock = broker.load_stock_from_broker(symbol)
        db_stock = DBStock(**stock.__dict__)
        session.add(db_stock)
    session.commit()

def populate_ticker_stocks(symbols, broker):
    """ Populate the tickers for the given symbol
    
    Parameters:
    -----------
     - symbols: list
        List of symbols
     - broker: moneypot.broker.YFinanceBroker
    """
    print(" - populating tickers ")
    session = Session()
    DBTickerStock.__table__.create(engine)
    tablename = DBTickerStock.__tablename__

    for symbol in symbols:
        print(symbol)
        # tickers = broker.load_ticker_from_broker(symbol)
        # session.bulk_save_objects(tickers)
        dfticker = broker.load_ticker_from_broker(symbol, frequency='15min')
        dfticker.to_sql(tablename, con=engine, if_exists='append', index=False)
        # session.bulk_save_objects(tickers)
    session.commit()

def populate_coins(symbols, broker):

    print(" - populating coins ")
    session = Session()
    DBCoin.__table__.create(engine)

    # Load data for symbols
    for symbol in symbols:
        print(symbol)
        coin = broker.load_coin_from_broker(symbol)
        db_coin = DBCoin(**coin.__dict__)
        session.add(db_coin)
    session.commit()

def populate_ticker_coins(symbols, broker):
    """ Populate the coin tickers for the given symbol
    
    Parameters:
    -----------
     - symbols: list
        List of symbols
    """
    print(" - populating coin tickers ")
    session = Session()
    DBTickerCoin.__table__.create(engine)
    tablename = DBTickerCoin.__tablename__

    for symbol in symbols:
        print(symbol)
        dfticker = broker.load_ticker_from_broker(symbol, frequency='5min')
        dfticker.to_sql(tablename, con=engine, if_exists='append', index=False)
        # session.bulk_save_objects(tickers)
    session.commit()