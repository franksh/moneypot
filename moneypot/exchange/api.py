import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

class Stock(BaseModel):
    symbol: str
    name: str

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/stock/", response_model=Stock)
async def create_stock(stock: Stock):
    # result = await some_library(stock)
    # return result
    return True

@app.get("/stock/", response_model=Stock)
async def get_stock():
    # result = await some_library(stock)
    # return result
    return True

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)