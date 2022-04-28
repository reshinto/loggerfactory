from elasticsearch import AsyncElasticsearch
from loguru import logger
import pytest
from src.loggingsfactory.loggers.asyncelk import AsyncElk


def test_async_elk_init_missing_appname_key():
    debug = False
    with pytest.raises(KeyError):
        AsyncElk(debug=debug)


def test_async_elk_init_missing_host_key():
    debug = False
    appname = "test"
    with pytest.raises(KeyError):
        AsyncElk(debug=debug, appname=appname)


def test_async_elk_init_missing_index_key():
    debug = False
    appname = "test"
    host = "https://localhost.com:9201"
    with pytest.raises(KeyError):
        AsyncElk(debug=debug, appname=appname, host=host)


def test_async_elk_init_missing_username_key():
    debug = False
    appname = "test"
    host = "https://localhost.com:9201"
    index = "appindex"
    with pytest.raises(KeyError):
        AsyncElk(debug=debug, appname=appname, host=host, index=index)


def test_async_elk_init_missing_pw_key():
    debug = False
    appname = "test"
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "user"
    with pytest.raises(KeyError):
        AsyncElk(
            debug=debug, appname=appname, host=host, index=index, username=username
        )


def test_async_elk_init():
    appname = "test"
    debug = True
    test = AsyncElk(appname=appname, debug=debug)
    assert isinstance(test, AsyncElk)

    debug = False
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "user"
    pw = "pw"
    test = AsyncElk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    assert isinstance(test, AsyncElk)


async def test_async_elk_async_log_wrong_level_type():
    logdata = "testabc"
    level = True

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = AsyncElk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    with pytest.raises(TypeError):
        await es.async_log(level, logdata)


async def test_async_elk_async_log_wrong_level_value():
    logdata = "testabc"
    level = "abc"

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = AsyncElk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    with pytest.raises(ValueError):
        await es.async_log(level, logdata)


async def test_async_elk_async_log_missing_arg():
    level = "abc"

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = AsyncElk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    with pytest.raises(TypeError):
        await es.async_log(level)


async def test_async_elk_async_log(mocker, caplog):
    logdata = "test123"
    level = "info"

    async def mock_log():
        logger.info(logdata)

    mocker.patch.context_manager(AsyncElasticsearch, "index", return_value=mock_log())

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = AsyncElk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    await es.async_log(level, logdata)
    assert (len(caplog.records)) == 1
    assert logdata in caplog.text


def test_async_elk_log():
    logdata = "test123"
    level = "info"

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = AsyncElk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    with pytest.raises(NotImplementedError):
        es.log(level, logdata)


async def test_async_elk_async_query(mocker):
    expected = "query"

    async def mock_query():
        return expected

    mocker.patch.context_manager(
        AsyncElasticsearch, "search", return_value=mock_query()
    )

    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = AsyncElk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    assert await es.async_query() == expected


def test_async_elk_query():
    appname = "abc"
    host = "https://localhost.com:9201"
    debug = False
    index = "appindex"
    username = "user"
    pw = "pw"

    es = AsyncElk(
        debug=debug, appname=appname, host=host, index=index, username=username, pw=pw
    )
    with pytest.raises(NotImplementedError):
        es.query()
