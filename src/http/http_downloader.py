# -*- coding: utf-8 -*-

import pycurl
import json, configparser
from io import BytesIO, StringIO
from ..exceptions.exceptions import HTTPError

PROMETHEUS_API_LINK_SEGMENT = "/api/v1/query?query="

def get_node_address():
    config_parser = configparser.ConfigParser()
    config_parser.read('config/global.config.ini')
    return config_parser['General']['node_address']

class HTTPEngine(object):
    """
    Built-in HTTP Engine, it allows to download contents through a user provided url.
    """

    def __init__(self):
        self.http_node_address = get_node_address()

    def download(self, query):
        """
        Download the content from a url given by the user and writes it
        on file from a provided path.

        :param str url: The url of the content
        :param str output_filename: The destination file to write the content
        :raises HTTPError: if the download fails (no 200 RESPONSE_CODE) 
        """

        self.c = pycurl.Curl()
        buffer = BytesIO()
        self.c.setopt(self.c.URL, self.http_node_address + query)
        self.c.setopt(self.c.WRITEDATA, buffer)
        self.c.perform()
        self.c.close()

        return StringIO(buffer.getvalue().decode('iso-8859-1'))
