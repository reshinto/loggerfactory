import json
import pytest
from src.loggingsfactory.loggers.loguru import Loguru


def test_loguru_init_missing_appname_key():
    with pytest.raises(KeyError):
        Loguru()
    debug = True
    with pytest.raises(KeyError):
        Loguru(debug=debug)


def test_loguru_init():
    appname = "test"
    test = Loguru(appname=appname)
    assert isinstance(test, Loguru)
    debug = True
    test = Loguru(debug=debug, appname=appname)
    assert isinstance(test, Loguru)


def test_loguru_log_missing_arg():
    appname = "test"
    level = True
    test = Loguru(appname=appname)
    with pytest.raises(TypeError):
        test.log(level)


def test_loguru_log_wrong_level_type():
    appname = "test"
    level = True
    logdata = "abc123"
    test = Loguru(appname=appname)
    with pytest.raises(TypeError):
        test.log(level, logdata)


def test_loguru_log_wrong_level_value():
    appname = "test"
    level = "abc"
    logdata = "abc123"
    test = Loguru(appname=appname)
    with pytest.raises(ValueError):
        test.log(level, logdata)


def test_loguru_log(caplog):
    appname = "test"
    logdata = "abc123"
    test = Loguru(appname=appname)
    level = "INFO"
    test.log(level, logdata)
    assert logdata in caplog.text
    assert level in caplog.text
    assert "test_loguru_log" in caplog.text
    level = "DEBUG"
    test.log(level, logdata)
    assert level in caplog.text
    level = "WARNING"
    test.log(level, logdata)
    assert level in caplog.text
    level = "CRITICAL"
    test.log(level, logdata)
    assert level in caplog.text
    level = "ERROR"
    test.log(level, logdata)
    assert level in caplog.text
    level = "EXCEPTION"
    test.log(level, logdata)
    assert level in caplog.text


def test_loguru_log_custom_func_name(caplog):
    appname = "test"
    logdata = "abc123"
    test = Loguru(appname=appname)
    custom_func_name = "myfunction"
    level = "INFO"
    test.log(level, logdata, custom_func_name)
    assert logdata in caplog.text
    assert level in caplog.text
    assert custom_func_name in caplog.text


def test_loguru_log_custom_logdata(caplog):
    appname = "test"
    logdata = json.dumps({"test": "abc123"})
    test = Loguru(appname=appname)
    level = "INFO"
    test.log(level, logdata, "", True)
    assert logdata in caplog.text
    assert level in caplog.text


async def test_loguru_async_log(caplog):
    appname = "test"
    logdata = "abc123"
    test = Loguru(appname=appname)
    level = "INFO"
    await test.async_log(level, logdata)
    assert logdata in caplog.text
    assert level in caplog.text
    assert "test_loguru_async_log" in caplog.text


def test_loguru_query():
    appname = "test"
    test = Loguru(appname=appname)
    assert test.query() is None


async def test_loguru_async_query():
    appname = "test"
    test = Loguru(appname=appname)
    assert await test.async_query() is None


def test_loguru_sql_query():
    appname = "test"
    test = Loguru(appname=appname)
    assert test.sql_query() is None
