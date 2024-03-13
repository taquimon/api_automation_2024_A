import logging

import requests

from config.config import HEADERS_TODO
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class RestClient:

    def __init__(self, headers=HEADERS_TODO):
        self.session = requests.Session()

        self.session.headers.update(headers)

    def request(self, method_name, url, body=None):
        """
        Method to call to request methods
        :param method_name:     GET, POST, PUT, DELETE
        :param url:
        :param body:            body to use in request
        :return:
        """
        response = self.select_method(method_name, self.session)(url=url, data=body)
        LOGGER.debug("Status Code %s: ", response.status_code)
        LOGGER.debug("Response Content %s: ", response.text)

        return response

    @staticmethod
    def select_method(method_name, session):
        methods = {
            "get": session.get,
            "post": session.post,
            "delete": session.delete,
            "put": session.put
        }
        return methods.get(method_name)