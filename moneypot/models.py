
import pandas as pd
from abc import abstractproperty
# from moneypot.database import Base, engine
import moneypot




# class Stock(DataFrame):
    # pass
    # columns: 
    # id = Column(Integer, primary_key=True, index=True)
    # symbol = Column(String, unique=True, index=True, nullable=False)
    # name = Column(String, nullable=False)
    # exchange = Column(String, nullable=False)
    # industry = Column(String)
    # description = Column(String)
    
    # def __repr__(self):
    #     return "<Stock(symbol={}, name={})>".format(
    #         self.symbol, self.name
    #     )    

class Stock(object):
    def __init__(self, id, symbol, name, **kwargs):
        self.id = id
        self.symbol = symbol
        self.name = name
        self.__dict__.update(kwargs)

    def __repr__(self):
        return "<Stock(id={}, symbol={}, name={})>".format(
            self.id, self.symbol, self.name
        )    

class Coin(object):
    def __init__(self, symbol, **kwargs):
        self.symbol = symbol
        self.__dict__.update(kwargs)

    def __repr__(self):
        return "<Coin(symbol={})>".format(
            self.symbol
        )

class Ticker(pd.DataFrame):
    """ Generic base class for tickers """

    @property
    @abstractproperty
    def expected_columns(cls)->list:
        """ The columns the dataframe has to have 
        
        Each subclass has to define a list of columns which have
        to be provided at initialization with data to ensure consistency
        """
        return []

    # Define how to aggregate columns. Independent of implementations.
    column_agg_funcs = {
        'stock_id': 'first',
        'symbol': 'first',
        'open': 'first',
        'low': 'min',
        'high': 'max',
        'close': 'last',
        'volume': 'sum',
        'n_trades': 'sum'
    }


    def __init__(self, data):

        input_columns = list(data.columns)
        assert set(input_columns) == set(self.expected_columns), \
            f"""Input data does not have the expected columns.
             - expected: {self.expected_columns}
             - given: {input_columns}
            """

        if isinstance(data, pd.DataFrame):
            df = data
            columns = df.columns

        # Dictionary
        elif isinstance(data, dict):
            df = pd.DataFrame.from_dict(data)
            columns = df.columns

        super(Ticker, self).__init__(df, columns=columns)



    def resample_time(self, interval):
        """ Resample the time scale of itself 
        
        The base columns (olhcv) are aggregated according to each columns.
        Other columns are aggregated with 'first'.

        Parameters:
        -----------
         - interval: str
            The time interval on wich to aggregate. See pandas doc.
            Examples: '15min', '1H', '1D'
        """
        # Define the aggregation of columns
        # columns = self._obj.columns
        # agg_base_cols = {'open': 'first', 'low': 'min', 'high': 'max',
        #                 'close': 'last', 'volume': 'sum'}
        # agg_other_cols = {col: 'first' for col in columns
        #               if col not in TickerAccessor.min_cols}
        # agg_funcs = {**agg_base_cols, **agg_other_cols}
        agg_funcs = {c:func for c,func in self.column_agg_funcs.items() 
                    if c in self.columns}

        # Resample
        self = (
                self.set_index('time').resample(interval)
                    .agg(agg_funcs)
                    .reset_index()
                    .dropna()
                )
        return self



class TickerStock(Ticker):

    # columns  = pd.Index(['stock_id', 'time', 'open', 'high', 'low', 'close', 'volume'])
    expected_columns = ['stock_id', 'time', 'open', 'high',
                        'low', 'close', 'volume']

    # __tablename__ = "ticker_stock"

    # stock_id = Column(Integer, ForeignKey('stock.id'), index=True)
    # stock = relationship(DBStock, cascade = "all,delete", backref = "ticker_stock")
    # time = Column(DateTime, nullable=False)

    # open = Column(Float(10, 2))
    # high = Column(Float(10, 2))
    # low = Column(Float(10, 2))
    # close = Column(Float(10, 2))
    # volume = Column(Float())

    # __table_args__ = (
    #     PrimaryKeyConstraint('stock_id', 'time'),
    #     {'extend_existing': True}
    # )

    # def __repr__(self):
    #     return "<TickerStock(stock_id={})>".format(
    #         self.stock_id
    #     )

    # def to_dict(self):
    #     """ Returns the object as a dict of its attributes """
    #     obj_dict = self.__dict__
    #     # Remove an unecessary attribute returned by SQL alchemy
    #     obj_dict.pop('_sa_instance_state', None)
    #     return obj_dict

