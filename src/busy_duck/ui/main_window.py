from __future__ import annotations

from datetime import datetime, time, timedelta

from PySide6.QtCore import QDate, Qt, QItemSelection, QItemSelectionModel
from PySide6.QtGui import QAction, QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QDateEdit,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from busy_duck.app import (
    get_analytics_for_window,
    get_events_in_window,
    sync_all,
)
from busy_duck.ui.event_table_model import EventTableModel
from busy_duck.ui.theme import DARK_THEME, LIGHT_THEME


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Busy Duck · Unified Calendar")
        self.resize(1360, 820)
        self.setMinimumSize(1050, 650)

        self.events = []
        self.model = EventTableModel()

        self._build_menu()
        self._build_ui()
        self._apply_theme()
        self.refresh_events()

    def _build_menu(self) -> None:
        about = QAction("About Busy Duck", self)
        about.triggered.connect(self._show_about)

        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(about)

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_sidebar())
        layout.addWidget(self._build_content(), 1)

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(245)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(22, 28, 22, 22)
        layout.setSpacing(12)

        logo = QLabel("🦆  BUSY DUCK")
        logo.setObjectName("logo")
        layout.addWidget(logo)

        tagline = QLabel("All your calendars in one pond.")
        tagline.setObjectName("tagline")
        tagline.setWordWrap(True)
        layout.addWidget(tagline)

        layout.addSpacing(28)

        for label in ("Overview", "Calendar", "Availability", "Insights"):
            button = QPushButton(label)
            button.setObjectName("navButton")
            button.setEnabled(label == "Calendar")
            layout.addWidget(button)

        layout.addSpacing(24)

        providers_title = QLabel("CONNECTED PROVIDERS")
        providers_title.setObjectName("sectionTitle")
        layout.addWidget(providers_title)

        for provider, color in (
            ("Google Calendar", "#4285F4"),
            ("Microsoft Outlook", "#0078D4"),
        ):
            row = QHBoxLayout()
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 18px;")
            name = QLabel(provider)
            name.setObjectName("providerLabel")
            row.addWidget(dot)
            row.addWidget(name)
            row.addStretch()
            layout.addLayout(row)

        layout.addStretch()

        local = QLabel("LOCAL-FIRST STORAGE\nSQLite database · Read-only sync")
        local.setObjectName("localStorage")
        layout.addWidget(local)

        return sidebar

    def _build_content(self) -> QWidget:
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(34, 28, 34, 26)
        layout.setSpacing(20)

        header = QHBoxLayout()

        title_box = QVBoxLayout()
        title = QLabel("Calendar overview")
        title.setObjectName("pageTitle")

        subtitle = QLabel("A clear view of your workday across every connected agenda.")
        subtitle.setObjectName("pageSubtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        header.addLayout(title_box)
        header.addStretch()

        self.theme_button = QPushButton("☾")
        self.theme_button.setToolTip("Toggle dark mode")
        self.theme_button.clicked.connect(self.toggle_theme)
        header.addWidget(self.theme_button)

        self.sync_button = QPushButton("↻  Sync calendars")
        self.sync_button.setObjectName("primaryButton")
        self.sync_button.clicked.connect(self.sync_all_providers)
        header.addWidget(self.sync_button)

        layout.addLayout(header)

        filters = QHBoxLayout()

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.dateChanged.connect(self.refresh_events)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate().addDays(7))
        self.end_date.dateChanged.connect(self.refresh_events)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search events, locations, or providers…")
        self.search.textChanged.connect(self._filter_events)

        self.view_selector = QComboBox()
        self.view_selector.addItems(["Agenda view", "Week view"])
        self.view_selector.setEnabled(False)

        filters.addWidget(QLabel("From"))
        filters.addWidget(self.start_date)
        filters.addWidget(QLabel("To"))
        filters.addWidget(self.end_date)
        filters.addWidget(self.search, 1)
        filters.addWidget(self.view_selector)

        layout.addLayout(filters)

        self.cards = QGridLayout()
        self.events_card = self._metric_card("EVENTS", "0", "#2F80ED")
        self.conflicts_card = self._metric_card("CONFLICTS", "0", "#D95D39")
        self.free_card = self._metric_card("AVAILABLE TIME", "—", "#2A9D8F")

        self.cards.addWidget(self.events_card, 0, 0)
        self.cards.addWidget(self.conflicts_card, 0, 1)
        self.cards.addWidget(self.free_card, 0, 2)
        layout.addLayout(self.cards)

        section_header = QHBoxLayout()
        section_title = QLabel("Unified agenda")
        section_title.setObjectName("sectionHeading")

        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")

        section_header.addWidget(section_title)
        section_header.addStretch()
        section_header.addWidget(self.status_label)
        layout.addLayout(section_header)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        layout.addWidget(self.table, 1)

        return content

    def _metric_card(self, label: str, value: str, color: str) -> QFrame:
        card = QFrame()
        card.setObjectName("metricCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 15, 18, 15)

        label_widget = QLabel(label)
        label_widget.setObjectName("metricLabel")

        value_widget = QLabel(value)
        value_widget.setObjectName("metricValue")
        value_widget.setProperty("metricColor", color)

        layout.addWidget(label_widget)
        layout.addWidget(value_widget)

        card.value_widget = value_widget
        return card

    def _date_range(self) -> tuple[datetime, datetime]:
        start = self.start_date.date().toPython()
        end = self.end_date.date().toPython()

        start_datetime = datetime.combine(start, time.min)
        end_datetime = datetime.combine(end, time.max)

        if start_datetime >= end_datetime:
            raise ValueError("The start date must be before the end date.")

        return start_datetime, end_datetime

    def refresh_events(self) -> None:
        try:
            start, end = self._date_range()
            self.events = get_events_in_window(start, end)
            self._render_events(self.events)

            analytics = get_analytics_for_window(start, end)
            self.events_card.value_widget.setText(str(analytics["events_count"]))
            self.conflicts_card.value_widget.setText(str(analytics["conflicts_count"]))

            free_time = analytics["free_time"]
            hours = free_time.total_seconds() / 3600
            self.free_card.value_widget.setText(f"{hours:.1f}h")

            self.status_label.setText(
                f"Updated {datetime.now().strftime('%H:%M')} · Local data"
            )
        except Exception as exc:
            self.status_label.setText("Unable to load calendar")
            QMessageBox.critical(self, "Calendar error", str(exc))

    def _render_events(self, events) -> None:
        conflicts = self._conflicting_events(events)
        rows = []

        for event in events:
            provider = str(event.provider_id)
            provider_name = (
                "Google Calendar"
                if "google" in provider.lower()
                else "Microsoft Outlook"
            )

            provider_color = (
                "#4285F4"
                if "google" in provider.lower()
                else "#0078D4"
            )

            rows.append(
                {
                    "Event": event.title or "Untitled event",
                    "Provider": provider_name,
                    "ProviderColor": provider_color,
                    "Starts": event.start_datetime.strftime(
                        "%d %b %Y · %H:%M"
                    ),
                    "Ends": event.end_datetime.strftime("%H:%M"),
                    "Location": event.location or "—",
                    "Status": "Conflict" if event in conflicts else "Confirmed",
                    "Description": event.description or "",
                }
            )

        self.model.set_rows(rows)
        self.table.resizeColumnsToContents()

    def _filter_events(self, text: str) -> None:
        query = text.strip().lower()

        if not query:
            self._render_events(self.events)
            return

        filtered = [
            event
            for event in self.events
            if query in " ".join(
                [
                    event.title or "",
                    event.description or "",
                    event.location or "",
                    str(event.provider_id),
                ]
            ).lower()
        ]

        self._render_events(filtered)

    def _conflicting_events(self, events) -> set:
        conflicts = set()

        for index, event in enumerate(events):
            for other in events[index + 1:]:
                if (
                    event.start_datetime < other.end_datetime
                    and other.start_datetime < event.end_datetime
                ):
                    conflicts.add(event)
                    conflicts.add(other)

        return conflicts

    def sync_all_providers(self) -> None:
        self.sync_button.setEnabled(False)
        self.sync_button.setText("⟳  Syncing…")
        self.status_label.setText("Synchronizing connected providers…")

        try:
            result = sync_all()
            summary = ", ".join(f"{name}: {count}" for name, count in result.items())

            QMessageBox.information(
                self,
                "Synchronization complete",
                f"Calendars synchronized successfully.\n\n{summary}",
            )
            self.refresh_events()
        except Exception as exc:
            QMessageBox.critical(self, "Synchronization error", str(exc))
        finally:
            self.sync_button.setEnabled(True)
            self.sync_button.setText("↻  Sync calendars")

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About Busy Duck",
            (
                "<h2>Busy Duck 🦆</h2>"
                "<p>All your calendars in one pond.</p>"
                "<p>A local-first calendar aggregation application.</p>"
                "<p><b>License:</b> GNU GPL v3</p>"
                "<p>This software is provided without warranty.</p>"
            ),
        )

    def _apply_theme(self) -> None:
        self.setStyleSheet(DARK_THEME if self.dark_mode else LIGHT_THEME)

    def toggle_theme(self) -> None:
        self.dark_mode = not self.dark_mode
        self.setStyleSheet(DARK_THEME if self.dark_mode else LIGHT_THEME)
        self.theme_button.setText("☀" if self.dark_mode else "☾")

    def _show_selected_event(
        self,
        selected: QItemSelection,
        deselected: QItemSelection,
    ) -> None:
        indexes = selected.indexes()
        if not indexes:
            return

        row = self.model.data(indexes[0], Qt.UserRole)
        if not row:
            return

        QMessageBox.information(
            self,
            row.get("Event", "Event details"),
            (
                f"<b>Provider:</b> {row.get('Provider', '—')}<br>"
                f"<b>When:</b> {row.get('Starts', '—')} – "
                f"{row.get('Ends', '—')}<br>"
                f"<b>Location:</b> {row.get('Location', '—')}<br><br>"
                f"{row.get('Description', '')}"
            ),
        )