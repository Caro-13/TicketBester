from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
                             QSpinBox, QLineEdit, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QBrush

from src.constants import (CONTINUE_BTN_WIDTH)

from src.db.requests import get_tarifs_for_event, get_need_reservation_for_event, create_client, create_reservation, \
    get_available_seats_for_event, add_ticket_to_reservation, cancel_reservation


class ReservationWidget(QWidget):
    def __init__(self, parent=None, event_id=None, event_name="Titre Événement"):
        super().__init__(parent)

        self.main_window = parent
        self.event_id = event_id
        self.event_name = event_name
        self.tarifs = []
        self.prix_total = 0.00
        self.need_reservation = get_need_reservation_for_event(self.event_id)

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
                {"id": 1, "name": "Normal", "price": 12.00},
                {"id": 2, "name": "Student", "price": 10.00},
            ]

    def _setup_header(self):
        header_layout = QHBoxLayout()

        # Bouton Retour (pour revenir à HomeWidget)
        self.btn_back = QPushButton("← Retour aux évènements")
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.setObjectName("backBtn")

        self.btn_back.clicked.connect(self._handle_back)

        header_layout.addWidget(self.btn_back)

        header_layout.addStretch()

        # Titre
        event_title = QLabel(f"Réservation: {self.event_name}")
        event_title.setObjectName("pageTitle")
        header_layout.addWidget(event_title)

        header_layout.addStretch()
        self.layout.addLayout(header_layout)

    def _setup_tarifs_section(self):
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)

        # --- Tarifs (Grid Layout) ---
        tarifs_label = QLabel("Sélectionnez vos tarifs")
        tarifs_label.setObjectName("littleSection")
        content_layout.addWidget(tarifs_label)

        tarifs_grid = QGridLayout()
        tarifs_grid.setHorizontalSpacing(40)
        tarifs_grid.setVerticalSpacing(15)

        self.quantity_spinboxes = {}  # Pour stocker les champs de quantité

        for i, tarif in enumerate(self.tarifs):
            # Ligne 1: Nom et Prix
            price = tarif['price']
            name_label = QLabel(f"{tarif['name']} ({price:.2f} CHF)")
            name_label.setObjectName("infosInput")

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
                details_label.setObjectName("starNote")
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
        button_text = "Continuer →" if self.need_reservation else "Aller au paiement →"
        self.btn_continue = QPushButton(button_text)
        self.btn_continue.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_continue.setFixedWidth(CONTINUE_BTN_WIDTH)
        self.btn_continue.setEnabled(False)  # Disabled until tickets selected
        self.btn_continue.setObjectName("continueBtn")

        # Pass the event_id when clicking continue
        self.btn_continue.clicked.connect(self._handle_continue)

        footer_layout.addWidget(self.total_label)
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_continue)

        self.layout.addWidget(footer_frame)

    def _get_client_infos_section(self):
        client_layout = QVBoxLayout()

        # Title
        client_info_label = QLabel("Informations du client")
        client_info_label.setObjectName("littleSection")
        client_layout.addWidget(client_info_label)

        # Grid for inputs
        client_grid = QGridLayout()
        client_grid.setHorizontalSpacing(20)
        client_grid.setVerticalSpacing(10)

        # Email
        email_label = QLabel("Email * :")
        email_label.setObjectName("infosInput")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("exemple@email.com")
        self.email_input.setObjectName("inputLine")
        self.email_input.textChanged.connect(self._update_total)

        # Firstname
        firstname_label = QLabel("Prénom * :")
        email_label.setObjectName("infosInput")
        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("Entrez votre prénom")
        self.firstname_input.setObjectName("inputLine")
        self.firstname_input.textChanged.connect(self._update_total)

        # Lastname
        lastname_label = QLabel("Nom * :")
        email_label.setObjectName("infosInput")
        self.lastname_input = QLineEdit()
        self.lastname_input.setPlaceholderText("Entrez votre nom")
        self.lastname_input.setObjectName("inputLine")
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
        note.setObjectName("starNote")
        self.layout.addWidget(note)

        return client_layout

    def _get_reservation_data(self):
        # Collect selected tarifs and quantities
        selected_tarifs = {}
        for tarif in self.tarifs:
            quantity = self.quantity_spinboxes[tarif['name']].value()
            if quantity > 0:
                selected_tarifs[tarif['name']] = {
                    'quantity': quantity,
                    'price': tarif['price'],
                    'tarif_id': tarif['id']
                }

        # Return all data as a dictionary
        return {
            'event_id': self.event_id,
            'event_name': self.event_name,
            'email': self.email_input.text().strip(),
            'firstname': self.firstname_input.text().strip(),
            'lastname': self.lastname_input.text().strip(),
            'tarifs': selected_tarifs,
            'total': self.prix_total,
            'need_reservation': self.need_reservation,
            'vendor_id' : 1
        }

    def _handle_continue(self):
        if self.need_reservation:
            self._go_to_seatmap()
        else:
            self._go_to_payment()

    def _go_to_seatmap(self):
        try:
            # 1. Collect reservation data
            reservation_data = self._get_reservation_data()

            # 2. Create or get client
            client_id = create_client(
                email=reservation_data['email'],
                firstname=reservation_data['firstname'],
                lastname=reservation_data['lastname']
            )

            if not client_id:
                QMessageBox.warning(self, "Erreur", "Impossible de créer le client.")
                return

            # 3. Create reservation (status will be 'pending')
            reservation_id = create_reservation(
                event_id=self.event_id,
                client_id=client_id
            )

            if not reservation_id:
                QMessageBox.warning(self, "Erreur", "Impossible de créer la réservation.")
                return

            # 4. Store all data including reservation_id and client_id
            reservation_data['reservation_id'] = reservation_id
            reservation_data['client_id'] = client_id
            self.main_window.reservation_data = reservation_data

            # 5. Navigate to seatmap where user will select seats
            self.main_window.show_seatmap_widget(reservation_data)

        except Exception as e:
            import traceback
            print(f"ERROR in _go_to_seatmap: {e}")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")

    def _go_to_payment(self):
        try:
            # 1. Collect reservation data
            reservation_data = self._get_reservation_data()

            # 2. Create or get client
            client_id = create_client(
                email=reservation_data['email'],
                firstname=reservation_data['firstname'],
                lastname=reservation_data['lastname']
            )

            if not client_id:
                QMessageBox.warning(self, "Erreur", "Impossible de créer le client.")
                return

            # 3. Create reservation
            reservation_id = create_reservation(
                event_id=self.event_id,
                client_id=client_id
            )

            if not reservation_id:
                QMessageBox.warning(self, "Erreur", "Impossible de créer la réservation.")
                return

            # 4. For events without seat selection, assign random available seats
            available_seats = get_available_seats_for_event(self.event_id)

            if not available_seats:
                QMessageBox.warning(self, "Erreur", "Aucun siège disponible.")
                return

            # 5. Create tickets for each tarif quantity
            seat_index = 0
            for tarif_name, tarif_info in reservation_data['tarifs'].items():
                quantity = tarif_info['quantity']

                for _ in range(quantity):
                    if seat_index >= len(available_seats):
                        QMessageBox.warning(self, "Erreur", "Pas assez de sièges disponibles.")
                        return

                    seat = available_seats[seat_index]
                    success = add_ticket_to_reservation(
                        reservation_id=reservation_id,
                        event_id=self.event_id,
                        seat_id=seat['id'],
                        tarif_name=tarif_name
                    )

                    if not success:
                        QMessageBox.warning(self, "Erreur", f"Impossible d'ajouter le billet {seat['name']}.")
                        return

                    seat_index += 1

            # 6. Store reservation data and navigate to payment
            reservation_data['reservation_id'] = reservation_id
            reservation_data['client_id'] = client_id
            self.main_window.reservation_data = reservation_data

            self.main_window.show_payment_widget(reservation_data)

        except Exception as e:
            print(f"Error in _go_to_payment: {e}")
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")

    def _update_total(self):
        total = 0.0

        for tarif in self.tarifs:
            quantity = self.quantity_spinboxes[tarif['name']].value()
            total += quantity * tarif['price']

        self.prix_total = total

        # Update display
        self.total_label.setText(f"Total: {self.prix_total:.2f} CHF")

        # Update button state
        self.update_can_continue()

    def update_can_continue(self):
        # Enable/disable continue button
        has_tickets = any(spinbox.value() > 0 for spinbox in self.quantity_spinboxes.values())
        has_identity = (
        self.email_input.text().strip() != "" and
        self.firstname_input.text().strip() != "" and
        self.lastname_input.text().strip() != ""
        )
        self.btn_continue.setEnabled(has_tickets and has_identity)

    def _handle_back(self):
        """If go back to home, delete pending reservation"""
        if (hasattr(self, 'reservation_data') and
                self.reservation_data and
                'reservation_id' in self.reservation_data):
            reservation_id = self.reservation_data['reservation_id']
            print(f"Cancelling pending reservation #{reservation_id}")
            cancel_reservation(reservation_id)
            self.reservation_data = None
            self.main_window.show_home_widget()
        self.main_window.show_home_widget()