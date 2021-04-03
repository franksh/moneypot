import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import inspect

import moneypot
from moneypot.exchange import Session
from moneypot.models import Stock

# class Stock(BaseModel):
#     symbol: str
#     name: str

class StockRequest(BaseModel):
    symbol: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.post("/stock/", response_model=StockRequest)
@app.post("/stock/")
async def create_stock(stock: StockRequest):
    # result = await some_library(stock)
    # return result
    return True

@app.get("/stock/")
async def get_stock():

    session = Session()
    stocks = session.query(Stock).all()
    # result = await some_library(stock)
    # return result
    return stocks
    # print(stocks)
    # return "Done"

@app.get("/stock/{stock_symbol}")
async def get_stock(stock_symbol: str):

    session = Session()
    stock = session.query(Stock).filter_by(symbol=stock_symbol).first()
    # .get({'symbol': stock_symbol})
    # result = await some_library(stock)
    # return result
    return stock

if __name__ == "__main__":
    port = moneypot.config['exchange']['port']
    uvicorn.run(app, reload=True, host="0.0.0.0", port=port)