import pandas as pd
from moneypot.paths import get_package_root
from moneypot.broker import YFinanceBroker
from moneypot.database import drop_stock_tables, populate_stocks, populate_ticker_stocks


def populate_db():
    """ Populates database with dummy content """
    
    # Base.metadata.drop_all(engine)
    drop_stock_tables()
    broker = YFinanceBroker()

    # Load list of symbols to load
    print(" - loading stock list")
    symbols_path = get_package_root() / "data" / "symbols.csv"
    symbols = pd.read_csv(symbols_path, squeeze=True)

    populate_stocks(symbols, broker)
    populate_ticker_stocks(symbols, broker)

    return

def main():
    """ Fill the database with dummy content. """

    # Safety check
    question_string = "WARNING: This will populate the database " +\
        "with YFinance data, based on all symbols listed at " +\
        " moneypot/data/symbols.csv, are you sure you want to proceed? (y/n): "
    answer = input(question_string)
    if answer != 'y':
        return
    else:
        populate_db()


if __name__ == '__main__':
    main()