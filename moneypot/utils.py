"""
Utilities for path finding and configuration files.
"""

from pathlib import Path
import configparser
import inspect
import moneypot
import shutil

def get_package_root():
    """
    Get the path of the package repository.
    """
    package_path = Path(inspect.getfile(moneypot))
    pkg_root = package_path.parents[0]
    return pkg_root


def get_config_path():
    """ Returns the config path """
    directory = Path.home() / ".moneypot_config"
    directory.mkdir(mode=0o700, parents=False, exist_ok=False)
    cfg_path = directory / "moneypot.cfg"
    if not cfg_path.exists():
        shutil.copy2(get_package_root() / "configs" /  "moneypot.cfg", cfg_path)
    return cfg_path


def load_config():
    """ Returns the config """
    cfgpath = get_config_path()

    config = configparser.ConfigParser()
    config.read(cfgpath)

    return config
    # iex_api = dict(config.items('IEX_API'))
