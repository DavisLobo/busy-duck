from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from busy_duck.app import bootstrap_app
from busy_duck.ui.main_window import MainWindow


def main() -> None:
    bootstrap_app()

    qt_app = QApplication(sys.argv)

    icon_path = Path(__file__).parent / "ui" / "busy_duck.svg"
    qt_app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.setWindowIcon(QIcon(str(icon_path)))
    window.show()

    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()