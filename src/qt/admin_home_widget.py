import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from src.constants import (MENU_BTN_WIDTH,MENU_BTN_HEIGHT)

class AdminHomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)

        # Title
        title = QLabel("Administration TicketBester")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Gestion des événements et du personnel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(50)

        # Horizontal button container
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)

        # Create event button
        event_btn = self.create_menu_button("icon_calendar.png", "Créer un événement",True)
        event_btn.clicked.connect(self.go_to_new_event)
        button_layout.addWidget(event_btn)

        # Add staff button
        staff_btn = self.create_menu_button("icon_staff.png", "Ajouter du personnel", True)
        staff_btn.clicked.connect(self.go_to_new_staff)
        button_layout.addWidget(staff_btn)

        # View stats button
        stats_btn = self.create_menu_button("icon_stats", "Voir les statistiques",True)
        stats_btn.clicked.connect(self.go_to_stats)
        button_layout.addWidget(stats_btn)

        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def create_menu_button(self, emoji_or_icon, title, is_icon = False):
        """Create a styled menu button with emoji or icon and title."""
        button = QPushButton()
        button.setFixedSize(MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setObjectName("homeBtn")

        # Create layout for button content
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.setSpacing(20)

        # Emoji or icon label
        if is_icon:
            # Icon label
            icon_label = QLabel()
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Load icon from res folder
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'res', emoji_or_icon)
            pixmap = QPixmap(icon_path)

            # Scale the icon to fit nicely (e.g., 80x80 pixels)
            scaled_pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
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
        title_label.setObjectName("homeTitle")

        btn_layout.addWidget(title_label)

        button.setLayout(btn_layout)

        return button

    def go_to_new_event(self):
        self.main_window.show_admin_new_event_widget()

    def go_to_new_staff(self):
        self.main_window.show_admin_new_staff_widget()

    def go_to_stats(self):
        self.main_window.show_admin_stats_widget()