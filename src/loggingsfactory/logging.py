"""Logging Factory class that generates Loguru, Elasticsearch, or AsyncElasticsearch class"""
from typing import Union

from .constants.keys import LoggerKeys
from .loggers.elk import Elk
from .loggers.asyncelk import AsyncElk
from .loggers.loguru import Loguru


class Loggers(Loguru):
    """
    The main loggers API which should be used.

    Methods must follow the interface format.
    Please refer to the interface class for available methods.

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

    def __new__(cls, **kwargs) -> Union[Loguru, Elk, AsyncElk]:
        """
        Depending on the debug and useasync key value pairs,
        will return a Loguru, Elk, or AsyncElk class.

        - debug: bool = set to True by default and will use Loguru logger.
                        If set to False, will use the ELK or AsyncElk logger.

        - useasync: bool = set to False by default and will use Elk logger.
                           If set to True, will use the AsyncElk logger.
                           Requires debug to be False.
        """
        debug: bool = (
            True
            if kwargs.get(LoggerKeys.DEBUG.value) is None
            else kwargs.get(LoggerKeys.DEBUG.value)
        )
        if debug:
            return Loguru(**kwargs)

        if kwargs.get(LoggerKeys.ASYNC.value):
            return AsyncElk(**kwargs)

        return Elk(**kwargs)
