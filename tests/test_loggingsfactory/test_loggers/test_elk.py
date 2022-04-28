from elasticsearch import Elasticsearch
from loguru import logger
import pytest
from src.loggingsfactory.loggers.elk import Elk


def test_elk_init_missing_appname_key():
    debug = False
    with pytest.raises(KeyError):
        Elk(debug=debug)


def test_elk_init_missing_host_key():
    debug = False
    appname = "test"
    with pytest.raises(KeyError):
        Elk(debug=debug, appname=appname)


def test_elk_init_missing_index_key():
    debug = False
    appname = "test"
    host = "https://localhost.com:9201"
    with pytest.raises(KeyError):
        Elk(debug=debug, appname=appname, host=host)


def test_elk_init_missing_username_key():
    debug = False
    appname = "test"
    host = "https://localhost.com:9201"
    index = "appindex"
    with pytest.raises(KeyError):
        Elk(debug=debug, appname=appname, host=host, index=index)


def test_elk_init_missing_pw_key():
    debug = False
    appname = "test"
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "user"
    with pytest.raises(KeyError):
        Elk(debug=debug, appname=appname, host=host, index=index, username=username)


def test_elk_init():
    appname = "test"
    debug = True
    test = Elk(appname=appname, debug=debug)
    assert isinstance(test, Elk)

    debug = False
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "user"
    pw = "pw"
    test = Elk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    assert isinstance(test, Elk)


def test_elk_log_wrong_level_type():
    logdata = "testabc"
    level = True

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = Elk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    with pytest.raises(TypeError):
        es.log(level, logdata)


def test_elk_log_wrong_level_value():
    logdata = "testabc"
    level = "abc"

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = Elk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    with pytest.raises(ValueError):
        es.log(level, logdata)


def test_elk_log_missing_arg():
    level = "abc"

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = Elk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    with pytest.raises(TypeError):
        es.log(level)


def test_elk_log(mocker, caplog):
    logdata = "test123"
    level = "info"

    def mock_log():
        logger.info(logdata)

    mocker.patch.context_manager(Elasticsearch, "index", return_value=mock_log())

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = Elk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    es.log(level, logdata)
    assert (len(caplog.records)) == 1
    assert logdata in caplog.text


async def test_elk_async_log():
    logdata = "test123"
    level = "info"

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = Elk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    with pytest.raises(NotImplementedError):
        await es.async_log(level, logdata)


def test_elk_query(mocker):
    expected = "query"

    def mock_query():
        return expected

    mocker.patch.context_manager(Elasticsearch, "search", return_value=mock_query())

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = Elk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    assert es.query() == expected


async def test_elk_async_query():
    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = Elk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    with pytest.raises(NotImplementedError):
        await es.async_query()
