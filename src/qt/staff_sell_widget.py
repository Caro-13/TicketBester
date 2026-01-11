from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QMessageBox,
                            QSpinBox, QFrame, QGridLayout)
from PyQt6.QtCore import Qt

from src.db.requests import (get_all_events, get_tarifs_for_event,
                             get_available_seats_for_event,
                             create_reservation, add_ticket_to_reservation,
                             get_need_reservation_for_event)


class StaffSellWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.selected_event_id = None
        self.selected_event_name = None
        self.tarifs = []
        self.prix_total = 0.0
        self.need_reservation = False
        self.quantity_spinboxes = {}

        # --- Layout Principal ---
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(25)

        # --- Titre et Navigation ---
        self._setup_header()

        # --- Event Selection ---
        self._setup_event_section()

        # --- Contenu Principal (Tarifs) ---
        self._setup_tarifs_section()

        # --- Section Récapitulatif et Paiement ---
        self._setup_footer()

        # Load events
        self.load_events()

    def _setup_header(self):
        header_layout = QHBoxLayout()

        back_btn = QPushButton("← Retour")
        back_btn.setObjectName("backBtn")
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)

        header_layout.addStretch()

        # Title
        title = QLabel("Vendre des billets")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)

        header_layout.addStretch()

        #Staff info
        staff_info = QLabel(f"Personnel: {self.main_window.staff_name or 'Non sélectionné'}")
        staff_info.setStyleSheet("font-weight: bold; color: #4CAF50;")
        header_layout.addWidget(staff_info)

        self.layout.addLayout(header_layout)

    def _setup_event_section(self):
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)

        # Section label
        event_section = QLabel("Sélectionner l'événement")
        event_section.setObjectName("littleSection")
        content_layout.addWidget(event_section)

        # Event selection grid
        event_grid = QGridLayout()
        event_grid.setHorizontalSpacing(20)
        event_grid.setVerticalSpacing(10)

        event_label = QLabel("Événement * :")
        event_label.setObjectName("infosInput")
        self.event_combo = QComboBox()
        self.event_combo.setMinimumWidth(400)
        self.event_combo.currentIndexChanged.connect(self.on_event_selected)

        event_grid.addWidget(event_label,0,0,Qt.AlignmentFlag.AlignRight)
        event_grid.addWidget(self.event_combo,0,1)

        content_layout.addLayout(event_grid)
        content_layout.addSpacing(30)

        self.layout.addWidget(content_frame)

    def _setup_tarifs_section(self):
        self.tarifs_frame = QFrame()
        self.tarifs_content_layout = QVBoxLayout(self.tarifs_frame)
        self.tarifs_content_layout.setSpacing(20)

        # --- Tarifs (Grid Layout) ---
        tarifs_label = QLabel("Sélectionnez les tarifs")
        tarifs_label.setObjectName("littleSection")
        self.tarifs_content_layout.addWidget(tarifs_label)

        self.tarifs_grid = QGridLayout()
        self.tarifs_grid.setHorizontalSpacing(40)
        self.tarifs_grid.setVerticalSpacing(15)

        self.tarifs_content_layout.addLayout(self.tarifs_grid)
        self.tarifs_content_layout.addStretch()

        # Initially hidden until event is selected
        self.tarifs_frame.setVisible(False)
        self.layout.addWidget(self.tarifs_frame)

    def _setup_footer(self):
        footer_frame = QFrame()
        footer_frame.setStyleSheet("border-top: 2px solid #313244;")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(0, 15, 0, 0)

        #Total label
        self.total_label = QLabel(f"Total: {self.prix_total:.2f} CHF")
        self.total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #fab387;")

        self.btn_continue = QPushButton("Continuer →")
        self.btn_continue.setObjectName("continueBtn")
        self.btn_continue.setEnabled(False)
        self.btn_continue.clicked.connect(self._handle_continue)

        footer_layout.addWidget(self.total_label)
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_continue)

        self.layout.addWidget(footer_frame)

    def load_events(self):
        """Load available events."""
        events = get_all_events()
        self.event_combo.clear()
        self.event_combo.addItem("-- Sélectionner un événement --", None)

        for event in events:
            event_id, name, type_name, date, time = event
            display_text = f"{name} - {date} {time}"
            self.event_combo.addItem(display_text, event_id)

    def on_event_selected(self, index):
        """Handle event selection."""
        event_id  = self.event_combo.currentData()

        if event_id :
            self.selected_event_id = event_id
            self.selected_event_name = self.event_combo.currentText()
            self.need_reservation = get_need_reservation_for_event(event_id)
            self.load_tarifs()
            self.tarifs_frame.setVisible(True)
        else:
            self.selected_event_id = None
            self.selected_event_name = None
            self.need_reservation = False
            self.clear_tarifs()
            self.tarifs_frame.setVisible(False)

    def load_tarifs(self):
        try:
            if self.selected_event_id:
                self.tarifs = get_tarifs_for_event(self.selected_event_id)
                self.clear_tarifs()
                self._populate_tarifs()
        except Exception as e:
            print(f"Error loading tarifs: {e}")
            QMessageBox.warning(self, "Erreur", "Impossible de charger les tarifs.")

    def _populate_tarifs(self):
        """Populate tarif selection grid."""
        self.quantity_spinboxes = {}

        for i, tarif in enumerate(self.tarifs):
            # Tarif name and price
            price = tarif['price']
            name_label = QLabel(f"{tarif['name']} ({price:.2f} CHF)")
            name_label.setObjectName("infosInput")

            # Quantity spinbox
            quantity_box = QSpinBox()
            quantity_box.setRange(0, 20)
            quantity_box.setValue(0)
            quantity_box.setFixedWidth(60)
            quantity_box.setObjectName("spinbox")
            quantity_box.valueChanged.connect(self.update_total)

            self.quantity_spinboxes[tarif['name']] = quantity_box

            # Add to grid
            self.tarifs_grid.addWidget(name_label, i, 0, Qt.AlignmentFlag.AlignLeft)
            self.tarifs_grid.addWidget(quantity_box, i, 1, Qt.AlignmentFlag.AlignRight)

            # Add note for special tarifs
            if '*' in tarif['name'] or tarif['name'].lower() in ['student', 'staff']:
                details_label = QLabel("* Contrôle à l'entrée")
                details_label.setObjectName("starNote")
                self.tarifs_grid.addWidget(details_label, i, 2, Qt.AlignmentFlag.AlignLeft)

    def clear_tarifs(self):
        """Clear tarif selection."""
        # Remove all widgets from layout
        while self.tarifs_grid.count():
            child = self.tarifs_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.quantity_spinboxes = {}
        self.update_total()

    def update_total(self):
        """Update total price and enable/disable continue button."""
        total = 0.0
        has_tickets = False

        for tarif in self.tarifs:
            quantity = self.quantity_spinboxes.get(tarif['name'], None)
            if quantity:
                total += quantity.value() * tarif['price']

        self.prix_total = total
        self.total_label.setText(f"Total: {self.prix_total:.2f} CHF")
        self._update_can_continue()

    def _update_can_continue(self):
        """Enable/disable continue button."""
        has_event = self.selected_event_id is not None
        has_tickets = any(spinbox.value() > 0 for spinbox in self.quantity_spinboxes.values())
        self.btn_continue.setEnabled(has_event and has_tickets)

    def _get_reservation_data(self):
        """Collect selected tarifs and quantities."""
        selected_tarifs = {}
        for tarif in self.tarifs:
            quantity = self.quantity_spinboxes[tarif['name']].value()
            if quantity > 0:
                selected_tarifs[tarif['name']] = {
                    'quantity': quantity,
                    'price': tarif['price'],
                    'tarif_id': tarif['id']
                }

        return {
            'event_id': self.selected_event_id,
            'event_name': self.selected_event_name,
            'tarifs': selected_tarifs,
            'total': self.prix_total,
            'need_reservation': self.need_reservation,
            'vendor_id': self.main_window.staff_id
        }

    def _handle_continue(self):
        """Handle continue button click."""
        if self.need_reservation:
            self._go_to_seatmap()
        else:
            self._go_to_payment()

    def _go_to_seatmap(self):
        """Navigate to seatmap for seat selection."""
        try:
            if not self.selected_event_id:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un événement.")
                return

            # Get reservation data
            reservation_data = self._get_reservation_data()

            if not reservation_data['tarifs']:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins un billet.")
                return

            # Create reservation with staff_id
            reservation_id = create_reservation(
                event_id=self.selected_event_id,
                client_id=None,
                vendor_id=self.main_window.staff_id
            )

            if not reservation_id:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la création de la réservation.")
                return

            # Add reservation_id and client_id to data
            reservation_data['reservation_id'] = reservation_id
            reservation_data['client_id'] = None

            # Navigate to seatmap
            self.main_window.show_staff_seatmap_widget(reservation_data)

        except Exception as e:
            import traceback
            print(f"ERROR in _go_to_seatmap: {e}")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")

        def go_back(self):
            self.main_window.show_staff_home_widget()

    def _go_to_payment(self):
        """Navigate directly to payment (for events without seat selection)."""
        try:
            # Get reservation data
            reservation_data = self._get_reservation_data()

            if not reservation_data['tarifs']:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins un billet.")
                return

            # Create reservation
            reservation_id = create_reservation(
                event_id=self.selected_event_id,
                client_id=None,
                staff_id=self.main_window.staff_id
            )

            if not reservation_id:
                QMessageBox.warning(self, "Erreur", "Impossible de créer la réservation.")
                return

            # Assign random available seats
            available_seats = get_available_seats_for_event(self.selected_event_id)

            if not available_seats:
                QMessageBox.warning(self, "Erreur", "Aucun siège disponible.")
                return

            # Create tickets for each tarif quantity
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
                        event_id=self.selected_event_id,
                        seat_id=seat['id'],
                        tarif_name=tarif_name
                    )

                    if not success:
                        QMessageBox.warning(self, "Erreur", f"Impossible d'ajouter le billet {seat['name']}.")
                        return

                    seat_index += 1

            # Add reservation_id and client_id to data
            reservation_data['reservation_id'] = reservation_id
            reservation_data['client_id'] = None

            # Navigate to payment
            self.main_window.show_staff_payment_widget(reservation_data)

        except Exception as e:
            import traceback
            print(f"ERROR in _go_to_payment: {e}")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")

    def go_back(self):
        """Return to staff home."""
        self.main_window.show_staff_home_widget()