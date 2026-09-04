from __future__ import annotations

from datetime import datetime, timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from busy_duck.app import get_analytics_for_window, get_events_in_window, sync_all


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Busy Duck")
        self.resize(1100, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        top_bar = QHBoxLayout()
        self.sync_button = QPushButton("Sincronizar")
        self.refresh_button = QPushButton("Atualizar eventos")
        self.analytics_button = QPushButton("Ver analytics")

        self.sync_button.clicked.connect(self.sync_all_providers)
        self.refresh_button.clicked.connect(self.refresh_events)
        self.analytics_button.clicked.connect(self.show_analytics)

        top_bar.addWidget(self.sync_button)
        top_bar.addWidget(self.refresh_button)
        top_bar.addWidget(self.analytics_button)
        self.layout.addLayout(top_bar)

        self.summary_label = QLabel("Nenhum evento carregado.")
        self.layout.addWidget(self.summary_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Título", "Provedor", "Início", "Fim", "Resumo"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.layout.addWidget(self.table)

        self.refresh_events()

    def sync_all_providers(self) -> None:
        try:
            result = sync_all()
            summary = ", ".join(f"{k}: {v}" for k, v in result.items())
            QMessageBox.information(self, "Sincronização", f"Sincronização concluída.\n{summary}")
            self.refresh_events()
        except Exception as exc:  # pragma: no cover
            QMessageBox.critical(self, "Erro", str(exc))

    def refresh_events(self) -> None:
        start = datetime.now() - timedelta(days=7)
        end = datetime.now() + timedelta(days=7)

        events = get_events_in_window(start, end)
        self._load_events(events)

        analytics = get_analytics_for_window(start, end)
        self.summary_label.setText(
            f"Eventos: {analytics['events_count']} | "
            f"Conflitos: {analytics['conflicts_count']} | "
            f"Tempo livre: {analytics['free_time']}"
        )

    def show_analytics(self) -> None:
        start = datetime.now() - timedelta(days=7)
        end = datetime.now() + timedelta(days=7)
        analytics = get_analytics_for_window(start, end)
        QMessageBox.information(
            self,
            "Analytics",
            (
                f"Eventos: {analytics['events_count']}\n"
                f"Conflitos: {analytics['conflicts_count']}\n"
                f"Tempo livre: {analytics['free_time']}"
            ),
        )

    def _load_events(self, events) -> None:
        self.table.setRowCount(len(events))
        for row, event in enumerate(events):
            self.table.setItem(row, 0, QTableWidgetItem(event.title or "Sem título"))
            self.table.setItem(row, 1, QTableWidgetItem(str(event.provider_id)))
            self.table.setItem(row, 2, QTableWidgetItem(event.start_datetime.strftime("%d/%m/%Y %H:%M")))
            self.table.setItem(row, 3, QTableWidgetItem(event.end_datetime.strftime("%d/%m/%Y %H:%M")))
            self.table.setItem(row, 4, QTableWidgetItem(event.description or "Sem resumo"))

        self.table.resizeColumnsToContents()