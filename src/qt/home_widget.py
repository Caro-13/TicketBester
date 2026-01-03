from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView, QLabel, QPushButton, QFrame, QAbstractItemView, QMessageBox)
from PyQt6.QtCore import Qt, QTimer

from src.db.requests import get_all_events

from src.qt.reservation_widget import ReservationWidget

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
        title = QLabel("Évènements")
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
        self.table.setHorizontalHeaderLabels(["ÉVÈNEMENT / TYPE", "DATE", "HEURE", ""])

        # Configuration visuelle du tableau
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # On va personnaliser la largeur des colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Nom (Flexible)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Date (Compacte)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Heure (Compacte)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Bouton (Flexible)

        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
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
                background-color: #45475a; 
                color: #fab387;
            }
            /* Style pour le bouton RESERVER */
            QPushButton#reserveButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton#reserveButton:hover {
                background-color: #b4befe;
            }
        """)

        self.layout.addWidget(self.table)
        self.refresh_data()

    def create_reserve_button(self, evt_id, evt_name):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        btn = QPushButton("Réserver")
        btn.setObjectName("reserveButton")

        btn.clicked.connect(lambda: QTimer.singleShot(0, lambda: self.window().show_reservation_widget(evt_id, evt_name)))

        layout.addWidget(btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        widget.setLayout(layout)
        return widget

    def refresh_data(self):
        try:
            # Fetch real data from database
            data = get_all_events()

            if not data:
                # Show message if no events found
                QMessageBox.information(
                    self,
                    "Information",
                    "Aucun événement disponible pour le moment."
                )
                self.table.setRowCount(0)
                return

            self.table.setRowCount(0)

            for row_idx, row_data in enumerate(data):
                evt_id = row_data[0]
                evt_name = row_data[1]
                type_name = row_data[2]
                date = row_data[3]
                hour = row_data[4]

                # Format date and time for display
                if hasattr(date, 'strftime'):
                    date_str = date.strftime('%d/%m/%Y')
                else:
                    date_str = str(date)

                if hasattr(hour, 'strftime'):
                    hour_str = hour.strftime('%H:%M')
                else:
                    hour_str = str(hour)[:5]  # Take first 5 chars (HH:MM)

                self.table.insertRow(row_idx)
                self.table.setRowHeight(row_idx, 70)

                # 1. ÉVÈNEMENT / TYPE
                cell_widget = QWidget()
                cell_layout = QVBoxLayout(cell_widget)
                cell_layout.setContentsMargins(0, 0, 0, 0)
                cell_layout.setSpacing(2)

                # Nom
                name_label = QLabel(str(evt_name))
                name_label.setStyleSheet("font-weight: bold; font-size: 15px; color: #cdd6f4;")

                # Type
                type_label = QLabel(f"Type: {str(type_name)}")
                type_label.setStyleSheet("font-style: italic; color: #a6adc8; font-size: 10px;")

                cell_layout.addWidget(name_label)
                cell_layout.addWidget(type_label)
                cell_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                self.table.setCellWidget(row_idx, 0, cell_widget)

                # 2. DATE
                item_date = QTableWidgetItem(str(date))
                item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                font = item_date.font()
                font.setPointSize(14)
                font.setBold(True)
                item_date.setFont(font)

                item_date.setForeground(QBrush(QColor("#fab387")))
                self.table.setItem(row_idx, 1, item_date)

                # 3. HEURE
                item_hour = QTableWidgetItem(str(hour))
                item_hour.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_hour.setForeground(QBrush(QColor("#a6adc8")))
                self.table.setItem(row_idx, 2, item_hour)

                # 4. Bouton "Réserver"
                self.table.setCellWidget(row_idx, 3, self.create_reserve_button(evt_id, evt_name))

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible de charger les événements:\n{str(e)}"
            )
            print(f"Error in refresh_data: {e}")