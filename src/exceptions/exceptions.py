# -*- coding: utf-8 -*-
 
"""
Exception indication a default in the http protocol,
it could be relative to the adress or the http
transfert via libcurl.

Exceptions have IDs 1XX.

Message shown when the exception is thrown below:
"""

"""
exception.exception.HTTPError.
    101: Wrong address structure
    102: PYCurl Error
"""

class HTTPError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

"""
exception.exception.JSONDataError.
    201: Inconsistent JSON Data from Node Test
"""

class JSONDataError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    
    