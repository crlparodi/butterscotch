"""
name: Cyril PARODI
date: 24/09/2019
module: panel.py
"""

# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from ..utils.conversions import convert_human

class Panel(QtWidgets.QFrame):
    def __init__(self, _metric_tuple, _index=0, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Minimum size: 190x90
        self.setMinimumSize(250, 100)
        self.setMaximumSize(250, 100)

        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        self.panel_name  = QtWidgets.QLabel(self)
        self.panel_value = QtWidgets.QLabel(self)

        self.panel_name.setGeometry(0, 0, 250, 30)
        self.panel_value.setGeometry(0, 20, 250, 70)

        self.panel_name.setAlignment(QtCore.Qt.AlignCenter)
        self.panel_value.setAlignment(QtCore.Qt.AlignCenter)

        self.panel_name.setText(_metric_tuple[0])
        self.panel_value.setText(_metric_tuple[1])

        self.panel_value.setFont(QtGui.QFont('SansSerifBold', 16))
        self.panel_layout = QtWidgets.QVBoxLayout()
        self.panel_layout.addWidget(self.panel_name)
        self.panel_layout.addWidget(self.panel_value)


