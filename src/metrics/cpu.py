"""
name: Cyril PARODI
date: 26/09/2019
module: cpu.py
"""

# -*- coding: utf-8 -*-

from .metric import MetricProcess, MetricPostProcess
from ..utils.conversions import convert_human

class CPUBoard(object):
    def __init__(self):
        self.metrics = {}

        self.metric_process = MetricProcess()
        self.metric_post_process = MetricPostProcess()

        self.metric_process.add_observer(self.metric_post_process)


    def process(self, _expr_dict):
        nbr_cores_tuple = (
            "Total number of Cores",
            self.metric_process.process(_expr_dict["panels"][0]["targets"][0]["expression"])
        )
        self.metrics["CPU_NBR_CORES"] = nbr_cores_tuple

        for core_index in range(int(nbr_cores_tuple[1])):
            core_freq = self.metric_process.process(
                _expr_dict["panels"][1]["targets"][0]["expression"],
                core_index
            )
            max_core_freq = self.metric_process.process(
                _expr_dict["panels"][1]["targets"][1]["expression"],
                core_index
            )
            final_core_freq_tuple = (
                f"CPU Core {core_index + 1} Frequency",
                convert_human(int(core_freq)) + "Hz / " + convert_human(int(max_core_freq)) + "Hz"
            )
            self.metrics[f"CPU_CORE_{core_index}_FREQ"] = final_core_freq_tuple

        return self.metrics