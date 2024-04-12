import json
import logging

from config.config import abs_path
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class ValidateResponse:

    def validate_response(self, actual_response=None, endpoint=None, stub=False):

        expected_response = self.read_input_data_json(f"{abs_path}/todo_api/input_data/{endpoint}.json")

        if stub:
            self.validate_value(expected_response["response"]["status"], actual_response["body"]["response"]["status"], "status_code")
            self.validate_value(expected_response["response"]["jsonBody"], actual_response["body"]["response"]["jsonBody"], "body")
            self.validate_value(expected_response["response"]["headers"],  actual_response["body"]["response"]["headers"], "headers")
        else:
            self.validate_value(expected_response["status_code"], actual_response["status_code"], "status_code")
            self.validate_value(expected_response["response"]["body"], actual_response["body"], "body")
            self.validate_value(expected_response["headers"],  actual_response["headers"], "headers")

    def validate_value(self, expected_value, actual_value, key_compare):
        """

        :param expected_value:
        :param actual_value:
        :param key_compare:
        :return:
        """
        LOGGER.info("Validating %s: ", key_compare)
        error_message = f"Expecting '{expected_value}' but received '{actual_value}'"
        if key_compare == "body":
            if isinstance(actual_value, list):
                if len(actual_value) > 0:
                    assert self.compare_json(expected_value[0], actual_value[0]), error_message
            else:
                assert self.compare_json(expected_value, actual_value), error_message
        elif key_compare == "headers":
            LOGGER.debug("Expected Headers: %s", expected_value.items())
            LOGGER.debug("Actual Headers: %s", actual_value.items())
            assert expected_value.items() <= actual_value.items(), error_message
        else:
            LOGGER.debug("Expected Status Code: %s", expected_value)
            LOGGER.debug("Actual Status Code: %s", actual_value)
            assert expected_value == actual_value, error_message

    @staticmethod
    def read_input_data_json(file_name):
        """

        :param file_name:
        :return:
        """
        LOGGER.debug("Reading file %s", file_name)
        with open(file_name, encoding="utf8") as json_file:
            data = json.load(json_file)
        LOGGER.debug("Content of '%s' : %s", file_name, data)
        json_file.close()

        return data

    @staticmethod
    def compare_json(json1, json2):
        """

        :param json1:
        :param json2:
        :return:
        """
        for key in json1.keys():
            if key in json2.keys():
                LOGGER.debug("Key '%s' found in json2", key)
            else:
                LOGGER.debug("Key '%s' not found in json2", key)
                return False
        return True


if __name__ == '__main__':
    v = ValidateResponse()
    v.validate_response()
