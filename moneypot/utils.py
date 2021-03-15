"""
Utilities for path finding and configuration files.
"""

from pathlib import Path
import configparser
import inspect
import moneypot
import shutil

from moneypot.paths import get_package_root, get_package_configs

def create_configs():
    """ Create the default config files """
    path_configs = get_package_configs()
    path_configs_templates = get_package_root() / "configs"
    path_configs.mkdir(mode=0o700, parents=False, exist_ok=True)

    # Configs to always overwrite 
    for config in ['supervisor.cfg']:
        shutil.copy2(path_configs_templates / (config + '.example'), path_configs / config )

    # Configs to only write if not exists
    for config in ['moneypot.cfg']:
        config_path = path_configs / config
        if not config_path.exists():
            shutil.copy2(path_configs_templates / (config + '.example'), path_configs / config )


def load_config(config):
    """ Returns the config """
    cfgpath = get_package_configs() / config

    config = configparser.ConfigParser()
    config.read(cfgpath)

    return config
