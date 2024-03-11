import logging

import requests

from config.config import HEADERS_TODO, URL_TODO
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestProjects:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_projects = f"{URL_TODO}/projects"
        cls.list_projects = []
        # call method first token refresh_token if needed
        # call second method using token to generate access_token if needed

    def test_get_all_projects(self):

        response = requests.get(url=self.url_projects, headers=HEADERS_TODO)

        LOGGER.info("Response from get all projects: %s", response.json())

        LOGGER.info("Status Code: %s", response.status_code)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_create_project(self):

        body_project = {
            "name": "Buy Milk"
        }
        response = requests.post(url=self.url_projects, headers=HEADERS_TODO, data=body_project)
        LOGGER.info("Response from create project: %s", response.json())
        LOGGER.info("Status Code: %s", response.status_code)
        id_project_created = response.json()["id"]
        self.list_projects.append(id_project_created)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_delete_project(self, create_project):
        id_project_delete = create_project["id"]
        url_todo = f"{self.url_projects}/{id_project_delete}"
        LOGGER.debug("URL to delete: %s", url_todo)

        response = requests.delete(url=url_todo, headers=HEADERS_TODO)

        LOGGER.info("Status Code: %s", response.status_code)
        assert response.status_code == 204, "wrong status code, expected 204"

    def test_update_project(self, create_project):
        id_project_update = create_project["id"]
        LOGGER.debug("Project to update: %s", id_project_update)
        url_todo_update = f"{self.url_projects}/{id_project_update}"
        body_project = {
            "name": "Update project"
        }
        response = requests.post(url=url_todo_update, headers=HEADERS_TODO, data=body_project)
        LOGGER.info("Response from update project: %s", response.json())
        LOGGER.info("Status Code: %s", response.status_code)
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
            response = requests.delete(url=url_delete_project, headers=HEADERS_TODO)
            if response.status_code == 204:
                LOGGER.info("Project Id: %s deleted", id_project)
