from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QLineEdit, QGridLayout,
                             QMessageBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt

from src.db.requests import create_payment


class StaffPaymentWidget(QWidget):
    def __init__(self, reservation_data, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.reservation_data = reservation_data
        self.total_price = self.reservation_data.get('total', 0.0)

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(30)

        self._setup_header()
        self.content_layout = QHBoxLayout()

        self._setup_payment_options()
        self._setup_cash_details()

        self.layout.addLayout(self.content_layout)
        self.layout.addStretch()

    def _setup_header(self):
        header_layout = QHBoxLayout()

        # Back button
        back_btn = QPushButton("← Retour")
        back_btn.setObjectName("backBtn")
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)

        header_layout.addStretch()

        # Title
        title = QLabel(f"Paiement - Total: {self.total_price:.2f} CHF")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Staff info
        staff_info = QLabel(f"Personnel: {self.main_window.staff_name or 'Non sélectionné'}")
        staff_info.setStyleSheet("font-weight: bold; color: #4CAF50;")
        header_layout.addWidget(staff_info)

        self.layout.addLayout(header_layout)

    def _setup_payment_options(self):
        self.options_frame = QFrame()
        self.options_frame.setFixedWidth(300)
        layout = QVBoxLayout(self.options_frame)
        layout.setSpacing(20)

        # Section title
        section_title = QLabel("Mode de paiement")
        section_title.setObjectName("littleSection")
        layout.addWidget(section_title)

        self.btn_cash = QPushButton("Espèces")
        self.btn_cash.setFixedHeight(60)
        self.btn_cash.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cash.setObjectName("paymentOptionBtn")
        self.btn_cash.clicked.connect(self._show_cash_fields)

        self.btn_twint = QPushButton("Twint")
        self.btn_twint.setFixedHeight(60)
        self.btn_twint.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_twint.setObjectName("paymentOptionBtn")
        self.btn_twint.clicked.connect(self._process_twint_payment)

        layout.addWidget(self.btn_cash)
        layout.addWidget(self.btn_twint)
        layout.addStretch()
        self.content_layout.addWidget(self.options_frame)

    def _setup_cash_details(self):
        self.cash_frame = QFrame()
        self.cash_frame.setStyleSheet("background: #181825; border-radius: 15px; border: 1px solid #313244;")
        self.cash_frame.setVisible(False)

        layout = QVBoxLayout(self.cash_frame)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Title
        cash_title = QLabel("Paiement en espèces")
        cash_title.setObjectName("littleSection")
        layout.addWidget(cash_title)

        grid = QGridLayout()
        grid.setSpacing(15)

        # Label style
        label_style = "font-size: 16px; color: #cdd6f4; font-weight: 500; border: none;"

        # Total to pay (read-only)
        lbl_total = QLabel("Montant à payer :")
        lbl_total.setStyleSheet(label_style)
        grid.addWidget(lbl_total, 0, 0)

        self.total_display = QLabel(f"{self.total_price:.2f} CHF")
        self.total_display.setStyleSheet("font-size: 20px; color: #fab387; font-weight: bold; border: none;")
        grid.addWidget(self.total_display, 0, 1, Qt.AlignmentFlag.AlignRight)

        # Amount received
        lbl_received = QLabel("Montant reçu :")
        lbl_received.setStyleSheet(label_style)
        grid.addWidget(lbl_received, 1, 0)

        self.amount_received = QDoubleSpinBox()
        self.amount_received.setRange(0, 10000)
        self.amount_received.setDecimals(2)
        self.amount_received.setSuffix(" CHF")
        self.amount_received.setValue(0.00)
        self.amount_received.setObjectName("spinbox")
        self.amount_received.setFixedHeight(40)
        self.amount_received.valueChanged.connect(self._calculate_change)
        grid.addWidget(self.amount_received, 1, 1)

        # Change to give
        lbl_change = QLabel("Monnaie à rendre :")
        lbl_change.setStyleSheet(label_style)
        grid.addWidget(lbl_change, 2, 0)

        self.change_display = QLabel("0.00 CHF")
        self.change_display.setStyleSheet("font-size: 18px; color: #a6e3a1; font-weight: bold; border: none;")
        grid.addWidget(self.change_display, 2, 1, Qt.AlignmentFlag.AlignRight)

        layout.addLayout(grid)
        layout.addSpacing(10)

        self.btn_pay_cash = QPushButton(f"Confirmer paiement")
        self.btn_pay_cash.setObjectName("confirmBtn")
        self.btn_pay_cash.setFixedHeight(50)
        self.btn_pay_cash.setEnabled(False)
        self.btn_pay_cash.clicked.connect(self._process_cash_payment)

        layout.addSpacing(10)
        layout.addWidget(self.btn_pay_cash)
        layout.addStretch()

        self.content_layout.addWidget(self.cash_frame)

    def _show_cash_fields(self):
        self.cash_frame.setVisible(True)

        self.btn_cash.setStyleSheet("background-color: #89b4fa; color: #1e1e2e; font-weight: bold;")
        self.btn_twint.setStyleSheet("")

    def _calculate_change(self):
        """Calculate change and validate payment."""
        received = self.amount_received.value()
        change = received - self.total_price

        if change >= 0:
            self.change_display.setText(f"{change:.2f} CHF")
            self.change_display.setStyleSheet("font-size: 18px; color: #a6e3a1; font-weight: bold; border: none;")
            self.btn_pay_cash.setEnabled(True)
            self.btn_pay_cash.setStyleSheet("background-color: #89b4fa; color: #1e1e2e; font-weight: bold;")
        else:
            self.change_display.setText(f"{change:.2f} CHF (insuffisant)")
            self.change_display.setStyleSheet("font-size: 18px; color: #f38ba8; font-weight: bold; border: none;")
            self.btn_pay_cash.setEnabled(False)
            self.btn_pay_cash.setStyleSheet("")

    def _process_cash_payment(self):
        # Show change to give if any
        change = self.amount_received.value() - self.total_price
        if change > 0:
            QMessageBox.information(
                self,
                "Monnaie à rendre",
                f"Monnaie à rendre au client :\n\n{change:.2f} CHF",
                QMessageBox.StandardButton.Ok
            )

        self._finalize_payment('cash')

    def _process_twint_payment(self):
        # Show confirmation for Twint
        reply = QMessageBox.question(
            self,
            "Confirmation Twint",
            f"Le client a-t-il effectué le paiement Twint de {self.total_price:.2f} CHF ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self._finalize_payment('twint')

    def _finalize_payment(self, method):
        try:
            # Disable all buttons immediately to prevent double-click
            self.btn_pay_cash.setEnabled(False)
            self.btn_twint.setEnabled(False)
            self.btn_cash.setEnabled(False)

            reservation_id = self.reservation_data.get('reservation_id')

            if not reservation_id:
                QMessageBox.warning(self, "Erreur", "Aucune réservation trouvée.")
                return

            payment_id = create_payment(
                reservation_id=reservation_id,
                total=self.total_price,
                method=method
            )

            if not payment_id:
                QMessageBox.warning(self, "Erreur", "Erreur lors du paiement.")
                return

            # Show success message
            method_text = "en espèces" if method == 'cash' else "par Twint"
            QMessageBox.information(
                self,
                "Paiement réussi",
                f"Paiement {method_text} de {self.total_price:.2f} CHF accepté!\n"
                f"Réservation #{reservation_id}\n\n"
                f"Les billets ont été vendus avec succès."
            )

            if self.main_window:
                self.main_window.show_staff_home_widget()

        except Exception as e:
            import traceback
            print(f"ERROR in _finalize_payment: {e}")
            print(traceback.format_exc())

            # If error, enable back buttons to try again paying
            self._enable_buttons()

            QMessageBox.critical(
                self,
                "Erreur",
                f"Une erreur est survenue lors du paiement: {str(e)}"
            )

    def _enable_buttons(self):
        """Re-enable payment buttons (only call on error)"""
        self.btn_twint.setEnabled(True)
        self.btn_cash.setEnabled(True)
        # Only re-enable pay button if amount is sufficient
        if self.cash_frame.isVisible():
            self._calculate_change()

    def go_back(self):
        """Return to staff home."""
        self.main_window.show_staff_home_widget()