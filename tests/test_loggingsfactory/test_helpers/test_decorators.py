from src.loggingsfactory.helpers.decorators import (
    connect_async_elk,
    connect_elk,
    print_retry_exception_msg,
)


def test_print_retry_exception_msg(caplog):
    expected = "testabc"

    def test():
        pass

    print_retry_exception_msg(Exception(expected), 1, test, [], {})
    assert "Exception has occurred" in caplog.text
    assert expected in caplog.text
    assert len(caplog.records) == 1


def test_connect_elk_debug_true():
    class MockLogger:
        @connect_elk
        def __init__(self, **kwargs):
            pass

    debug = True
    result = MockLogger(debug=debug)
    assert result.__dict__.get("es") is None


def test_connect_elk_debug_false():
    from elasticsearch import Elasticsearch

    class MockLogger:
        @connect_elk
        def __init__(self, **kwargs):
            self.username = kwargs.get("username")
            self.pw = kwargs.get("pw")

    debug = False
    host = "https://localhost.com:9201"
    username = "user"
    pw = "pw"
    result = MockLogger(debug=debug, host=host, username=username, pw=pw)
    assert str(result.__dict__.get("es")) == str(Elasticsearch([host]))


def test_connect_async_elk_debug_true():
    class MockLogger:
        @connect_async_elk
        def __init__(self, **kwargs):
            pass

    debug = True
    result = MockLogger(debug=debug)
    assert result.__dict__.get("es") is None


def test_connect_async_elk_debug_false():
    from elasticsearch import AsyncElasticsearch

    class MockLogger:
        @connect_async_elk
        def __init__(self, **kwargs):
            self.username = kwargs.get("username")
            self.pw = kwargs.get("pw")

    debug = False
    host = "https://localhost.com:9201"
    username = "user"
    pw = "pw"
    result = MockLogger(debug=debug, host=host, username=username, pw=pw)
    assert str(result.__dict__.get("es")) == str(AsyncElasticsearch([host]))
