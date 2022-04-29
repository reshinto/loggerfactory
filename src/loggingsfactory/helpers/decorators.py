"""Decorator helper functions for logging"""
import functools
from types import FunctionType
from typing import Any, Dict, List
from elasticsearch import Elasticsearch, AsyncElasticsearch

from ..constants.config import BasicConfig, BoolConfig
from ..helpers.formats import format_elk_url
from ..helpers.singletons import logger


def print_retry_exception_msg(
    e: Any,
    retry_attempt: int,
    func: FunctionType,
    args: List[Any],
    kwargs: Dict[str, Any],
):
    """Print log error when retry failed"""
    logger.exception(
        "Exception has occurred with the following "
        + f"message: '{e}' "
        + "It was ignored and has occurred for "
        + f"'{retry_attempt}' times. "
        + f"Number of retries left: {BasicConfig.MAX_RETRIES.value - retry_attempt}."
        + "When attempting to run "
        + f"{repr(func)} with the following arguments: "
        + f"{args} keyword arguments: {kwargs}."
    )


def connect_elk(func):
    """
    Connect to Sync elasticsearch library.
    Use for Sync and class methods.
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        for retry_attempt in range(BasicConfig.MAX_RETRIES.value):
            try:
                self.es = Elasticsearch(
                    [format_elk_url(kwargs)],
                    use_ssl=BoolConfig.USE_SSL.value,
                    http_auth=(self.username, self.pw),
                    verify_certs=BoolConfig.VERIFY_CERTS.value,
                )
                break
            except Exception as e:
                print_retry_exception_msg(e, retry_attempt + 1, func, args, kwargs)
        return result

    return wrapper


def connect_async_elk(func):
    """
    Connect to Async elasticsearch library.
    Use for Async and class methods.
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        for retry_attempt in range(BasicConfig.MAX_RETRIES.value):
            try:
                self.es = AsyncElasticsearch(
                    [format_elk_url(kwargs)],
                    use_ssl=BoolConfig.USE_SSL.value,
                    http_auth=(self.username, self.pw),
                    verify_certs=BoolConfig.VERIFY_CERTS.value,
                    max_retries=BasicConfig.MAX_RETRIES.value,
                    retry_on_timeout=BoolConfig.RETRY_ON_TIMEOUT.value,
                )
                break
            except Exception as e:
                print_retry_exception_msg(e, retry_attempt + 1, func, args, kwargs)
        return result

    return wrapper
