"""
Contains the data handler class.
"""
from moneypot.base import Base


class DataHandler(Base):
    def __init__(self,
                 config=None):
        super().__init__(config)
