"""
name: Cyril PARODI
date: 28/09/2019
module: disk.py
"""

# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from .metric import MetricRequest, MetricCallback
from src.utils.conversions import convert_human, convert_percent

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

            r_rate_data = eval(r_rate_data)
            w_rate_data = eval(w_rate_data)
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
            rootfs_avail = self.request.process(self.expressions[
                                                         "panels"][
                                                    2]["targets"][0][
                                                    "expression"], 1)
            rootfs_total = self.request.process(self.expressions[
                                                         "panels"][
                                                    2]["targets"][1][
                                                    "expression"], 1)

            rootfs_avail = eval(rootfs_avail)
            rootfs_total = eval(rootfs_total)

            rootfs_used = rootfs_total - rootfs_avail
            rootfs_used_percent = convert_percent((rootfs_used /
                                                       rootfs_total) * 100)

            used_rootfs = (
                "Used Root FileSystem",
                f"{rootfs_used_percent} %"
            )
            #################################################################

            """
            Pack all the data
            """
            #################################################################
            self.metrics["DISK_RRATE"] = r_rate
            self.metrics["DISK_WRATE"] = w_rate
            self.metrics["USED_ROOTFS"] = used_rootfs
            #################################################################

            self.ready.emit(self.metrics)
            self.sleep(1)

    def run(self):
        self.refresh()