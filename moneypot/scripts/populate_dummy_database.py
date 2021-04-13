import random
from datetime import datetime    

from moneypot.models import Stock, Ticker
from moneypot.exchange import Session, Base, engine

def rand():
    " Shorthand to get a random number "
    return random.randint(10,50)

def populate_db():
    """ Populates database with dummy content """
    Base.metadata.drop_all(engine)

    populate_stocks()
    populate_tickers()

    print("Successfully populated")
    return

def populate_stocks():
    """ Populate the stocks table """
    stocks_data = [
        {'id': 1, 'symbol': 'AAPL', 'name': 'Apple'},
        {'id': 2, 'symbol': 'TSLA', 'name': 'Tesla'},
        {'id': 3, 'symbol': 'GME', 'name': 'Gamestop'},
    ]
    session = Session()
    # Create table 
    # Stock.create(engine)
    # Base.metadata.create_all(engine)
    # Stock.__table__.drop(engine)
    Stock.__table__.create(engine)

    for stock_data in stocks_data:
        stock = Stock(**stock_data)
        session.add(stock)
    # doctor_strange = Stock()  
    # session.add(doctor_strange)  
    session.commit()

def populate_tickers():
    """ Populate the tickers table """

    N = lambda: random.randint(10,50) # Random number generator
    vol = lambda: random.randint(1000,1000000) # Random number generator

    tickers_data = [
        {'stock_id': 1, 'time': datetime.strptime("2020-01-01", "%Y-%m-%d"), 'open': N(), 'high': N(), 'low': N(), 'close': N(), 'volume': vol()},
        {'stock_id': 1, 'time': datetime.strptime("2020-01-02", "%Y-%m-%d"), 'open': N(), 'high': N(), 'low': N(), 'close': N(), 'volume': vol()},
        {'stock_id': 1, 'time': datetime.strptime("2020-01-03", "%Y-%m-%d"), 'open': N(), 'high': N(), 'low': N(), 'close': N(), 'volume': vol()},
        {'stock_id': 2, 'time': datetime.strptime("2020-01-01", "%Y-%m-%d"), 'open': N(), 'high': N(), 'low': N(), 'close': N(), 'volume': vol()},
    ]
    session = Session()
    # Create table 
    # Stock.create(engine)
    # Base.metadata.create_all(engine)
    # Ticker.__table__.drop(engine)
    Ticker.__table__.create(engine)

    for ticker_data in tickers_data:
        ticker = Ticker(**ticker_data)
        session.add(ticker)
    # doctor_strange = Stock()  
    # session.add(doctor_strange)  
    session.commit()


def main():
    """ Fill the database with dummy content. """

    # Safety check
    question_string = "WARNING: This will populate the database " +\
        "with dummy content, are you sure you want to proceed? (y/n): "
    answer = input(question_string)
    if answer != 'y':
        return
    else:
        populate_db()




if __name__ == '__main__':
    main()