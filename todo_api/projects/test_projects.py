import logging

import requests

from utils.logger import get_logger

token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
LOGGER = get_logger(__name__, logging.DEBUG)


class TestProjects:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        url_todo = "https://api.todoist.com/rest/v2/projects"
        headers_todo = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url=url_todo, headers=headers_todo)

        LOGGER.info("Response from get all projects: %s", response.json())
        # get the project id
        project_list = response.json()
        cls.id_project = project_list[1]["id"]

    def test_get_all_projects(self):
        url_todo = "https://api.todoist.com/rest/v2/projects"
        headers_todo = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url=url_todo, headers=headers_todo)

        LOGGER.info("Response from get all projects: %s", response.json())

        LOGGER.info("Status Code: %s", response.status_code)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_create_project(self):
        url_todo = "https://api.todoist.com/rest/v2/projects"
        headers_todo = {
            "Authorization": f"Bearer {token}"
        }
        body_project = {
            "name": "Buy Milk"
        }
        response = requests.post(url=url_todo, headers=headers_todo, data=body_project)
        LOGGER.info("Response from create project: %s", response.json())
        LOGGER.info("Status Code: %s", response.status_code)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_delete_project(self):
        url_todo = f"https://api.todoist.com/rest/v2/projects/{self.id_project}"
        LOGGER.debug("URL to delete: %s", url_todo)
        headers_todo = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.delete(url=url_todo, headers=headers_todo)

        LOGGER.info("Status Code: %s", response.status_code)
        assert response.status_code == 204, "wrong status code, expected 204"