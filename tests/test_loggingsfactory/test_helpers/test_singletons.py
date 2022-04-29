from src.loggingsfactory.helpers.singletons import LogCounter
from src.loggingsfactory.helpers.singletons import SetupLoguru


def test_logcounter():
    logcounter = LogCounter()
    assert isinstance(logcounter, LogCounter)
    assert logcounter.counter == 0
    logcounter.increment()
    assert logcounter.counter == 1


def test_setuploguru():

    logger = SetupLoguru()
    assert isinstance(logger, SetupLoguru)
