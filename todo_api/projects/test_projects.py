import logging

import pytest

from config.config import URL_TODO, MAX_PROJECTS
from entities.project import Project
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestProjects:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_projects = f"{URL_TODO}/projects"
        cls.list_projects = []
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()

    @pytest.mark.project
    def test_get_all_projects(self, test_log_name):
        """
        Test get all projects
        :param test_log_name:   fixture to log the Start and Complete test logs
        """

        response = self.rest_client.request("get", url=self.url_projects)
        self.validate.validate_response(response, "get_all_projects")

    def test_create_project(self, test_log_name):
        """

        :param test_log_name:   fixture to log the Start and Complete test logs
        """
        body_project = {
            "name": "Buy Milk"
        }
        response = self.rest_client.request("post", url=self.url_projects, body=body_project)

        id_project_created = response["body"]["id"]
        self.list_projects.append(id_project_created)

        self.validate.validate_response(response, "create_project")

    def test_delete_project(self, create_project, test_log_name):

        url_todo = f"{self.url_projects}/{create_project}"
        LOGGER.debug("URL to delete: %s", url_todo)

        response = self.rest_client.request("delete",url=url_todo)

        self.validate.validate_response(response, "delete_project")

    def test_update_project(self, create_project, test_log_name):

        LOGGER.debug("Project to update: %s", create_project)
        url_todo_update = f"{self.url_projects}/{create_project}"
        body_project = {
            "name": "Update project"
        }
        response = self.rest_client.request("post", url=url_todo_update, body=body_project)

        # add to list of projects to be deleted in cleanup
        self.list_projects.append(create_project)
        self.validate.validate_response(response, "update_project")

    @pytest.mark.functional
    def test_max_number_of_projects(self, test_log_name):
        """
        Test max number of projects can be created, an error should be returned
        :param test_log_name:
        """
        response = self.rest_client.request("get", url=self.url_projects)
        number_of_projects = len(response["body"])
        LOGGER.debug("Number of current projects: %s", number_of_projects)
        project = Project()
        for index in range(number_of_projects, MAX_PROJECTS):
            body_project = {
                "name": f"Project {index}"
            }
            project_created, _ = project.create_project(body=body_project)
            project_id = project_created["body"]["id"]
            self.list_projects.append(project_id)

        response, _ = project.create_project()

        assert response["status_code"] == 403

    @classmethod
    def teardown_class(cls):
        """
        Delete all projects used in test
        """
        LOGGER.info("Cleanup projects...")
        for id_project in cls.list_projects:
            url_delete_project = f"{URL_TODO}/projects/{id_project}"
            response = cls.rest_client.request("delete", url=url_delete_project)
            if response["status_code"] == 204:
                LOGGER.info("Project Id: %s deleted", id_project)
