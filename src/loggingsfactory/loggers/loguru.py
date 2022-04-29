"""Loguru library wrapper"""
from typing import Any, Dict, Optional, Union

from ..helpers.singletons import logcounter, logger
from ..constants.config import LogLevels
from ..helpers.formats import (
    format_log_data,
    check_log_level_type,
    check_log_level_value,
)
from ..loggers.interface import LoggerInterface


class Loguru(LoggerInterface):
    """
    Loguru library wrapper that inherits the LoggerInterface self variables and methods.

    This only support the 'log' and 'async_log' methods.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize LoggerInterface, self variables and loguru library."""
        super().__init__(**kwargs)

    def log(
        self,
        level: str,
        logdata: Union[str, Dict[str, Any]],
        custom_func_name: Optional[str] = "",
        use_custom_logdata: Optional[bool] = False,
        date: Optional[str] = None,
        _reduce_stack_level: Optional[int] = 0,
    ) -> None:
        """Override inherited method from LoggerInterface"""
        check_log_level_type(level)

        _level: str = level.upper()
        data: str = format_log_data(
            self,
            _level,
            logdata,
            custom_func_name,
            use_custom_logdata,
            date,
            _reduce_stack_level,
        )
        if _level == LogLevels.INFO.value:
            logger.info(data)
        elif _level == LogLevels.DEBUG.value:
            logger.debug(data)
        elif _level == LogLevels.WARNING.value:
            logger.warning(data)
        elif _level == LogLevels.ERROR.value:
            logger.error(data)
        elif _level == LogLevels.CRITICAL.value:
            logger.critical(data)
        elif _level == LogLevels.EXCEPTION.value:
            logger.exception(data)
        else:
            check_log_level_value(level)

        logcounter.increment()
        logger.info(f"Total logs count: {logcounter.counter}")

    async def async_log(
        self,
        level: str,
        logdata: Union[str, Dict[str, Any]],
        custom_func_name: Optional[str] = "",
        use_custom_logdata: Optional[bool] = False,
        date: Optional[str] = None,
    ) -> None:
        """Override inherited method from LoggerInterface"""
        self.log(level, logdata, custom_func_name, use_custom_logdata, date, 1)

    def query(self, *args, **kwargs) -> None:
        """Not used"""

    async def async_query(self, *args, **kwargs) -> None:
        """Not used"""

    def sql_query(self, *args, **kwargs) -> None:
        """Not used"""
