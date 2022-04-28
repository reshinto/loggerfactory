"""AsyncElasticsearch library wrapper"""
from datetime import datetime
from typing import Any, Dict, Optional, Union

from ..helpers.decorators import connect_async_elk
from ..constants.config import BasicConfig
from ..helpers.formats import (
    check_log_level,
    format_elk_query_payload,
    format_log_data,
)
from ..loggers.interface import LoggerInterface


class AsyncElk(LoggerInterface):
    """
    Async Elasticsearch library wrapper that inherits the LoggerInterface self variables and methods.

    Connects to AsyncElasticsearch using the 'connect_async_elk' decorator and when upon initializing.

    This only support Asynchronous methods.

    sql_query: method = this is inherited from LoggerInterface. But only supports synchronous method.
    """

    @connect_async_elk
    def __init__(self, **kwargs) -> None:
        """Initialize LoggerInterface, self variables and AsyncElasticsearch library."""
        super().__init__(**kwargs)

    def log(self, *args, **kwargs):
        """Not used"""
        raise NotImplementedError("Please use 'async_log' method instead.")

    async def async_log(
        self,
        level: str,
        logdata: Union[str, Dict[str, Any]],
        custom_func_name: Optional[str] = "",
        use_custom_logdata: Optional[bool] = False,
        date: Optional[str] = None,
        _reduce_stack_level: Optional[int] = 0,
    ) -> None:
        """Override inherited method from LoggerInterface"""
        check_log_level(level)

        await self.es.index(
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

    def query(self, *args, **kwargs) -> Any:
        """Not used"""
        raise NotImplementedError("Please use 'async_query' method instead.")

    async def async_query(
        self,
        custompayload: Optional[Dict[str, Any]] = None,
        size: int = BasicConfig.DEFAULT_SIZE.value,
        cache: bool = True,
    ) -> None:
        """Override inherited method from LoggerInterface"""
        return await self.es.search(
            index=self.index,
            size=size,
            body=format_elk_query_payload(
                self.appname, datetime.now().isoformat(), custompayload
            ),
            request_cache=cache,
        )
