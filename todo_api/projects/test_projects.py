import logging

import pytest

from config.config import URL_TODO
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestProjects:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_projects = f"{URL_TODO}/projects"
        cls.list_projects = []
        cls.rest_client = RestClient()
        # call method first token refresh_token if needed
        # call second method using token to generate access_token if needed

    @pytest.mark.project
    def test_get_all_projects(self):

        response = self.rest_client.request("get", url=self.url_projects)

        assert response.status_code == 200, "wrong status code, expected 200"

    def test_create_project(self):

        body_project = {
            "name": "Buy Milk"
        }
        response = self.rest_client.request("post", url=self.url_projects, body=body_project)

        id_project_created = response.json()["id"]
        self.list_projects.append(id_project_created)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_delete_project(self, create_project):
        id_project_delete = create_project["id"]
        url_todo = f"{self.url_projects}/{id_project_delete}"
        LOGGER.debug("URL to delete: %s", url_todo)

        response = self.rest_client.request("delete",url=url_todo)

        assert response.status_code == 204, "wrong status code, expected 204"

    def test_update_project(self, create_project):
        id_project_update = create_project["id"]
        LOGGER.debug("Project to update: %s", id_project_update)
        url_todo_update = f"{self.url_projects}/{id_project_update}"
        body_project = {
            "name": "Update project"
        }
        response = self.rest_client.request("post", url=url_todo_update, body=body_project)

        # add to list of projects to be deleted in cleanup
        self.list_projects.append(id_project_update)
        assert response.status_code == 200, "wrong status code, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        Delete all projects used in test
        """
        LOGGER.info("Cleanup projects...")
        for id_project in cls.list_projects:
            url_delete_project = f"{URL_TODO}/projects/{id_project}"
            response = cls.rest_client.request("delete", url=url_delete_project)
            if response.status_code == 204:
                LOGGER.info("Project Id: %s deleted", id_project)
