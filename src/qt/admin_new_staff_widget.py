from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QMessageBox,
                             QTableWidget, QTableWidgetItem, QHeaderView, QGridLayout)
from PyQt6.QtCore import Qt

from src.db.requests import add_staff_member, get_all_staff


class AdminNewStaffWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()
        self.load_staff_list()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 30, 50, 30)

        # Header
        header_layout = QHBoxLayout()

        back_btn = QPushButton("← Retour")
        back_btn.setFixedWidth(120)
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Title
        title = QLabel("Gestion du personnel")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        # Add staff section
        add_section = QLabel("Ajouter un nouveau membre")
        add_section.setObjectName("littleSection")
        layout.addWidget(add_section)

        # Form
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(10)

        name_label = QLabel("Nom complet * :")
        name_label.setObjectName("infosInput")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom complet du membre du personnel")
        self.name_input.setObjectName("inputLine")
        self.name_input.setMinimumWidth(400)

        form_layout.addWidget(name_label, 0, 0, Qt.AlignmentFlag.AlignRight)
        form_layout.addWidget(self.name_input, 0, 1)

        layout.addLayout(form_layout)

        # Add button
        add_btn_layout = QHBoxLayout()
        add_btn_layout.addStretch()

        add_btn = QPushButton("Ajouter le membre")
        add_btn.setObjectName("continueBtn")
        add_btn.clicked.connect(self.add_staff_action)
        add_btn_layout.addWidget(add_btn)

        layout.addLayout(add_btn_layout)

        # Separator
        layout.addSpacing(30)

        # Staff list section
        list_section = QLabel("Liste du personnel")
        list_section.setObjectName("littleSection")
        layout.addWidget(list_section)

        # Staff table
        self.staff_table = QTableWidget()
        self.staff_table.setColumnCount(2)
        self.staff_table.setHorizontalHeaderLabels(["ID", "Nom"])
        self.staff_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.staff_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.staff_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.staff_table.setAlternatingRowColors(True)
        self.staff_table.setMinimumHeight(300)
        self.staff_table.setShowGrid(False)
        self.staff_table.verticalHeader().setVisible(False)

        layout.addWidget(self.staff_table)

        self.setLayout(layout)

    def add_staff_action(self):
        """Validate and add new staff member."""
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom.")
            return

        staff_id = add_staff_member(name)

        if staff_id:
            QMessageBox.information(
                self,
                "Succès",
                f"Le membre '{name}' a été ajouté avec succès!\nID: {staff_id}"
            )
            self.name_input.clear()
            self.load_staff_list()
        else:
            QMessageBox.critical(
                self,
                "Erreur",
                "Une erreur est survenue lors de l'ajout du membre."
            )

    def load_staff_list(self):
        """Load and display all staff members."""
        staff_list = get_all_staff()

        self.staff_table.setRowCount(len(staff_list))

        for row, staff in enumerate(staff_list):
            staff_id, name = staff

            id_item = QTableWidgetItem(str(staff_id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.staff_table.setItem(row, 0, id_item)

            name_item = QTableWidgetItem(name)
            self.staff_table.setItem(row, 1, name_item)

        # Adjust column widths
        self.staff_table.resizeColumnToContents(0)

    def go_back(self):
        self.main_window.show_admin_home_widget()