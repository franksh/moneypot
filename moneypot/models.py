from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String, DateTime, UniqueConstraint, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import event, DDL, DateTime

from moneypot.exchange import Base, engine

class Stock(Base):
    __tablename__ = "stocks"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    industry = Column(String)
    description = Column(String)
    # price = Column(Numeric(10, 2))
    # forward_pe = Column(Numeric(10, 2))
    # forward_eps = Column(Numeric(10, 2))
    # dividend_yield = Column(Numeric(10, 2))
    # ma50 = Column(Numeric(10, 2))
    # ma200 = Column(Numeric(10, 2))
    
    def __repr__(self):
        return "<Stock(symbol={}, name={})>".format(
            self.symbol, self.name
        )

    def to_dict(self):
        """ Returns the object as a dict of its attributes
        """
        obj_dict = self.__dict__
        # Remove an unecessary attribute returned by SQL alchemy
        obj_dict.pop('_sa_instance_state', None)
        return obj_dict
        


class Ticker(Base):
    __tablename__ = "tickers"

    stock_id = Column(Integer, ForeignKey('stocks.id'), index=True)
    stock = relationship(Stock, cascade = "all,delete", backref = "tickers")
    time = Column(DateTime, nullable=False)

    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    close = Column(Numeric(10, 2))
    volume = Column(Numeric())

    __table_args__ = (
        PrimaryKeyConstraint('stock_id', 'time'),
        {'extend_existing': True}
    )


    def __repr__(self):
        return "<Ticker(stock_id={})>".format(
            self.stock_id
        )

    def to_dict(self):
        """ Returns the object as a dict of its attributes
        """
        obj_dict = self.__dict__
        # Remove an unecessary attribute returned by SQL alchemy
        obj_dict.pop('_sa_instance_state', None)
        return obj_dict

# # Special: Transform table to Timescaledb hypertable
event.listen(
    Ticker.__table__,
    'after_create',
    DDL(f"SELECT create_hypertable('{Ticker.__tablename__}', 'time');")
)

# Create all the tables in the database which are
# defined by Base's subclasses
Base.metadata.create_all(engine)