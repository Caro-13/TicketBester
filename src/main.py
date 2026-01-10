import sys
import os

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

# project constants
from constants import (WINDOW_WIDTH,WINDOW_HEIGHT,MENU_BTN_WIDTH,MENU_BTN_HEIGHT,ICON_WIDTH,ICON_HEIGHT)

# Import all widgets
from src.qt.home_widget import HomeWidget
from src.qt.reservation_widget import ReservationWidget
from src.qt.seatmap_widget import ConcertHall
from src.qt.payment_widget import PaymentWidget
from src.qt.admin_home_widget import AdminHomeWidget
from src.qt.admin_new_event_widget import AdminNewEventWidget
from src.qt.admin_new_staff_widget import AdminNewStaffWidget
from src.qt.admin_stats_widget import AdminStatsWidget
from src.qt.staff_home_widget import StaffHomeWidget
from src.qt.staff_sell_widget import StaffSellWidget
from src.qt.staff_scan_widget import StaffScanWidget


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

        # Staff member info (for staff mode)
        self.staff_id = None
        self.staff_name = None

        # Start with launcher
        self.show_launcher_widget()

    def clear_central_widget(self):
        """Clear central widget to display new view."""
        if self.current_widget:
            self.centralwidget.layout().removeWidget(self.current_widget)
            self.current_widget.deleteLater()
            self.current_widget = None

    """launcher widget"""
    def show_launcher_widget(self):
        self.clear_central_widget()

        # Create launcher widget
        launcher_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(40)
        layout.setContentsMargins(50, 80, 50, 80)

        # Title
        title = QLabel("TicketBester")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Sélectionnez votre mode de connexion")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(60)

        # Horizontal button container
        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Client button
        client_btn = self.create_menu_button("icon_client.png", "Client", "Réserver des billets", True)
        client_btn.clicked.connect(self.show_home_widget)
        button_layout.addWidget(client_btn)

        # Staff button
        staff_btn = self.create_menu_button("icon_staff.png", "Personnel", "Vente et scan de billets", True)
        staff_btn.clicked.connect(self.show_staff_home_widget)
        button_layout.addWidget(staff_btn)

        # Admin button
        admin_btn = self.create_menu_button("icon_admin.png", "Administrateur", "Gérer les événements", True)
        admin_btn.clicked.connect(self.show_admin_home_widget)
        button_layout.addWidget(admin_btn)

        layout.addLayout(button_layout)
        layout.addStretch()

        launcher_widget.setLayout(layout)

        self.current_widget = launcher_widget
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Launcher")

    def create_menu_button(self, emoji_or_icon, title, description, is_icon=False):
        """Create a styled menu button with emoji or icon, title, and description."""
        button = QPushButton()
        button.setFixedSize(MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setObjectName("launcherBtn")

        # Create layout for button content
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.setSpacing(15)

        # Emoji or icon label
        if is_icon:
            # Icon label
            icon_label = QLabel()
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Load icon from res folder
            icon_path = os.path.join(os.path.dirname(__file__), 'res', emoji_or_icon)
            pixmap = QPixmap(icon_path)

            # Scale the icon to fit nicely
            scaled_pixmap = pixmap.scaled(ICON_WIDTH, ICON_WIDTH, Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)

            btn_layout.addWidget(icon_label)
        else:
            # Emoji label
            emoji_label = QLabel(emoji_or_icon)
            emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            emoji_font = QFont()
            emoji_font.setPointSize(48)
            emoji_label.setFont(emoji_font)

            btn_layout.addWidget(emoji_label)

        # Title label
        title_label = QLabel(title)
        title_label.setWordWrap(True)
        title_label.setObjectName("launcherTitle")

        # Description label
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setObjectName("launcherDescription")

        btn_layout.addWidget(title_label)
        btn_layout.addWidget(desc_label)

        button.setLayout(btn_layout)

        return button

    """client widgets"""
    def show_home_widget(self):
        """Show client home page."""
        self.clear_central_widget()
        self.current_widget = HomeWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Client")

    def show_reservation_widget(self, event_id, event_name):
        self.clear_central_widget()
        self.current_widget = ReservationWidget(self, event_id=event_id, event_name=event_name)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle(f"TicketBester - Réservation #{event_id}")

    #def show_seatmap_widget(self, event_id,reservation_data): #merge confict --> study which to keep, how to modify
    def show_seatmap_widget(self, event_id, quantity, total_price):
        self.clear_central_widget()
        self.current_widget = ConcertHall(event_id=event_id, quantity=quantity, total_price=total_price, parent=self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Sélection des sièges")

    #def show_payment_widget(self,event_id,reservation_data): #merge confict --> study which to keep, how to modify
    def show_payment_widget(self, total_price):
        self.clear_central_widget()
        # On crée le widget de paiement avec le prix reçu
        self.current_widget = PaymentWidget(self, total_price=total_price)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle(f"TicketBester - Paiement ({total_price:.2f} CHF)")


    """admin widgets"""
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

    """Staff widgets"""
    def show_staff_home_widget(self):
        self.clear_central_widget()
        self.current_widget = StaffHomeWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Personnel")

    def show_staff_sell_widget(self):
        self.clear_central_widget()
        self.current_widget = StaffSellWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Vente de billets")

    def show_staff_scan_widget(self):
        self.clear_central_widget()
        self.current_widget = StaffScanWidget(self)
        self.centralwidget.layout().addWidget(self.current_widget)
        self.setWindowTitle("TicketBester - Scanner les billets")

    def set_staff_info(self, staff_id, staff_name):
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

    window = TicketBester()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()