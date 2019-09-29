"""
name: Cyril PARODI
date: 29/09/2019
module: http_request.py
"""

# -*- coding: utf-8 -*-

import pycurl
import configparser
from io import BytesIO, StringIO
from ..exceptions.exceptions import HTTPError

PROMAPI_CONFIG_SEGMENT = "/api/v1/status/config"
PROMAPI_QUERY_SEGMENT = "/api/v1/query?query="

def get_address_from_config():
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini')
    return config_parser['General']['node_address']

class HTTPRequester(object):
    """
    Built-in HTTP Engine, it allows to download contents through a user
    provided url.
    """

    def __init__(self):
        self.http_node_address = get_address_from_config()

    def request(self, query):
        """
        Download the content from a url given by the user and writes it
        on file from a provided path.

        :param str query: The query to request
        :raises HTTPError: if the download fails (no 200 RESPONSE_CODE) 
        """

        self.c = pycurl.Curl()
        buffer = BytesIO()
        self.c.setopt(self.c.URL, self.http_node_address + query)
        self.c.setopt(self.c.WRITEDATA, buffer)

        try:
            self.c.perform()
        except pycurl.error as e_pycurl:
            raise HTTPError(101, "PYCurl Error : " + str(e_pycurl))

        res = self.c.getinfo(self.c.RESPONSE_CODE)
        if res != 200:
            raise HTTPError(102, f"Impossible to reach the Node : {res}")

        self.c.close()

        return StringIO(buffer.getvalue().decode('iso-8859-1'))
