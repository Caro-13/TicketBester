import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QGridLayout, QApplication, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from src.db.requests import get_seats_with_status_for_event


# QPushButton for seats with a style
class Seat(QPushButton):
    """Bouton de siege individuel stylise avec bordure visible immediatement."""

    def __init__(self, seat_data, color_hex, category, width=35, height=28):
        super().__init__(seat_data['name'])
        self.seat_id = seat_data['id']
        self.category = category
        self.color_hex = color_hex
        self.status = seat_data['status']
        self.setFixedSize(width, height)
        self.setCheckable(True)

        # Disable if not available
        if self.status in ['SOLD', 'RESERVED', 'HOLD']:
            self.setEnabled(False)

        self.apply_style()

    def apply_style(self):
        if self.status == 'SOLD':
            # Grey for sold seats
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: #6c7086;
                    color: #1e1e2e;
                    border: 2px solid #6c7086;
                    border-radius: 4px;
                    font-size: 9px;
                    font-weight: bold;
                }}
            """)
        elif self.status in ['RESERVED', 'HOLD']:
            # Light purple for reserved/hold seats
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: #b4befe;
                    color: #1e1e2e;
                    border: 2px solid #b4befe;
                    border-radius: 4px;
                    font-size: 9px;
                    font-weight: bold;
                }}
            """)
        else:
            # Original style for available seats
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: #1e1e2e;
                    color: #cdd6f4;
                    border: 2px solid {self.color_hex}; /* Bordure solide et coloree */
                    border-radius: 4px;
                    font-size: 9px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #313244;
                    border: 2px solid #ffffff; /* La bordure devient blanche au survol */
                }}
                QPushButton:checked {{
                    background-color: {self.color_hex}; /* Le fond se remplit au clic */
                    color: #11111b; 
                    border: 2px solid {self.color_hex};
                }}
            """)


# Seating sector
class Sector(QFrame):
    """Conteneur de groupe de sieges avec alignement interne."""

    def __init__(self, color_hex, seats_data, category="", sw=35, sh=28):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{ 
                border: 1px solid {color_hex}; 
                background: #181825; 
                border-radius: 8px; 
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        grid = QGridLayout()
        grid.setSpacing(4)

        self.seats = []

        # Sort seats by ID to ensure proper order
        sorted_seats = sorted(seats_data, key=lambda x: x['id'])

        # Calculate grid dimensions based on sector
        num_seats = len(sorted_seats)
        if category == "Balcon Haut":
            rows, cols = 2, 15
        elif category in ["Balcon Gauche", "Balcon Droit"]:
            rows, cols = 10, 2
        elif category == "VIP":
            rows, cols = 2, 10
        elif category in ["SPC Gauche", "SPC Droit"]:
            rows, cols = 2, 2
        elif category == "Standard":
            rows, cols = 5, 10
        else:
            # Default calculation
            cols = int(num_seats ** 0.5) + 1
            rows = (num_seats + cols - 1) // cols

        for idx, seat_data in enumerate(sorted_seats):
            r = idx // cols
            c = idx % cols
            btn = Seat(seat_data, color_hex, category, sw, sh)
            grid.addWidget(btn, r, c)
            self.seats.append(btn)

        layout.addLayout(grid)


class ConcertHall(QWidget):
    def __init__(self, event_id, parent=None):
        super().__init__(parent)
        self.event_id = event_id
        self.setWindowTitle("Systeme de Reservation - Salle de Concert")
        self.setStyleSheet("background-color: #1e1e2e;")

        # Load seats from database
        self.seats_data = get_seats_with_status_for_event(event_id)
        self._organize_seats_by_sector()

        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(40)

        # Left side (Map + Title + Scene)
        self.plan_container = QVBoxLayout()
        self.plan_container.setSpacing(20)

        # Header (Home + Titre)
        header_layout = QHBoxLayout()

        # Home button
        self.btn_home = QPushButton("← Home")
        self.btn_home.setFixedWidth(100)
        self.btn_home.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_home.setStyleSheet("""
                    QPushButton {
                        background-color: transparent; 
                        color: #89b4fa;
                        border: none;
                        font-weight: bold;
                        padding: 5px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        color: #b4befe;
                    }
                """)

        header_layout.addWidget(self.btn_home)
        header_layout.addStretch()

        self.plan_container.addLayout(header_layout)

        # Title
        self.main_title = QLabel("Sélection des sièges")
        self.main_title.setStyleSheet("""
                    color: #fab387; 
                    font-size: 32px; 
                    font-weight: bold; 
                    margin-bottom: 10px;
                """)
        self.plan_container.addWidget(self.main_title)

        # Grid for organizing sectors
        self.hall_grid = QGridLayout()
        self.hall_grid.setSpacing(10)

        # Creation of sectors from DB data
        self.balcon_haut = Sector("#f9e2af", self.sector_seats.get("Balcon Haut", []), "Balcon Haut")
        self.balcon_gauche = Sector("#f9e2af", self.sector_seats.get("Balcon Gauche", []), "Balcon Gauche")
        self.balcon_droit = Sector("#f9e2af", self.sector_seats.get("Balcon Droit", []), "Balcon Droit")
        self.vip = Sector("#f38ba8", self.sector_seats.get("VIP", []), "VIP")
        self.spc_gauche = Sector("#a6e3a1", self.sector_seats.get("SPC Gauche", []), "SPC Gauche", sw=55)
        self.spc_droit = Sector("#a6e3a1", self.sector_seats.get("SPC Droit", []), "SPC Droit", sw=55)
        self.standard = Sector("#6cbdf9", self.sector_seats.get("Standard", []), "Standard")

        # Adding sectors to the grid
        self.hall_grid.addWidget(self.balcon_haut, 0, 1, 1, 3)
        self.hall_grid.addWidget(self.balcon_gauche, 0, 0, 3, 1)
        self.hall_grid.addWidget(self.balcon_droit, 0, 4, 3, 1)
        self.hall_grid.addWidget(self.spc_gauche, 1, 1)
        self.hall_grid.addWidget(self.vip, 1, 2)
        self.hall_grid.addWidget(self.spc_droit, 1, 3)
        self.hall_grid.addWidget(self.standard, 2, 1, 1, 3)

        # Stretch Management
        self.hall_grid.setRowStretch(3, 1)

        self.plan_container.addLayout(self.hall_grid)

        # Stage label
        scene_lbl = QLabel("SCÈNE")
        scene_lbl.setFixedHeight(70)
        scene_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scene_lbl.setStyleSheet("""
            background-color: #313244; color: #cdd6f4; 
            border: 1px solid #45475a; border-radius: 12px; 
            font-size: 26px; font-weight: bold;
        """)
        self.plan_container.addWidget(scene_lbl)

        # Stretch Management
        self.plan_container.addStretch()

        self.main_layout.addLayout(self.plan_container, stretch=4)

        # Side shutter
        self._setup_side_panel()

        # Connections
        self._connect_all_seats()

    def _organize_seats_by_sector(self):
        """Organize seats by sector name."""
        self.sector_seats = {}
        for seat in self.seats_data:
            sector_name = seat['sector']
            if sector_name not in self.sector_seats:
                self.sector_seats[sector_name] = []
            self.sector_seats[sector_name].append(seat)

    def _setup_side_panel(self):
        self.side_panel = QFrame()
        self.side_panel.setFixedWidth(320)
        self.side_panel.setStyleSheet("background: #181825; border-radius: 15px; border: 1px solid #313244;")
        side_layout = QVBoxLayout(self.side_panel)
        side_layout.setContentsMargins(20, 25, 20, 25)

        title = QLabel("SÉLECTION")
        title.setStyleSheet("color: #fab387; font-weight: bold; font-size: 20px; border: none;")
        side_layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #313244; border: none;")
        line.setFixedHeight(1)
        side_layout.addWidget(line)
        side_layout.addSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        self.info_list = QLabel("Aucun siege selectionne")
        self.info_list.setStyleSheet("color: #bac2de; border: none; font-size: 13px;")
        self.info_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.info_list.setWordWrap(True)
        scroll.setWidget(self.info_list)

        side_layout.addWidget(scroll)
        side_layout.addStretch()

        self.btn_confirm = QPushButton("Confirmer la selection")
        self.btn_confirm.setFixedHeight(50)
        self.btn_confirm.setStyleSheet("""
            QPushButton {
                background: #89b4fa; color: #1e1e2e; 
                font-weight: bold; font-size: 14px; border-radius: 8px;
            }
            QPushButton:hover { background: #b4befe; }
        """)
        side_layout.addWidget(self.btn_confirm)

        self.main_layout.addWidget(self.side_panel)

    def _connect_all_seats(self):
        sectors = [self.balcon_haut, self.balcon_gauche, self.balcon_droit,
                   self.spc_gauche, self.spc_droit, self.vip, self.standard]
        for sector in sectors:
            for s in sector.seats:
                s.clicked.connect(self.update_info)

    def update_info(self):
        selected = []
        sectors = [self.balcon_haut, self.balcon_gauche, self.balcon_droit,
                   self.spc_gauche, self.spc_droit, self.vip, self.standard]
        for sector in sectors:
            for s in sector.seats:
                if s.isChecked():
                    selected.append(f"• {s.category} : {s.text()}")
        self.info_list.setText("\n".join(selected) if selected else "Aucun siege sélectionné")

    def get_selected_seats(self):
        """Return list of selected seat IDs."""
        selected_ids = []
        sectors = [self.balcon_haut, self.balcon_gauche, self.balcon_droit,
                   self.spc_gauche, self.spc_droit, self.vip, self.standard]
        for sector in sectors:
            for s in sector.seats:
                if s.isChecked():
                    selected_ids.append(s.seat_id)
        return selected_ids


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConcertHall(event_id=1)
    window.show()
    sys.exit(app.exec())