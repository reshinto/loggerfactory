import pytest
from src.loggersfactory.loggers.interface import LoggerInterface


def test_loggerinterface_abstract_methods_undeclared():
    with pytest.raises(TypeError):
        LoggerInterface()


class MockLogger(LoggerInterface):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def log(self):
        pass

    async def async_log(self):
        pass

    def query(self):
        pass

    async def async_query(self):
        pass


def test_loggerinterface_init_missing_appname_key():
    with pytest.raises(KeyError):
        MockLogger()


def test_loggerinterface_init_missing_host_key():
    appname = "test"
    debug = False
    with pytest.raises(KeyError):
        MockLogger(appname=appname, debug=debug)


def test_loggerinterface_init_missing_index_key():
    appname = "test"
    debug = False
    host = "https://localhost.com:9201"
    index = "appindex"
    with pytest.raises(KeyError):
        MockLogger(appname=appname, debug=debug, host=host, index=index)


def test_loggerinterface_init_missing_username_key():
    appname = "test"
    debug = False
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "user"
    with pytest.raises(KeyError):
        MockLogger(
            appname=appname, debug=debug, host=host, index=index, username=username
        )


def test_loggerinterface_init_missing_pw_key():
    appname = "test"
    debug = False
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "user"
    with pytest.raises(KeyError):
        MockLogger(
            appname=appname, debug=debug, host=host, index=index, username=username
        )


def test_loggerinterface_init():
    appname = "test"
    debug = True
    test = MockLogger(appname=appname, debug=debug)
    assert isinstance(test, MockLogger)
    debug = False
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "user"
    pw = "pw"
    test = MockLogger(
        appname=appname, debug=debug, host=host, index=index, username=username, pw=pw
    )
    assert isinstance(test, MockLogger)


def test_loggerinterface_sql_query_debug_true():
    appname = "test"
    debug = True
    test = MockLogger(appname=appname, debug=debug)
    query = "query"
    assert test.sql_query(query) is None


def test_loggerinterface_sql_query(monkeypatch):
    appname = "test"
    debug = False
    host = "https://localhost.com:9201"
    index = "appindex"
    username = "user"
    pw = "pw"
    query = "query"

    class MockConnect:
        def __aenter__(self):
            return self

        def __aexit__(self, *error_info):
            return self

        def close(self):
            return "close"

    def mock_client_connect(self, *args, **kwargs):
        return MockConnect()

    monkeypatch.setattr("es.elastic.api.Connection", mock_client_connect)

    class MockPandas:
        def __aenter__(self):
            return self

        def __aexit__(self, *error_info):
            return self

        def read_sql(self, *args, **kwargs):
            return "mock pandas"

    def mock_client_pandas(self, *args, **kwargs):
        return MockPandas().read_sql(query)

    monkeypatch.setattr("pandas.read_sql", mock_client_pandas)
    test = MockLogger(
        appname=appname, debug=debug, host=host, index=index, username=username, pw=pw
    )

    assert test.sql_query(query) == "mock pandas"
