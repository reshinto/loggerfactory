"""Loguru library wrapper"""
from typing import Any, Dict, Optional, Union
import loguru

from ..helpers.singletons import logcounter
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

    - self.logger: loguru.Logger = this is the Loguru library logger instance.

    - self.logger.add("logs/logfile.log") = this auto creates the log folder and logfile.log inside it.
                                            auto creation happens when the logger is initialized,
                                            or when unit tests are run.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize LoggerInterface, self variables and loguru library."""
        super().__init__(**kwargs)

        self.logger: loguru.Logger = loguru.logger
        self.logger.add("logs/logfile.log")

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
            self.logger.info(data)
        elif _level == LogLevels.DEBUG.value:
            self.logger.debug(data)
        elif _level == LogLevels.WARNING.value:
            self.logger.warning(data)
        elif _level == LogLevels.ERROR.value:
            self.logger.error(data)
        elif _level == LogLevels.CRITICAL.value:
            self.logger.critical(data)
        elif _level == LogLevels.EXCEPTION.value:
            self.logger.exception(data)
        else:
            check_log_level_value(level)

        logcounter.increment()
        self.logger.info(f"Total logs count: {logcounter.counter}")

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
