import logging

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


def before_all(context):
    LOGGER.debug("Before all")
    context.url = "/projects"


def before_feature(context, feature):
    LOGGER.debug("Before Feature")
    LOGGER.debug("Feature tags: %s", feature.tags)


def before_scenario(context, scenario):
    LOGGER.debug("Before Scenario")
    LOGGER.debug("Scenario tags: %s", scenario.tags)
    LOGGER.debug("Scenario Name: %s", scenario.name)


def after_scenario(context, scenario):
    LOGGER.debug("After Scenario")


def after_feature(context, feature):
    LOGGER.debug("After Feature")


def after_all(context):
    LOGGER.debug("After all")
