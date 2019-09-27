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
        cpu_board_process = CPUBoardProcess(expr_parser.parse()["cpu"])
        cpu_board_process.cpu_ready_signal.connect(self.generate_cpu_board)
        cpu_board_process.start()

        self.set_UI()

    def generate_cpu_board(self, _board_group):
        xpos, ypos = 0, 0

        cpu_board = Board(_board_group, "CPU")
        nbr_cores_panel = Panel(_board_group["CPU_NBR_CORES"])
        cpu_board.add_item(nbr_cores_panel, 0, 0)

        ypos = 1
        for core_index in range(int(_board_group["CPU_NBR_CORES"][1])):
            cpu_board.add_item(Panel(_board_group[f"CPU_CORE_{core_index}_FREQ"]), xpos, ypos)
            ypos += 1
            if ypos % ((int(_board_group["CPU_NBR_CORES"][1]) / 2) + 1) == 0:
                xpos += 1
                ypos = 1
        cpu_board.freeze_layout()

    def refresh_cpu_board(self, _board_group):
        pass

    def set_UI(self):
        dashboard_menu = self.menuBar()
        dashboard_central_widget = QtWidgets.QWidget()
        file_menu = dashboard_menu.addMenu("&Fichier")
        edit_menu = dashboard_menu.addMenu("&Edit")
        help_menu = dashboard_menu.addMenu("&Help")
        file_menu.addAction("Quitter")

        dbox = QtWidgets.QVBoxLayout()
        dbox.setContentsMargins(20, 20, 20, 20)

        dashboard_central_widget.setLayout(dbox)
        self.setCentralWidget(dashboard_central_widget)






