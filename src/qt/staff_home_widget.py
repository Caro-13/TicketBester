import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont,QPixmap

from src.constants import (MENU_BTN_WIDTH,MENU_BTN_HEIGHT,ICON_WIDTH,ICON_HEIGHT)

from src.db.requests import get_all_staff


class StaffHomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()
        self.load_staff_list()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)

        # Back button to launcher
        back_layout = QHBoxLayout()
        self.btn_launcher = QPushButton("← Retour au menu")
        self.btn_launcher.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_launcher.clicked.connect(self.main_window.show_launcher_widget)
        self.btn_launcher.setObjectName("backBtn")
        back_layout.addWidget(self.btn_launcher)
        back_layout.addStretch()
        layout.addLayout(back_layout)

        # Title
        title = QLabel("Personnel TicketBester")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Vente et contrôle des billets")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        # Staff selection
        selection_layout = QVBoxLayout()
        selection_layout.setSpacing(10)

        select_label = QLabel("Sélectionnez votre identité:")
        select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        select_font = QFont()
        select_font.setPointSize(12)
        select_label.setFont(select_font)
        selection_layout.addWidget(select_label)

        self.staff_combo = QComboBox()
        self.staff_combo.setMinimumWidth(300)
        self.staff_combo.setMaximumWidth(500)
        self.staff_combo.currentIndexChanged.connect(self.on_staff_selected)

        combo_container = QHBoxLayout()
        combo_container.addStretch()
        combo_container.addWidget(self.staff_combo)
        combo_container.addStretch()
        selection_layout.addLayout(combo_container)

        layout.addLayout(selection_layout)

        layout.addSpacing(30)

        # Horizontal button container
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(30)

        # Sell tickets button
        sell_btn = self.create_menu_button("icon_tickets.png", "Vendre des billets",True)
        sell_btn.clicked.connect(self.go_to_sell)
        self.button_layout.addWidget(sell_btn)

        # Scan tickets button
        scan_btn = self.create_menu_button("icon_scan.png", "Scanner des billets",True)
        scan_btn.clicked.connect(self.go_to_scan)
        self.button_layout.addWidget(scan_btn)

        layout.addLayout(self.button_layout)
        layout.addStretch()

        # Initially disable buttons until staff is selected
        self.set_buttons_enabled(False)

        self.setLayout(layout)

    def create_menu_button(self, emoji_or_icon, title, is_icon=False):
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
            scaled_pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
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

    def load_staff_list(self):
        """Load staff members into combo box."""
        staff_list = get_all_staff()

        self.staff_combo.clear()
        self.staff_combo.addItem("-- Sélectionner --", None)

        for staff_id, name in staff_list:
            self.staff_combo.addItem(name, staff_id)

    def on_staff_selected(self, index):
        """Handle staff selection."""
        staff_data = self.staff_combo.currentData()

        if staff_data is not None:
            staff_id = staff_data
            staff_name = self.staff_combo.currentText()
            self.main_window.set_staff_info(staff_id, staff_name)
            self.set_buttons_enabled(True)
        else:
            self.main_window.set_staff_info(None, None)
            self.set_buttons_enabled(False)

    def set_buttons_enabled(self, enabled):
        """Enable or disable action buttons."""
        for i in range(self.button_layout.count()):
            widget = self.button_layout.itemAt(i).widget()
            if widget and isinstance(widget, QPushButton):
                widget.setEnabled(enabled)

    def go_to_sell(self):
        """Navigate to sell tickets page."""
        if self.main_window.staff_id is None:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner votre identité.")
            return
        self.main_window.show_staff_sell_widget()

    def go_to_scan(self):
        """Navigate to scan tickets page."""
        if self.main_window.staff_id is None:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner votre identité.")
            return
        self.main_window.show_staff_scan_widget()