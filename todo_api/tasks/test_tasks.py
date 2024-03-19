import json
import logging

from config.config import URL_TODO
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

    def test_get_all_tasks(self, test_log_name):
        """
        Test get all sections
        """
        response = self.rest_client.request("get", url=self.url_tasks)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    def test_create_section(self, test_log_name):
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
    #

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

    # @classmethod
    # def teardown_class(cls):
    #     """
    #     Delete all projects used in test
    #     """
    #     LOGGER.info("Cleanup sections...")
    #     for id_section in cls.list_sections:
    #         url_delete_section = f"{URL_TODO}/sections/{id_section}"
    #         response = cls.rest_client.request("delete", url=url_delete_section)
    #         if response.status_code == 204:
    #             LOGGER.info("Section Id: %s deleted", id_section)
