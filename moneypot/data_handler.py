"""
Contains the data handler class.
"""
from moneypot.base import Base

import requests

class DataHandler(Base):
    """ Basic handling of data
    """
    def __init__(self,
                 config=None,
                 sandbox_mode=True
                 ):

        if sandbox_mode:
            print("Data Handler is in sandbox mode")

        super().__init__(config)
