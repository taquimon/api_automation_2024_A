"""
(c) Copyright Jalasoft. 2024

conftest.py
    file that contains fixtures for tests
"""
import logging

import pytest

from config.config import URL_TODO
from entities.project import Project
from entities.section import Section
from entities.task import Task
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture(name="create_project")
def create_project_fixture(request):
    """
    Fixture to create a new project
    :param request:   Request object to get params for commandline
    """
    environment = request.config.getoption("--env")
    LOGGER.critical("Environment selected: %s", environment)
    LOGGER.debug("Create project fixture")
    project = Project()
    project_created, _ = project.create_project()
    project_id = project_created["body"]["id"]

    yield project_id
    delete_project(project_id, project)


@pytest.fixture(name="create_section")
def create_section(create_project):
    """
    Fixture to create section
    :param create_project:  Fixture with project created
    """
    LOGGER.debug("Create section fixture")
    section = Section()
    section_created, _ = section.create_section(create_project)
    id_section_created = section_created["body"]["id"]
    yield id_section_created


@pytest.fixture(name="create_task")
def create_task_fixture():
    """
    Fixture to create task
    """
    task = Task()
    task_created, _ = task.create_tasks()
    id_task_created = task_created["body"]["id"]
    yield id_task_created
    delete_task(id_task_created, task)


@pytest.fixture()
def get_project():
    """
    Fixture to get a project
    :return: str   return project id
    """
    rest_client = RestClient()
    response = rest_client.request("get", URL_TODO+"/projects")
    project_id = response["body"][1]["id"]
    LOGGER.debug("Project ID: %s", project_id)
    return project_id


@pytest.fixture()
def _test_log_name(request):
    """
    Fixture to Log the test names in logs
    :param request:     Object to get the test node name
    """
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)


def delete_project(project_id, project):
    """
    Fixture to delete project
    :param project_id:  str     project id to be deleted
    :param project:     object  project object
    """
    project.delete_project(project_id)


@pytest.fixture()
def create_comment(create_task):
    """
    Fixture to create comment
    :param create_task:     task id to be created the comment
    """
    LOGGER.debug("Task id: %s", create_task)
    body_comment = {
            "task_id": f"{create_task}",
            "content": "Need one bottle of milk",
        }
    rest_client = RestClient()
    url_comments = f"{URL_TODO}/comments"
    response = rest_client.request("post", url=url_comments, body=body_comment)
    id_comment_created = response["body"]["id"]
    yield id_comment_created
    delete_comment(id_comment_created, rest_client)


def delete_task(task_id, task):
    """
    Fixture to delete a task
    :param task_id:    str      Task id to be deleted
    :param task:       object   Task object
    """
    task.delete_task(task_id)


def delete_comment(comment_id, rest_client):
    """
    Method to delete a comment
    :param comment_id:      str     Comment id to be deleted
    :param rest_client:     object  Rest Client object to make calls
    """
    LOGGER.info("Cleanup comment...")
    url_delete_comment = f"{URL_TODO}/comments/{comment_id}"
    response = rest_client.request("delete", url=url_delete_comment)
    if response["status_code"] == 204:
        LOGGER.info("Comment Id: %s deleted", comment_id)


def pytest_addoption(parser):
    """
    PyTest method to get parameters from shell
    :param parser:  object  Parse object to manage the custom parameters
    """
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )
