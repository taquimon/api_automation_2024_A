import logging

from config.config import URL_TODO
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Section:

    def __init__(self, rest_client=None):
        self.url_sections = f"{URL_TODO}/sections"
        if rest_client is None:
            self.rest_client = RestClient()

    def create_section(self, project_id):
        # body_project = body
        # if body is None:
        body_section = {
            "project_id": f"{project_id}",
            "name": "Section from fixture"
        }
        response = self.rest_client.request("post", url=self.url_sections, body=body_section)

        return response, self.rest_client

    def delete_section(self, section_id):
        """
        Delete section
        :param section_id:
        :return:
        """
        LOGGER.info("Cleanup section...")
        url_delete_section = f"{URL_TODO}/section/{section_id}"
        response = self.rest_client.request("delete", url=url_delete_section)
        if response["status_code"] == 204:
            LOGGER.info("Project Id: %s deleted", section_id)
