from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from src.db.requests import scan_ticket
from datetime import datetime


class StaffScanWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.scan_history = []
        self.init_ui()

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

        staff_info = QLabel(f"Personnel: {self.main_window.staff_name or 'Non sélectionné'}")
        staff_info.setStyleSheet("font-weight: bold; color: #4CAF50;")
        header_layout.addWidget(staff_info)

        layout.addLayout(header_layout)

        # Title
        title = QLabel("Scanner les billets")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Door selection
        door_layout = QHBoxLayout()
        door_label = QLabel("Porte d'entrée:")
        door_label.setMinimumWidth(120)
        door_font = QFont()
        door_font.setPointSize(12)
        door_label.setFont(door_font)

        self.door_combo = QComboBox()
        self.door_combo.addItems(["Porte A", "Porte B"])
        self.door_combo.setMinimumWidth(200)

        door_layout.addWidget(door_label)
        door_layout.addWidget(self.door_combo)
        door_layout.addStretch()
        layout.addLayout(door_layout)

        layout.addSpacing(20)

        # Scan section
        scan_section = QLabel("Scanner un billet")
        scan_font = QFont()
        scan_font.setPointSize(18)
        scan_font.setBold(True)
        scan_section.setFont(scan_font)
        layout.addWidget(scan_section)

        # Ticket ID input
        input_layout = QHBoxLayout()

        self.ticket_input = QLineEdit()
        self.ticket_input.setPlaceholderText("Entrez le numéro du billet ou scannez le code-barre...")
        self.ticket_input.setObjectName("inputLine")
        self.ticket_input.returnPressed.connect(self.scan_ticket_action)

        scan_btn = QPushButton("Scanner")
        scan_btn.setFixedSize(120, 50)
        scan_btn.setObjectName("validateBtn")
        scan_btn.clicked.connect(self.scan_ticket_action)

        input_layout.addWidget(self.ticket_input)
        input_layout.addWidget(scan_btn)

        layout.addLayout(input_layout)

        # Status message
        self.status_label = QLabel("")
        self.status_label.setMinimumHeight(60)
        self.status_label.setObjectName("statusNeutral")
        layout.addWidget(self.status_label)

        layout.addSpacing(20)

        # Scan history
        history_label = QLabel("Historique des scans")
        history_label.setFont(scan_font)
        layout.addWidget(history_label)

        # Statistics
        stats_layout = QHBoxLayout()

        self.total_scans_label = QLabel("Total scans: 0")
        self.total_scans_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4CAF50;")
        stats_layout.addWidget(self.total_scans_label)

        stats_layout.addSpacing(30)

        self.success_scans_label = QLabel("Réussis: 0")
        self.success_scans_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4CAF50;")
        stats_layout.addWidget(self.success_scans_label)

        stats_layout.addSpacing(30)

        self.failed_scans_label = QLabel("Échoués: 0")
        self.failed_scans_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #f44336;")
        stats_layout.addWidget(self.failed_scans_label)

        stats_layout.addStretch()

        clear_history_btn = QPushButton("Effacer l'historique")
        clear_history_btn.clicked.connect(self.clear_history)
        stats_layout.addWidget(clear_history_btn)

        layout.addLayout(stats_layout)

        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Heure", "Billet #", "Statut", "Message"])
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.history_table.setMaximumHeight(300)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setShowGrid(False)
        self.history_table.verticalHeader().setVisible(False)

        layout.addWidget(self.history_table)

        layout.addStretch()
        self.setLayout(layout)

    def scan_ticket_action(self):
        """Scan a ticket."""
        ticket_id_str = self.ticket_input.text().strip()

        if not ticket_id_str:
            self.show_status("Veuillez entrer un numéro de billet", "error")
            return

        try:
            ticket_id = int(ticket_id_str)
        except ValueError:
            self.show_status("Numéro de billet invalide", "error")
            self.ticket_input.clear()
            return

        if not self.main_window.staff_id:
            self.show_status("Erreur: Personnel non identifié", "error")
            return

        # Get selected door
        door = self.door_combo.currentText()[-1]

        # Scan the ticket
        result = scan_ticket(ticket_id, self.main_window.staff_id, door)

        # Add to history
        scan_record = {
            'time': datetime.now().strftime("%H:%M:%S"),
            'ticket_id': ticket_id,
            'success': result['success'],
            'message': result['message']
        }
        self.scan_history.insert(0, scan_record)  # Add to beginning

        # Update display
        if result['success']:
            self.show_status(f"✓ {result['message']}", "success")
        else:
            self.show_status(f"✗ {result['message']}", "error")

        self.update_history_table()
        self.update_statistics()

        # Clear input
        self.ticket_input.clear()
        self.ticket_input.setFocus()

    def show_status(self, message, status_type):
        """Show status message with color coding."""
        self.status_label.setText(message)

        if status_type == "success":
            self.status_label.setObjectName("statusSuccess")
            self.status_label.style().unpolish(self.status_label)
            self.status_label.style().polish(self.status_label)
        elif status_type == "error":
            self.status_label.setObjectName("statusError")
            self.status_label.style().unpolish(self.status_label)
            self.status_label.style().polish(self.status_label)
        else:
            self.status_label.setObjectName("statusNeutral")
            self.status_label.style().unpolish(self.status_label)
            self.status_label.style().polish(self.status_label)

        # Auto-clear after 3 seconds
        QTimer.singleShot(3000, lambda: self.status_label.setText(""))

    def update_history_table(self):
        """Update the scan history table."""
        self.history_table.setRowCount(len(self.scan_history))

        for row, record in enumerate(self.scan_history):
            # Time
            time_item = QTableWidgetItem(record['time'])
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 0, time_item)

            # Ticket ID
            id_item = QTableWidgetItem(str(record['ticket_id']))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 1, id_item)

            # Status
            status_item = QTableWidgetItem("✓ Réussi" if record['success'] else "✗ Échoué")
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if record['success']:
                status_item.setForeground(QColor("#4CAF50"))
            else:
                status_item.setForeground(QColor("#f44336"))
            self.history_table.setItem(row, 2, status_item)

            # Message
            message_item = QTableWidgetItem(record['message'])
            self.history_table.setItem(row, 3, message_item)

    def update_statistics(self):
        """Update scan statistics."""
        total = len(self.scan_history)
        success = sum(1 for r in self.scan_history if r['success'])
        failed = total - success

        self.total_scans_label.setText(f"Total scans: {total}")
        self.success_scans_label.setText(f"Réussis: {success}")
        self.failed_scans_label.setText(f"Échoués: {failed}")

    def clear_history(self):
        """Clear scan history."""
        reply = QMessageBox.question(
            self,
            "Confirmer",
            "Voulez-vous vraiment effacer l'historique des scans?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.scan_history = []
            self.update_history_table()
            self.update_statistics()
            self.status_label.setText("")

    def go_back(self):
        """Return to staff home."""
        self.main_window.show_staff_home_widget()