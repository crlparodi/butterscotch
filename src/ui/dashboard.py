# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from ..query.expressions import ExpressionParserResolver

class Dashboard(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super(Dashboard, self).__init__(*args, **kwargs)
        self.list = []
        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle("butterscotch")

        expr_parser = ExpressionParserResolver()
        expr_parser.parse()
        self.list = expr_parser.resolve()

        self.setUI()

    def setUI(self):
        dashboard_menu = self.menuBar()
        dashboard_central_widget = QtWidgets.QWidget()
        file_menu = dashboard_menu.addMenu("&Fichier")
        file_menu.addAction("Quitter")

        panels = []
        dbox = QtWidgets.QGridLayout()
        dbox.setContentsMargins(20, 20, 20, 20)

        for item in self.list:
            for i in range(len(item.get_data())):
                panel_box = QtWidgets.QWidget()
                panel_layout = QtWidgets.QVBoxLayout()
                panel_label = QtWidgets.QLabel(self)
                panel_label.setText(item.get_query() + f"({i})")
                panel_value = QtWidgets.QLabel(self)
                panel_value.setText(item.get_data()[i].get_value())
                panel_layout.addWidget(panel_label)
                panel_layout.addWidget(panel_value)
                panel_box.setLayout(panel_layout)
                panels.append(panel_box)

        x, y = 0, 0
        for panel in panels:
            dbox.addWidget(panel, y, x)
            x += 1
            if not x % 3:
                y += 1
                x = 0

        dashboard_central_widget.setLayout(dbox)
        self.setCentralWidget(dashboard_central_widget)
        self.show()