# -*- coding: utf-8 -*-

import json
from datetime import datetime
from PyQt5 import QtCore
from ..http.http_downloader import HTTPEngine, PROMETHEUS_API_LINK_SEGMENT

class MetricData(object):
    """
    Piece of data from a specific hardware or a harware specification.

    :param str name: The name of the data (it could be the hardware itself of a spec from the hardware)
    :param date date: The date and time of the data retrieval
    :param int/float value: The value behind the data
    """

    def __init__(self, _instance="", _value=[]):
        """ Constructor method """
        self.instance = _instance
        self.date = datetime.now()
        self.value = _value
    
    def get_query(self): 
        """ Return the name of the data """
        return self.query

    def get_date(self): 
        """ Return the date when the snapshot was taken """
        return self.date

    def get_value(self): 
        """ Return the value behind the data """
        return self.value

    def set_value(self, _value):
        """ This method is used to set the data from a given time """
        self.value = _value


class MetricSet(object):
    def __init__(self, _query):
        self.query = _query
        self.data = []

    def get_query(self):
        return self.query

    def get_data(self):
        return self.data

    def add_metric_data(self, metric_data):
        self.data.append(metric_data)

    def remove_metric_data(self, metric_data):
        del(self.data[metric_data])


class MetricObservable(object):
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        del(self.observers[observer])

    def notify(self, process):
        for observer in self.observers:
            observer.update(process)


class MetricProcess(MetricObservable):
    def __init__(self, _query):
        super().__init__()
        self.set = MetricSet(_query)
        self.data_ready = False

    def process(self):
        downloader = HTTPEngine()
        hardware_json_data = json.load(downloader.download(PROMETHEUS_API_LINK_SEGMENT + self.set.get_query()))

        try:
            for result in hardware_json_data['data']['result']:
                self.set.add_metric_data(MetricData(
                    _instance=result['metric']['instance'],
                    _value=result['value'][1]
                ))
            self.data_ready = True
        except json.JSONDecodeError as ejson:
            print("Failed to get metric, passing...")

        if self.data_ready:
            self.notify(self)

    def get_metric_set(self):
        return self.set


class MetricObserver(object):
    def update(self, observarble_obj):
        raise NotImplementedError


class MetricPostProcess(MetricObserver, QtCore.QObject):
    def update(self, process):
        print("Query :", process.get_metric_set().get_query())
