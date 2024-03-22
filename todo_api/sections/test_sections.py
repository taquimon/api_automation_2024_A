import logging

import allure
import pytest
import requests

from config.config import HEADERS_TODO, URL_TODO
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("TODO API")
@allure.story("Sections")
class TestSections:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("Setup Class method")
        cls.url_sections = f"{URL_TODO}/sections"
        cls.list_sections = []
        cls.rest_client = RestClient()

    @allure.feature("List Sections")
    @allure.title("Test get all sections")
    @allure.description("Test that show the response of list of all sections")
    @allure.tag("acceptance", "sections", "sanity")
    @allure.testcase("TC-1254")
    @allure.issue("BUG-123")
    @pytest.mark.acceptance
    def test_get_all_sections(self, create_project, test_log_name):
        """
        Test get all sections
        """
        url_get_all_sections = f"{URL_TODO}/sections?project_id={create_project}"
        response = self.rest_client.request("get", url=url_get_all_sections)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @allure.feature("Create Sections")
    @allure.title("Test create section")
    @allure.description("Test that show the response of create section")
    @allure.tag("acceptance", "sections", "sanity")
    @allure.testcase("http://testlink/TC-1254")
    @pytest.mark.acceptance
    def test_create_section(self, create_project, test_log_name):
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
    def test_delete_section(self, create_section, test_log_name):
        """
        Test delete section
        """
        url_section_delete = f"{self.url_sections}/{create_section}"
        response = self.rest_client.request("delete", url=url_section_delete)

        assert response["status_code"] == 204, "wrong status code, expected 204"

    @pytest.mark.acceptance
    def test_update_section(self, create_section, test_log_name):
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

    # @classmethod
    # def teardown_class(cls):
    #     """
    #     Delete all projects used in test
    #     """
    #     LOGGER.info("Cleanup sections...")
    #     for id_section in cls.list_sections:
    #         url_delete_section = f"{URL_TODO}/sections/{id_section}"
    #         response = cls.rest_client.request("delete", url=url_delete_section)
    #         if response["status_code"] == 204:
    #             LOGGER.info("Section Id: %s deleted", id_section)