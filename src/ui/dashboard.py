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
from src.query.expressions import ExpressionParserResolver
from src.metrics.cpu import CPUDataProcessing
from src.metrics.memory import MemoryDataProcessing
from src.metrics.disk import DiskDataProcessing

class Dashboard(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)

        print("Generating the dashboard ...")

        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle("butterscotch - Dashboard")

        expr_parser = ExpressionParserResolver()

        """
        Building the CPU Board
        """
        #################################################################
        self.cpu_board_process = CPUDataProcessing(expr_parser.parse()["cpu"])
        self.cpu_board = self.generate_cpu_board(self.cpu_board_process.generate())

        self.cpu_board_process.cpu_ready_signal.connect(self.refresh_cpu_board)
        self.cpu_board_process.start()
        #################################################################

        """
        Building the Memory Board
        """
        #################################################################
        self.memory_board_process = MemoryDataProcessing(expr_parser.parse()["memory"])
        self.memory_board = self.generate_memory_board(self.memory_board_process.generate())

        self.memory_board_process.mem_ready_signal.connect(self.refresh_memory_board)
        self.memory_board_process.start()
        #################################################################

        """
        Building the Disk Board
        """
        #################################################################
        self.disk_board_process = DiskDataProcessing(expr_parser.parse()["disk"])
        self.disk_board = self.generate_disk_board(self.disk_board_process.generate())

        self.disk_board_process.ready.connect(self.refresh_disk_board)
        self.disk_board_process.start()
        #################################################################

        self.set_UI(
            [
                self.cpu_board,
                self.memory_board,
                self.disk_board
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
            self.cpu_board.panels[f"CPU_CORE_{core_index}_FREQ"].panel_value.setText(
                _board_group[f"CPU_CORE_{core_index}_FREQ"][1]
            )

    def generate_memory_board(self, _board_group={}):
        memory_board = Board(_board_group, "Memory")

        used_ram = Panel(_board_group["USED_RAM"])
        memory_board.add_item(used_ram, "USED_RAM",  0, 0)

        used_swap = Panel(_board_group["USED_SWAP"])
        memory_board.add_item(used_swap, "USED_SWAP", 0, 1)

        memory_board.freeze_layout()

        return memory_board

    def refresh_memory_board(self, _board_group={}):
        self.memory_board.panels["USED_RAM"].panel_value.setText(_board_group["USED_RAM"][1])

        self.memory_board.panels["USED_SWAP"].panel_value.setText(_board_group["USED_SWAP"][1])

    def generate_disk_board(self, _board_group={}):
        disk_board = Board(_board_group, "Disk")

        read_rate = Panel(_board_group["DISK_RRATE"])
        disk_board.add_item(read_rate, "DISK_RRATE",  0, 0)

        write_rate = Panel(_board_group["DISK_WRATE"])
        disk_board.add_item(write_rate, "DISK_WRATE", 0, 1)

        used_rootfs = Panel(_board_group["USED_ROOTFS"])
        disk_board.add_item(used_rootfs, "USED_ROOTFS", 0, 2)

        disk_board.freeze_layout()

        return disk_board

    def refresh_disk_board(self, _board_group={}):
        self.disk_board.panels["DISK_RRATE"].panel_value.setText(_board_group["DISK_RRATE"][1])
        self.disk_board.panels["DISK_WRATE"].panel_value.setText(_board_group["DISK_WRATE"][1])
        self.disk_board.panels["USED_ROOTFS"].panel_value.setText(
            _board_group["USED_ROOTFS"][1])

    def set_UI(self, _boards=[]):
        dashboard_menu = self.menuBar()
        dashboard_central_widget = QtWidgets.QWidget()
        file_menu = dashboard_menu.addMenu("&Fichier")
        file_menu.addAction("Quitter")
        edit_menu = dashboard_menu.addMenu("&Edit")
        edit_menu.addAction("Préférences")
        help_menu = dashboard_menu.addMenu("&Help")
        help_menu.addAction("À propos")

        dbox = QtWidgets.QVBoxLayout()
        dbox.setContentsMargins(20, 20, 20, 20)

        for board in _boards:
            dbox.addWidget(board)

        dashboard_central_widget.setLayout(dbox)
        self.setCentralWidget(dashboard_central_widget)
