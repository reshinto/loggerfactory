from src.loggingsfactory.helpers.singletons import LogCounter


def test_logcounter():
    logcounter = LogCounter()
    assert isinstance(logcounter, LogCounter)
    assert logcounter.counter == 0
    logcounter.increment()
    assert logcounter.counter == 1
