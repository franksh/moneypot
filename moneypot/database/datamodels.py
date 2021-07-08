
# import moneypot
from . import base
from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Float, Integer, String, DateTime, UniqueConstraint, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import event, DDL, DateTime

from moneypot.models import Stock

### SQLAlchemy Models
class DBStock(base.Base):
    __tablename__ = "stock"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    industry = Column(String)
    description = Column(String)
    
    def __repr__(self):
        return "<Stock(symbol={}, name={})>".format(
            self.symbol, self.name
        )    

    def to_model(self) -> Stock:
        """ Return the model that corresponds to this DB Model """
        obj_dict = self.__dict__
        # Remove an unecessary attribute returned by SQL alchemy
        obj_dict.pop('_sa_instance_state', None)
        stock = Stock(**obj_dict)
        return stock

class DBTickerStock(base.Base):
    __tablename__ = "ticker_stock"

    stock_id = Column(Integer, ForeignKey('stock.id'), index=True)
    stock = relationship(DBStock, cascade = "all,delete", backref = "ticker_stock")
    time = Column(DateTime, nullable=False)

    open = Column(Float(10, 2))
    high = Column(Float(10, 2))
    low = Column(Float(10, 2))
    close = Column(Float(10, 2))
    volume = Column(Float())

    __table_args__ = (
        PrimaryKeyConstraint('stock_id', 'time'),
        {'extend_existing': True}
    )

    def __repr__(self):
        return "<TickerStock(stock_id={})>".format(
            self.stock_id
        )

    def to_dict(self):
        """ Returns the object as a dict of its attributes """
        obj_dict = self.__dict__
        # Remove an unecessary attribute returned by SQL alchemy
        obj_dict.pop('_sa_instance_state', None)
        return obj_dict



class DBCoin(base.Base):
    __tablename__ = "coin"
    __table_args__ = {'extend_existing': True}

    symbol = Column(String, primary_key=True, index=True)
    
    def __repr__(self):
        return "<Coin(symbol={})>".format(self.symbol)

    def to_dict(self):
        """ Returns the object as a dict of its attributes """
        obj_dict = self.__dict__
        # Remove an unecessary attribute returned by SQL alchemy
        obj_dict.pop('_sa_instance_state', None)
        return obj_dict

class DBTickerCoin(base.Base):
    __tablename__ = "ticker_coin"

    symbol = Column(String, ForeignKey('coin.symbol'), index=True)
    # stock_id = Column(Integer, ForeignKey('stocks.id'), index=True)
    crypto = relationship(DBCoin, cascade = "all,delete", backref = "ticker_coin")
    
    time = Column(DateTime, nullable=False)
    open = Column(Float(10, 2))
    high = Column(Float(10, 2))
    low = Column(Float(10, 2))
    close = Column(Float(10, 2))
    volume = Column(Float())
    n_trades = Column(Float())

    __table_args__ = (
        PrimaryKeyConstraint('symbol', 'time'),
        {'extend_existing': True}
    )

    def __repr__(self):
        return "<TickerCoin(symbol={})>".format(
            self.symbol
        )

    def to_dict(self):
        """ Returns the object as a dict of its attributes """
        obj_dict = self.__dict__
        # Remove an unecessary attribute returned by SQL alchemy
        obj_dict.pop('_sa_instance_state', None)
        return obj_dict


# # Special: Transform table to Timescaledb hypertable
event.listen(
    DBTickerStock.__table__,
    'after_create',
    DDL(f"SELECT create_hypertable('{DBTickerStock.__tablename__}', 'time');")
)

event.listen(
    DBTickerCoin.__table__,
    'after_create',
    DDL(f"SELECT create_hypertable('{DBTickerCoin.__tablename__}', 'time');")
)
# Create all the tables in the database which are
# defined by Base's subclasses
base.Base.metadata.create_all(base.engine)