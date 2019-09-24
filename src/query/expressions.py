# -*- coding: utf-8 -*-

import json
from ..metrics.metric import *

API_EXPR_PATH = "api/expressions.json"

class ExpressionParserResolver(object):
    def __init__(self, *args, **kwargs):
        self.query_dict = {}

    def parse(self):
        with open(API_EXPR_PATH) as query_config_file:
            self.query_dict = json.load(query_config_file)

    def resolve(self):
        metric_set_list = []
        for panel in self.query_dict["panels"]:
            metric_proc = MetricProcess(panel)
            metric_obs = MetricPostProcess()
            metric_proc.add_observer(metric_obs)
            metric_set = metric_proc.process()
            metric_set_list.append(metric_set)

        return metric_set_list

