import sys
import os

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from constants import (WINDOW_WIDTH,WINDOW_HEIGHT)

from src.qt.home_widget import HomeWidget
from src.qt.payment_widget import PaymentWidget
from src.qt.reservation_widget import ReservationWidget
from src.qt.seatmap_widget import ConcertHall

class TicketBester(QMainWindow):

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'qt', 'GUI.ui')

        # Chargement du fichier .ui dans la classe
        loadUi(ui_path, self)

        self.setWindowTitle("TicketBester")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

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

    def show_seatmap_widget(self,reservation_data):
        self.clear_central_widget()
        self.current_widget = ConcertHall(reservation_data, parent=self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle(f"TicketBester - Sélection des sièges")

    def show_payment_widget(self,reservation_data): # ToDo Faire le widget
        self.clear_central_widget()
        # On crée le widget de paiement avec le prix reçu
        self.current_widget = PaymentWidget(reservation_data, parent=self)
        self.centralwidget.layout().addWidget(self.current_widget)
        total_price = reservation_data['total']
        self.setWindowTitle("TicketBester - Paiement ({total_price:.2f} CHF)")




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