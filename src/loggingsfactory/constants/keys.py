"""Logger most commonly used keys"""
from enum import Enum


class LoggerKeys(Enum):
    """Basic logger keys to be declared during initialization"""

    DEBUG = "debug"
    ASYNC = "useasync"
    HOST = "host"
    USERNAME = "username"
    PW = "pw"
    INDEX = "index"
    APPNAME = "appname"
    VERSION = "version"
    PORT = "port"
