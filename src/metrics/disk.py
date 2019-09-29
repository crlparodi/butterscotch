"""
name: Cyril PARODI
date: 28/09/2019
module: disk.py
"""

# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from .metric import MetricRequest, MetricCallback
from ..utils.conversions import convert_human, convert_percent

class DiskDataProcessing(QtCore.QThread):
    ready = QtCore.pyqtSignal(object)

    def __init__(self, _expressions={}):
        super(DiskDataProcessing, self).__init__()

        self.expressions = _expressions

        self.metrics = {}

        self.request = MetricRequest()
        self.callback = MetricCallback()

        self.request.add_observer(self.callback)

    def generate(self):
        self.metrics["DISK_RRATE"] = ("Disk Read Rate", "0 B/s")
        self.metrics["DISK_WRATE"] = ("Disk Write Rate", "0 B/s")
        self.metrics["USED_ROOTFS"] = ("Used Root FileSystem", "0 %")

        return self.metrics

    def refresh(self):
        while True:
            """
            Request the rates data
            """
            #################################################################
            r_rate_data = self.request.process(self.expressions["panels"][0]["targets"][0]["expression"])
            w_rate_data = self.request.process(self.expressions["panels"][1]["targets"][0]["expression"])
            #################################################################

            """
            Get back the Rates data (R + W)
            """
            #################################################################
            r_rate = (
                "Disk Read Rate",
                f"{convert_human(r_rate_data)}o/s"
            )
            w_rate = (
                "Disk Write Rate",
                f"{convert_human(w_rate_data)}o/s"
            )
            #################################################################

            """
            Request and process the Used RootFS data
            """
            #################################################################

            #################################################################

            """
            Pack all the data
            """
            #################################################################
            self.metrics["DISK_RRATE"] = r_rate
            self.metrics["DISK_WRATE"] = w_rate
            #################################################################

            self.ready.emit(self.metrics)
            self.sleep(1)

    def run(self):
        self.refresh()