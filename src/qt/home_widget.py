from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView, QLabel, QPushButton, QFrame, QAbstractItemView)
from PyQt6.QtCore import Qt

from db.requests import get_all_events_with_names
from src.db.requests import get_all_events


class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # --- Layout Principal ---
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # --- En-tête (Titre + Bouton) ---
        header_layout = QHBoxLayout()

        # Titre
        title = QLabel("Evènements")
        title.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #fab387; 
            font-family: 'Segoe UI';
        """)
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Bouton "Actualiser"
        self.btn_refresh = QPushButton("Actualiser")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.refresh_data)
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45475a;
                border-color: #585b70;
            }
        """)
        header_layout.addWidget(self.btn_refresh)

        self.layout.addLayout(header_layout)

        # --- Barre de séparation décorative ---
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #45475a;")
        self.layout.addWidget(line)

        # --- Tableau des Événements ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["EVENEMENT", "TYPE", "DATE", "HEURE"])

        # Configuration visuelle du tableau
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)  # Pas de numéros de ligne
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Pleine largeur
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Lecture seule
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Style CSS spécifique au tableau
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e2e;       
                alternate-background-color: #2a2a3c;
                border: none;
                gridline-color: #313244;
                color: #cdd6f4;                  
            }
            QHeaderView::section {
                background-color: #1e1e2e;
                color: #89b4fa;
                font-weight: bold;
                border: none;
                border-bottom: 2px solid #313244;
                padding: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #313244;
                color: #cdd6f4;
            }
            QTableWidget::item:selected {
                background-color: #313244;
                color: #fab387;
            }
        """)

        self.layout.addWidget(self.table)

        self.refresh_data()

    def refresh_data(self):
        # TODO: Change this to get_all_events_with_names() when ready
        #data = get_all_events_with_names()
        # False data for demonstration purposes
        data = [("Concert de Rock", "Concert", "2024-07-15", "20:00"),
            ("Exposition d'Art", "Exposition", "2024-08-01", "10:00"),
            ("Festival de Jazz", "Festival", "2024-09-10", "18:30"),
            ("Conférence Tech", "Conférence", "2024-10-05", "09:00"),
            ("Otello", "Théâtre", "2024-11-20", "19:30")]

        self.table.setRowCount(0)

        for row_idx, (evt_name, type_name, date, hour) in enumerate(data):
            self.table.insertRow(row_idx)
            self.table.setRowHeight(row_idx, 60)

            item_evt_name = QTableWidgetItem(str(evt_name))
            item_evt_name.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            font = item_evt_name.font()
            font.setBold(True)
            font.setPointSize(11)
            item_evt_name.setFont(font)

            item_type_name = QTableWidgetItem(str(type_name))
            item_type_name.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
            item_type_name.setForeground(QBrush(QColor("#89b4fa")))

            item_date = QTableWidgetItem(str(date))
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            item_hour = QTableWidgetItem(str(hour))
            item_hour.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_hour.setForeground(QBrush(QColor("#a6adc8")))

            self.table.setItem(row_idx, 0, item_evt_name)
            self.table.setItem(row_idx, 1, item_type_name)
            self.table.setItem(row_idx, 2, item_date)
            self.table.setItem(row_idx, 3, item_hour)