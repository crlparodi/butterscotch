"""
name: Cyril PARODI
date: 28/09/2019
module: memory.py
"""

# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from .metric import MetricRequest, MetricCallback
from ..utils.conversions import convert_percent

class MemoryDataProcessing(QtCore.QThread):
    mem_ready_signal = QtCore.pyqtSignal(object)

    def __init__(self, _expr_dict = {}):
        super(MemoryDataProcessing, self).__init__()

        self.expr_dict = _expr_dict

        self.metrics = {}

        self.metric_process = MetricRequest()
        self.metric_post_process = MetricCallback()

        self.metric_process.add_observer(self.metric_post_process)

    def generate(self):
        self.metrics["USED_RAM"] = ("Used RAM", "0 %")
        self.metrics["USED_SWAP"] = ("Used SWAP", "0 %")

        return self.metrics

    def refresh(self):
        while True:

            """
            Get back the RAM data and calculate the Used RAM Percentage
            """
            #################################################################
            used_ram = \
                eval(self.metric_process.process(self.expr_dict["panels"][0]["targets"][0]["expression"])) - \
                (
                    eval(self.metric_process.process(self.expr_dict["panels"][0]["targets"][1]["expression"])) +
                    eval(self.metric_process.process(self.expr_dict["panels"][0]["targets"][2]["expression"])) +
                    eval(self.metric_process.process(self.expr_dict["panels"][0]["targets"][3]["expression"]))
                )
            used_ram_percentage = used_ram / eval(self.metric_process.process(self.expr_dict["panels"][0]["targets"][0]["expression"])) * 100
            used_ram_percentage_str = str(used_ram_percentage)

            used_ram_tuple = (
                "Used RAM",
                f"{convert_percent(used_ram_percentage_str)} %"
            )
            #################################################################

            """
            Get back the Swap data and calculate the Used Swap Percentage
            """
            #################################################################
            used_swap = \
                eval(self.metric_process.process(self.expr_dict["panels"][1]["targets"][0]["expression"])) - \
                eval(self.metric_process.process(self.expr_dict["panels"][1]["targets"][1]["expression"]))

            used_swap_percentage = used_swap / eval(self.metric_process.process(self.expr_dict["panels"][1]["targets"][0]["expression"])) * 100
            used_swap_percentage_str = str(used_swap_percentage)

            used_swap_tuple = (
                "Used Swap",
                f"{convert_percent(used_swap_percentage_str)} %"
            )
            #################################################################

            """
            Pack all the data
            """
            #################################################################
            self.metrics["USED_RAM"] = used_ram_tuple
            self.metrics["USED_SWAP"] = used_swap_tuple
            #################################################################

            """
            Send all the data
            """
            #################################################################
            self.mem_ready_signal.emit(self.metrics)
            self.sleep(1) # Wait one second before refreshing
            #################################################################

    def run(self):
        self.refresh()