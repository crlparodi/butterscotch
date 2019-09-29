"""
name: Cyril PARODI
date: 24/09/2019
module: metric.py
"""

# -*- coding: utf-8 -*-

import json
from ..http.http_request import HTTPRequester, PROMAPI_QUERY_SEGMENT
from ..exceptions.exceptions import HTTPError

"""
    Metrics processing observer pattern.
    These classes allows to the processing metrics controllers to update  
    the data.
    only when the expressions are resolved and stored into the  
    MetricSet/Data classes.
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
    def update(self, _value):
        raise NotImplementedError


"""
    Metrics Controller classes, theses classes are called when we wants to get
    a new metric value.
"""

class MetricRequest(MetricObservable):
    def __init__(self):
        super().__init__()
        self.data_valid = False

    def process(self, _expr, _value_index=0):
        value = "--"

        try:
            json_dict = json.load(HTTPRequester().request(
                PROMAPI_QUERY_SEGMENT + _expr
            ))

            # Verify that there's no error (parse error for example)
            if json_dict["status"] == "success":
                # Verify that the query is correct (so the query returns data)
                if json_dict['data']['result']:
                    value = json_dict['data']['result'][_value_index][
                        "value"][1]
                    self.data_valid = True
                else:
                    raise KeyError
            else:
                raise HTTPError

        except HTTPError:
            print(f"Failed to download the data for {_expr}, passing...")
        except json.JSONDecodeError:
            print(f"Failed to decode JSON for {_expr}, passing...")
        except KeyError:
            print(f"No data for {_expr}, passing...")

        if self.data_valid:
            return self.notify(value)


class MetricCallback(MetricObserver):
    def update(self, _value):
        return _value
