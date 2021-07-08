""" Base class for brokers """
from abc import ABC, abstractmethod

from moneypot.models import Stock, TickerStock, Coin, TickerCoin

class Broker(ABC):
    """ Abstract Base class for all brokers. 
    
    Specific brokers should inherit from this, and implement its functions,
    which have to be adapted to the API of the broker.
    
    Broker is an abstract class (using the abc module) which can't be
    instantiated. Many of its methods are abstractmethods, 
    meaning they *have* to be implemented by child classes.
    """
    def __init__(self):
        pass
    

class StockBroker(Broker):

    def __init__(self):
        pass

    @abstractmethod
    def load_stock_from_broker(self, symbol: str) -> Stock:
        """ Return the info on a stock """
        pass

    @abstractmethod
    def load_ticker_from_broker(self, symbol: str, frequency: str, max_date: str) -> TickerStock:
        """ Return the ticker for a stock """
        pass

class CryptoBroker(Broker):

    def __init__(self):
        pass

    @abstractmethod
    def load_coin_from_broker(self, symbol: str) -> Coin:
        """ Return the info on a crypto """
        pass

    @abstractmethod
    def load_ticker_from_broker(self, symbol: str, frequency: str) -> TickerCoin:
        """ Return the ticker for a crypto """
        pass
