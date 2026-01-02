import sys
import os

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from src.qt.home_widget import HomeWidget
from src.qt.reservation_widget import ReservationWidget
from src.qt.seatmap_widget import ConcertHall

class TicketBester(QMainWindow):

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'qt', 'GUI.ui')

        # Chargement du fichier .ui dans la classe
        loadUi(ui_path, self)

        self.setWindowTitle("TicketBester")

        if self.centralwidget.layout() is None:
            self.centralwidget.setLayout(QVBoxLayout())

        # Gestionnaire de Vues
        self.current_widget = None
        self.show_home_widget()


    def clear_central_widget(self):
        """Nettoie le widget central pour afficher une nouvelle vue."""
        if self.current_widget:
            self.centralwidget.layout().removeWidget(self.current_widget)
            self.current_widget.deleteLater()
            self.current_widget = None

    def show_reservation_widget(self, event_id, event_name):
        """Affiche la page de réservation pour un événement donné."""
        self.clear_central_widget()
        self.current_widget = ReservationWidget(self, event_id=event_id, event_name=event_name)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle(f"TicketBester - Réservation #{event_id}")

    def show_home_widget(self):
        """Revient à la page d'accueil."""
        self.clear_central_widget()
        self.current_widget = HomeWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester")

    def show_seatmap_widget(self):
        self.clear_central_widget()
        self.current_widget = ConcertHall(self)
        self.current_widget.btn_home.clicked.connect(self.show_home_widget)
        self.current_widget.btn_confirm.clicked.connect(self.show_home_widget) # ToDo Rediriger vers payment
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Sélection des sièges")

    def show_payment_widget(self): # ToDo Faire le widget
        self.clear_central_widget()
        # self.current_widget = ConcertHall(self)
        # self.current_widget.btn_confirm.clicked.connect(self.show_home_widget)
        # self.centralwidget.layout().addWidget(self.current_widget)
        # self.setWindowTitle("TicketBester")


def main():
    app = QApplication(sys.argv)

    # Chargement du QSS
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