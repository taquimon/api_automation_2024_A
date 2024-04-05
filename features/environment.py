import logging

from config.config import URL_TODO
from entities.project import Project
from entities.section import Section
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


def before_all(context):
    LOGGER.debug("Before all")
    context.list_projects = []
    context.rest_client = RestClient()
    context.validate = ValidateResponse()
    context.project = Project()
    context.section = Section()
    context.resource_list = {
        "tasks": [],
        "sections": [],
        "projects": [],
    }


def before_feature(context, feature):
    LOGGER.debug("Before Feature")
    LOGGER.debug("Feature tags: %s", feature.tags)


def before_scenario(context, scenario):
    LOGGER.debug("Before Scenario")
    LOGGER.debug("Scenario tags: %s", scenario.tags)
    LOGGER.debug("Scenario Name: %s", scenario.name)
    if "project_id" in scenario.tags:
        project, _ = context.project.create_project()
        context.project_id = project["body"]["id"]
        # add to project list to be deleted at the end of execution
        context.resource_list["projects"].append(context.project_id)
        LOGGER.debug("Project created in before scenario: %s", context.project_id)

    if "section_id" in scenario.tags:
        project, _ = context.project.create_project()
        LOGGER.debug("project for section %s", project["body"]["id"])
        section, _ = context.section.create_section(project_id=project["body"]["id"])
        context.section_id = section["body"]["id"]
        context.resource_list["projects"].append(project["body"]["id"])
        context.resource_list["sections"].append(context.section_id)
        LOGGER.debug("Section created in before scenario: %s", context.section_id)


def after_scenario(context, scenario):
    LOGGER.debug("After Scenario")


def after_feature(context, feature):
    LOGGER.debug("After Feature")
    delete_resources(context)

def after_all(context):
    LOGGER.debug("After all")


def delete_resources(context):
    LOGGER.debug("Delete Resources...")
    for resource in context.resource_list:
        for resource_id in context.resource_list[resource]:
            url = f"{URL_TODO}/{resource}/{resource_id}"
            context.rest_client.request("delete", url)
            LOGGER.debug("Deleting %s with id: %s", resource, resource_id)
