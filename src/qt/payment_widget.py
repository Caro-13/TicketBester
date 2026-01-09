from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QLineEdit, QGridLayout)
from PyQt6.QtCore import Qt


class PaymentWidget(QWidget):
    def __init__(self, parent=None, total_price=0.0):
        super().__init__(parent)
        self.main_window = parent
        self.total_price = total_price

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
        title = QLabel(f"Paiement - Total: {self.total_price:.2f} CHF")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #fab387;")
        self.layout.addWidget(title)

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

        if self.main_window:
            self.btn_twint.clicked.connect(self.main_window.show_home_widget)

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
        self.btn_pay.setEnabled(False)

        if self.main_window:
            self.btn_pay.clicked.connect(self.main_window.show_home_widget)

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