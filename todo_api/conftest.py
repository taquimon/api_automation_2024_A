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
    project_id = response.json()["id"]

    yield project_id
    delete_project(project_id, rest_client)


@pytest.fixture()
def create_section(create_project):

    LOGGER.debug("Create section fixture")

    body_section = {
        "project_id": f"{create_project}",
        "name": "Section from fixture"
    }
    url_section = URL_TODO+"/sections"
    rest_client = RestClient()
    response = rest_client.request("post", url_section, body=body_section)

    return response.json()


@pytest.fixture()
def create_task():
    content_task_body = {
        "content": "Task created from fixture",
        "due_string": "tomorrow at 12:00",
        "due_lang": "en",
        "priority": 4
    }
    url_tasks = URL_TODO + "/tasks"
    rest_client = RestClient()
    response = rest_client.request("post", url=url_tasks, body=content_task_body)
    id_task_created = response.json()["id"]
    yield id_task_created

@pytest.fixture()
def get_project():
    rest_client = RestClient()
    response = rest_client.request("get", URL_TODO+"/projects")
    project_id = response.json()[1]["id"]
    LOGGER.debug("Project ID: %s", project_id)
    return project_id


@pytest.fixture()
def test_log_name(request):
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)


def delete_project(project_id, rest_client):
    LOGGER.info("Cleanup project...")
    url_delete_project = f"{URL_TODO}/projects/{project_id}"
    response = rest_client.request("delete", url=url_delete_project)
    if response.status_code == 204:
        LOGGER.info("Project Id: %s deleted", project_id)


def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )