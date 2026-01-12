from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt

from src.db.requests import create_payment
from src.constants import BACK_BTN_WIDTH


class PaymentWidget(QWidget):
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
        self._setup_card_details()

        self.layout.addLayout(self.content_layout)
        self.layout.addStretch()

    def _setup_header(self):
        header_layout = QHBoxLayout()

        # btn home
        self.btn_home = QPushButton("⌂ Home")
        self.btn_home.setFixedWidth(BACK_BTN_WIDTH)
        self.btn_home.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_home.setObjectName("backBtn")

        # Link to home
        if self.main_window and hasattr(self.main_window, 'show_home_widget'):
            self.btn_home.clicked.connect(self.main_window.show_home_widget)

        header_layout.addWidget(self.btn_home)
        header_layout.addSpacing(20)  # Petit espace entre le bouton et le titre

        # Title
        title = QLabel(f"Paiement - Total: {self.total_price:.2f} CHF")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #fab387;")
        header_layout.addWidget(title)

        header_layout.addStretch()  # Pousse tout vers la gauche

        self.layout.addLayout(header_layout)

    def _setup_payment_options(self):
        self.options_frame = QFrame()
        self.options_frame.setFixedWidth(300)
        layout = QVBoxLayout(self.options_frame)
        layout.setSpacing(20)

        self.btn_card = QPushButton("Carte Bancaire")
        self.btn_card.setFixedHeight(60)
        self.btn_card.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_card.setObjectName("paymentOptionBtn")
        self.btn_card.clicked.connect(self._show_card_fields)

        self.btn_twint = QPushButton("Twint")
        self.btn_twint.setFixedHeight(60)
        self.btn_twint.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_twint.setObjectName("paymentOptionBtn")
        self.btn_twint.clicked.connect(self._process_twint_payment)

        layout.addWidget(self.btn_card)
        layout.addWidget(self.btn_twint)
        layout.addStretch()
        self.content_layout.addWidget(self.options_frame)

    def _setup_card_details(self):
        self.card_frame = QFrame()
        self.card_frame.setStyleSheet("background: #181825; border-radius: 15px; border: 1px solid #313244;")
        self.card_frame.setVisible(False)

        layout = QVBoxLayout(self.card_frame)
        layout.setContentsMargins(30, 30, 30, 30)

        grid = QGridLayout()
        grid.setSpacing(15)

        # Label style
        label_style = "font-size: 16px; color: #cdd6f4; font-weight: 500; border: none;"

        # Text fields style
        input_style = "font-weight: bold;"

        # Card number
        lbl_num = QLabel("Numéro de la carte :")
        lbl_num.setStyleSheet(label_style)
        grid.addWidget(lbl_num, 0, 0, 1, 2)

        self.card_num = QLineEdit()
        self.card_num.setPlaceholderText("0000 0000 0000 0000")
        self.card_num.setObjectName("inputLine")
        self.card_num.setStyleSheet(input_style)
        self.card_num.textChanged.connect(self._validate_inputs)
        grid.addWidget(self.card_num, 1, 0, 1, 2)

        # Exp date and CVV
        lbl_exp = QLabel("Date exp :")
        lbl_exp.setStyleSheet(label_style)
        lbl_cvv = QLabel("CVV :")
        lbl_cvv.setStyleSheet(label_style)

        grid.addWidget(lbl_exp, 2, 0)
        grid.addWidget(lbl_cvv, 2, 1)

        self.card_expiry = QLineEdit()
        self.card_expiry.setPlaceholderText("MM/AA")
        self.card_expiry.setObjectName("inputLine")
        self.card_expiry.setStyleSheet(input_style)
        self.card_expiry.textChanged.connect(self._validate_inputs)

        self.card_cvc = QLineEdit()
        self.card_cvc.setPlaceholderText("123")
        self.card_cvc.setObjectName("inputLine")
        self.card_cvc.setStyleSheet(input_style)
        self.card_cvc.textChanged.connect(self._validate_inputs)

        grid.addWidget(self.card_expiry, 3, 0)
        grid.addWidget(self.card_cvc, 3, 1)

        layout.addLayout(grid)

        self.btn_pay = QPushButton(f"Payer {self.total_price:.2f} CHF")
        self.btn_pay.setObjectName("confirmBtn")
        self.btn_pay.setFixedHeight(50)
        if self.total_price > 0:
            self.btn_pay.setEnabled(False)
        else:
            self.btn_pay.setEnabled(True)
            self.btn_pay.setStyleSheet("background-color: #89b4fa; color: #1e1e2e; font-weight: bold;")
        self.btn_pay.clicked.connect(self._process_card_payment)

        layout.addSpacing(20)
        layout.addWidget(self.btn_pay)
        self.content_layout.addWidget(self.card_frame)

    def _show_card_fields(self):
        self.card_frame.setVisible(True)

        self.btn_card.setStyleSheet("background-color: #89b4fa; color: #1e1e2e; font-weight: bold;")
        self.btn_twint.setStyleSheet("")

    # Check if all fields are filled
    def _validate_inputs(self):
        num = self.card_num.text().strip()
        exp = self.card_expiry.text().strip()
        cvc = self.card_cvc.text().strip()

        # Validation condition
        is_valid = len(num) >= 12 and len(exp) == 5 and len(cvc) >= 3

        self.btn_pay.setEnabled(is_valid)

        if is_valid:
            self.btn_pay.setStyleSheet("background-color: #89b4fa; color: #1e1e2e; font-weight: bold;")
        else:
            self.btn_pay.setStyleSheet("")

    def _process_card_payment(self):
        self._finalize_payment('card')

    def _process_twint_payment(self):
        self._finalize_payment('twint')

    def _finalize_payment(self, method):
        try:
            # Disable all buttons immediately to prevent double-click
            self.btn_pay.setEnabled(False)
            self.btn_twint.setEnabled(False)
            self.btn_card.setEnabled(False)

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
            QMessageBox.information(
                self,
                "Paiement réussi",
                f"Votre paiement de {self.total_price:.2f} CHF a été accepté!\n"
                f"Réservation #{reservation_id}"
            )

            if self.main_window:
                self.main_window.show_confirmation_widget(self.reservation_data)

        except Exception as e:
            import traceback
            print(f"ERROR in _finalize_payment: {e}")
            print(traceback.format_exc())

            #if error enable back buttons to try again paying
            self._enable_buttons()

            QMessageBox.critical(
                self,
                "Erreur",
                f"Une erreur est survenue lors du paiement: {str(e)}"
            )

    def _enable_buttons(self):
        """Re-enable payment buttons (only call on error)"""
        self.btn_twint.setEnabled(True)
        self.btn_card.setEnabled(True)
        # Only re-enable pay button if card fields are valid
        if self.card_frame.isVisible():
            self._validate_inputs()