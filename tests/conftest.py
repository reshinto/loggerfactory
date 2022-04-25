import pytest
from _pytest.logging import caplog as _caplog
from loguru import logger


@pytest.fixture
def caplog(_caplog):
    handler_id = logger.add(_caplog.handler, format="{message} {extra}")
    yield _caplog
    logger.remove(handler_id)
