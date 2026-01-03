from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
                             QSpinBox, QLineEdit, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QBrush

from src.db.requests import get_tarifs_for_event, get_all_events_details

class ReservationWidget(QWidget):
    def __init__(self, parent=None, event_id=None, event_name="Titre Événement"):
        super().__init__(parent)

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
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                color: #89b4fa;
                border: none;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                color: #b4befe;
            }
        """)

        self.btn_back.clicked.connect(self.window().show_home_widget)

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
            quantity_box.setStyleSheet("""
                QSpinBox {
                    background-color: #313244;
                    border: 1px solid #45475a;
                    border-radius: 4px;
                    padding: 5px;
                    color: #cdd6f4;
                }
            """)

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
        self.btn_continue.setFixedWidth(150)
        self.btn_continue.setEnabled(False)  # Disabled until tickets selected
        self.btn_continue.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton:disabled {
                background-color: #45475a;
                color: #6c7086;
            }
        """)

        self.btn_continue.clicked.connect(self.window().show_seatmap_widget)

        footer_layout.addWidget(self.total_label)
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_continue)

        self.layout.addWidget(footer_frame)

    def _update_total(self):
        total = 0.0

        for tarif in self.tarifs:
            quantity = self.quantity_spinboxes[tarif['name']].value()
            total += quantity * tarif['price']

        self.prix_total = total

        # Update display
        self.total_label.setText(f"Total: {self.prix_total:.2f} CHF")

        # Enable/disable continue button
        has_tickets = any(spinbox.value() > 0 for spinbox in self.quantity_spinboxes.values())
        self.btn_continue.setEnabled(has_tickets)
