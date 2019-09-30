"""
name: Cyril PARODI
date: 29/09/2019
module: http_config.py
"""

# -*- coding: utf-8 -*-

import configparser

PROMAPI_FALSE_REQUEST = "/"
PROMAPI_READY = "/-/ready"
PROMAPI_CONFIG_SEGMENT = "/api/v1/status/config"
PROMAPI_QUERY_SEGMENT = "/api/v1/query?query="

def get_address_from_config():
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini')
    return config_parser['General']['node_address']