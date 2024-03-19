import json
import logging

import requests

from config.config import HEADERS_TODO, URL_TODO
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestComments:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("Setup Class method")
        cls.url_comments = f"{URL_TODO}/comments"
        # cls.list_sections = []
        cls.rest_client = RestClient()

    def test_get_all_comments(self, create_task, test_log_name):
        """
        Test get all comments
        :param test_log_name:
        """
        url_get_all_comments = f"{URL_TODO}/sections?task_id={create_task}"
        response = self.rest_client.request("get", url=url_get_all_comments)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    def test_create_comment(self, create_task, test_log_name):
        """

        :param create_task:
        :param test_log_name:
        :return:
        """
        body_comment = {
            "task_id": f"{create_task}",
            "content": "Need one bottle of milk",
        }
        response = self.rest_client.request("post", url=self.url_comments, body=body_comment)
        # id_section_created = response.json()["id"]
        # self.list_sections.append(id_section_created)
        assert response["status_code"] == 200, "wrong status code, expected 200"

    def test_delete_comment(self, create_comment, test_log_name):
        """
        Test delete comment
        """
        url_comment_delete = f"{self.url_comments}/{create_comment}"
        response = self.rest_client.request("delete", url=url_comment_delete)

        assert response["status_code"] == 204, "wrong status code, expected 204"

    def test_update_comment(self, create_comment, test_log_name):
        """
        Test update comment
        """

        LOGGER.debug("Comment to update: %s", create_comment)
        url_comment_update = f"{self.url_comments}/{create_comment}"
        body_comment_update = {
            "content": "Update comment auto"
        }
        response = self.rest_client.request("post", url=url_comment_update, body=body_comment_update)
        # self.list_sections.append(id_section_update)

        assert response["status_code"] == 200, "wrong status code, expected 200"