import segno
from io import BytesIO
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtGui import QPixmap, QImage
import os

from src.constants import BACK_BTN_WIDTH


class ConfirmationWidget(QWidget):
    def __init__(self, reservation_data, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.reservation_data = reservation_data

        # Get data
        self.reservation_id = self.reservation_data.get('reservation_id', "N/A")
        self.event_name = self.reservation_data.get('event_name', "Concert")
        self.venue = "Salle de Concert Principale"
        self.total_price = self.reservation_data.get('total', 0.0)

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 40, 50, 40)
        self.layout.setSpacing(20)

        self._setup_header()
        self._setup_ticket_view()

        self.layout.addStretch()

    def _setup_header(self):
        home_layout = QHBoxLayout()
        self.btn_home = QPushButton("⌂ Home")
        self.btn_home.setFixedWidth(BACK_BTN_WIDTH)
        self.btn_home.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_home.setObjectName("backBtn")

        if self.main_window and hasattr(self.main_window, 'show_home_widget'):
            self.btn_home.clicked.connect(self.main_window.show_home_widget)

        home_layout.addWidget(self.btn_home)
        home_layout.addStretch()
        self.layout.addLayout(home_layout)

        self.title = QLabel("Paiement réussi !")
        self.title.setStyleSheet("font-size: 32px; font-weight: bold; color: #a6e3a1; margin-top: 10px;")
        self.layout.addWidget(self.title)

    def _setup_ticket_view(self):
        self.ticket_frame = QFrame()
        self.ticket_frame.setFixedWidth(500)
        self.ticket_frame.setStyleSheet("""
            QFrame {
                background: #181825; 
                border-radius: 15px; 
                border: 2px solid #313244;
            }
        """)
        ticket_layout = QVBoxLayout(self.ticket_frame)
        ticket_layout.setContentsMargins(30, 30, 30, 30)
        ticket_layout.setSpacing(15)

        # Concert name
        name_lbl = QLabel(self.event_name.upper())
        name_lbl.setStyleSheet("font-size: 26px; font-weight: bold; color: #fab387; border: none;")
        name_lbl.setWordWrap(True)
        ticket_layout.addWidget(name_lbl)

        # QR code
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setStyleSheet("background: white; padding: 10px; border-radius: 10px; border: none;")

        # Create QR code
        qr_pixmap = self._generate_qr_pixmap(f"Numero de reservation : {self.reservation_id}")
        if qr_pixmap:
            self.qr_label.setPixmap(qr_pixmap)

        ticket_layout.addWidget(self.qr_label)

        # Séparator
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #313244; border: none;")
        ticket_layout.addWidget(line)

        # Details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(8)

        def add_detail(label, value):
            container = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #9399b2; font-size: 14px; border: none;")
            val = QLabel(value)
            val.setStyleSheet("color: #cdd6f4; font-size: 16px; font-weight: 500; border: none;")
            container.addWidget(lbl)
            container.addStretch()
            container.addWidget(val)
            details_layout.addLayout(container)

        add_detail("Lieu :", self.venue)
        add_detail("N° Réservation :", f"#{self.reservation_id}")
        add_detail("Montant payé :", f"{self.total_price:.2f} CHF")

        ticket_layout.addLayout(details_layout)

        # Acknowledgement
        footer_line = QFrame()
        footer_line.setFixedHeight(1)
        footer_line.setStyleSheet("background-color: #313244; border: none;")
        ticket_layout.addWidget(footer_line)

        thanks_lbl = QLabel("Merci pour votre achat !")
        thanks_lbl.setStyleSheet("color: #a6e3a1; font-style: italic; border: none;")
        thanks_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ticket_layout.addWidget(thanks_lbl)

        self.layout.addWidget(self.ticket_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.download_btn = QPushButton("Télécharger le ticket")
        self.download_btn.setFixedWidth(250)
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.setObjectName("downloadBtn")
        self.download_btn.clicked.connect(self._download_qr)

        self.layout.addWidget(self.download_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    # Create QR code
    def _generate_qr_pixmap(self, data):
        try:
            qr = segno.make(data, error='L')

            out = BytesIO()
            qr.save(out, kind='png', scale=5)

            q_img = QImage.fromData(out.getvalue())
            return QPixmap.fromImage(q_img)
        except Exception as e:
            print(f"Erreur lors de la génération du QR : {e}")
            return None

    # Download QR code in download folder
    def _download_qr(self):
        # Get qr code
        pixmap = self.qr_label.pixmap()
        if pixmap.isNull():
            return

        # Get downloads path
        downloads_path = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DownloadLocation
        )

        # Filename
        file_name = f"Ticket_Reservation_{self.reservation_id}.png"
        full_path = os.path.join(downloads_path, file_name)

        # Download image in downloads folder
        if pixmap.save(full_path, "PNG"):
            print(f"QR Code sauvegardé dans : {full_path}")
            self.download_btn.setText("Enregistré dans Téléchargements")
            self.download_btn.setStyleSheet(self.download_btn.styleSheet() + "background-color: #a6e3a1;")
        else:
            print("Erreur lors de la sauvegarde.")