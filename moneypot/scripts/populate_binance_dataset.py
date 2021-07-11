import pandas as pd
from moneypot.paths import get_package_root
from moneypot.broker import BinanceBroker
from moneypot.database import drop_coin_tables, populate_coins, populate_ticker_coins

START_DATE = "1 Jul, 2021"

def update_coin_list():
    """ Define the list of coins to load data for """
    broker = BinanceBroker()
    binance_pairs = broker.get_binance_pairs_by_marketcap(base_coin='USDT',
                                          was_traded_before='2021-01-01')
    coin_list = binance_pairs.head(10)
    from moneypot.paths import get_package_root
    pkg_root = get_package_root()
    coin_list.to_csv(pkg_root / "data" / "coins.csv", index=False)


def populate_db():
    """ Populates database with dummy content """
    
    # Base.metadata.drop_all(engine)
    broker = BinanceBroker()

    # Load list of symbols to load
    print(" - loading stock list")
    coins_path = get_package_root() / "data" / "coins.csv"
    coins = pd.read_csv(coins_path, squeeze=True)

    populate_coins(coins, broker)
    populate_ticker_coins(coins['symbol'], broker, start_date=START_DATE)

    return

def main():
    """ Fill the database with content. """

    # Safety check
    # question_string = "WARNING: This will populate the database " +\
        # "with Binance data, based on all symbols listed at " +\
        # " moneypot/data/coins.csv, are you sure you want to proceed? (y/n): "

    # question_string = "WARNING: Do you want to drop the old tables?"
    # answer = input(question_string)
    # if answer == 'y':
    #     print(" - dropping tables")
    print(" - dropping old tables")
    drop_coin_tables()
    # else:
    print(" - populating data")
    print(f" - start date: {START_DATE}")
    populate_db()


if __name__ == '__main__':
    # update_coin_list()
    main()
