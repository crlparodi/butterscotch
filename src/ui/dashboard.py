"""
name: Cyril PARODI
date: 24/09/2019
module: dashboard.py
"""

# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from .board import Board
from .panel import Panel
from ..query.expressions import ExpressionParserResolver

class Dashboard(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)
        self.board_list = []
        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle("butterscotch - Dashboard")

        expr_parser = ExpressionParserResolver()
        expr_parser.parse()
        self.board_list = expr_parser.resolve()

        self.generator = DashboardGenerator()
        self.dashboard_content = self.generator.generate_boards(self.board_list)
        self.set_UI(self.dashboard_content)


    def set_UI(self, _dashboard_content):
        dashboard_menu = self.menuBar()
        dashboard_central_widget = QtWidgets.QWidget()
        file_menu = dashboard_menu.addMenu("&Fichier")
        edit_menu = dashboard_menu.addMenu("&Edit")
        help_menu = dashboard_menu.addMenu("&Help")
        file_menu.addAction("Quitter")

        dbox = QtWidgets.QVBoxLayout()
        dbox.setContentsMargins(20, 20, 20, 20)

        for board in _dashboard_content:
            dbox.addWidget(board)

        dashboard_central_widget.setLayout(dbox)
        self.setCentralWidget(dashboard_central_widget)
        self.show()


class DashboardGenerator(object):
    def __init__(self, *args, **kwargs):
        self.boards = []

    def generate_boards(self, _board_group):
        xpos, ypos = 0, 0

        cpu_board = Board(_board_group["CPU"], "CPU")
        cpu_board.add_item(Panel(_board_group["CPU"]["CPU_NBR_CORES"]), 0, 0)

        ypos = 1
        for core_index in range(int(_board_group["CPU"]["CPU_NBR_CORES"][1])):
            cpu_board.add_item(Panel(_board_group["CPU"][f"CPU_CORE_{core_index}_FREQ"]), xpos, ypos)
            ypos += 1
            if ypos % ((int(_board_group["CPU"]["CPU_NBR_CORES"][1]) / 2) + 1) == 0:
                xpos += 1
                ypos = 1
        cpu_board.freeze_layout()

        self.boards.append(cpu_board)

        return self.boards

