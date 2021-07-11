import pandas as pd

from binance import Client

import moneypot
from moneypot.models import Coin, TickerCoin
from .base import CryptoBroker


class BinanceBroker(CryptoBroker):
    """ Broker for the Binance API
    
    Binance API explanation:
    https://binance-docs.github.io/apidocs/spot/en/
    """
    def __init__(self):
        api_key = moneypot.config['binance']['API_KEY']
        secret_key = moneypot.config['binance']['SECRET_KEY']
        self.client = Client(api_key, secret_key)


    def load_coin_from_broker(self, symbol: str) -> Coin:
        """ Return the info on a coin """
        coin = Coin(**{
            'symbol': symbol
        })
        return coin

    def load_ticker_from_broker(self, symbol: str, start_date: str, frequency: str) -> TickerCoin:
        """ Return the ticker for a crypto """

        # Parameter is actually i.e. Client.KLINE_INTERVAL_5MINUTE
        freq_to_interval = {
            '1min': '1m',
            '5min': '5m',
            '15min': '15m',
        }
        interval = freq_to_interval[frequency]

        # Load data
        # candles = self.client.get_klines(symbol=symbol, interval=interval)
        klines = self.client.get_historical_klines(symbol, 
                            # Client.KLINE_INTERVAL_1MINUTE,
                            interval,
                            start_str=start_date,
                            limit=1000)

        # Process
        dfticker = self.parse_candles(klines, symbol)
        return dfticker


    def load_available_coins(self) -> list:
        """ Load all available trading pairs on binance  """
        coins = self.client.get_all_tickers()
        dfcoins = pd.DataFrame(coins)
        return dfcoins


    def get_binance_pairs_by_marketcap(self, base_coin='USDT',
                                       was_traded_before=None):
        """ Return all pairs with the base coin on binance by marketcap

        For example for USDT: BTCUSDT, ETHUSDT, etc.

        Parameters:
        -----------
         - base_coin: str
         - was_traded_before: datetime or str
            The first trading date of the pair has to be before this.
        """
        # Get coinmarketcap pairs
        from moneypot.broker import get_all_coins_by_marketcap_coinmarketcap
        cmap = get_all_coins_by_marketcap_coinmarketcap()
        # Add base_pais pairs
        cmap['base_pair'] = cmap['symbol'].apply(lambda x: "".join([x, base_coin]))

        # Get binance pairs
        # from moneypot.broker import BinanceBroker
        # broker = BinanceBroker()
        binance_coins = self.load_available_coins()

        # List all paris available in binance
        cmap['is_pair_in_binance'] = cmap.apply(lambda x: x['base_pair'] in 
                                                binance_coins['symbol'].values,
                                                axis=1)
        binance_pairs = cmap.loc[cmap['is_pair_in_binance']]
        binance_pairs = binance_pairs[['rank', 'base_pair', 'name', 'first_historical_data', 'last_historical_data']].reset_index(drop=True)
        binance_pairs = binance_pairs.rename(columns={'base_pair': 'symbol',
                                                      'rank': 'rank_marketcap'})
        print(" - number of pairs found on binance: ", len(binance_pairs))

        # was_traded_before
        if was_traded_before:
            print(f" - filtering pairs by first trading date: {was_traded_before}")
            binance_pairs = binance_pairs.loc[binance_pairs['first_historical_data']<was_traded_before]
            print(" - number of pairs after filtering: ", len(binance_pairs))

        return binance_pairs


    def parse_candles(self, candles, symbol) -> TickerCoin:
        """ Cast raw candle data to DataFrame 
        
        Parameters:
        -----------
         - candles: list(list)
            A list where each item is a list with the raw data of a candle.
            This is the data returned from the Binance API

         - symbol: str
            The coin symbol.

        Returns:
        --------
         - dfticker: TickerCoin
            The coin ticker
        
        """
        import pandas as pd
        columns = ['time_open', 'open', 'high', 'low', 'close', 'volume', 'time_close', 'volume_quote_asset', 'n_trades', 'buy_base_asset_vol', 'buy_quote_asset_vol', 'ignore']
        df = pd.DataFrame(candles, columns=columns)


        # Convert dtypes
        df['time_open'] = pd.to_datetime(df['time_open'], unit='ms')
        df['time_close'] = pd.to_datetime(df['time_close'], unit='ms')
        cols_float = ['open', 'high', 'low', 'close', 'volume', 'volume_quote_asset', 'buy_base_asset_vol', 'buy_quote_asset_vol']
        df[cols_float] = df[cols_float].astype(float)

        # Chose what to save/drop
        drop_cols = ['time_close', 'volume_quote_asset', 'buy_base_asset_vol', 'buy_quote_asset_vol', 'ignore']
        rename_cols = {'time_open': 'time'}
        df = df.drop(columns=drop_cols)
        df = df.rename(columns=rename_cols)

        # df['symbol'] = symbol
        df.insert(loc=0, column='symbol', value=symbol)

        dfticker = TickerCoin(df)

        return dfticker

