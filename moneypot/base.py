"""
Contains base class from which other classes are derived
"""

import moneypot.utils as utils

class Base():

    def __init__(self,
                 config=None
                 ):

        if config is None:
            cfg_path = utils.get_config_path()
            print("no config given, using config at" + cfg_path)
            config = utils.load_config()

        self.config = config

        # database_config = cfgpath
