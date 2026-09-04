from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QLineEdit,
    QVBoxLayout,
)

from busy_duck.app import (
    get_connected_accounts,
    sync_all,
    update_account,
)


class AccountSetupDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.editing_account_id: str | None = None
        self._accounts_loaded = False

        self.setWindowTitle("Account setup · Busy Duck")
        self.setMinimumSize(560, 520)

        self._build_ui()
        self._load_accounts()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        title = QLabel("Connect your calendar accounts")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        description = QLabel(
            "Add accounts from supported providers. "
            "Busy Duck stores normalized calendar data locally."
        )
        description.setWordWrap(True)
        description.setObjectName("pageSubtitle")
        layout.addWidget(description)

        connected_title = QLabel("CONNECTED ACCOUNTS")
        connected_title.setObjectName("sectionTitle")
        layout.addWidget(connected_title)

        self.accounts_list = QListWidget()
        self.accounts_list.setMinimumHeight(130)
        layout.addWidget(self.accounts_list)

        form_title = QLabel("ADD ACCOUNT")
        form_title.setObjectName("sectionTitle")
        layout.addWidget(form_title)

        form = QFormLayout()
        form.setSpacing(10)

        self.provider = QComboBox()
        self.provider.addItem("Google Calendar", "google")
        self.provider.addItem("Microsoft Outlook", "outlook")

        self.email = QLineEdit()
        self.email.setPlaceholderText("name@company.com")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Your name")

        self.calendar_name = QLineEdit()
        self.calendar_name.setText("Primary")
        self.calendar_name.setPlaceholderText("Work calendar")

        form.addRow("Provider", self.provider)
        form.addRow("Email", self.email)
        form.addRow("Name", self.username)
        form.addRow("Calendar", self.calendar_name)

        layout.addLayout(form)

        note = QLabel(
            "Development mode: provider connection currently uses "
            "the built-in demo connector. OAuth integration can be added "
            "without changing this screen."
        )
        note.setWordWrap(True)
        note.setObjectName("statusLabel")
        layout.addWidget(note)

        buttons = QDialogButtonBox()
        self.connect_button = buttons.addButton(
            "Connect account",
            QDialogButtonBox.AcceptRole,
        )
        buttons.addButton(QDialogButtonBox.Cancel)

        self.connect_button.clicked.connect(self._connect_account)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def _load_accounts(self) -> None:
        self.accounts_list.clear()

        accounts = get_connected_accounts()

        if not accounts:
            item = QListWidgetItem("No accounts connected yet.")
            item.setFlags(Qt.NoItemFlags)
            self.accounts_list.addItem(item)
            self._accounts_loaded = True
            return

        for account in accounts:
            item = QListWidgetItem(
                f"●  {account['provider']}  ·  {account['email']}\n"
                f"    {account['username']}  ·  Double-click to edit"
            )
            item.setData(Qt.UserRole, account)
            self.accounts_list.addItem(item)

            if not self._accounts_loaded:
                self.accounts_list.itemDoubleClicked.connect(self._edit_account)
                self._accounts_loaded = True
        self._accounts_loaded = True

    def _connect_account(self) -> None:
        email = self.email.text().strip()
        username = self.username.text().strip() or "User"
        calendar_name = self.calendar_name.text().strip() or "Primary"
        provider_name = self.provider.currentData()

        if "@" not in email:
            QMessageBox.warning(
                self,
                "Invalid email",
                "Enter a valid account email address.",
            )
            self.email.setFocus()
            return

        self.connect_button.setEnabled(False)
        self.connect_button.setText("Connecting…")

        try:
            if self.editing_account_id is not None:
                update_account(
                    account_id=self.editing_account_id,
                    username=username,
                    email=email,
                )
                message = f"{email} was updated successfully."
            else:
                sync_all(
                    provider_configs=[
                        {
                            "provider_name": provider_name,
                            "email": email,
                            "username": username,
                            "external_calendar_id": (
                                f"{provider_name}-{email}-primary"
                            ),
                            "calendar_name": calendar_name,
                        }
                    ]
                )
                message = f"{email} was added successfully."

            self._load_accounts()
            self.editing_account_id = None
            self.email.clear()
            self.username.clear()
            self.connect_button.setText("Connect account")

            QMessageBox.information(self, "Account saved", message)
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Connection failed",
                str(exc),
            )
        finally:
            self.connect_button.setEnabled(True)
            self.connect_button.setText("Connect account")

    def _edit_account(self, item: QListWidgetItem) -> None:
        account = item.data(Qt.UserRole)

        self.provider.setCurrentIndex(
            self.provider.findData(account["slug"])
        )
        self.email.setText(account["email"])
        self.username.setText(account["username"])

        self.editing_account_id: str | None = account["id"]
        self.connect_button.setText("Save changes")