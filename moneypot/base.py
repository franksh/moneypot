
from moneypot import *

class Base():

    def __init__(self,
                 config=None
                 ):

        if config is None:
            cfg_path = get_config_path()
            print("no config given, using config at" + cfg_path)
            config = load_config()

        self.config = config

        # database_config = cfgpath
