import pytest

import logging

import pytest

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def fixture_example(request):

    LOGGER.debug("Fixture example")
    environment = request.config.getoption("--env")
    LOGGER.critical("Environment selected: %s", environment)

    return environment


def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )