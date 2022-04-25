"""Elasticsearch library wrapper"""
from datetime import datetime
from typing import Any, Dict, Optional, Union

from ..constants.config import BasicConfig
from ..helpers.decorators import connect_elk
from ..helpers.formats import (
    check_log_level,
    format_elk_query_payload,
    format_log_data,
)
from ..loggers.interface import LoggerInterface


class Elk(LoggerInterface):
    """
    Elasticsearch library wrapper that inherits the LoggerInterface self variables and methods.

    Connects to Elasticsearch using the 'connect_elk' decorator and when upon initializing.

    This only support synchronous methods.

    sql_query: method = this is inherited from LoggerInterface.
    """

    @connect_elk
    def __init__(self, **kwargs) -> None:
        """Initialize LoggerInterface, self variables and Elasticsearch library."""
        super().__init__(**kwargs)

    def log(
        self,
        level: str,
        logdata: Union[str, Dict[str, Any]],
        custom_func_name: Optional[str] = "",
        use_custom_logdata: Optional[bool] = False,
        date: Optional[str] = None,
        _reduce_stack_level: Optional[int] = 0,
    ):
        """Override inherited method from LoggerInterface"""
        check_log_level(level)

        self.es.index(
            index=self.index,
            document=format_log_data(
                self,
                level.upper(),
                logdata,
                custom_func_name,
                use_custom_logdata,
                date,
                _reduce_stack_level,
            ),
        )

    async def async_log(self, *args, **kwargs) -> None:
        """Not used"""
        raise NotImplementedError("Please use 'log' method instead.")

    def query(
        self,
        custompayload: Optional[Dict[str, Any]] = None,
        size: int = BasicConfig.DEFAULT_SIZE.value,
        cache: bool = True,
    ) -> Any:
        """Override inherited method from LoggerInterface"""
        return self.es.search(
            index=self.index,
            size=size,
            body=format_elk_query_payload(
                self.appname, datetime.now().isoformat(), custompayload
            ),
            request_cache=cache,
        )

    async def async_query(self, *args, **kwargs) -> None:
        """Not used"""
        raise NotImplementedError("Please use 'query' method instead.")
