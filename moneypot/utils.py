import os
# python 3
import configparser


def get_config_path():
    """ Returns the config path """
    home = os.path.expanduser("~")
    cfg_path = os.path.join(home, ".moneypot_config", "moneypot.cfg")
    return cfg_path


def load_config():
    """ Returns the config """
    cfgpath = get_config_path()

    config = configparser.ConfigParser()
    config.read(cfgpath)

    return config
    # iex_api = dict(config.items('IEX_API'))
