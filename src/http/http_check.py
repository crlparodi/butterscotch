# -*- coding: utf-8 -*-

import pycurl
import json
from src.exceptions.exceptions import HTTPError
from .http_request import HTTPRequester
from .http_config import PROMAPI_READY, PROMAPI_CONFIG_SEGMENT, \
    HTTP_ADDRESS_OK, HTTP_ADDRESS_ERROR

def http_address_verification(_http_address=None):
    """
    Does a first connection with the address to verify if it's OK

    Technically, we request the following link :
        - http_address + PROMAPI_CONFIG_SEGMENT
        so for example : http://localhost:9090/api/v1/status/config
    and regards the status indicated in the JSON stream ("success"|"error"),
    this function returns ...

    :return HTTP_ADDRESS_OK (True): if the verification is a success
    :return HTTP_ADDRESS_ERROR (False): if the verification results on an
                                        "error" status from the JSON
    """
    print("Checking the HTTP Address ...")

    # Preparing the request http engine
    if _http_address:
        requester = HTTPRequester(_http_address)
    else:
        requester = HTTPRequester()

    try:
        # First step : Getting the Ready Signal from the Server
        if http_api_is_ready(requester):
            # Second step : Getting back the config of the server
            if http_api_get_config(requester):
                # If all the requirements are solved
                print("HTTP Address Check Succeed ...")
                return HTTP_ADDRESS_OK

    except HTTPError as e_http:
        print("ERROR : HTTPError ", e_http.code, "-", e_http.message)
        print("HTTP Address Verification failed...")

    except TypeError as e_type:
        print("ERROR : TypeError - ", e_type)
        print("HTTP Address Verification failed...")

    return HTTP_ADDRESS_ERROR


def http_api_is_ready(_requester):
    """
    Getting the ready signal from the server

    :param _requester:
    :return True: if OK.
    """
    if "Ready" in _requester.request(
            PROMAPI_READY,
            _check_content_type=True
    ):
        return True

    return False


def http_api_get_config(_requester):
    """
    Retrieving the configuration of the server

    :param _requester:
    :return True: if the configuration exists
    """
    api_config_json = json.load(_requester.request(
        PROMAPI_CONFIG_SEGMENT,
        _check_content_type=True
    ))

    if api_config_json['data']['yaml']:
        return True

    return False