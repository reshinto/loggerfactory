import pytest
from elasticsearch import Elasticsearch, AsyncElasticsearch
from loguru import logger
from src.loggingsfactory.loggers.asyncelk import AsyncElk
from src.loggingsfactory.loggers.elk import Elk
from src.loggingsfactory.loggers.loguru import Loguru
from src.loggingsfactory.logging import Loggers


def test_loggers_loguru_missing_appname():
    with pytest.raises(KeyError):
        Loggers()


def test_loggers_loguru():
    appname = "test"
    test = Loggers(appname=appname)
    assert isinstance(test, Loguru)


def test_loggers_elk_with_missing_host_key():
    appname = "test"
    debug = False
    with pytest.raises(KeyError):
        Loggers(appname=appname, debug=debug)


def test_loggers_elk_with_missing_index_key():
    appname = "test"
    debug = False
    host = "https://localhost.com:9201"
    with pytest.raises(KeyError):
        Loggers(appname=appname, debug=debug, host=host)


def test_loggers_elk_with_missing_username_key():
    appname = "test"
    debug = False
    host = "https://localhost.com:9201"
    index = "appindex"
    with pytest.raises(KeyError):
        Loggers(appname=appname, debug=debug, host=host, index=index)


def test_loggers_elk_with_missing_pw_key():
    appname = "test"
    debug = False
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "username"
    with pytest.raises(KeyError):
        Loggers(appname=appname, debug=debug, host=host, index=index, username=username)


def test_loggers_elk(mocker, caplog):
    appname = "test"
    debug = False
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "username"
    pw = "pw"
    es = Loggers(
        appname=appname, debug=debug, host=host, index=index, username=username, pw=pw
    )

    logdata = "test123"
    level = "info"

    def mock_log():
        logger.info(logdata)

    mocker.patch.context_manager(Elasticsearch, "index", return_value=mock_log())
    es.log(level, logdata)
    assert logdata in caplog.text
    assert isinstance(es, Elk)


def test_loggers_async_elk_with_missing_host_key():
    appname = "test"
    debug = False
    useasync = True
    with pytest.raises(KeyError):
        Loggers(appname=appname, debug=debug, useasync=useasync)


def test_loggers_async_elk_with_missing_index_key():
    appname = "test"
    debug = False
    useasync = True
    host = "https://localhost.com:9201"
    with pytest.raises(KeyError):
        Loggers(appname=appname, debug=debug, host=host, useasync=useasync)


def test_loggers_async_elk_with_missing_username_key():
    appname = "test"
    debug = False
    useasync = True
    host = "https://localhost.com:9201"
    index = "appindex"
    with pytest.raises(KeyError):
        Loggers(appname=appname, debug=debug, host=host, index=index, useasync=useasync)


def test_loggers_async_elk_with_missing_pw_key():
    appname = "test"
    debug = False
    useasync = True
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "username"
    with pytest.raises(KeyError):
        Loggers(
            appname=appname,
            debug=debug,
            host=host,
            index=index,
            username=username,
            useasync=useasync,
        )


async def test_loggers_async_elk(mocker, caplog):
    appname = "test"
    debug = False
    useasync = True
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "username"
    pw = "pw"
    es = Loggers(
        appname=appname,
        debug=debug,
        host=host,
        index=index,
        username=username,
        pw=pw,
        useasync=useasync,
    )

    logdata = "test123"
    level = "info"

    async def mock_log():
        logger.info(logdata)

    mocker.patch.context_manager(AsyncElasticsearch, "index", return_value=mock_log())
    await es.async_log(level, logdata)
    assert logdata in caplog.text
    assert isinstance(es, AsyncElk)
