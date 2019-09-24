# -*- coding: utf-8 -*-

import json
from datetime import datetime
from ..http.http_downloader import HTTPEngine, PROMETHEUS_API_LINK_SEGMENT

"""
    Tuples designing the type and the format of the MetricData
"""

metric_type = ("NONE", "QUERY", "SET", "SERIES")
metric_format = ("NONE", "NUMBER", "PERCENT", "RATE")

"""
    Classes containing the panel data and all the targets (the expressions)
    for it.
    These expressions, when transmitted to the Prometheus Server and the 
    temporal data returned, are returned as MetricData (from 1 to many if the expression
    is a query or a query-set) into a MetricSet which is the panel wrapper (and contains
    the key and description). 
"""

class MetricData(object):
    """
    Piece of data from a specific hardware or a harware specification.

    :param str exp: The expression behind the data
    :param str instance: The instance where the data is get back
    :param str type: The type of the data (QUERY, QUERY-SET or SERIES)
    :param date date: The date and time of the data retrieval
    :param int/float value: The value behind the data
    :param str format: The formatting of the value (NUMBER, PERCENT or RATE)
    :param int decimals: The number of decimals for formatting
    :param str unit: The unit of the value (literal string)
    """

    def __init__(self, _json_panel_target, _instance="", _value=[]):
        """ Constructor method """
        self.expr = _json_panel_target["expr"]
        self.instance = _instance
        self.type = metric_type[0]
        self.date = datetime.now()
        self.value = _value
        self.format = _json_panel_target["format"]
        self.decimals = _json_panel_target["decimals"]
        self.unit = _json_panel_target["unit"]
        self.set_type(_json_panel_target["type"])

    def get_expr(self):
        return self.expr

    def get_instance(self):
        """ Return the name of the data """
        return self.instance

    def get_type(self):
        return self.type

    def get_date(self): 
        """ Return the date when the snapshot was taken """
        return self.date

    def get_value(self): 
        """ Return the value behind the data """
        return self.value

    def set_type(self, _json_panel_target_type):
        if _json_panel_target_type == "query":
            self.type = metric_type[1]
        elif _json_panel_target_type == "query-set":
            self.type = metric_type[2]
        elif _json_panel_target_type == "time-series":
            self.type = metric_type[3]

    def set_value(self, _value):
        """ This method is used to set the data from a given time """
        self.value = _value


class MetricSet(object):
    """
    This is the python logic representation of the panel.

    :param str key: The key of the panel representation
    :param str desc: The description of the panel representation
    :param list data: The list of MetricData (1 for a simple query, MANY for a query-set)
    """
    def __init__(self, _json_panel):
        """ Constructor method """
        self.key = _json_panel["key"]
        self.desc = _json_panel["desc"]
        self.exprs = []
        self.data = []

    def get_exprs(self):
        return self.exprs

    def get_data(self):
        return self.data

    def add_metric_data(self, _json_panel_target):
        self.data.append( _json_panel_target)

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

    def notify(self, process):
        for observer in self.observers:
            return observer.update(process)


class MetricObserver(object):
    def update(self, observarble_obj):
        raise NotImplementedError


"""
    Metrics Controller classes, theses classes are called when we wants to get
    a new metric Set with MetricData(s).
"""


class MetricProcess(MetricObservable):
    def __init__(self, _json_panel):
        super().__init__()
        self.json_panel = _json_panel
        self.set = MetricSet(self.json_panel)
        self.data_ready = False

    def process(self):
        downloader = HTTPEngine()
        for expr in self.set.get_exprs():
            hardware_json_data = json.load(downloader.download(PROMETHEUS_API_LINK_SEGMENT + expr))

            try:
                for result in hardware_json_data['data']['result']:
                    self.set.add_metric_data(MetricData(
                        self.json_panel,
                        _instance=result['metric']['instance'],
                        _value=result['value'][1]
                    ))
            except json.JSONDecodeError as ejson:
                print("Failed to get metric, passing...")
                assert False

        self.data_ready = True

        if self.data_ready:
            return self.notify(self)

    def get_metric_set(self):
        return self.set



class MetricPostProcess(MetricObserver):
    def update(self, process):
        return process.get_metric_set()
