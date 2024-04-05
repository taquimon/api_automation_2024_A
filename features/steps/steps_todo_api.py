import json
import logging

from behave import given, when, then, step

from config.config import URL_TODO
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@when(u'I call to {endpoint} endpoint using "{method_name}" method  and {param} body')
def call_endpoint(context, endpoint, method_name, param):
    url_feature = f"{URL_TODO}/{endpoint}"
    LOGGER.debug("URL: %s", url_feature)
    body_feature = None

    if method_name == "POST":
        if context.text:
            LOGGER.debug("JSON param: %s", context.text)
            body_feature = update_data_json(context, json.loads(context.text))
        else:
            body_feature, new_feature_url = get_data_by_feature(endpoint, context)
            # TODO: update feature file to only have 1
            url_feature = new_feature_url
        LOGGER.debug("Body: %s", body_feature)
    elif method_name == "DELETE":
        _, new_feature_url = get_data_by_feature(endpoint, context)
        url_feature = new_feature_url

    response = context.rest_client.request(method_name=method_name, url=url_feature, body=body_feature)
    # store id to clean up
    if method_name == "POST":
        context.resource_list[endpoint].append(response["body"]["id"])

    context.response = response
    LOGGER.debug("Response: ", response)


@then(u'I receive the response and validate using "{json_file}" json')
def receive_response(context, json_file):
    context.validate.validate_response(context.response, f"{json_file}")
    LOGGER.debug(u'STEP: Then I receive the response')


@step(u'I validate the status code is {status_code:d}')
def validate_status_code(context, status_code):
    assert status_code == context.response["status_code"], f"expected {status_code} but received {context.response["status_code"]}"
    LOGGER.debug("STEP: Then I valida the status code is %s", status_code)


def get_data_by_feature(feature, context):
    LOGGER.debug("Feature: %s", feature)
    body = {}
    url = f"{URL_TODO}/{feature}/"
    LOGGER.debug("URL feature: %s", url)
    if feature == "projects":
        body = {"name": "Project"}
        if hasattr(context, "project_id"):
            url = url + context.project_id
    elif feature == "sections":
        body = {"name": "Section"}
        if hasattr(context, "section_id"):
            url = url + context.section_id
    else:
        LOGGER.error("Feature does not exist")

    LOGGER.debug("New URL feature: %s", url)
    LOGGER.debug("Body data by feature: %s", body)
    return body, url


def update_data_json(context, data):
    keys = ["project_id", "section_id", "task_id"]
    for k in keys:
        for d in data.keys():
            if k == d and hasattr(context, k):
                data[d] = getattr(context, k)  # "project_id" = context.project_id
                LOGGER.debug("Key changed: %s ", d)
    LOGGER.debug("New JSON data: %s", data)
    return data