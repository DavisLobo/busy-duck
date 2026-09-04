from __future__ import annotations

import keyring
from PySide6.QtCore import QSettings

SERVICE_NAME = "busy-duck"

_settings = QSettings("BusyDuck", "BusyDuck")


def get_value(key: str, default: str = "") -> str:
    return str(_settings.value(key, default))


def set_value(key: str, value: str) -> None:
    _settings.setValue(key, value)
    _settings.sync()


def get_secret(key: str) -> str:
    return keyring.get_password(SERVICE_NAME, key) or ""


def set_secret(key: str, value: str) -> None:
    if value:
        keyring.set_password(SERVICE_NAME, key, value)
    else:
        try:
            keyring.delete_password(SERVICE_NAME, key)
        except keyring.errors.PasswordDeleteError:
            pass