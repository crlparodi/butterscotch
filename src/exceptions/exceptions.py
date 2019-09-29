"""
name: Cyril PARODI
date: 29/09/2019
module: exceptions.py
"""

# -*- coding: utf-8 -*-

"""
exception.exception.HTTPError
    101: PYCurl Error + ERROR_MSG
    102: Impossible to reach the Node + HTTP_CODE
"""

class HTTPError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
