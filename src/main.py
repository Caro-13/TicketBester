import sys
import os

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from src.qt.home_widget import HomeWidget

class TicketBester(QMainWindow):

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'qt', 'GUI.ui')

        # Chargement du fichier .ui dans la classe
        loadUi(ui_path, self)

        self.setWindowTitle("TicketBester")

        if self.centralwidget.layout() is None:
            self.centralwidget.setLayout(QVBoxLayout())

        # Home Widget
        self.home_widget = HomeWidget(self)
        self.centralwidget.layout().addWidget(self.home_widget)

    def run(self):
        # Start the event loop
        sys.exit(self.app.exec())

def main():
    app = QApplication(sys.argv)

    style_path = os.path.join(os.path.dirname(__file__), 'qt', 'styles.qss')
    try:
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"QSS file not found: ({style_path})")

    window = TicketBester()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
