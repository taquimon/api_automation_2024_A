import logging
import unittest

import allure
from nose2.tools import params

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestUnitTestExample(unittest.TestCase):

    def setUp(self):
        LOGGER.debug("Setup")

    @classmethod
    def setUpClass(cls):
        LOGGER.debug("SetupClass")

    def tearDown(self):
        LOGGER.debug("teardown")

    @classmethod
    def tearDownClass(cls):
        LOGGER.debug("tearDownClass")

    def test_example_one(self):
        LOGGER.debug("Test one")

    @allure.story("test todo API")
    @params("name1", "name2", "name3")
    def test_example_two(self, name):
        LOGGER.debug("Test two: %s", name)


if __name__ == '__main__':
    unittest.main()
