import json
import logging

from wiremock.server import WireMockServer

from config.config import abs_path
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class WiremockStub:
    def create_stub(self, endpoint):
        """
        Create stub in wiremock
        :return:
        """

        with WireMockServer() as wiremock:
            # url_mappings = f"http://localhost:8088/__admin/mappings"
            url_mappings_server = f"http://localhost:{wiremock.port}/__admin/mappings"
            validate = ValidateResponse()
            stub_data = validate.read_input_data_json(f"{abs_path}/todo_api/input_data/{endpoint}.json")
            rest_client = RestClient(headers={})
            LOGGER.debug("URL Mappings: %s", url_mappings_server)
            response = rest_client.request("post", url=url_mappings_server, body=json.dumps(stub_data))
            # url_mappings_stub = f"{url_mappings}/296d4992-3769-45a2-9d21-8366d14a5ce8"
            # response = rest_client.request("get", url=url_mappings_stub)

            print(response["body"])
            print(response["status_code"])
            print(response["headers"])


if __name__ == '__main__':
    mock = WiremockStub()
    mock.create_stub()
