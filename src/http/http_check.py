# -*- coding: utf-8 -*-

import pycurl
import json
from ..exceptions.exceptions import HTTPError, JSONDataError
from .http_downloader import HTTPEngine


def http_address_verification():
    json_str_io = None # Contains all the JSON Data

    try:
        json_str_io = test_connection("/api/v1/status/config")

        if json_str_io != None:
            if check_transaction_success(json_str_io):
                return True

    except HTTPError as ehttp:
        print("HTTPError - Code", ehttp.code, "-", ehttp.message)
        return False
    
    except JSONDataError as ejson:
        print("JSONDataError - Code", ejson.code, "-", ejson.message)
        return False

def test_connection(addr):
    """ 
    Verifying that the app can access the node
    
    :param str addr: The address complement of the node.
    """
    downloader = HTTPEngine()

    try:
        str_io = downloader.download(addr)
        return str_io

    except pycurl.error as epycurl:
        raise HTTPError(102, "PYCurl Error : " + str(epycurl))
    

def check_transaction_success(json_str_io):
    """ Verifying that the file data is consistent """
    json_test_data = json.load(json_str_io)

    if json_test_data['status'] == "success":
        return True

    raise JSONDataError(201, "Inconsistent JSON Data from Node Test")
