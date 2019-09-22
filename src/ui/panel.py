# -*- coding: utf-8 -*-

from ..metrics.metric import MetricSet
from PyQt5 import QtWidgets, QtCore

class PanelModel(QtCore.QAbstractItemModel):
    def __init__(self, _set, _data_index, parent=None, *args, **kwargs):
        super(PanelModel, self).__init__(*args, **kwargs)
        self.set = _set
        self.data_index = _data_index

    def data(self, index, role):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant
        #return str(self.set.get_data()[self.data_index].get_value())
        return "Braise"


class PanelView(QtWidgets.QAbstractItemView):
    def __init__(self, parent=None, *args, **kwargs):
        super(PanelView, self).__init__(*args, **kwargs)
