"""
Run the exchange api
"""
import uvicorn

import moneypot
from moneypot.exchange.api import app


def main():
    port = moneypot.config['exchange']['port']
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()