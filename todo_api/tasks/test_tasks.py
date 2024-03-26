import json
import logging

import pytest

from config.config import URL_TODO
from entities.task import Task
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestTasks:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("Setup Class method")
        cls.url_tasks = f"{URL_TODO}/tasks"
        cls.list_tasks = []
        cls.rest_client = RestClient()
        cls.task = Task()

    def test_get_all_tasks(self, test_log_name):
        """
        Test get all sections
        """
        response = self.rest_client.request("get", url=self.url_tasks)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @pytest.mark.acceptance
    def test_create_task(self, test_log_name):
        """
        Test create section
        """
        content_task_body = {
            "content": "Buy Milk",
            "due_string": "tomorrow at 12:00",
            "due_lang": "en",
            "priority": 4
        }

        response = self.rest_client.request("post", url=self.url_tasks, body=content_task_body)
        id_task_created = response["body"]["id"]
        self.list_tasks.append(id_task_created)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @pytest.mark.functional
    def test_create_task_by_project(self, create_project, test_log_name):
        """
        Create a task inside a project
        :param create_project:
        :param test_log_name:
        :return:
        """
        response, _ = self.task.create_tasks(project_id=create_project)
        id_task_created = response["body"]["id"]
        self.list_tasks.append(id_task_created)
        assert response["status_code"] == 200, "wrong status code, expected 200"

    @pytest.mark.functional
    def test_create_task_by_section(self, create_section, test_log_name):
        """
        Create a task inside a section
        :param create_section:
        :param test_log_name:
        :return:
        """
        response, _ = self.task.create_tasks(section_id=create_section)
        id_task_created = response["body"]["id"]
        self.list_tasks.append(id_task_created)
        assert response["status_code"] == 200, "wrong status code, expected 200"

    @pytest.mark.functional
    def test_create_task_by_project_and_section(self, create_project, create_section, test_log_name):
        """
        Create a task inside a project and section
        :param create_section:
        :param test_log_name:
        :return:
        """
        response, _ = self.task.create_tasks(project_id=create_project, section_id=create_section)
        id_task_created = response["body"]["id"]
        self.list_tasks.append(id_task_created)
        assert response["status_code"] == 200, "wrong status code, expected 200"

    def test_delete_task(self, create_task, test_log_name):
        """
        Test delete section
        """
        url_task_delete = f"{self.url_tasks}/{create_task}"
        response = self.rest_client.request("delete", url=url_task_delete)

        assert response["status_code"] == 204, "wrong status code, expected 204"

    def test_close_task(self, create_task, test_log_name):
        """
        Test delete section
        """
        url_task_close = f"{self.url_tasks}/{create_task}/close"
        response = self.rest_client.request("post", url=url_task_close)

        assert response["status_code"] == 204, "wrong status code, expected 204"

    def test_reopen_task(self, create_task, test_log_name):
        """
        Test delete section
        """
        url_task_reopen = f"{self.url_tasks}/{create_task}/reopen"
        response = self.rest_client.request("post", url=url_task_reopen)

        assert response["status_code"] == 204, "wrong status code, expected 204"

    def test_update_task(self, create_task, test_log_name):
        """
        Test update section
        """
        LOGGER.debug("Task to update: %s", create_task)
        url_task_update = f"{self.url_tasks}/{create_task}"
        body_task_update = {
            "content": "Update task auto"
        }
        response = self.rest_client.request("post", url=url_task_update, body=body_task_update)
        # self.list_sections.append(id_section_update)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        Delete all tasks used in test
        """
        LOGGER.info("Cleanup tasks...")
        for id_task in cls.list_tasks:
            url_delete_task = f"{URL_TODO}/tasks/{id_task}"
            response = cls.rest_client.request("delete", url=url_delete_task)
            if response["status_code"] == 204:
                LOGGER.info("Task Id: %s deleted", id_task)
