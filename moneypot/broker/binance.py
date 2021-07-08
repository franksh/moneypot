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

    def load_ticker_from_broker(self, symbol: str, frequency: str) -> TickerCoin:
        """ Return the ticker for a crypto """

        # Parameter is actually i.e. Client.KLINE_INTERVAL_5MINUTE
        freq_to_interval = {
            '1min': '1m',
            '5min': '5m',
            '15min': '15m',
        }
        interval = freq_to_interval[frequency]

        # Load data
        candles = self.client.get_klines(symbol=symbol, interval=interval)

        # Process
        dfticker = self.parse_candles(candles, symbol)
        return dfticker


    def load_available_cryptos(self) -> list:
        """ Return a list of all info on a crypto """
        coins = self.client.get_all_tickers()
        return coins


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

