"""
(c) Copyright Jalasoft. 2024

test_logger.py
    test the configuration of logger file and get_logger method
"""
import logging
import unittest
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestLogger(unittest.TestCase):
    """
    Class to test get_logger method
    """
    def test_logger(self):
        """
        Method to test logging levels
        """
        LOGGER.debug("log DEBUG level")
        LOGGER.info("log INFO level")
        LOGGER.warning("log WARNING level")
        LOGGER.error("log ERROR level")
        LOGGER.critical("log CRITICAL level")
