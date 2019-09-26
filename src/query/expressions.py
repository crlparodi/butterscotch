# -*- coding: utf-8 -*-

import json
from ..metrics.metric import *
from ..metrics.cpu import CPUBoard

API_EXPR_PATH = "api/expressions.json"

class ExpressionParserResolver(object):
    def __init__(self, *args, **kwargs):
        self.expr_dict = {}

    def parse(self):
        with open(API_EXPR_PATH) as query_config_file:
            self.expr_dict = json.load(query_config_file)

    def resolve(self):
        metrics_dict = {}
        metrics_dict["CPU"] = CPUBoard().process(self.expr_dict["cpu"])

        return metrics_dict

        """
        metrics_dict = {
            "CPU" : {
                "CPU_NBR_CORES" : ("STR1", "STR2")
                "CPU_CORE_X_FREQ" : ("STR1", "STR2")
            }
            etc...
        }
        """


