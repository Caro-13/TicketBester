import sys
import os

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout

from constants import (WINDOW_WIDTH,WINDOW_HEIGHT)

from src.qt.admin_home_widget import AdminHomeWidget
from src.qt.admin_new_event_widget import AdminNewEventWidget
from src.qt.admin_new_staff_widget import AdminNewStaffWidget
from src.qt.admin_stats_widget import AdminStatsWidget


class TicketBesterAdmin(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'qt', 'GUI.ui')

        # Load UI file
        loadUi(ui_path, self)

        self.setWindowTitle("TicketBester - Administration")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        if self.centralwidget.layout() is None:
            self.centralwidget.setLayout(QVBoxLayout())

        # View manager
        self.current_widget = None
        self.show_admin_home_widget()

    def clear_central_widget(self):
        if self.current_widget:
            self.centralwidget.layout().removeWidget(self.current_widget)
            self.current_widget.deleteLater()
            self.current_widget = None

    def show_admin_home_widget(self):
        self.clear_central_widget()
        self.current_widget = AdminHomeWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Administration")

    def show_admin_new_event_widget(self):
        self.clear_central_widget()
        self.current_widget = AdminNewEventWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Nouvel événement")

    def show_admin_new_staff_widget(self):
        self.clear_central_widget()
        self.current_widget = AdminNewStaffWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Nouveau personnel")

    def show_admin_stats_widget(self):
        self.clear_central_widget()
        self.current_widget = AdminStatsWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Statistiques")


def main():
    app = QApplication(sys.argv)

    # Load QSS stylesheet
    style_path = os.path.join(os.path.dirname(__file__), 'qt', 'styles.qss')
    try:
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"QSS file not found: ({style_path})")

    window = TicketBesterAdmin()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()