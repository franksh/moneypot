

from moneypot.models import Stock
from moneypot.exchange import Session, Base, engine

def populate_db():
    """ Populates database with dummy content """

    stocks_data = [
        {'id': 1, 'symbol': 'AAPL', 'name': 'Apple'},
        {'id': 2, 'symbol': 'TSLA', 'name': 'Tesla'},
        {'id': 3, 'symbol': 'GME', 'name': 'Gamestop'},
    ]
    session = Session()
    # Create table 
    # Stock.create(engine)
    # Base.metadata.create_all(engine)
    Stock.__table__.drop(engine)
    Stock.__table__.create(engine)

    for stock_data in stocks_data:
        stock = Stock(**stock_data)
        session.add(stock)
    # doctor_strange = Stock()  
    # session.add(doctor_strange)  
    session.commit()
    print("Successfully populated")
    return

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