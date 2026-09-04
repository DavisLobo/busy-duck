from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class EventTableModel(QAbstractTableModel):
    def __init__(self, rows=None):
        super().__init__()
        self._rows = rows or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        return 5

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        row = self._rows[index.row()]
        return row[index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            headers = ["Título", "Provedor", "Início", "Fim", "Resumo"]
            return headers[section]

        return section + 1