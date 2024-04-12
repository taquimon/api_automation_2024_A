"""
(c) Copyright Jalasoft. 2024

test_projects.py
    file that contains pytest tests for projects endpoint
"""
import logging

import allure
import pytest

from config.config import URL_TODO, MAX_PROJECTS
from entities.project import Project
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger
from utils.wiremock_stubs import WiremockStub

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("TODO API")
@allure.story("Labels")
class TestProjects:
    """
    Class for Test projects endpoint
    """
    @classmethod
    def setup_class(cls):
        """
        Setup Class to initialize variables or objects
        """
        LOGGER.debug("SetupClass method")
        cls.url_labels = f"{URL_TODO}/labels"
        cls.list_projects = []
        cls.rest_client = RestClient(headers={})
        cls.validate = ValidateResponse()
        cls.wiremock = WiremockStub()

    @allure.tag("acceptance", "label", "stub")
    def test_get_label(self, _test_log_name):
        """
        Test get Label using stubs
        """
        # wiremock request to create GET label endpoint
        wiremock, response_stub = self.wiremock.create_stub("get_label_stub")
        # get ID of stub label created
        label_id_stub = response_stub["body"]["id"]
        url_mappings_label = f"http://localhost:{wiremock.port}/__admin/mappings/{label_id_stub}"
        LOGGER.debug("URL label mapping: %s", url_mappings_label)

        response = self.rest_client.request("get", url=url_mappings_label)
        LOGGER.debug("Response get label: %s", response)
        self.validate.validate_response(response, "get_label_stub", stub=True)

    def test_create_label(self, _test_log_name):
        """
        Test create Label using stubs
        """
        wiremock, response_stub = self.wiremock.create_stub("create_label_stub")
        # get ID of stub label created
        label_id_stub = response_stub["body"]["id"]
        url_mappings_label = f"http://localhost:{wiremock.port}/__admin/mappings/{label_id_stub}"
        LOGGER.debug("URL label mapping: %s", url_mappings_label)
        response = self.rest_client.request("get", url=url_mappings_label)
        LOGGER.debug("Response get label: %s", response)
        self.validate.validate_response(response, "create_label_stub", stub=True)
