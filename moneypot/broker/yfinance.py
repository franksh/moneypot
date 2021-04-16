import requests
import yfinance
import pandas as pd

import moneypot
from moneypot.models import Stock, Ticker
from moneypot.exchange import get_stock_id_by_symbol

from .base import Broker


class YFinanceBroker(Broker):
    """ Broker for the YFinance API

    API used is here:
    https://rapidapi.com/finance.yahoo.api/api/yahoo-finance-low-latency
    """
    def __init__(self):

        self.headers = {
            'x-rapidapi-key': moneypot.config['yfinance']['RAPID_API_KEY'],
            'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
        }


    def load_stock(self, symbol: str) -> Stock:
        """ Return the info on a stock """

        # symbol = 'AAPL'
        url = f"https://yahoo-finance-low-latency.p.rapidapi.com/v11/finance/quoteSummary/{symbol}"
        
        querystring = {
            'modules': 'assetProfile,quoteType'
        }

        response = requests.request("GET", url, headers=self.headers, params=querystring)
        # Parse response
        import json
        data = json.loads(response.text)

        if data['quoteSummary']['error']:
            error_msg = "API Error: {code} - {description}".format(**data['quoteSummary']['error'])
            print(error_msg)

        res = data['quoteSummary']['result'][0]

        assetProfile_fields = ['industry', '']

        data = {
            'symbol': res['quoteType']['symbol'],
            'name': res['quoteType']['shortName'],
            'description': res['assetProfile']['longBusinessSummary'],
            'exchange': res['quoteType']['exchange'],
            'industry': res['assetProfile']['industry'],
        }

        stock = Stock(**data)
        return stock

    def load_ticker(self, symbol: str, frequency: str = '15m', max_date: str = None) -> Ticker:
        """ Return the ticker for a stock 
        
        Ranges: m, d, wk, mo
        Frequency (interval): 15m, ?

        Returns:
        --------
         - tickers: list(Ticker)
            A list of Tickers

        """
        url = f"https://yahoo-finance-low-latency.p.rapidapi.com/v8/finance/chart/{symbol}"

        # Ranges: m, d, wk, mo
        querystring = {
            "interval": "15m",
            "range": "60d",
            # "region":"DE", 
            "events":"div,split"}


        response = requests.request("GET", url, headers=self.headers, params=querystring)

        # Parse response
        import json
        data = json.loads(response.text)

        if data['chart']['error']:
            print("API ERROR: ", data['chart']['error'])
            return

        results = data['chart']['result']

        result = results[0]
        # meta = result['meta']

        timestamps = result['timestamp']
        quote = result['indicators']['quote'][0]

        datadf = {'time': timestamps, **quote}
        dfticker = pd.DataFrame(datadf)
        dfticker['time'] = pd.to_datetime(dfticker['time'], unit='s')
        # dfticker.head()

        stock_id = get_stock_id_by_symbol(symbol)

        tickers = []
        for _, tick in dfticker.iterrows():

            ticker_data = { **tick, 'stock_id': stock_id }
            ticker = Ticker(**ticker_data)
            tickers.append(ticker)

        return tickers
