import logging

import requests

from config.config import HEADERS_TODO, URL_TODO
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestSections:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("Setup Class method")
        cls.url_sections = f"{URL_TODO}/sections"
        cls.list_sections = []
        cls.rest_client = RestClient()

    def test_get_all_sections(self, create_project):
        """
        Test get all sections
        """
        project_id = create_project["id"]
        url_get_all_sections = f"{URL_TODO}/sections?project_id={project_id}"
        response = self.rest_client.request("get",url=url_get_all_sections)

        assert response.status_code == 200, "wrong status code, expected 200"

    def test_create_section(self, get_project):
        """
        Test create section
        """
        body_section = {
            "project_id": f"{get_project}",
            "name": "Section created with automation"
        }

        response = self.rest_client.request("post", url=self.url_sections, body=body_section)
        id_section_created = response.json()["id"]
        self.list_sections.append(id_section_created)

        assert response.status_code == 200, "wrong status code, expected 200"

    def test_delete_section(self, create_section):
        """
        Test delete section
        """
        id_project_delete = create_section["id"]
        url_section_delete = f"{self.url_sections}/{id_project_delete}"
        response = self.rest_client.request("delete", url=url_section_delete)

        assert response.status_code == 204, "wrong status code, expected 204"

    def test_update_section(self, create_section):
        """
        Test update section
        """

        id_section_update = create_section["id"]
        LOGGER.debug("Section to update: %s", id_section_update)
        url_todo_update = f"{self.url_sections}/{id_section_update}"
        body_section_update = {
            "name": "Update section auto"
        }
        response = self.rest_client.request("post", url=url_todo_update, body=body_section_update)
        self.list_sections.append(id_section_update)

        assert response.status_code == 200, "wrong status code, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        Delete all projects used in test
        """
        LOGGER.info("Cleanup sections...")
        for id_section in cls.list_sections:
            url_delete_section = f"{URL_TODO}/section/{id_section}"
            response = cls.rest_client.request("delete", url=url_delete_section)
            if response.status_code == 204:
                LOGGER.info("Section Id: %s deleted", id_section)