from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                             QProgressBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.db.requests import get_event_statistics


class AdminStatsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()
        self.load_statistics()

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

        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setFixedWidth(120)
        refresh_btn.clicked.connect(self.load_statistics)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Title
        title = QLabel("Statistiques des événements")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Statistics table
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(8)
        self.stats_table.setHorizontalHeaderLabels([
            "ID",
            "Événement",
            "Date",
            "Statut",
            "Billets vendus",
            "Billets scannés",
            "Places totales",
            "Taux de remplissage"
        ])

        # Configure table
        self.stats_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.stats_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.stats_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.stats_table.setAlternatingRowColors(True)
        self.stats_table.setSortingEnabled(True)
        self.stats_table.setShowGrid(False)
        self.stats_table.verticalHeader().setVisible(False)

        layout.addWidget(self.stats_table)

        # Summary section
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(30)

        self.total_events_label = QLabel("Total d'événements: 0")
        self.total_events_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        summary_layout.addWidget(self.total_events_label)

        self.total_tickets_label = QLabel("Total de billets vendus: 0")
        self.total_tickets_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        summary_layout.addWidget(self.total_tickets_label)

        self.total_scanned_label = QLabel("Total de billets scannés: 0")
        self.total_scanned_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        summary_layout.addWidget(self.total_scanned_label)

        summary_layout.addStretch()
        layout.addLayout(summary_layout)

        self.setLayout(layout)

    def load_statistics(self):
        """Load and display event statistics."""
        stats = get_event_statistics()

        self.stats_table.setRowCount(len(stats))
        self.stats_table.setSortingEnabled(False)  # Disable while populating

        total_tickets = 0
        total_scanned = 0

        for row, event_stat in enumerate(stats):
            # ID
            id_item = QTableWidgetItem(str(event_stat['id']))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stats_table.setItem(row, 0, id_item)

            # Event name
            name_item = QTableWidgetItem(event_stat['name'])
            self.stats_table.setItem(row, 1, name_item)

            # Date
            date_str = event_stat['start_at'].strftime("%d/%m/%Y %H:%M")
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stats_table.setItem(row, 2, date_item)

            # Status
            status_map = {
                'on_sale': 'En vente',
                'on_site': 'Sur place',
                'cancelled': 'Annulé',
                'finished': 'Terminé'
            }
            status_text = status_map.get(event_stat['status'], event_stat['status'])
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Color code status
            if event_stat['status'] == 'on_sale':
                status_item.setBackground(Qt.GlobalColor.green)
            elif event_stat['status'] == 'cancelled':
                status_item.setBackground(Qt.GlobalColor.red)
            elif event_stat['status'] == 'finished':
                status_item.setBackground(Qt.GlobalColor.lightGray)

            self.stats_table.setItem(row, 3, status_item)

            # Tickets sold
            tickets_sold = event_stat['tickets_sold']
            sold_item = QTableWidgetItem(str(tickets_sold))
            sold_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stats_table.setItem(row, 4, sold_item)
            total_tickets += tickets_sold

            # Tickets scanned
            tickets_scanned = event_stat['tickets_scanned']
            scanned_item = QTableWidgetItem(str(tickets_scanned))
            scanned_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stats_table.setItem(row, 5, scanned_item)
            total_scanned += tickets_scanned

            # Total seats
            total_seats = event_stat['total_seats']
            seats_item = QTableWidgetItem(str(total_seats))
            seats_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stats_table.setItem(row, 6, seats_item)

            # Fill rate with progress bar
            if total_seats > 0:
                fill_rate = (tickets_sold / total_seats) * 100
                fill_widget = QWidget()
                fill_layout = QVBoxLayout()
                fill_layout.setContentsMargins(5, 5, 5, 5)

                progress = QProgressBar()
                progress.setMaximum(100)
                progress.setValue(int(fill_rate))
                progress.setFormat(f"{fill_rate:.1f}%")
                progress.setStyleSheet("""
                    QProgressBar {
                        text-align: center;
                        border: 1px solid #ccc;
                        border-radius: 3px;
                        background-color: #f0f0f0;
                    }
                    QProgressBar::chunk {
                        background-color: #4CAF50;
                    }
                """)

                fill_layout.addWidget(progress)
                fill_widget.setLayout(fill_layout)
                self.stats_table.setCellWidget(row, 7, fill_widget)
            else:
                fill_item = QTableWidgetItem("N/A")
                fill_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.stats_table.setItem(row, 7, fill_item)

        # Update summary labels
        self.total_events_label.setText(f"Total d'événements: {len(stats)}")
        self.total_tickets_label.setText(f"Total de billets vendus: {total_tickets}")
        self.total_scanned_label.setText(f"Total de billets scannés: {total_scanned}")

        # Adjust column widths
        self.stats_table.resizeColumnsToContents()
        self.stats_table.setSortingEnabled(True)  # Re-enable sorting

    def go_back(self):
        """Return to admin home."""
        self.main_window.show_admin_home_widget()