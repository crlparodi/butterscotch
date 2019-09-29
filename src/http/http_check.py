# -*- coding: utf-8 -*-

import pycurl
import json
from ..exceptions.exceptions import HTTPError
from .http_request import HTTPRequester, PROMAPI_CONFIG_SEGMENT


def first_connection_test():
    try:
        requester = HTTPRequester()
        json_test = json.load(requester.request(PROMAPI_CONFIG_SEGMENT))

        if json_test['status'] == "success":
            return True

    except HTTPError as e_http:
        print("HTTPError - ", e_http.code, "-", e_http.message)
        return False

