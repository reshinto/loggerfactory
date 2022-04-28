"""Logger related configurations"""
from enum import IntEnum, Enum, Flag
from typing import List


class BasicConfig(IntEnum):
    """Basic configuration"""

    FUNCTION_LOCATION_INDEX = 3
    FUNCTION_NAME_INDEX = 3
    URLPARSE_PATH_INDEX = 2
    MAX_RETRIES = 10
    TIMEOUT = 30
    MAX_SIZE = 25
    PORT = 9201
    DEFAULT_SIZE = 10000


class BoolConfig(Flag):
    """Bool configuration"""

    USE_SSL = False
    VERIFY_CERTS = False
    CACHE = True
    USE_ES_DB = True
    RETRY_ON_TIMEOUT = True


class StringConfig(Enum):
    """String configuration"""

    VERSION = "1.0"
    SCHEME = "https"
    NUM_OF_DECORATORS = "num_of_decorators"


class LogLevels(Enum):
    """Supported log levels"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    EXCEPTION = "EXCEPTION"


LOG_LEVELS: List[str] = [level.value for level in LogLevels]
