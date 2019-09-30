"""
name: Cyril PARODI
date: 29/09/2019
module: http_request.py
"""

# -*- coding: utf-8 -*-

import pycurl
from io import BytesIO, StringIO
from .http_config import get_address_from_config
from ..exceptions.exceptions import HTTPError

class HTTPRequester(object):
    """
    Built-in HTTP Engine, it allows to download contents through a user
    provided url.
    """

    def __init__(self, _http_address=None):
        if not _http_address:
            self.http_address = get_address_from_config()
        else:
            self.http_address = _http_address

    def request(self, _query, _check_content_type=False):
        """
        Download the content from a url given by the user and writes it
        on file from a provided path.

        :param str query: The query to request
        :raises HTTPError: if the download fails (no 200 RESPONSE_CODE) 
        """

        self.c = pycurl.Curl()
        buffer = BytesIO()
        self.c.setopt(self.c.URL, self.http_address + _query)
        self.c.setopt(self.c.WRITEDATA, buffer)
        # self.c.setopt(self.c.VERBOSE, True)

        try:
            self.c.perform()
        except pycurl.error as e_pycurl:
            raise HTTPError(101, "libcurl error : " + str(e_pycurl.args[1]))

        self.handle_response(self.c.getinfo(self.c.RESPONSE_CODE))

        content_type = self.c.getinfo(self.c.CONTENT_TYPE)
        self.c.close()

        if _check_content_type:
            return self.handle_content(
                content_type,
                StringIO(buffer.getvalue().decode('iso-8859-1'))
            )
        else:
            return StringIO(buffer.getvalue().decode('iso-8859-1'))

    def handle_response(self, _res):
        if _res != 200:
            raise HTTPError(102, f"Impossible to reach the Node : {_res}")

    def handle_content(self, _content_type, _io):
        if "text/plain" in  _content_type:
            return _io.getvalue()
        elif "application/json" in  _content_type:
            return _io
        else:
            raise TypeError("The output is not a plain text or a JSON. "
                            "Please check the node address.")
