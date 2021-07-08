"""
Path handling.
"""
import inspect
from pathlib import Path

import simplejson as json

import moneypot

def get_package_root():
    """
    Get the path of the package repository.
    """
    package_path = Path(inspect.getfile(moneypot))
    pkg_root = package_path.parents[0]
    return pkg_root

def get_package_scripts():
    """
    Get the path of the package scripts folder.
    """
    package_path = get_package_root() / "scripts"
    scripts = list(package_path.glob("*.py"))
    scripts = [ s.stem for s in scripts ]
    return scripts

def get_package_configs():
    """
    Get the path of the config directory.
    """
    pkg_conf = Path.home() / ".moneypot"
    return pkg_conf

def get_package_logs():
    """
    Get the path of the logs directory.
    """
    pkg_logs = get_package_root() / "logs"
    return pkg_logs

