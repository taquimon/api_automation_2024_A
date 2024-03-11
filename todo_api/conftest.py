import logging

import pytest
import requests

from config.config import URL_TODO, HEADERS_TODO
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_project(request):

    LOGGER.debug("Create project fixture")
    environment = request.config.getoption("--env")
    LOGGER.critical("Environment selected: %s", environment)
    body_project = {
        "name": "Project from fixture"
    }
    url_project = URL_TODO+"/projects"
    response = requests.post(url_project, headers=HEADERS_TODO, data=body_project)
    LOGGER.info("Response from create project fixture: %s", response.json())
    return response.json()


def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )