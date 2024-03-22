"""
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=etaquichiri&password=phantom&scope=&client_secret='
"""
import logging

import pytest

from config.config import URL_TODO
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestFastAPI:
    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_token = "http://127.0.0.1:8000/token"
        headers_fast_api = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body_token = {
            "grant_type": "",
            "username": "etaquichiri",
            "password": "phantom",
            "scope": "",
            "client_secret": ""
        }

        cls.rest_client = RestClient(headers=headers_fast_api)
        response = cls.rest_client.request("post", url=cls.url_token, body=body_token)
        cls.acces_token = response.json()["access_token"]

    def test_get_users(self):
        HEADERS_FAST_API = {
            "Authorization": f"Bearer {self.acces_token}"
        }
        url_get_users = "http://127.0.0.1:8000/users/me/"
        rest_client = RestClient(headers=HEADERS_FAST_API)
        response = rest_client.request("get", url=url_get_users)
