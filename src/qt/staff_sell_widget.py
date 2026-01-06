from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox,
                             QFormLayout, QScrollArea, QSpinBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.db.requests import (get_all_events, get_tarifs_for_event,
                             get_available_seats_for_event, create_client,
                             create_reservation, add_ticket_to_reservation,
                             create_payment)


class StaffSellWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.selected_event_id = None
        self.cart = []  # List of {seat_id, seat_name, tarif_name, price, supplement}
        self.init_ui()
        self.load_events()

    def init_ui(self):
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        # Content widget
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)

        # Header
        header_layout = QHBoxLayout()

        back_btn = QPushButton("← Retour")
        back_btn.setFixedWidth(120)
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)

        header_layout.addStretch()

        staff_info = QLabel(f"Personnel: {self.main_window.staff_name or 'Non sélectionné'}")
        staff_info.setStyleSheet("font-weight: bold; color: #4CAF50;")
        header_layout.addWidget(staff_info)

        layout.addLayout(header_layout)

        # Title
        title = QLabel("Vendre des billets")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Event selection
        event_layout = QHBoxLayout()
        event_label = QLabel("Événement:")
        event_label.setMinimumWidth(100)
        self.event_combo = QComboBox()
        self.event_combo.setMinimumWidth(400)
        self.event_combo.currentIndexChanged.connect(self.on_event_selected)
        event_layout.addWidget(event_label)
        event_layout.addWidget(self.event_combo)
        event_layout.addStretch()
        layout.addLayout(event_layout)

        # Client information section
        client_section = QLabel("Informations client")
        client_font = QFont()
        client_font.setPointSize(16)
        client_font.setBold(True)
        client_section.setFont(client_font)
        layout.addWidget(client_section)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("client@email.com")
        form_layout.addRow("Email:", self.email_input)

        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("Prénom")
        form_layout.addRow("Prénom:", self.firstname_input)

        self.lastname_input = QLineEdit()
        self.lastname_input.setPlaceholderText("Nom")
        form_layout.addRow("Nom:", self.lastname_input)

        layout.addLayout(form_layout)

        # Ticket selection section
        ticket_section = QLabel("Sélection des billets")
        ticket_section.setFont(client_font)
        layout.addWidget(ticket_section)

        selection_layout = QHBoxLayout()

        # Tarif selection
        tarif_layout = QVBoxLayout()
        tarif_label = QLabel("Tarif:")
        self.tarif_combo = QComboBox()
        self.tarif_combo.setMinimumWidth(200)
        tarif_layout.addWidget(tarif_label)
        tarif_layout.addWidget(self.tarif_combo)
        selection_layout.addLayout(tarif_layout)

        # Seat selection
        seat_layout = QVBoxLayout()
        seat_label = QLabel("Place:")
        self.seat_combo = QComboBox()
        self.seat_combo.setMinimumWidth(200)
        seat_layout.addWidget(seat_label)
        seat_layout.addWidget(self.seat_combo)
        selection_layout.addLayout(seat_layout)

        # Add to cart button
        add_btn = QPushButton("Ajouter au panier")
        add_btn.setFixedSize(150, 50)
        add_btn.clicked.connect(self.add_to_cart)
        selection_layout.addWidget(add_btn)
        selection_layout.addStretch()

        layout.addLayout(selection_layout)

        # Cart table
        cart_label = QLabel("Panier")
        cart_label.setFont(client_font)
        layout.addWidget(cart_label)

        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["Place", "Tarif", "Prix", "Supplément", "Total"])
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cart_table.setMaximumHeight(200)
        layout.addWidget(self.cart_table)

        # Cart actions
        cart_actions = QHBoxLayout()

        clear_cart_btn = QPushButton("Vider le panier")
        clear_cart_btn.clicked.connect(self.clear_cart)
        cart_actions.addWidget(clear_cart_btn)

        cart_actions.addStretch()

        self.total_label = QLabel("Total: 0.00 CHF")
        total_font = QFont()
        total_font.setPointSize(16)
        total_font.setBold(True)
        self.total_label.setFont(total_font)
        cart_actions.addWidget(self.total_label)

        layout.addLayout(cart_actions)

        # Payment section
        payment_section = QLabel("Paiement")
        payment_section.setFont(client_font)
        layout.addWidget(payment_section)

        payment_layout = QHBoxLayout()
        payment_label = QLabel("Méthode:")
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Carte bancaire", "Espèces", "Twint"])
        payment_layout.addWidget(payment_label)
        payment_layout.addWidget(self.payment_combo)
        payment_layout.addStretch()
        layout.addLayout(payment_layout)

        # Confirm sale button
        confirm_layout = QHBoxLayout()
        confirm_layout.addStretch()

        confirm_btn = QPushButton("Confirmer la vente")
        confirm_btn.setFixedSize(200, 50)
        confirm_btn.setObjectName("validateBtn")
        confirm_btn.clicked.connect(self.confirm_sale)
        confirm_layout.addWidget(confirm_btn)

        layout.addLayout(confirm_layout)

        content.setLayout(layout)
        scroll.setWidget(content)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

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
        self.selected_event_id = self.event_combo.currentData()

        if self.selected_event_id:
            self.load_tarifs()
            self.load_seats()
        else:
            self.tarif_combo.clear()
            self.seat_combo.clear()

    def load_tarifs(self):
        """Load tarifs for selected event."""
        if not self.selected_event_id:
            return

        tarifs = get_tarifs_for_event(self.selected_event_id)
        self.tarif_combo.clear()
        self.tarif_combo.addItem("-- Sélectionner --", None)

        for tarif in tarifs:
            display = f"{tarif['name']} - {tarif['price']:.2f} CHF"
            self.tarif_combo.addItem(display, tarif)

    def load_seats(self):
        """Load available seats for selected event."""
        if not self.selected_event_id:
            return

        seats = get_available_seats_for_event(self.selected_event_id)
        self.seat_combo.clear()
        self.seat_combo.addItem("-- Sélectionner --", None)

        for seat in seats:
            display = f"{seat['name']} ({seat['sector']})"
            if seat['supplement'] > 0:
                display += f" +{seat['supplement']:.2f} CHF"
            self.seat_combo.addItem(display, seat)

    def add_to_cart(self):
        """Add selected ticket to cart."""
        tarif_data = self.tarif_combo.currentData()
        seat_data = self.seat_combo.currentData()

        if not tarif_data or not seat_data:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un tarif et une place.")
            return

        # Check if seat already in cart
        for item in self.cart:
            if item['seat_id'] == seat_data['id']:
                QMessageBox.warning(self, "Erreur", "Cette place est déjà dans le panier.")
                return

        cart_item = {
            'seat_id': seat_data['id'],
            'seat_name': seat_data['name'],
            'sector': seat_data['sector'],
            'tarif_name': tarif_data['name'],
            'price': tarif_data['price'],
            'supplement': seat_data['supplement']
        }

        self.cart.append(cart_item)
        self.update_cart_display()

    def update_cart_display(self):
        """Update cart table and total."""
        self.cart_table.setRowCount(len(self.cart))
        total = 0

        for row, item in enumerate(self.cart):
            self.cart_table.setItem(row, 0, QTableWidgetItem(f"{item['seat_name']} ({item['sector']})"))
            self.cart_table.setItem(row, 1, QTableWidgetItem(item['tarif_name']))
            self.cart_table.setItem(row, 2, QTableWidgetItem(f"{item['price']:.2f} CHF"))
            self.cart_table.setItem(row, 3, QTableWidgetItem(f"{item['supplement']:.2f} CHF"))

            item_total = item['price'] + item['supplement']
            total += item_total
            self.cart_table.setItem(row, 4, QTableWidgetItem(f"{item_total:.2f} CHF"))

        self.total_label.setText(f"Total: {total:.2f} CHF")

    def clear_cart(self):
        """Clear all items from cart."""
        self.cart = []
        self.update_cart_display()

    def confirm_sale(self):
        """Process the sale."""
        # Validation
        if not self.email_input.text() or not self.firstname_input.text() or not self.lastname_input.text():
            QMessageBox.warning(self, "Erreur", "Veuillez remplir toutes les informations client.")
            return

        if not self.cart:
            QMessageBox.warning(self, "Erreur", "Le panier est vide.")
            return

        if not self.selected_event_id:
            QMessageBox.warning(self, "Erreur", "Aucun événement sélectionné.")
            return

        # Create client
        client_id = create_client(
            self.email_input.text(),
            self.firstname_input.text(),
            self.lastname_input.text()
        )

        if not client_id:
            QMessageBox.critical(self, "Erreur", "Erreur lors de la création du client.")
            return

        # Create reservation
        reservation_id = create_reservation(self.selected_event_id, client_id, self.main_window.staff_id)

        if not reservation_id:
            QMessageBox.critical(self, "Erreur", "Erreur lors de la création de la réservation.")
            return

        # Add tickets
        for item in self.cart:
            success = add_ticket_to_reservation(
                reservation_id,
                self.selected_event_id,
                item['seat_id'],
                item['tarif_name']
            )
            if not success:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout du billet {item['seat_name']}.")
                return

        # Create payment
        payment_method_map = {
            "Carte bancaire": "card",
            "Espèces": "cash",
            "Twint": "twint"
        }
        payment_method = payment_method_map[self.payment_combo.currentText()]

        total = sum(item['price'] + item['supplement'] for item in self.cart)
        payment_id = create_payment(reservation_id, total, payment_method)

        if not payment_id:
            QMessageBox.critical(self, "Erreur", "Erreur lors de la création du paiement.")
            return

        QMessageBox.information(
            self,
            "Succès",
            f"Vente confirmée!\n\nRéservation #{reservation_id}\n{len(self.cart)} billet(s) vendu(s)\nTotal: {total:.2f} CHF"
        )

        # Reset form
        self.clear_cart()
        self.email_input.clear()
        self.firstname_input.clear()
        self.lastname_input.clear()
        self.load_seats()  # Refresh available seats

    def go_back(self):
        """Return to staff home."""
        self.main_window.show_staff_home_widget()