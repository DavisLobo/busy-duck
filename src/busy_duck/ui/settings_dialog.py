from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QWidget,
    QMessageBox,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
)

from busy_duck.config_store import (
    get_secret,
    get_value,
    set_secret,
    set_value,
)


class SettingsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Settings · Busy Duck")
        self.setMinimumSize(620, 500)

        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        title = QLabel("Busy Duck settings")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        subtitle = QLabel(
            "Configure providers without editing environment files."
        )
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(subtitle)

        tabs = QTabWidget()
        tabs.addTab(self._build_general_tab(), "General")
        tabs.addTab(self._build_google_tab(), "Google Calendar")
        tabs.addTab(self._build_outlook_tab(), "Microsoft Outlook")
        layout.addWidget(tabs)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _build_general_tab(self) -> QWidget:
        from PySide6.QtWidgets import QWidget

        page = QWidget()
        form = QFormLayout(page)

        self.db_path = QLineEdit()
        self.days = QSpinBox()
        self.days.setRange(1, 365)

        form.addRow("Database path", self.db_path)
        form.addRow("Sync window in days", self.days)

        return page

    def _build_google_tab(self):
        return self._build_provider_tab("google")

    def _build_outlook_tab(self):
        return self._build_provider_tab("outlook")

    def _build_provider_tab(self, provider: str):
        from PySide6.QtWidgets import QWidget

        page = QWidget()
        layout = QVBoxLayout(page)

        note = QLabel(
            "These credentials are stored in the operating system "
            "credential manager."
        )
        note.setWordWrap(True)
        note.setObjectName("statusLabel")
        layout.addWidget(note)

        group = QGroupBox("OAuth application")
        form = QFormLayout(group)

        client_id = QLineEdit()
        client_secret = QLineEdit()
        redirect_uri = QLineEdit()

        client_secret.setEchoMode(QLineEdit.Password)

        setattr(self, f"{provider}_client_id", client_id)
        setattr(self, f"{provider}_client_secret", client_secret)
        setattr(self, f"{provider}_redirect_uri", redirect_uri)

        form.addRow("Client ID", client_id)
        form.addRow("Client secret", client_secret)
        form.addRow("Redirect URI", redirect_uri)

        layout.addWidget(group)
        layout.addStretch()

        return page

    def _load_values(self) -> None:
        self.db_path.setText(get_value("database/path", "./data/busy_duck.db"))
        self.days.setValue(int(get_value("sync/window_days", "7")))

        for provider in ("google", "outlook"):
            getattr(self, f"{provider}_client_id").setText(
                get_value(f"{provider}/client_id")
            )
            getattr(self, f"{provider}_client_secret").setText(
                get_secret(f"{provider}/client_secret")
            )
            getattr(self, f"{provider}_redirect_uri").setText(
                get_value(f"{provider}/redirect_uri")
            )

    def _save(self) -> None:
        if self.days.value() < 1:
            QMessageBox.warning(
                self,
                "Invalid configuration",
                "The sync window must be at least one day.",
            )
            return

        set_value("database/path", self.db_path.text().strip())
        set_value("sync/window_days", str(self.days.value()))

        for provider in ("google", "outlook"):
            set_value(
                f"{provider}/client_id",
                getattr(self, f"{provider}_client_id").text().strip(),
            )
            set_secret(
                f"{provider}/client_secret",
                getattr(self, f"{provider}_client_secret").text(),
            )
            set_value(
                f"{provider}/redirect_uri",
                getattr(self, f"{provider}_redirect_uri").text().strip(),
            )

        self.accept()