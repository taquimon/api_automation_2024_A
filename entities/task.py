import logging

from config.config import URL_TODO
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Task:

    def __init__(self, rest_client=None):
        self.url_tasks = f"{URL_TODO}/tasks"
        if rest_client is None:
            self.rest_client = RestClient()

    def create_tasks(self, project_id=None, section_id=None):

        content_task_body = {
            "content": "Task created using entity",
            "due_string": "tomorrow at 12:00",
            "due_lang": "en",
            "priority": 4
        }
        if project_id:
            content_task_body["project_id"] = project_id
        if section_id:
            content_task_body["section_id"] = section_id
        LOGGER.debug("Task body: %s", content_task_body)
        response = self.rest_client.request("post", url=self.url_tasks, body=content_task_body)

        return response, self.rest_client

    def delete_task(self, task_id):
        """
        Delete task
        :param task_id:
        :return:
        """
        LOGGER.info("Cleanup task...")
        url_delete_task = f"{URL_TODO}/tasks/{task_id}"
        response = self.rest_client.request("delete", url=url_delete_task)
        if response["status_code"] == 204:
            LOGGER.info("Task Id: %s deleted", task_id)
