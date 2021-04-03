import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import inspect
from starlette.responses import RedirectResponse

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
    # return {"Hello": "World"}
    return RedirectResponse(url='/docs')


# @app.post("/stock/", response_model=StockRequest)
@app.post("/stock/")
async def create_stock(stock: StockRequest):
    # result = await some_library(stock)
    # return result
    return True

@app.get("/stock/")
async def get_stock():
    """ Get a list of all stocks """

    session = Session()
    stocks = session.query(Stock).all()
    # result = await some_library(stock)
    # return result
    return stocks
    # print(stocks)
    # return "Done"

@app.get("/stock/{stock_symbol}")
async def get_stock(stock_symbol: str):
    """ Get information on a particular stock """

    session = Session()
    stock = session.query(Stock).filter_by(symbol=stock_symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail=f"Symbol {stock_symbol} not found")
    # .get({'symbol': stock_symbol})
    # result = await some_library(stock)
    # return result
    return stock

if __name__ == "__main__":
    port = moneypot.config['exchange']['port']
    uvicorn.run(app, host="0.0.0.0", port=port)