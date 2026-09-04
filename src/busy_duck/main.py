from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from busy_duck.app import bootstrap_app
from busy_duck.ui.main_window import MainWindow


def main() -> None:
    bootstrap_app()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()