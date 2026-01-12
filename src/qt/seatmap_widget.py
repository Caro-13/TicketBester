import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QGridLayout, QApplication, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal

from src.constants import (SEAT_WIDTH,SEAT_HEIGHT,SEAT_GRID_SPACING,SEAT_LARGE_WIDTH,BACK_BTN_WIDTH,CONFIRM_BTN_HEIGHT,SIDE_PANEL_WIDTH)

from src.db.requests import get_seats_with_status_for_event, get_sector_supplements_for_event, \
    add_ticket_to_reservation, cancel_reservation, delete_reservation


# QPushButton for seats with a style
class Seat(QPushButton):
    """Bouton de siege individuel stylise avec bordure visible immediatement."""

    def __init__(self, seat_data, color_hex, category, width=SEAT_WIDTH, height=SEAT_HEIGHT):
        super().__init__(seat_data['name'])
        self.seat_id = seat_data['id']
        self.category = category
        self.color_hex = color_hex
        self.status = seat_data['status']
        self.setFixedSize(width, height)
        self.setCheckable(True)

        # Disable if not available
        if self.status in ['SOLD', 'RESERVED']:
            self.setEnabled(False)

        self.apply_style()

    def apply_style(self):
        if self.status == 'SOLD':
            # Grey for sold seats
            self.setObjectName("seatSold")
        elif self.status == 'RESERVED' :
            # Light purple for reserved/hold seats
            self.setObjectName("seatReserved")
        else:
            # Original style for available seats
            self.setObjectName("seatAvailable")
            # But colors change dynamically
            self.setStyleSheet(f"""
                        QPushButton#seatAvailable {{
                            color: #ffffff;
                            border: 2px solid {self.color_hex};
                        }}
                        QPushButton#seatAvailable:hover {{
                            color: #ffffff;
                            border: 2px solid #ffffff;
                        }}
                        QPushButton#seatAvailable:checked {{
                            background-color: {self.color_hex};
                            border: 2px solid {self.color_hex};
                        }}
                    """)


