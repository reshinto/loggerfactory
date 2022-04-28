"""Logging interface to enforce all logger wrappers to follow the same format"""
from typing import Any, Dict, Optional, Union
import abc
import pandas as pd
from pandas.core.api import DataFrame
from es.elastic.api import connect
from es.baseapi import BaseConnection

from ..constants.config import BasicConfig, BoolConfig, StringConfig
from ..constants.keys import LoggerKeys
from ..helpers.formats import format_elk_url


class LoggerInterface(abc.ABC):
    """
    The loggers interface used for all logger types.

    All parent classes must follow this LoggerInterface format.

    Basic required keys for all logger types:
        - appname: str = name of app (e.g.: samapi, argapi, etc.)
        - debug: bool = set to True by default.
                        If set to False, will use the ELK or AsyncElk logger.
        - useasync: bool = set to False by default.
                           If set to True, will use the AsyncElk logger.
                           However, debug must be False to use this.

    Elasticsearch and AsyncElasticsearch required keys:
        - host: str = hostname of the ELK server
                      supports https://elasticsearch.com:9201, https://elasticsearch.com, elasticsearch.com
        - index: str = index name of the ELK server
        - username: str = username of the ELK server
        - pw: str = pw of the ELK server
        - port: int = port of the ELK server, default is 9201

    Optional keys:
        - version: str = log version, default is 1.0
    """

    def __init__(self, **kwargs) -> None:
        # Required keys
        self.appname: str = kwargs[LoggerKeys.APPNAME.value]

        # Optional keys
        self.debug: bool = (
            True
            if kwargs.get(LoggerKeys.DEBUG.value) is None
            else kwargs.get(LoggerKeys.DEBUG.value)
        )
        self.version: str = (
            kwargs.get(LoggerKeys.VERSION.value) or StringConfig.VERSION.value
        )

        # elasticsearch keys
        self.config: Dict[str, Any] = kwargs
        if not self.debug:
            self.host: str = kwargs[LoggerKeys.HOST.value]
            self.index: str = kwargs[LoggerKeys.INDEX.value]
            self.username: str = kwargs[LoggerKeys.USERNAME.value]
            self.pw: Any = kwargs[LoggerKeys.PW.value]

    @abc.abstractmethod
    def log(
        self,
        level: str,
        logdata: Union[str, Dict[str, Any]],
        custom_func_name: Optional[str] = None,
        use_custom_logdata: Optional[bool] = None,
        date: Optional[str] = None,
        _reduce_stack_level: Optional[int] = 0,
    ) -> None:
        """
        Log data to the appropriate loggers.

        - level: str = accept log level that are declared in the LogLevels class
                     DEBUG, INFO, WARNING, ERROR, CRITICAL, EXCEPTION

        - logdata: Union[str, Dict[str, Any]] = data to be logged
                                                Dictionary formats will be auto converted into a string
                                                This will use the default logging format by default.
                                                Set use_custom_logdata to True to use custom logging format.

        - custom_func_name: Optional[str] = By default, the name of the function that is calling the log function will be used.
                                            If you want to use a custom name, set this to the custom name.

        - use_custom_logdata: Optional[bool] = set to True to use custom logging format.
                                               If set to True, logdata can use it's own format.
                                               All data will be auto converted into a string data format.
        - date: str = date is auto set. Use this to override the auto date and time format.

        - _reduce_stack_level: int = do not touch this.
                                     Required for auto detecting name of the function that is calling the log function.
        """

    @abc.abstractmethod
    async def async_log(
        self,
        level: str,
        logdata: Union[str, Dict[str, Any]],
        custom_func_name: Optional[str] = None,
        use_custom_logdata: Optional[bool] = None,
        date: Optional[str] = None,
    ) -> None:
        """
        Async log data to the appropriate loggers.

        - level: str = accept log level that are declared in the LogLevels class
                     DEBUG, INFO, WARNING, ERROR, CRITICAL, EXCEPTION

        - logdata: Union[str, Dict[str, Any]] = data to be logged
                                                Dictionary formats will be auto converted into a string
                                                This will use the default logging format by default.
                                                Set use_custom_logdata to True to use custom logging format.

        - custom_func_name: Optional[str] = By default, the name of the function that is calling the log function will be used.
                                            If you want to use a custom name, set this to the custom name.

        - use_custom_logdata: Optional[bool] = set to True to use custom logging format.
                                               If set to True, logdata can use it's own format.
                                               All data will be auto converted into a string data format.

        - date: str = date is auto set. Use this to override the auto date and time format.
        """

    @abc.abstractmethod
    def query(
        self, custompayload: Optional[Dict[str, Any]], size: int, cache: bool
    ) -> Any:
        """
        Make query to Elasticsearch.

        - custompayload: Optional[Dict[str, Any]] = custom payload to be sent to the search the Elasticsearch server.
                                                    If not set, will use the default payload.

        - size: int = number of results to be returned.
                      If not set, will use the default size of 10,000.

        - cache: bool = set to True to cache the query.
                        If not set, will use the default True value.
        """

    @abc.abstractmethod
    async def async_query(
        self, custompayload: Optional[Dict[str, Any]], size: int, cache: bool
    ) -> Any:
        """
        Make query to AsyncElasticsearch.

        - custompayload: Optional[Dict[str, Any]] = custom payload to be sent to the search the Elasticsearch server.
                                                    If not set, will use the default payload.
                                                    Refer to format_elk_query_payload for an example.

        - size: int = number of results to be returned.
                      If not set, will use the default size of 10,000.

        - cache: bool = set to True to cache the query.
                        If not set, will use the default True value.
        """

    def sql_query(self, query: str, **kwargs) -> DataFrame:
        """
        Make query to elasticsearch-dbapi

        - query: str = query to be sent to the elasticsearch-dbapi server.
                       Query format is in SQL.
        """
        if self.debug:
            return None

        conn: BaseConnection = connect(
            host=format_elk_url(self.config, BoolConfig.USE_ES_DB.value),
            port=self.config.get(LoggerKeys.PORT.value) or BasicConfig.PORT.value,
            scheme=StringConfig.SCHEME.value,
            user=self.username,
            password=self.pw,
            verify_certs=BoolConfig.VERIFY_CERTS.value,
        )
        data: DataFrame = pd.read_sql(query, kwargs.get("conn"))
        conn.close()
        return data
