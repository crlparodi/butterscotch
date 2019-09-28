"""
name: Cyril PARODI
date: 24/09/2019
module: dashboard.py
"""

# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import time as time
from .board import Board
from .panel import Panel
from ..query.expressions import ExpressionParserResolver
from ..metrics.cpu import CPUBoardProcess

class Dashboard(QtWidgets.QMainWindow):
    """
        TODO: Better Board Management (Init then Refresh)
    """

    def __init__(self, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)

        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle("butterscotch - Dashboard")

        expr_parser = ExpressionParserResolver()

        self.cpu_board_process = CPUBoardProcess(expr_parser.parse()["cpu"])

        self.cpu_board_process.cpu_ready_signal.connect(self.refresh_cpu_board)
        self.cpu_board_process.start()

        self.cpu_board = self.generate_cpu_board(self.cpu_board_process.generate())

        self.set_UI(
            [
                self.cpu_board,
            ]
        )

    def generate_cpu_board(self, _board_group={}):
        xpos, ypos = 0, 0

        cpu_board = Board(_board_group, "CPU")
        nbr_cores_panel = Panel(_board_group["CPU_NBR_CORES"])
        cpu_board.add_item(nbr_cores_panel, "CPU_NBR_CORES",  0, 0)

        ypos = 1
        for core_index in range(int(_board_group["CPU_NBR_CORES"][1])):
            cpu_board.add_item(Panel(_board_group[f"CPU_CORE_{core_index}_FREQ"]), f"CPU_CORE_{core_index}_FREQ", xpos, ypos)
            ypos += 1
            if ypos % ((int(_board_group["CPU_NBR_CORES"][1]) / 2) + 1) == 0:
                xpos += 1
                ypos = 1
        cpu_board.freeze_layout()

        return cpu_board

    def refresh_cpu_board(self, _board_group={}):
        for core_index in range(int(_board_group["CPU_NBR_CORES"][1])):
            self.cpu_board.panels[f"CPU_CORE_{core_index}_FREQ"].panel_name.setText(
                _board_group[f"CPU_CORE_{core_index}_FREQ"][0]
            )
            self.cpu_board.panels[f"CPU_CORE_{core_index}_FREQ"].panel_value.setText(
                _board_group[f"CPU_CORE_{core_index}_FREQ"][1]
            )

    def set_UI(self, _boards=[]):
        dashboard_menu = self.menuBar()
        dashboard_central_widget = QtWidgets.QWidget()
        file_menu = dashboard_menu.addMenu("&Fichier")
        edit_menu = dashboard_menu.addMenu("&Edit")
        help_menu = dashboard_menu.addMenu("&Help")
        file_menu.addAction("Quitter")

        dbox = QtWidgets.QVBoxLayout()
        dbox.setContentsMargins(20, 20, 20, 20)

        for board in _boards:
            dbox.addWidget(board)

        dashboard_central_widget.setLayout(dbox)
        self.setCentralWidget(dashboard_central_widget)






