"""
name: Cyril PARODI
date: 26/09/2019
module: board.py
"""

# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

class Board(QtWidgets.QGroupBox):
    def __init__(self, _board, _name, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.panels = {}

        # Layout of the Board
        self.layout = QtWidgets.QGridLayout()

        # There's only one key at the top of the board
        # But this is the only way to get back the name of the Key
        self.setTitle(_name)

    def add_item(self, _item, _name, _line, _column):
        self.panels[_name] = _item
        self.layout.addWidget(_item, _line, _column)

    def freeze_layout(self):
        self.setLayout(self.layout)
