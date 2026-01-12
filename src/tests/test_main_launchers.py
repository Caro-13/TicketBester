"""
Unit tests for main launcher files.
Tests the main application launchers and their initialization.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, MENU_BTN_WIDTH, MENU_BTN_HEIGHT,SEAT_WIDTH, SEAT_HEIGHT, SEAT_LARGE_WIDTH,MAIN_MARGIN, SECTION_SPACING, BUTTON_SPACING

# Create QApplication instance for testing
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)


def mock_loadui_side_effect(ui_file, widget):
    """Mock loadUi to set up basic UI structure"""
    # Create a central widget with layout
    widget.centralwidget = QWidget()
    widget.centralwidget.setLayout(QVBoxLayout())
    return None


class TestTicketBesterMain(unittest.TestCase):
    """Test main.py launcher"""

    @patch('src.qt.home_widget.HomeWidget')
    @patch('src.main.loadUi')
    def test_main_window_initialization(self, mock_loadui, mock_home_widget):
        """Test main window initializes correctly"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main import TicketBester
        window = TicketBester()

        self.assertIsNotNone(window)
        self.assertEqual(window.windowTitle(), "TicketBester")

    @patch('src.qt.home_widget.HomeWidget')
    @patch('src.main.loadUi')
    def test_clear_central_widget(self, mock_loadui, mock_home_widget):
        """Test clearing central widget"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main import TicketBester
        window = TicketBester()
        mock_widget = Mock()
        window.current_widget = mock_widget

        window.clear_central_widget()

        self.assertIsNone(window.current_widget)

    @patch('src.qt.home_widget.HomeWidget')
    @patch('src.main.loadUi')
    def test_set_staff_info(self, mock_loadui, mock_home_widget):
        """Test setting staff information"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main import TicketBester
        window = TicketBester()
        window.set_staff_info(5, "Test Staff")

        self.assertEqual(window.staff_id, 5)
        self.assertEqual(window.staff_name, "Test Staff")

    @patch('src.qt.home_widget.HomeWidget')
    @patch('src.main.loadUi')
    def test_show_home_widget(self, mock_loadui, mock_home_widget):
        """Test showing home widget"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main import TicketBester
        window = TicketBester()
        # It's already shown in __init__, so just verify
        self.assertIsNotNone(window.current_widget)

    @patch('src.qt.admin_home_widget.AdminHomeWidget')
    @patch('src.qt.home_widget.HomeWidget')
    @patch('src.main.loadUi')
    def test_show_admin_home_widget(self, mock_loadui, mock_home_widget, mock_admin_widget):
        """Test showing admin home widget"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main import TicketBester
        window = TicketBester()
        window.show_admin_home_widget()

        self.assertIsNotNone(window.current_widget)
        self.assertEqual(window.windowTitle(), "TicketBester - Administration")

    @patch('src.qt.staff_home_widget.StaffHomeWidget')
    @patch('src.qt.home_widget.HomeWidget')
    @patch('src.main.loadUi')
    def test_show_staff_home_widget(self, mock_loadui, mock_home_widget, mock_staff_widget):
        """Test showing staff home widget"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main import TicketBester
        window = TicketBester()
        window.show_staff_home_widget()

        self.assertIsNotNone(window.current_widget)
        self.assertEqual(window.windowTitle(), "TicketBester - Personnel")


class TestTicketBesterClient(unittest.TestCase):
    """Test main_client.py launcher"""

    @patch('src.qt.home_widget.HomeWidget')
    @patch('src.main_client.loadUi')
    def test_client_window_initialization(self, mock_loadui, mock_home_widget):
        """Test client window initializes correctly"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main_client import TicketBester
        window = TicketBester()

        self.assertIsNotNone(window)
        self.assertEqual(window.windowTitle(), "TicketBester")

    @patch('src.qt.reservation_widget.ReservationWidget')
    @patch('src.qt.home_widget.HomeWidget')
    @patch('src.main_client.loadUi')
    def test_show_reservation_widget(self, mock_loadui, mock_home_widget, mock_reservation_widget):
        """Test showing reservation widget in client mode"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main_client import TicketBester
        window = TicketBester()
        window.show_reservation_widget(1, "Test Event")

        self.assertIsNotNone(window.current_widget)
        self.assertEqual(window.windowTitle(), "TicketBester - Réservation #1")


class TestTicketBesterAdmin(unittest.TestCase):
    """Test main_admin.py launcher"""

    @patch('src.qt.admin_home_widget.AdminHomeWidget')
    @patch('src.main_admin.loadUi')
    def test_admin_window_initialization(self, mock_loadui, mock_admin_widget):
        """Test admin window initializes correctly"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main_admin import TicketBesterAdmin
        window = TicketBesterAdmin()

        self.assertIsNotNone(window)
        self.assertEqual(window.windowTitle(), "TicketBester - Administration")

    @patch('src.qt.admin_new_event_widget.AdminNewEventWidget')
    @patch('src.qt.admin_home_widget.AdminHomeWidget')
    @patch('src.main_admin.loadUi')
    def test_show_admin_new_event_widget(self, mock_loadui, mock_admin_widget, mock_new_event_widget):
        """Test showing new event widget"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main_admin import TicketBesterAdmin
        window = TicketBesterAdmin()
        window.show_admin_new_event_widget()

        self.assertIsNotNone(window.current_widget)
        self.assertEqual(window.windowTitle(), "TicketBester - Nouvel événement")

    @patch('src.qt.admin_new_staff_widget.AdminNewStaffWidget')
    @patch('src.qt.admin_home_widget.AdminHomeWidget')
    @patch('src.main_admin.loadUi')
    def test_show_admin_new_staff_widget(self, mock_loadui, mock_admin_widget, mock_new_staff_widget):
        """Test showing new staff widget"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main_admin import TicketBesterAdmin
        window = TicketBesterAdmin()
        window.show_admin_new_staff_widget()

        self.assertIsNotNone(window.current_widget)
        self.assertEqual(window.windowTitle(), "TicketBester - Nouveau personnel")


