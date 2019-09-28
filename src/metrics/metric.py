"""
name: Cyril PARODI
date: 24/09/2019
module: metric.py
"""

# -*- coding: utf-8 -*-

import json
from ..http.http_request import HTTPEngine, PROMETHEUS_API_LINK_SEGMENT
from ..exceptions.exceptions import HTTPError

"""
    Metrics processing observer pattern.
    These classes allows to the processing metrics controllers to update the data
    only when the expressions are resolved and stored into the MetricSet/Data classes.
"""

class MetricObservable(object):
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        del(self.observers[observer])

    def notify(self, _value):
        for observer in self.observers:
            return observer.update(_value)


class MetricObserver(object):
    def update(self):
        raise NotImplementedError


"""
    Metrics Controller classes, theses classes are called when we wants to get
    a new metric Set with MetricData(s).
"""

class MetricProcess(MetricObservable):
    def __init__(self):
        super().__init__()

    def process(self, _expr, _value_index=0):
        try:
            hardware_json_data = json.load(HTTPEngine().request(PROMETHEUS_API_LINK_SEGMENT + _expr))
            value = hardware_json_data['data']['result'][_value_index]["value"][1]
            self.data_ready = True
        except HTTPError as ehttp:
            print(f"Failed to download the data for {_expr}, passing...")
        except json.JSONDecodeError as ejson:
            print(f"Failed to get metric for {_expr}, passing...")

        if self.data_ready:
            return self.notify(value)


class MetricPostProcess(MetricObserver):
    def update(self, _value):
        return _value
