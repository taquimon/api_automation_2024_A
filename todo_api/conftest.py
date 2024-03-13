import logging

import pytest
import requests

from config.config import URL_TODO, HEADERS_TODO
from helpers.rest_client import RestClient
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
    rest_client = RestClient()
    response = rest_client.request("post", url_project, body=body_project)

    return response.json()


@pytest.fixture()
def create_section(get_project):

    LOGGER.debug("Create section fixture")

    body_section = {
        "project_id": f"{get_project}",
        "name": "Section from fixture"
    }
    url_section = URL_TODO+"/sections"
    rest_client = RestClient()
    response = rest_client.request("post", url_section, body=body_section)

    return response.json()


@pytest.fixture()
def get_project():
    rest_client = RestClient()
    response = rest_client.request("get", URL_TODO+"/projects")
    project_id = response.json()[1]["id"]
    LOGGER.debug("Project ID: %s", project_id)
    return project_id


def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )