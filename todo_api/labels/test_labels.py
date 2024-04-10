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
        cls.url_projects = f"{URL_TODO}/labels"
        cls.list_projects = []
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.wiremock = WiremockStub()

    def test_get_label(self, _test_log_name):
        """
        :return:
        """
        # wiremock request
        self.wiremock.create_stub("get_label_stub")
        # self.wiremock.test("get_label")
