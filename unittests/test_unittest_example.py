import logging
import unittest

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

    def test_example_two(self):
        LOGGER.debug("Test two")


if __name__ == '__main__':
    unittest.main()
