import logging

import requests

from config.config import HEADERS_TODO, URL_TODO
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestSections:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("Setup Class method")
        cls.url_sections = f"{URL_TODO}/sections"
        cls.list_sections = []

    def test_get_all_sections(self, create_project):
        """
        Test get all sections
        """
        project_id = create_project["id"]
        url_get_all_sections = f"{URL_TODO}/sections?project_id={project_id}"
        response = requests.get(url=url_get_all_sections, headers=HEADERS_TODO)
        LOGGER.info("Response from get all sections: %s", response.json())

        LOGGER.info("Status Code: %s", response.status_code)
        assert response.status_code == 200, "wrong status code, expected 200"

    # def test_create_section(self):
    #     """
    #     Test create section
    #     """
    # def test_delete_section(self):
    #     """
    #     Test delete section
    #     """
    #
    # def test_update_section(self):
    #     """
    #     Test update section
    #     """

    @classmethod
    def teardown_class(cls):
        """
        Delete all projects used in test
        """
        LOGGER.info("Cleanup sections...")
        for id_section in cls.list_sections:
            url_delete_section = f"{URL_TODO}/section/{id_section}"
            response = requests.delete(url=url_delete_section, headers=HEADERS_TODO)
            if response.status_code == 204:
                LOGGER.info("Section Id: %s deleted", id_section)