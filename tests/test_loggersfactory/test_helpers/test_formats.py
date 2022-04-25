from datetime import datetime
import json
import pytest
from src.loggersfactory.helpers.formats import (
    _format_log_data,
    check_log_level,
    check_log_level_type,
    check_log_level_value,
    format_elk_query_payload,
    format_elk_url,
    format_log_data,
)


def test_format_elk_url():
    hostname = "localhost.com"
    expected = "https://b'':9201"
    config = {}
    assert format_elk_url(config) == expected
    expected = "https://localhost.com"
    config = {"host": expected}
    assert format_elk_url(config) == expected + ":9201"
    expected = "https://localhost.com:9201"
    config = {"host": expected}
    assert format_elk_url(config) == expected
    config = {"host": hostname}
    assert format_elk_url(config) == expected
    port = 111
    config = {"host": hostname, "port": port}
    assert format_elk_url(config) == "https://localhost.com:111"
    expected = "localhost.com"
    config = {"host": "https://localhost.com:9201"}
    assert format_elk_url(config, True) == expected
    config = {"host": hostname}
    assert format_elk_url(config, True) == expected


def test__format_log_data():
    level = "INFO"
    logdata = "test"
    date = "2020-01-01T00:00:00.000Z"
    appname = "test"
    version = "1.0.0"
    result = json.dumps(
        {
            "log": logdata,
            "version": version,
            "logger_level": level,
            "functional_name": "_multicall",
            "app_name": appname,
            "timestamp": date,
        }
    )
    assert (
        _format_log_data(level, logdata, date, appname, version, "", False, 0) == result
    )
    result = json.dumps(
        {
            "log": logdata,
            "version": version,
            "logger_level": level,
            "functional_name": "_hookexec",
            "app_name": appname,
            "timestamp": date,
        }
    )
    assert (
        _format_log_data(level, logdata, date, appname, version, "", False, 1) == result
    )
    result = json.dumps(
        {
            "log": logdata,
            "version": version,
            "logger_level": level,
            "functional_name": "test__format_log_data",
            "app_name": appname,
            "timestamp": date,
        }
    )
    assert (
        _format_log_data(level, logdata, date, appname, version, "", False, -2)
        == result
    )


def test__format_log_data_custom_func_name():
    level = "INFO"
    logdata = "test"
    date = "2020-01-01T00:00:00.000Z"
    custom_func_name = "myfunction"
    appname = "test"
    version = "1.0.0"
    result = json.dumps(
        {
            "log": logdata,
            "version": version,
            "logger_level": level,
            "functional_name": custom_func_name,
            "app_name": appname,
            "timestamp": date,
        }
    )
    assert (
        _format_log_data(
            level, logdata, date, appname, version, custom_func_name, False, 0
        )
        == result
    )
    result = json.dumps(
        {
            "log": logdata,
            "version": version,
            "logger_level": level,
            "functional_name": custom_func_name,
            "app_name": appname,
            "timestamp": date,
        }
    )
    assert (
        _format_log_data(
            level, logdata, date, appname, version, custom_func_name, False, 1
        )
        == result
    )


def test__format_log_data_custom_logdata():
    level = "INFO"
    logdata = json.dumps({"test": "custom log data"})
    assert _format_log_data(level, logdata, None, None, None, "", True, 0) == logdata
    assert _format_log_data(level, logdata, None, None, None, "", True, 1) == logdata


def test_format_log_data():
    class Test:
        def __init__(self):
            self.appname = "test"
            self.version = "1.0.0"

    self = Test()
    level = "INFO"
    logdata = "test"
    date = "2020-01-01T00:00:00.000Z"
    result = json.dumps(
        {
            "log": logdata,
            "version": self.version,
            "logger_level": level,
            "functional_name": "pytest_pyfunc_call",
            "app_name": self.appname,
            "timestamp": date,
        }
    )
    assert format_log_data(self, level, logdata, "", False, date, 0) == result
    result = json.dumps(
        {
            "log": logdata,
            "version": self.version,
            "logger_level": level,
            "functional_name": "_multicall",
            "app_name": self.appname,
            "timestamp": date,
        }
    )
    assert format_log_data(self, level, logdata, "", False, date, 1) == result
    result = json.dumps(
        {
            "log": logdata,
            "version": self.version,
            "logger_level": level,
            "functional_name": "test_format_log_data",
            "app_name": self.appname,
            "timestamp": date,
        }
    )
    assert format_log_data(self, level, logdata, "", False, date, -1) == result


def test_format_log_data_custom_func_name():
    class Test:
        def __init__(self):
            self.appname = "test"
            self.version = "1.0.0"

    self = Test()
    level = "INFO"
    logdata = "test"
    date = "2020-01-01T00:00:00.000Z"
    custom_func_name = "myfunction"
    result = json.dumps(
        {
            "log": logdata,
            "version": self.version,
            "logger_level": level,
            "functional_name": custom_func_name,
            "app_name": self.appname,
            "timestamp": date,
        }
    )
    assert (
        format_log_data(self, level, logdata, custom_func_name, False, date, 0)
        == result
    )
    result = json.dumps(
        {
            "log": logdata,
            "version": self.version,
            "logger_level": level,
            "functional_name": custom_func_name,
            "app_name": self.appname,
            "timestamp": date,
        }
    )
    assert (
        format_log_data(self, level, logdata, custom_func_name, False, date, 1)
        == result
    )


def test_format_log_data_custom_logdata():
    class Test:
        def __init__(self):
            self.appname = "test"
            self.version = "1.0.0"

    self = Test()
    level = "INFO"
    logdata = json.dumps({"test": "custom log data"})
    assert format_log_data(self, level, logdata, "", True, None, 0) == logdata
    assert format_log_data(self, level, logdata, "", True, None, 1) == logdata


def test_format_elk_query_payload():
    appname = "test"
    date = datetime.now().isoformat()
    payload = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "bool": {
                            "should": [{"match_phrase": {"app_name.keyword": appname}}],
                            "minimum_should_match": 1,
                        }
                    },
                    {
                        "range": {
                            "timestamp": {
                                "gte": "2021-09-24T02:58:43.647Z",
                                "lte": date,
                                "format": "strict_date_optional_time",
                            }
                        }
                    },
                ]
            }
        }
    }
    assert format_elk_query_payload(appname, date) == payload


def test_format_elk_query_payload_custom_payload():
    payload = {"test": "custom payload"}
    assert format_elk_query_payload("", "", payload) == payload


def test_check_log_level_type_typeerror():
    with pytest.raises(TypeError):
        check_log_level_type(True)


def test_check_log_level_type():
    assert check_log_level_type("INFO") is None


def test_check_log_level_value_valueerror():
    with pytest.raises(ValueError):
        check_log_level_value("abc")


def test_check_log_level_value():
    assert check_log_level_value("INFO") is None
    assert check_log_level_value("DEBUG") is None
    assert check_log_level_value("WARNING") is None
    assert check_log_level_value("ERROR") is None
    assert check_log_level_value("CRITICAL") is None
    assert check_log_level_value("EXCEPTION") is None


def test_check_log_level_valueerror():
    with pytest.raises(ValueError):
        check_log_level("abc")


def test_check_log_level_typeerror():
    with pytest.raises(TypeError):
        check_log_level(True)
    with pytest.raises(TypeError):
        check_log_level()


def test_check_log_level():
    assert check_log_level("INFO") is None
    assert check_log_level("DEBUG") is None
    assert check_log_level("WARNING") is None
    assert check_log_level("ERROR") is None
    assert check_log_level("CRITICAL") is None
    assert check_log_level("EXCEPTION") is None
