from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String
from sqlalchemy.orm import relationship

from moneypot.exchange import Base, engine

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    # price = Column(Numeric(10, 2))
    # forward_pe = Column(Numeric(10, 2))
    # forward_eps = Column(Numeric(10, 2))
    # dividend_yield = Column(Numeric(10, 2))
    # ma50 = Column(Numeric(10, 2))
    # ma200 = Column(Numeric(10, 2))

# Create all the tables in the database which are
# defined by Base's subclasses such as User
Base.metadata.create_all(engine)