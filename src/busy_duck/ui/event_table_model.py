from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor


class EventTableModel(QAbstractTableModel):
    HEADERS = ["Event", "Provider", "Starts", "Ends", "Location", "Status"]

    def __init__(self, rows: list[dict] | None = None) -> None:
        super().__init__()
        self._rows = rows or []

    def set_rows(self, rows: list[dict]) -> None:
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.HEADERS)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = self._rows[index.row()]
        column = self.HEADERS[index.column()]

        if role == Qt.DisplayRole:
            return row.get(column, "")

        if role == Qt.ToolTipRole:
            return row.get("Description", "")

        if role == Qt.ForegroundRole:
            if column == "Status":
                return QColor("#D95D39" if row.get(column) == "Conflict" else "#2A9D8F")

            if column == "Provider":
                return QColor(row.get("ProviderColor", "#172033"))

        if role == Qt.UserRole:
            return row

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.HEADERS[section]

        return section + 1

    def sort(self, column, order=Qt.AscendingOrder) -> None:
        key = self.HEADERS[column]
        self.layoutAboutToBeChanged.emit()
        self._rows.sort(
            key=lambda row: str(row.get(key, "")).lower(),
            reverse=order == Qt.DescendingOrder,
        )
        self.layoutChanged.emit()