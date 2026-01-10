from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox, QDateTimeEdit,
                             QMessageBox, QFormLayout, QScrollArea)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QAction, QIcon

from src.constants import (BACK_BTN_WIDTH,CANCEL_BTN_WIDTH,CONTINUE_BTN_WIDTH)

from src.db.requests import create_event, get_all_type_of_event_names, get_all_rooms_names, get_all_config_names, \
    get_type_id, get_room_id, get_config_id


class AdminNewEventWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()

    def init_ui(self):
        # Main layout - similar to your other widgets
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        back_btn = QPushButton("← Retour")
        back_btn.setFixedWidth(BACK_BTN_WIDTH)
        back_btn.setObjectName("backBtn")
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)

        header_layout.addStretch()
        self.layout.addLayout(header_layout)

        # Title
        title = QLabel("Créer un nouvel événement")
        title.setObjectName("pageTitle")
        self.layout.addWidget(title)

        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Event type
        self.type_combo = QComboBox()
        self.type_combo.addItem("Sélectionner un type")
        self.type_combo.model().item(0).setEnabled(False)
        self.type_combo.addItems(get_all_type_of_event_names())
        self.type_combo.setMinimumWidth(400)

        form_layout.addRow("Type d'événement *:", self.type_combo)

        # Event name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom de l'événement")
        self.name_input.setMinimumWidth(400)
        self.name_input.setObjectName("inputLine")
        form_layout.addRow("Nom de l'événement *:", self.name_input)


        min_start_at = QDateTime.currentDateTime().addSecs(2 * 3600) #in 2H

        # Start date/time
        self.start_datetime = QDateTimeEdit()
        self.start_datetime.setDateTime(min_start_at)
        self.start_datetime.setMinimumDateTime(min_start_at)
        self.start_datetime.setCalendarPopup(True)
        self.start_datetime.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.start_datetime.setButtonSymbols(QDateTimeEdit.ButtonSymbols.UpDownArrows)
        self.start_datetime.setMinimumWidth(400)
        form_layout.addRow("Date et heure de début *:", self.start_datetime)


        # End date/time
        self.end_datetime = QDateTimeEdit()
        self.end_datetime.setDateTime(min_start_at.addSecs(7200)) # +2H
        self.end_datetime.setCalendarPopup(True)
        self.end_datetime.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.end_datetime.setButtonSymbols(QDateTimeEdit.ButtonSymbols.UpDownArrows)
        self.end_datetime.setMinimumWidth(400)
        form_layout.addRow("Date et heure de fin *:", self.end_datetime)

        # Room
        self.room_combo = QComboBox()
        self.room_combo.setObjectName("comboBox")
        self.room_combo.addItem("Choisissez une salle")
        self.room_combo.model().item(0).setEnabled(False) #can't choose "Choisissez une salle"
        self.room_combo.addItems(get_all_rooms_names())
        self.room_combo.setMinimumWidth(400)
        form_layout.addRow("Salle *:", self.room_combo)

        # Configuration
        self.config_combo = QComboBox()
        self.config_combo.setObjectName("comboBox")
        self.config_combo.addItem("Choisissez une configuration")
        self.config_combo.model().item(0).setEnabled(False)
        self.config_combo.addItems(get_all_config_names())
        self.config_combo.setMinimumWidth(400)
        form_layout.addRow("Configuration *:", self.config_combo)

        self.layout.addLayout(form_layout)
        self.layout.addSpacing(20)

        # Required fields note
        note = QLabel("* Champs obligatoires")
        note.setObjectName("startNote")
        self.layout.addWidget(note)

        self.layout.addSpacing(10)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Annuler")
        cancel_btn.setFixedWidth(CANCEL_BTN_WIDTH)
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.go_back)
        button_layout.addWidget(cancel_btn)

        create_btn = QPushButton("Créer l'événement")
        create_btn.setFixedWidth(CONTINUE_BTN_WIDTH)
        create_btn.setObjectName("continueBtn")
        create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        create_btn.clicked.connect(self.create_event_action)
        button_layout.addWidget(create_btn)

        self.layout.addLayout(button_layout)
        self.layout.addStretch()


    def create_event_action(self):
        # Validation
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom d'événement.")
            return

        if self.type_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un type d'événement.")
            return

        if self.room_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une salle.")
            return

        if self.config_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une configuration.")
            return

        if self.start_datetime.dateTime() >= self.end_datetime.dateTime():
            QMessageBox.warning(self, "Erreur", "La date de fin doit être après la date de début.")
            return


        # Create event
        event_name = self.name_input.text().strip()

        type_name = self.type_combo.currentText().strip()
        type_id = get_type_id(type_name)

        start_at = self.start_datetime.dateTime().toPyDateTime().replace(second=0, microsecond=0)
        end_at = self.end_datetime.dateTime().toPyDateTime().replace(second=0, microsecond=0)

        room_name = self.room_combo.currentText().strip()
        room_id = get_room_id(room_name)

        config_name = self.config_combo.currentText().strip()
        config_id = get_config_id(config_name)

        event_id = create_event(event_name, type_id, start_at, end_at, room_id, config_id)

        if event_id:
            QMessageBox.information(
                self,
                "Succès",
                f"L'événement '{event_name}' a été créé avec succès!\nID: {event_id}"
            )
            self.clear_form()
        else:
            QMessageBox.critical(
                self,
                "Erreur",
                "Une erreur est survenue lors de la création de l'événement."
            )

    def clear_form(self):
        """Clear all form fields."""
        self.name_input.clear()
        self.type_combo.setCurrentIndex(0)
        min_start_at = QDateTime.currentDateTime().addSecs(2 * 3600)
        self.start_datetime.setDateTime(min_start_at)
        self.end_datetime.setDateTime(min_start_at.addSecs(7200))
        self.room_combo.setCurrentIndex(0)
        self.config_combo.setCurrentIndex(0)

    def go_back(self):
        """Return to admin home."""
        self.main_window.show_admin_home_widget()