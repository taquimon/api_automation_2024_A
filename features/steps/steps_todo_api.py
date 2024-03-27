import logging

from behave import given, when, then
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@given(u'I set the URL and headers')
def set__url_and_headers(context):
    LOGGER.debug("I set the URL: %s and headers", context.url)


@when(u'I call to projects endpoint using "{method_name}" method  and without body')
def call_endpoint(context, method_name):
    LOGGER.debug("STEP: When I call to projects endpoint using %s method  and without body", method_name)


@then(u'I receive the response')
def receive_response(context):
    LOGGER.debug(u'STEP: Then I receive the response')


@then(u'I validate the status code is {status_code:d}')
def validate_status_code(context, status_code):
    LOGGER.debug("STEP: Then I valida the status code is %s", status_code)