class TestTicketBesterStaff(unittest.TestCase):
    """Test main_staff.py launcher"""

    @patch('src.qt.staff_home_widget.StaffHomeWidget')
    @patch('src.main_staff.loadUi')
    def test_staff_window_initialization(self, mock_loadui, mock_staff_widget):
        """Test staff window initializes correctly"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main_staff import TicketBesterStaff
        window = TicketBesterStaff()

        self.assertIsNotNone(window)
        self.assertEqual(window.windowTitle(), "TicketBester - Personnel")
        self.assertIsNone(window.staff_id)
        self.assertIsNone(window.staff_name)

    @patch('src.qt.staff_home_widget.StaffHomeWidget')
    @patch('src.main_staff.loadUi')
    def test_set_staff_info(self, mock_loadui, mock_staff_widget):
        """Test setting staff info in staff mode"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main_staff import TicketBesterStaff
        window = TicketBesterStaff()
        window.set_staff_info(3, "Staff Member")

        self.assertEqual(window.staff_id, 3)
        self.assertEqual(window.staff_name, "Staff Member")

    @patch('src.qt.staff_sell_widget.StaffSellWidget')
    @patch('src.qt.staff_home_widget.StaffHomeWidget')
    @patch('src.main_staff.loadUi')
    def test_show_staff_sell_widget(self, mock_loadui, mock_staff_widget, mock_sell_widget):
        """Test showing staff sell widget"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main_staff import TicketBesterStaff
        window = TicketBesterStaff()
        window.show_staff_sell_widget()

        self.assertIsNotNone(window.current_widget)
        self.assertEqual(window.windowTitle(), "TicketBester - Vente de billets")

    @patch('src.qt.staff_scan_widget.StaffScanWidget')
    @patch('src.qt.staff_home_widget.StaffHomeWidget')
    @patch('src.main_staff.loadUi')
    def test_show_staff_scan_widget(self, mock_loadui, mock_staff_widget, mock_scan_widget):
        """Test showing staff scan widget"""
        mock_loadui.side_effect = mock_loadui_side_effect

        from src.main_staff import TicketBesterStaff
        window = TicketBesterStaff()
        window.show_staff_scan_widget()

        self.assertIsNotNone(window.current_widget)
        self.assertEqual(window.windowTitle(), "TicketBester - Scanner les billets")


class TestConstants(unittest.TestCase):
    """Test constants.py values"""

    def test_window_dimensions(self):
        """Test window size constants"""
        self.assertEqual(WINDOW_WIDTH, 1200)
        self.assertEqual(WINDOW_HEIGHT, 620)
        self.assertIsInstance(WINDOW_WIDTH, int)
        self.assertIsInstance(WINDOW_HEIGHT, int)

    def test_button_dimensions(self):
        """Test button size constants"""
        self.assertEqual(MENU_BTN_WIDTH, 280)
        self.assertEqual(MENU_BTN_HEIGHT, 250)
        self.assertGreater(MENU_BTN_WIDTH, 0)
        self.assertGreater(MENU_BTN_HEIGHT, 0)

    def test_seat_dimensions(self):
        """Test seat size constants"""
        self.assertEqual(SEAT_WIDTH, 35)
        self.assertEqual(SEAT_HEIGHT, 28)
        self.assertEqual(SEAT_LARGE_WIDTH, 55)
        self.assertGreater(SEAT_LARGE_WIDTH, SEAT_WIDTH)

    def test_spacing_constants(self):
        """Test spacing constants"""
        self.assertEqual(MAIN_MARGIN, 50)
        self.assertEqual(SECTION_SPACING, 30)
        self.assertEqual(BUTTON_SPACING, 30)


if __name__ == '__main__':
    unittest.main(verbosity=2)