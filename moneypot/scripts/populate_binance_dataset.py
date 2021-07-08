import pandas as pd
from moneypot.paths import get_package_root
from moneypot.broker import BinanceBroker
from moneypot.database import drop_coin_tables, populate_coins, populate_ticker_coins


def populate_db():
    """ Populates database with dummy content """
    
    # Base.metadata.drop_all(engine)
    drop_coin_tables()
    broker = BinanceBroker()

    # Load list of symbols to load
    print(" - loading stock list")
    symbols_path = get_package_root() / "data" / "coins.csv"
    symbols = pd.read_csv(symbols_path, squeeze=True)

    populate_coins(symbols, broker)
    populate_ticker_coins(symbols, broker)

    return

def main():
    """ Fill the database with dummy content. """

    # Safety check
    question_string = "WARNING: This will populate the database " +\
        "with Binance data, based on all symbols listed at " +\
        " moneypot/data/coins.csv, are you sure you want to proceed? (y/n): "
    answer = input(question_string)
    if answer != 'y':
        return
    else:
        populate_db()


if __name__ == '__main__':
    main()


# from moneypot import config
# from moneypot.models import Coin, TickerCoin
# from moneypot.database import Base, engine, Session

# from moneypot.broker import BinanceBroker

# # def populate_crypto_tickers():
# #     """ Download all crypto Tickers """
# #     api_key = config['binance']['API_KEY']
# #     secret_key = config['binance']['SECRET_KEY']


# def drop_coin_tables():
#     """ Drops the stock tables from the database """
#     tables_to_drop = [Coin.__table__, TickerCoin.__table__]
#     Base.metadata.drop_all(bind=engine, tables=tables_to_drop)

# def populate_db():
#     """ Populates database with dummy content """
    
#     # Base.metadata.drop_all(engine)
#     drop_coin_tables()
#     broker = BinanceBroker()


# #     # Load list of symbols to load
# #     print(" - loading stock list")
# #     symbols_path = get_package_root() / "data" / "symbols.csv"
# #     symbols = pd.read_csv(symbols_path, squeeze=True)
#     symbols = ['BTCEUR', 'BNBEUR']

#     populate_coins(symbols, broker)
#     populate_tickers_coins(symbols, broker)

# #     return

# def populate_coins(symbols, broker):
#     """ Populate coins for list of symbols """

#     print(" - populating coins ")

#     session = Session()

#     Coin.__table__.create(engine)

#     # Load coin data for symbols
#     for symbol in symbols:
#         print(symbol)
#         coin = broker.load_coin_from_broker(symbol)    
#         session.add(coin)
#     session.commit()

# def populate_tickers_coins(symbols, broker):
#     """ Populate the coin tickers for the given symbol
    
#     Parameters:
#     -----------
#      - symbols: list
#         List of symbols
#      - broker: moneypot.broker.Binance

#     """
#     print(" - populating coins tickers ")

#     # session = Session()

#     TickerCoin.__table__.create(engine)

#     for symbol in symbols:
#         print(symbol)
#         dfticker = broker.load_ticker_from_broker(symbol, frequency='5min', max_date=None)
#         # session.bulk_save_objects(tickers)
#         dfticker.to_sql('ticker_coin', con=engine,
#                          if_exists='append', index=False)

#     # session.commit()


# def main():
#     """ Fill the database with Binance data content. """

#     # Safety check
#     question_string = "WARNING: This will populate the database " +\
#         "with Binance data, based on all symbols listed at " +\
#         " moneypot/data/coins.csv, are you sure you want to proceed? (y/n): "
#     answer = input(question_string)
#     if answer != 'y':
#         return
#     else:
#         populate_db()


# if __name__ == '__main__':
#     main()