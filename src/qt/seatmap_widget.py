import sys
from pickletools import bytes_types

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QApplication, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal


# QPushButton for seats with a style
class Seat(QPushButton):
    """Bouton de siege individuel stylise avec bordure visible immediatement."""

    def __init__(self, label, color_hex, category, width=35, height=28):
        super().__init__(label)
        self.category = category
        self.color_hex = color_hex
        self.setFixedSize(width, height)
        self.setCheckable(True)
        self.apply_style()

    def apply_style(self):
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

    def __init__(self, color_hex, rows, cols, prefix="", category="", sw=35, sh=28):
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
        for r in range(rows):
            for c in range(cols):
                seat_num = f"{prefix}{r * cols + c + 1}"
                btn = Seat(seat_num, color_hex, category, sw, sh)
                grid.addWidget(btn, r, c)
                self.seats.append(btn)

        layout.addLayout(grid)


class ConcertHall(QWidget): # ToDo Ajouter les informations à transmettre
    def __init__(self, parent=None):
        super().__init__(parent)
        super().__init__()
        self.setWindowTitle("Systeme de Reservation - Salle de Concert")
        self.resize(1400, 900)
        self.setStyleSheet("background-color: #1e1e2e;")

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

        # Creation of sectors
        self.balcon_haut = Sector("#f9e2af", 2, 15, "BH", "Balcon Haut")
        self.balcon_gauche = Sector("#f9e2af", 10, 2, "BG", "Balcon Gauche")
        self.balcon_droit = Sector("#f9e2af", 10, 2, "BD", "Balcon Droit")
        self.vip = Sector("#f38ba8", 2, 10, "V", "VIP")
        self.spc_gauche = Sector("#a6e3a1", 2, 2, "SPG", "SPC", sw=55)
        self.spc_droit = Sector("#a6e3a1", 2, 2, "SPD", "SPC", sw=55)
        self.standard = Sector("#6cbdf9", 5, 10, "S", "Standard")

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConcertHall()
    window.show()
    sys.exit(app.exec())
