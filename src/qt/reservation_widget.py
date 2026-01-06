from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
                             QSpinBox, QLineEdit, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QBrush

from src.constants import (CONTINUE_BTN_WIDTH)

from src.db.requests import get_tarifs_for_event, get_all_events_details

class ReservationWidget(QWidget):
    def __init__(self, parent=None, event_id=None, event_name="Titre Événement"):
        super().__init__(parent)

        self.main_window = parent
        self.event_id = event_id
        self.event_name = event_name
        self.tarifs = []
        self.prix_total = 0.00

        # --- Layout Principal ---
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(25)

        # --- Titre et Navigation ---
        self._setup_header()

        # Load tarifs from database
        self._load_tarifs()

        # --- Contenu Principal (Tarifs) ---
        self._setup_tarifs_section()

        # --- Section Récapitulatif et Paiement ---
        self._setup_footer()

    def _load_tarifs(self):
        try:
            if self.event_id:
                self.tarifs = get_tarifs_for_event(self.event_id)

        except Exception as e:
            print(f"Error loading tarifs: {e}")
            # Use dummy data on error
            self.tarifs = [
                {"id": 1, "name": "Normal", "price": 12.00, "discount_percent": None, "discount_code": None},
                {"id": 2, "name": "Student", "price": 10.00, "discount_percent": None, "discount_code": None},
            ]

    def _setup_header(self):
        header_layout = QHBoxLayout()

        # Bouton Retour (pour revenir à HomeWidget)
        self.btn_back = QPushButton("← Retour aux évènements")
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.setObjectName("backBtn")

        self.btn_back.clicked.connect(self.main_window.show_home_widget)

        header_layout.addWidget(self.btn_back)

        header_layout.addStretch()

        # Titre
        event_title = QLabel(f"Réservation: {self.event_name}")
        event_title.setStyleSheet("font-size: 28px; font-weight: bold; color: #fab387;")
        header_layout.addWidget(event_title)

        header_layout.addStretch()
        self.layout.addLayout(header_layout)

    def _setup_tarifs_section(self):
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)

        # --- Tarifs (Grid Layout) ---
        tarifs_label = QLabel("Sélectionnez vos tarifs")
        tarifs_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #cdd6f4;")
        content_layout.addWidget(tarifs_label)

        tarifs_grid = QGridLayout()
        tarifs_grid.setHorizontalSpacing(40)
        tarifs_grid.setVerticalSpacing(15)

        self.quantity_spinboxes = {}  # Pour stocker les champs de quantité

        for i, tarif in enumerate(self.tarifs):
            # Ligne 1: Nom et Prix
            price = tarif['price']
            name_label = QLabel(f"{tarif['name']} ({price:.2f} CHF)")
            name_label.setStyleSheet("font-size: 15px; font-weight: 500;")

            # Ligne 2: Champ de Quantité (SpinBox)
            quantity_box = QSpinBox()
            quantity_box.setRange(0, 10)  # Max 10 billets par tarif
            quantity_box.setValue(0)
            quantity_box.setFixedWidth(60)
            quantity_box.setObjectName("spinbox")

            # Connect to update total
            quantity_box.valueChanged.connect(self._update_total)
            self.quantity_spinboxes[tarif['name']] = quantity_box

            # Placement dans la grille (Nom, Quantité, Détails)
            tarifs_grid.addWidget(name_label, i, 0, Qt.AlignmentFlag.AlignLeft)
            tarifs_grid.addWidget(quantity_box, i, 1, Qt.AlignmentFlag.AlignRight)

            # Add note for special tarifs (those with *)
            if '*' in tarif['name'] or tarif['name'].lower() in ['student', 'staff']:
                details_label = QLabel("* Contrôle à l'entrée")
                details_label.setStyleSheet("font-size: 10px; color: #6c7086; font-style: italic;")
                tarifs_grid.addWidget(details_label, i, 2, Qt.AlignmentFlag.AlignLeft)

        content_layout.addLayout(tarifs_grid)
        content_layout.addSpacing(30)
        content_layout.addLayout(self._get_client_infos_section())


        content_layout.addStretch()

        self.layout.addWidget(content_frame)

    def _setup_footer(self):
        footer_frame = QFrame()
        footer_frame.setStyleSheet("border-top: 2px solid #313244;")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(0, 15, 0, 0)

        # Label Total
        self.total_label = QLabel(f"Total: {self.prix_total:.2f} CHF")
        self.total_label.setObjectName("TotalLabel")
        self.total_label.setStyleSheet("QLabel#TotalLabel {font-size: 20px; font-weight: bold; color: #fab387;}")

        # Bouton Continuer/Payer (Côté droit)
        self.btn_continue = QPushButton("Continuer →")
        self.btn_continue.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_continue.setFixedWidth(CONTINUE_BTN_WIDTH)
        self.btn_continue.setEnabled(False)  # Disabled until tickets selected
        self.btn_continue.setObjectName("continueBtn")

        # Pass the event_id when clicking continue
        self.btn_continue.clicked.connect(self._go_to_seatmap)

        footer_layout.addWidget(self.total_label)
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_continue)

        self.layout.addWidget(footer_frame)

    def _get_client_infos_section(self):
        client_layout = QVBoxLayout()

        # Title
        client_info_label = QLabel("Informations du client")
        client_info_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #cdd6f4;")
        client_layout.addWidget(client_info_label)

        # Grid for inputs
        client_grid = QGridLayout()
        client_grid.setHorizontalSpacing(20)
        client_grid.setVerticalSpacing(10)

        # Email
        email_label = QLabel("Email * :")
        email_label.setStyleSheet("font-size: 14px; color: #cdd6f4;")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("exemple@email.com")
        self.email_input.setObjectName("inputLine")
        self.email_input.textChanged.connect(self._update_total)

        # Firstname
        firstname_label = QLabel("Prénom * :")
        firstname_label.setStyleSheet("font-size: 14px; color: #cdd6f4;")
        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("Entrez votre prénom")
        self.firstname_input.setObjectName("inputLine")  # Fixed: was self.email_input
        self.firstname_input.textChanged.connect(self._update_total)

        # Lastname
        lastname_label = QLabel("Nom * :")
        lastname_label.setStyleSheet("font-size: 14px; color: #cdd6f4;")
        self.lastname_input = QLineEdit()
        self.lastname_input.setPlaceholderText("Entrez votre nom")
        self.lastname_input.setObjectName("inputLine")  # Fixed: was self.email_input
        self.lastname_input.textChanged.connect(self._update_total)

        # Add to grid
        client_grid.addWidget(email_label, 0, 0, Qt.AlignmentFlag.AlignRight)
        client_grid.addWidget(self.email_input, 0, 1)
        client_grid.addWidget(firstname_label, 1, 0, Qt.AlignmentFlag.AlignRight)
        client_grid.addWidget(self.firstname_input, 1, 1)
        client_grid.addWidget(lastname_label, 2, 0, Qt.AlignmentFlag.AlignRight)
        client_grid.addWidget(self.lastname_input, 2, 1)

        client_layout.addLayout(client_grid)

        # Required fields note
        note = QLabel("* Champs obligatoires")
        note.setStyleSheet("color: #666; font-style: italic;")
        self.layout.addWidget(note)

        return client_layout

    def _go_to_seatmap(self):
        self.main_window.show_seatmap_widget(self.event_id)

    def _update_total(self):
        total = 0.0

        for tarif in self.tarifs:
            quantity = self.quantity_spinboxes[tarif['name']].value()
            total += quantity * tarif['price']

        self.prix_total = total

        # Update display
        self.total_label.setText(f"Total: {self.prix_total:.2f} CHF")

        # Update button state
        self.update_can_go_to_seatmap()

    def update_can_go_to_seatmap(self):
        # Enable/disable continue button
        has_tickets = any(spinbox.value() > 0 for spinbox in self.quantity_spinboxes.values())
        has_identity = (
        self.email_input.text().strip() != "" and
        self.firstname_input.text().strip() != "" and
        self.lastname_input.text().strip() != ""
        )
        self.btn_continue.setEnabled(has_tickets and has_identity)