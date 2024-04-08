"""
(c) Copyright Jalasoft. 2024

test_sections.py
    file that contains pytest tests for sections endpoint
"""
import logging

import allure
import pytest

from config.config import URL_TODO
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("TODO API")
@allure.story("Sections")
class TestSections:
    """
    Class to test section endpoint
    """
    @classmethod
    def setup_class(cls):
        """
        Setup Class to initialize variables or objects
        """
        LOGGER.debug("Setup Class method")
        cls.url_sections = f"{URL_TODO}/sections"
        cls.list_sections = []
        cls.rest_client = RestClient()

    @allure.feature("List Sections")
    @allure.title("Test get all sections")
    @allure.description("Test that show the response of list of all sections")
    @allure.tag("acceptance", "sections", "sanity")
    @pytest.mark.acceptance
    def test_get_all_sections(self, create_project, _test_log_name):
        """
        Test get all sections
        :param create_project:
        :param _test_log_name:
        """
        url_get_all_sections = f"{URL_TODO}/sections?project_id={create_project}"
        response = self.rest_client.request("get", url=url_get_all_sections)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @allure.feature("Create Sections")
    @allure.title("Test create section")
    @allure.description("Test that show the response of create section")
    @allure.tag("acceptance", "sections", "sanity")
    @pytest.mark.acceptance
    def test_create_section(self, create_project, _test_log_name):
        """
        Test create section
        """
        body_section = {
            "project_id": f"{create_project}",
            "name": "Section created with automation"
        }

        response = self.rest_client.request("post", url=self.url_sections, body=body_section)
        id_section_created = response["body"]["id"]
        self.list_sections.append(id_section_created)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @pytest.mark.acceptance
    def test_delete_section(self, create_section, _test_log_name):
        """
        Test delete section
        """
        url_section_delete = f"{self.url_sections}/{create_section}"
        response = self.rest_client.request("delete", url=url_section_delete)

        assert response["status_code"] == 204, "wrong status code, expected 204"

    @pytest.mark.acceptance
    def test_update_section(self, create_section, _test_log_name):
        """
        Test update section
        """
        LOGGER.debug("Section to update: %s", create_section)
        url_todo_update = f"{self.url_sections}/{create_section}"
        body_section_update = {
            "name": "Update section auto"
        }
        response = self.rest_client.request("post", url=url_todo_update, body=body_section_update)
        # self.list_sections.append(create_section)

        assert response["status_code"] == 200, "wrong status code, expected 200"
