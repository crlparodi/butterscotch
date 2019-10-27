# -*- coding: utf-8 -*-

import json
from src.metrics.metric import *
from src.metrics.cpu import CPUDataProcessing

API_EXPR_PATH = "api/expressions.json"

class ExpressionParserResolver(object):
    def __init__(self, *args, **kwargs):
        self.expr_dict = {}

    def parse(self):
        with open(API_EXPR_PATH) as query_config_file:
            self.expr_dict = json.load(query_config_file)
            return self.expr_dict