# class Coin():
#     __tablename__ = "coin"
#     __table_args__ = {'extend_existing': True}

#     symbol = Column(String, primary_key=True, index=True)
    
#     def __repr__(self):
#         return "<Coin(symbol={})>".format(self.symbol)

#     def to_dict(self):
#         """ Returns the object as a dict of its attributes """
#         obj_dict = self.__dict__
#         # Remove an unecessary attribute returned by SQL alchemy
#         obj_dict.pop('_sa_instance_state', None)
#         return obj_dict

class TickerCoin(Ticker):
    # columns  = pd.Index(['stock_id', 'time', 'open', 'high', 'low', 'close', 'volume'])
    expected_columns = ['symbol', 'time', 'open', 'high', 'low',
                        'close', 'volume', 'n_trades']
    # __tablename__ = "ticker_coin"

    # symbol = Column(String, ForeignKey('coin.symbol'), index=True)
    # # stock_id = Column(Integer, ForeignKey('stocks.id'), index=True)
    # crypto = relationship(DBCoin, cascade = "all,delete", backref = "ticker_coin")
    
    # time = Column(DateTime, nullable=False)
    # open = Column(Float(10, 2))
    # high = Column(Float(10, 2))
    # low = Column(Float(10, 2))
    # close = Column(Float(10, 2))
    # volume = Column(Float())
    # n_trades = Column(Float())

    # __table_args__ = (
    #     PrimaryKeyConstraint('symbol', 'time'),
    #     {'extend_existing': True}
    # )

    # def __repr__(self):
    #     return "<TickerCoin(symbol={})>".format(
    #         self.symbol
    #     )

    # def to_dict(self):
    #     """ Returns the object as a dict of its attributes """
    #     obj_dict = self.__dict__
    #     # Remove an unecessary attribute returned by SQL alchemy
    #     obj_dict.pop('_sa_instance_state', None)
    #     return obj_dict



# class Ticker(D)
# @pd.api.extensions.register_dataframe_accessor("ticker")
# class TickerAccessor:
#     """ This adds a neat 'ticker' namespace to pandas

#     Example:
#     ----------
#     >>> ds = pd.Dataframe(..data..)
#     >>> ds.ticker.bounds
#     (Timestamp('2020-01-03 08:00:00'), Timestamp('2021-07-04 08:40:00'))
#     """
#     # The minimum columns that are required
#     min_cols = ['time', 'open', 'high', 'low', 'close']

#     def __init__(self, pandas_obj):
#         self._validate(pandas_obj)
#         self._obj = pandas_obj

#     @staticmethod
#     def _validate(obj):
#         # verify if basic columns are present
#         cols = TickerAccessor.min_cols
#         if any([col not in obj.columns for col in cols]):
#             raise AttributeError("Data does not have correct columns (time,o,h,c,l).")

#     @property
#     def bounds(self):
#         return (self._obj.time.min(), self._obj.time.max())

#     def resample(self, interval):
#         """ Resample the time scale of itself 
        
#         The base columns (olhcv) are aggregated according to each columns.
#         Other columns are aggregated with 'first'.

#         Parameters:
#         -----------
#          - interval: str
#             The time interval on wich to aggregate. See pandas doc.
#             Examples: '15min', '1H', '1D'
#         """
#         # Define the aggregation of columns
#         columns = self._obj.columns
#         agg_base_cols = {'open': 'first', 'low': 'min', 'high': 'max',
#                         'close': 'last', 'volume': 'sum'}
#         agg_other_cols = {col: 'first' for col in columns
#                       if col not in TickerAccessor.min_cols}
#         agg_funcs = {**agg_base_cols, **agg_other_cols}
#         # Resample
#         self._obj = (
#                 self._obj.set_index('time').resample(interval).agg(agg_funcs)
#                     .reset_index()
#                     .dropna()
#                 )
#         return self._obj


