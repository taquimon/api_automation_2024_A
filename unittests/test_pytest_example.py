import logging
import sys

import pytest

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestPytestExample:

    def setup_method(self):
        LOGGER.debug("Setup method")

    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")

    def teardown_method(self):
        LOGGER.debug("teardown")

    @classmethod
    def teardown_class(cls):
        LOGGER.debug("tearDownClass")

    @pytest.mark.smoke
    def test_example_zero(self):
        LOGGER.debug("Test zero")

    @pytest.mark.smoke
    # @pytest.mark.skip(reason="BUG related: 123123")
    # @pytest.mark.skipif(condition, message)
    @pytest.mark.skipif(sys.platform == "win32", reason="not executable on Windows OS")
    def test_example_one(self, fixture_example):
        LOGGER.debug("Test one environment: %s", fixture_example)

    @pytest.mark.acceptance
    @pytest.mark.parametrize("name_parameter", ["one", "two", "three"])
    def test_example_two(self, fixture_example, name_parameter):
        LOGGER.debug("Test two: %s", name_parameter)