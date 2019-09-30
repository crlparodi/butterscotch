"""
name: Cyril PARODI
date: 26/09/2019
module: cpu.py
"""

# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from .metric import MetricRequest, MetricCallback
from ..utils.conversions import convert_human

class CPUDataProcessing(QtCore.QThread):
    cpu_ready_signal = QtCore.pyqtSignal(object)

    def __init__(self, _expr_dict):
        super(CPUDataProcessing, self).__init__()

        self.expr_dict = _expr_dict

        self.metrics = {}

        self.metric_process = MetricRequest()
        self.metric_post_process = MetricCallback()

        self.metric_process.add_observer(self.metric_post_process)

    def generate(self):
        nbr_cores_tuple = (
            "Total number of Cores",
            self.metric_process.process(self.expr_dict["panels"][0]["targets"][0]["expression"])
        )
        self.metrics["CPU_NBR_CORES"] = nbr_cores_tuple

        for core_index in range(int(nbr_cores_tuple[1])):
            core_freq = "0"
            max_core_freq = "0"

            final_core_freq_tuple = (
                f"CPU Core {core_index + 1} Frequency",
                convert_human(core_freq) + "Hz / " + convert_human(max_core_freq) + "Hz"
            )
            self.metrics[f"CPU_CORE_{core_index}_FREQ"] = final_core_freq_tuple

        return self.metrics

    def refresh(self):
        while True:
            nbr_cores_tuple = (
                "Total number of Cores",
                self.metric_process.process(self.expr_dict["panels"][0]["targets"][0]["expression"])
            )
            self.metrics["CPU_NBR_CORES"] = nbr_cores_tuple

            for core_index in range(int(nbr_cores_tuple[1])):
                core_freq = self.metric_process.process(
                    self.expr_dict["panels"][1]["targets"][0]["expression"],
                    core_index
                )
                max_core_freq = self.metric_process.process(
                    self.expr_dict["panels"][1]["targets"][1]["expression"],
                    core_index
                )
                final_core_freq_tuple = (
                    f"CPU Core {core_index + 1} Frequency",
                    convert_human(core_freq) + "Hz / " + convert_human(max_core_freq) + "Hz"
                )
                self.metrics[f"CPU_CORE_{core_index}_FREQ"] = final_core_freq_tuple

            self.cpu_ready_signal.emit(self.metrics)
            self.sleep(1)

    def run(self):
        self.refresh()