# Seating sector
class Sector(QFrame):
    """Conteneur de groupe de sieges avec alignement interne."""

    def __init__(self, color_hex, seats_data, category="", sw=SEAT_WIDTH, sh=SEAT_HEIGHT):
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
        grid.setSpacing(SEAT_GRID_SPACING)

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
    def __init__(self, reservation_data= None , parent=None):
        super().__init__(parent)
        self.reservation_data = reservation_data
        self.event_id = self.reservation_data["event_id"]
        self.tarifs = self.reservation_data["tarifs"]
        self.nbr_seat_to_choose = sum(tarif_info['quantity'] for tarif_info in self.tarifs.values())
        self.total_price = self.reservation_data["total"]
        self.actual_total_price = self.total_price

        self.is_staff_sell = reservation_data.get('vendor_id') != 1

        self.setWindowTitle("Systeme de Reservation - Salle de Concert")
        self.setStyleSheet("background-color: #1e1e2e;")

        # Load seats from database
        self.seats_data = get_seats_with_status_for_event(self.event_id)
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

        # Back button (to return to tarif selection)
        self.btn_back = QPushButton("← Tarifs")
        self.btn_back.setFixedWidth(BACK_BTN_WIDTH)
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.setObjectName("backBtn")
        self.btn_back.clicked.connect(self._handle_back_to_reservation)

        # Home button
        self.btn_home = QPushButton("⌂ Home")
        self.btn_home.setFixedWidth(BACK_BTN_WIDTH)
        self.btn_home.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_home.setObjectName("backBtn")
        self.btn_home.clicked.connect(self._handle_home)

        header_layout.addWidget(self.btn_back)
        header_layout.addSpacing(10)
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
        self.spc_gauche = Sector("#a6e3a1", self.sector_seats.get("SPC Gauche", []), "SPC Gauche", sw=SEAT_LARGE_WIDTH )
        self.spc_droit = Sector("#a6e3a1", self.sector_seats.get("SPC Droit", []), "SPC Droit", sw=SEAT_LARGE_WIDTH )
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

        # Nbr left of seat label
        self.nbr_selection_left_lbl = QLabel(
            ("Sélectionnez encore " + str(self.nbr_seat_to_choose)
             if self.nbr_seat_to_choose != 0 else "Tout les sièges ont été sélectionné")
        )
        self.nbr_selection_left_lbl.setFixedHeight(70)
        self.nbr_selection_left_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nbr_selection_left_lbl.setStyleSheet("""
                    background-color: #89b4fa; color: #cdd6f4; 
                    border: 1px solid #45475a; border-radius: 12px; 
                    font-size: 26px; font-weight: bold;
                """)
        self.plan_container.addWidget(self.nbr_selection_left_lbl)

        # Stretch Management
        self.plan_container.addStretch()

        self.main_layout.addLayout(self.plan_container, stretch=4)

        # Right side with two panels
        right_side_layout = QVBoxLayout()
        right_side_layout.setSpacing(20)

        # Legend panel
        self._setup_legend_panel()
        right_side_layout.addWidget(self.legend_panel)

        # Selection panel
        self._setup_side_panel()
        right_side_layout.addWidget(self.side_panel)

        self.main_layout.addLayout(right_side_layout)

        # Connections
        self._connect_all_seats()

        # Link for confirm button
        if parent and hasattr(parent, 'show_payment_widget'):
            self.btn_confirm.clicked.connect(self._on_confirm_clicked)

    def _organize_seats_by_sector(self):
        """Organize seats by sector name."""
        self.sector_seats = {}
        for seat in self.seats_data:
            sector_name = seat['sector']
            if sector_name not in self.sector_seats:
                self.sector_seats[sector_name] = []
            self.sector_seats[sector_name].append(seat)

    def _setup_legend_panel(self):
        """Legends to seat status and sectors"""
        self.legend_panel = QFrame()
        self.legend_panel.setFixedWidth(320)
        self.legend_panel.setStyleSheet("background: #181825; border-radius: 15px; border: 1px solid #313244;")
        legend_layout = QVBoxLayout(self.legend_panel)
        legend_layout.setContentsMargins(20, 20, 20, 20)
        legend_layout.setSpacing(10)

        title = QLabel("LÉGENDE")
        title.setStyleSheet("color: #fab387; font-weight: bold; font-size: 16px; border: none;")
        legend_layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #313244; border: none;")
        line.setFixedHeight(1)
        legend_layout.addWidget(line)

        # Status section
        status_title = QLabel("Statuts")
        status_title.setStyleSheet("color: #cdd6f4; font-weight: bold; font-size: 13px; border: none; margin-top: 5px;")
        legend_layout.addWidget(status_title)

        # Sold
        sold_layout = QHBoxLayout()
        sold_box = QLabel()
        sold_box.setFixedSize(15, 15)
        sold_box.setStyleSheet("background-color: #6c7086; border: 1px solid #6c7086; border-radius: 3px;")
        sold_text = QLabel("Vendu")
        sold_text.setStyleSheet("color: #bac2de; font-size: 12px; border: none;")
        sold_layout.addWidget(sold_box)
        sold_layout.addWidget(sold_text)
        sold_layout.addStretch()
        legend_layout.addLayout(sold_layout)

        # Reserved
        reserved_layout = QHBoxLayout()
        reserved_box = QLabel()
        reserved_box.setFixedSize(15, 15)
        reserved_box.setStyleSheet("background-color: #b4befe; border: 1px solid #b4befe; border-radius: 3px;")
        reserved_text = QLabel("Réservé")
        reserved_text.setStyleSheet("color: #bac2de; font-size: 12px; border: none;")
        reserved_layout.addWidget(reserved_box)
        reserved_layout.addWidget(reserved_text)
        reserved_layout.addStretch()
        legend_layout.addLayout(reserved_layout)

        # Separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet("background-color: #313244; border: none;")
        line2.setFixedHeight(1)
        legend_layout.addWidget(line2)

        # Sectors section
        sectors_title = QLabel("Catégories")
        sectors_title.setStyleSheet(
            "color: #cdd6f4; font-weight: bold; font-size: 13px; border: none; margin-top: 5px;")
        legend_layout.addWidget(sectors_title)

        # Define sectors with their colors
        sectors = [
            ("#f9e2af", "Balcon"),
            ("#f38ba8", "VIP"),
            ("#a6e3a1", "SPC"),
            ("#6cbdf9", "Standard")
        ]

        for color, name in sectors:
            sector_layout = QHBoxLayout()
            sector_box = QLabel()
            sector_box.setFixedSize(15, 15)
            sector_box.setStyleSheet(f"background-color: {color}; border: 1px solid {color}; border-radius: 3px;")
            sector_text = QLabel(name)
            sector_text.setStyleSheet("color: #bac2de; font-size: 12px; border: none;")
            sector_layout.addWidget(sector_box)
            sector_layout.addWidget(sector_text)
            sector_layout.addStretch()
            legend_layout.addLayout(sector_layout)

        # Check if there are supplements in the data
        try:
            sector_supplements = get_sector_supplements_for_event(self.event_id)
        except Exception as e:
            print(f"Error loading supplements: {e}")
            sector_supplements = {}

        if sector_supplements:
            # Separator
            line3 = QFrame()
            line3.setFrameShape(QFrame.Shape.HLine)
            line3.setStyleSheet("background-color: #313244; border: none;")
            line3.setFixedHeight(1)
            legend_layout.addWidget(line3)

            # Supplements section
            supplements_title = QLabel("Suppléments")
            supplements_title.setStyleSheet("color: #cdd6f4; font-weight: bold; font-size: 13px; border: none; margin-top: 5px;")
            legend_layout.addWidget(supplements_title)

            for sector_name, supplement in sector_supplements.items():
                supp_layout = QHBoxLayout()
                supp_text = QLabel(f"{sector_name}: +{supplement:.2f} CHF")
                supp_text.setStyleSheet("color: #bac2de; font-size: 12px; border: none;")
                supp_layout.addWidget(supp_text)
                supp_layout.addStretch()
                legend_layout.addLayout(supp_layout)

        legend_layout.addStretch()

    def _setup_side_panel(self):
        self.side_panel = QFrame()
        self.side_panel.setFixedWidth(SIDE_PANEL_WIDTH)
        self.side_panel.setStyleSheet("background: #181825; border-radius: 15px; border: 1px solid #313244;")
        side_layout = QVBoxLayout(self.side_panel)
        side_layout.setContentsMargins(20, 25, 20, 25)

        self.title = QLabel("SÉLECTION")
        self.title.setStyleSheet("color: #fab387; font-weight: bold; font-size: 20px; border: none;")
        side_layout.addWidget(self.title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #313244; border: none;")
        line.setFixedHeight(1)
        side_layout.addWidget(line)
        side_layout.addSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        self.info_list = QLabel("Aucun siege sélectionné")
        self.info_list.setStyleSheet("color: #bac2de; border: none; font-size: 13px;")
        self.info_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.info_list.setWordWrap(True)
        scroll.setWidget(self.info_list)

        side_layout.addWidget(scroll)
        side_layout.addStretch()

        self.btn_confirm = QPushButton(f"Confirmer la selection ({self.total_price} CHF)")
        self.btn_confirm.setFixedHeight(CONFIRM_BTN_HEIGHT)
        self.btn_confirm.setObjectName("confirmBtn")
        self.btn_confirm.setEnabled(False)
        side_layout.addWidget(self.btn_confirm)

    def _connect_all_seats(self):
        sectors = [self.balcon_haut, self.balcon_gauche, self.balcon_droit,
                   self.spc_gauche, self.spc_droit, self.vip, self.standard]
        for sector in sectors:
            for s in sector.seats:
                s.clicked.connect(self.update_info)

    def update_info(self):
        clicked_seat = self.sender()

        # Count how much seats are check
        currently_selected = []
        for sector in [self.balcon_haut, self.balcon_gauche, self.balcon_droit,
                       self.spc_gauche, self.spc_droit, self.vip, self.standard]:
            for s in sector.seats:
                if s.isChecked():
                    currently_selected.append(s)

        # If there's more than seat to choose, we uncheck the last checked
        if len(currently_selected) > self.nbr_seat_to_choose:
            if clicked_seat:
                clicked_seat.setChecked(False)
            return

        selected = []
        sectors = [self.balcon_haut, self.balcon_gauche, self.balcon_droit,
                   self.spc_gauche, self.spc_droit, self.vip, self.standard]

        actual_nbr_selection = 0
        self.actual_total_price = self.total_price

        for sector in sectors:
            for s in sector.seats:
                if s.isChecked():
                    sector_supplements = get_sector_supplements_for_event(self.event_id)

                    actual_nbr_selection += 1

                    if s.category in sector_supplements:
                        for sector_name, supplement in sector_supplements.items():
                            if sector_name == s.category:
                                self.actual_total_price += supplement
                                print(f"{supplement} of supplement added")

                    selected.append(f"• {s.category} : {s.text()}")

        self.nbr_selection_left_lbl.setText(
            f"Sélectionnez encore {self.nbr_seat_to_choose - actual_nbr_selection}"
            if self.nbr_seat_to_choose - actual_nbr_selection != 0
            else "Tous les sièges ont été sélectionnés"
        )

        self.btn_confirm.setText(f"Confirmer la selection ({self.actual_total_price} CHF)")

        if self.nbr_seat_to_choose - actual_nbr_selection == 0:
            self.btn_confirm.setStyleSheet("background-color: #89b4fa; color: white;")
            self.btn_confirm.setEnabled(True)
            self.nbr_selection_left_lbl.setStyleSheet("""
                                            background-color: #313244; color: #cdd6f4; 
                                            border: 1px solid #45475a; border-radius: 12px; 
                                            font-size: 26px; font-weight: bold;
                                        """)
        else:
            self.btn_confirm.setStyleSheet("background-color: transparent; color: white;")
            self.btn_confirm.setEnabled(False)
            self.nbr_selection_left_lbl.setStyleSheet("""
                                background-color: #89b4fa; color: #cdd6f4; 
                                border: 1px solid #45475a; border-radius: 12px; 
                                font-size: 26px; font-weight: bold;
                            """)

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

    # Send actual price to main.py
    def _on_confirm_clicked(self):
        try:
            main_win = self.window()

            if self.is_staff_sell:
                if not hasattr(main_win, 'show_payment_widget'):
                    QMessageBox.warning(self, "Erreur", "Impossible de continuer au paiement.")
                    return
            else:
                if not hasattr(main_win, 'show_payment_widget'):
                    QMessageBox.warning(self, "Erreur", "Impossible de continuer au paiement.")
                    return

            # Get selected seats
            selected_seat_ids = self.get_selected_seats()

            if len(selected_seat_ids) != self.nbr_seat_to_choose:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner tous les sièges requis.")
                return

            # Get reservation data
            reservation_id = self.reservation_data.get('reservation_id')
            event_id = self.reservation_data.get('event_id')
            tarifs = self.reservation_data.get('tarifs', {})

            if not reservation_id:
                QMessageBox.warning(self, "Erreur", "Aucune réservation trouvée.")
                return

            # Create tickets for each selected seat
            # Match seats to tarifs in order
            tarif_list = []
            for tarif_name, tarif_info in tarifs.items():
                quantity = tarif_info['quantity']
                for _ in range(quantity):
                    tarif_list.append(tarif_name)

            # Assign seats to tarifs
            if len(selected_seat_ids) != len(tarif_list):
                QMessageBox.warning(self, "Erreur", "Nombre de sièges ne correspond pas aux tarifs.")
                return

            # Create a ticket for each selected seat
            for i, seat_id in enumerate(selected_seat_ids):
                tarif_name = tarif_list[i]

                success = add_ticket_to_reservation(
                    reservation_id=reservation_id,
                    event_id=event_id,
                    seat_id=seat_id,
                    tarif_name=tarif_name
                )

                if not success:
                    QMessageBox.warning(
                        self,
                        "Erreur",
                        f"Impossible d'ajouter le billet pour le siège #{seat_id}."
                    )
                    return

            # Update reservation data with actual total (including supplements)
            self.reservation_data['total'] = self.actual_total_price
            self.reservation_data['selected_seats'] = selected_seat_ids

            if self.is_staff_sell :
                main_win.show_staff_payment_widget(self.reservation_data)
            else :
                main_win.show_payment_widget(self.reservation_data)

        except Exception as e:
            import traceback
            print(f"ERROR in _on_confirm_clicked: {e}")
            print(traceback.format_exc())
            QMessageBox.critical(
                self,
                "Erreur",
                f"Une erreur est survenue lors de la confirmation: {str(e)}"
            )

    def _handle_home(self):
        """home --> drop pending reservation"""

        # Get reservation ID and cancel it
        reservation_id = self.reservation_data.get('reservation_id')
        if reservation_id:
            print(f"Cancelling pending reservation #{reservation_id}")
            cancel_reservation(reservation_id)

        # Get the main window (use window() instead of parent())
        main_win = self.window()

        if main_win:
            # Clear the reservation data in main window
            if hasattr(main_win, 'reservation_data'):
                main_win.reservation_data = None

            # Navigate to home
            if hasattr(main_win, 'show_home_widget'):
                main_win.show_home_widget()


    def _handle_back_to_reservation(self):
        main_win = self.window()

        # Delete the current pending reservation
        reservation_id = self.reservation_data.get('reservation_id')
        if reservation_id:
            print(f"Deleting pending reservation #{reservation_id} (user going back to tarifs)")
            delete_reservation(reservation_id)

            # Clear reservation data from main window
            if main_win and hasattr(main_win, 'reservation_data'):
                main_win.reservation_data = None

        #back to tarifs selection
        if main_win and hasattr(main_win, 'show_reservation_widget'):
            # Get event info from current reservation data
            event_id = self.reservation_data.get('event_id')
            event_name = self.reservation_data.get('event_name', 'Événement')

            if event_id:
                main_win.show_reservation_widget(event_id, event_name)
            else:
                # Fallback: just go to home if we don't have event info
                if hasattr(main_win, 'show_home_widget'):
                    main_win.show_home_widget()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConcertHall(event_id=1, quantity=1, total_price=50)
    window.show()
    sys.exit(app.exec())