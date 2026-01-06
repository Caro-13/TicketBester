import sys
import os

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout

from constants import (WINDOW_WIDTH,WINDOW_HEIGHT)

from src.qt.staff_home_widget import StaffHomeWidget
from src.qt.staff_sell_widget import StaffSellWidget
from src.qt.staff_scan_widget import StaffScanWidget


class TicketBesterStaff(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'qt', 'GUI.ui')

        # Load UI file
        loadUi(ui_path, self)

        self.setWindowTitle("TicketBester - Personnel")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        if self.centralwidget.layout() is None:
            self.centralwidget.setLayout(QVBoxLayout())

        # View manager
        self.current_widget = None

        # Staff member info (in real app, get from login)
        self.staff_id = None
        self.staff_name = None

        self.show_staff_home_widget()

    def clear_central_widget(self):
        """Clear central widget to display new view."""
        if self.current_widget:
            self.centralwidget.layout().removeWidget(self.current_widget)
            self.current_widget.deleteLater()
            self.current_widget = None

    def show_staff_home_widget(self):
        """Show staff dashboard."""
        self.clear_central_widget()
        self.current_widget = StaffHomeWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Personnel")

    def show_staff_sell_widget(self):
        """Show ticket selling page."""
        self.clear_central_widget()
        self.current_widget = StaffSellWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Vente de billets")

    def show_staff_scan_widget(self):
        """Show ticket scanning page."""
        self.clear_central_widget()
        self.current_widget = StaffScanWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Scanner les billets")

    def set_staff_info(self, staff_id, staff_name):
        """Set the current staff member info."""
        self.staff_id = staff_id
        self.staff_name = staff_name


def main():
    app = QApplication(sys.argv)

    # Load QSS stylesheet
    style_path = os.path.join(os.path.dirname(__file__), 'qt', 'styles.qss')
    try:
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"QSS file not found: ({style_path})")

    window = TicketBesterStaff()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()