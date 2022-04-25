"""Helper functions"""
from datetime import datetime
import json
import inspect
from collections.abc import Mapping
from typing import Any, Dict, Optional, Union
from urllib.parse import urlparse

from ..constants.config import LOG_LEVELS, BasicConfig, StringConfig
from ..constants.keys import LoggerKeys


def format_elk_url(config: Dict[str, Any], use_es_db: bool = False) -> str:
    """
    Return the correct elk url format for different environments and elk libraries.
    Supports https://elasticsearch.com:9201, https://elasticsearch.com, elasticsearch.com
    """
    raw_host: Any = urlparse(config.get(LoggerKeys.HOST.value))
    host: str = raw_host.hostname or raw_host[BasicConfig.URLPARSE_PATH_INDEX.value]
    port: str = config.get(LoggerKeys.PORT.value) or BasicConfig.PORT.value
    return host if use_es_db else f"{StringConfig.SCHEME.value}://{host}:{port}"


def _format_log_data(*args: Union[str, bool, Mapping]) -> str:
    """
    Format or return custom format of log data

    requires:
      level: str = one of the LogLevel member
      logdata: str or dict = default log data, or entire custom log format data
      date: str = date and time log was created
      appname: str = app name
      version: str = log version
      custom_func_name: str = by default name of the function that uses the logging will be used.
                              Adding this value will allow custom naming of the function name.
      use_custom_logdata: bool = if False use default logdata format,
                                 if True use custom logdata format.
    """
    (
        level,
        logdata,
        date,
        appname,
        version,
        custom_func_name,
        use_custom_logdata,
        _reduce_stack_level,
    ) = args
    data: str = json.dumps(logdata) if isinstance(logdata, Mapping) else logdata

    if use_custom_logdata:
        return data

    functionname: str = (
        custom_func_name
        or inspect.stack()[
            BasicConfig.FUNCTION_LOCATION_INDEX.value + _reduce_stack_level
        ][BasicConfig.FUNCTION_NAME_INDEX.value]
    )

    return json.dumps(
        {
            "log": data,
            "version": version,
            "logger_level": level,
            "functional_name": functionname,
            "app_name": appname,
            "timestamp": date,
        }
    )


def format_log_data(self, *args: Union[str, bool, Mapping]) -> str:
    """
    Format or return custom format of log data

    Requires:
        level: str = one of the LogLevel member
        logdata: str or dict = default log data, or entire custom log format data
        version: str = log version
        custom_func_name: str = by default name of the function that uses the logging will be used.
                                Adding this value will allow custom naming of the function name.
        use_custom_logdata: bool = if False use default logdata format,
                                   if True use custom logdata format.
    """
    (
        level,
        logdata,
        custom_func_name,
        use_custom_logdata,
        custom_date,
        _reduce_stack_level,
    ) = args
    date: str = custom_date or datetime.now().isoformat()
    return _format_log_data(
        level,
        logdata,
        date,
        self.appname,
        self.version,
        custom_func_name,
        use_custom_logdata,
        _reduce_stack_level,
    )


def format_elk_query_payload(
    appname: str, current_datetime: str, payload: Optional[Dict[str, Any]] = None
):
    """Set and get the standard payload required for the elk search"""
    if payload:
        return payload

    return {
        "query": {
            "bool": {
                "filter": [
                    {
                        "bool": {
                            "should": [{"match_phrase": {"app_name.keyword": appname}}],
                            "minimum_should_match": 1,
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": "2021-09-24T02:58:43.647Z",
                                "lte": current_datetime,
                                "format": "strict_date_optional_time",
                            }
                        }
                    },
                ]
            }
        }
    }


def check_log_level_type(level: Any) -> None:
    """
    Check if the log level type is valid
    """
    if not isinstance(level, str):
        raise TypeError(f"Log level must be a string, not {type(level)}")


def check_log_level_value(level: str) -> None:
    """
    Check if the log level value is valid
    """
    if level.upper() not in LOG_LEVELS:
        raise ValueError(f"Log level must be one of {str(LOG_LEVELS)}")


def check_log_level(level: Any) -> None:
    """
    Check if level value is a valid string data type.
    Check if level value is a valid value type in accordance with the LogLevel.
    """
    check_log_level_type(level)
    check_log_level_value(level)
