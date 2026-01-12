"""
Unit tests for database requests module.
Tests all CRUD operations and business logic in src/db/requests.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db import requests


class TestEventRequests(unittest.TestCase):
    """Test event-related database requests"""

    @patch('src.db.requests._get_connection')
    def test_get_all_events_success(self, mock_conn):
        """Test fetching all events successfully"""
        # Setup mock
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, 'Concert de Rock', 'Concert', datetime(2026, 7, 15).date(), datetime(2026, 7, 15, 20, 0).time()),
            (2, 'Exposition', 'Exposition', datetime(2026, 8, 1).date(), datetime(2026, 8, 1, 10, 0).time())
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        # Execute
        result = requests.get_all_events()

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], 'Concert de Rock')
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('src.db.requests._get_connection')
    def test_get_all_events_empty(self, mock_conn):
        """Test fetching events when none exist"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_all_events()

        self.assertEqual(result, [])

    @patch('src.db.requests._get_connection')
    def test_get_all_events_exception(self, mock_conn):
        """Test handling exception when fetching events"""
        mock_conn.side_effect = Exception("Database connection error")

        result = requests.get_all_events()

        self.assertEqual(result, [])

    @patch('src.db.requests._get_connection')
    def test_get_all_events_details_success(self, mock_conn):
        """Test fetching event details by ID"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (
            1, 'Concert de Rock', datetime(2026, 7, 15, 20, 0),
            datetime(2026, 7, 15, 22, 30), 'on_sale', 'Concert',
            False, True, 'ISC Room', 'Rue de l\'Industrie 42'
        )
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_all_events_details(1)

        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Concert de Rock')
        self.assertEqual(result['status'], 'on_sale')
        self.assertTrue(result['need_reservation'])

    @patch('src.db.requests._get_connection')
    def test_get_all_events_details_not_found(self, mock_conn):
        """Test fetching details for non-existent event"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_all_events_details(999)

        self.assertIsNone(result)


class TestTarifRequests(unittest.TestCase):
    """Test tarif-related database requests"""

    @patch('src.db.requests._get_connection')
    def test_get_tarifs_for_event_success(self, mock_conn):
        """Test fetching tarifs for an event"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, 'Normal', 50.00, None, None),
            (2, 'Student', 35.00, None, None),
            (3, 'Staff', 25.00, None, None)
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_tarifs_for_event(1)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['name'], 'Normal')
        self.assertEqual(result[0]['price'], 50.00)
        self.assertEqual(result[1]['name'], 'Student')

    @patch('src.db.requests._get_connection')
    def test_get_tarifs_for_event_free(self, mock_conn):
        """Test fetching tarifs for free event"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (4, 'Normal', 0.00, None, None),
            (5, 'Student', 0.00, None, None)
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_tarifs_for_event(2)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['price'], 0.00)

    @patch('src.db.requests._get_connection')
    def test_get_tarifs_for_event(self, mock_conn):
        """Test fetching tarifs"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, 'Normal', 50.00, None, None),
            (2, 'Student', 35.00, None, None)
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_tarifs_for_event(1)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Normal')
        self.assertEqual(result[0]['price'], 50.00)
        self.assertEqual(result[1]['name'], 'Student')
        self.assertEqual(result[1]['price'], 35.00)


class TestSeatRequests(unittest.TestCase):
    """Test seat-related database requests"""

    @patch('src.db.requests._get_connection')
    def test_get_available_seats_success(self, mock_conn):
        """Test fetching available seats"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, 'S1', 'Standard', 'Standard', 0.00, 'AVAILABLE'),
            (2, 'S2', 'Standard', 'Standard', 0.00, 'AVAILABLE')
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_available_seats_for_event(1)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'S1')
        self.assertEqual(result[0]['status'], 'AVAILABLE')

    @patch('src.db.requests._get_connection')
    def test_get_seats_with_status(self, mock_conn):
        """Test fetching all seats with their status"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, 'S1', 'Standard', 'Standard', 0.00, 'AVAILABLE'),
            (2, 'S2', 'Standard', 'Standard', 0.00, 'SOLD'),
            (3, 'S3', 'Standard', 'Standard', 0.00, 'RESERVED')
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_seats_with_status_for_event(1)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[1]['status'], 'SOLD')
        self.assertEqual(result[2]['status'], 'RESERVED')

    @patch('src.db.requests._get_connection')
    def test_get_sector_supplements(self, mock_conn):
        """Test fetching sector supplements"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ('VIP', 25.00),
            ('Balcon Haut', 15.00)
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_sector_supplements_for_event(1)

        self.assertEqual(len(result), 2)
        self.assertEqual(result['VIP'], 25.00)
        self.assertEqual(result['Balcon Haut'], 15.00)


class TestClientRequests(unittest.TestCase):
    """Test client-related database requests"""

    @patch('src.db.requests._get_connection')
    def test_create_client_new(self, mock_conn):
        """Test creating a new client"""
        mock_cursor = Mock()
        mock_cursor.fetchone.side_effect = [None, (1,)]  # Not exists, then return ID
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.create_client('test@example.com', 'John', 'Doe')

        self.assertEqual(result, 1)
        mock_connection.commit.assert_called_once()

    @patch('src.db.requests._get_connection')
    def test_create_client_existing(self, mock_conn):
        """Test creating client that already exists"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (5,)  # Already exists
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.create_client('existing@example.com', 'Jane', 'Smith')

        self.assertEqual(result, 5)

    @patch('src.db.requests._get_connection')
    def test_create_client_exception(self, mock_conn):
        """Test handling exception when creating client"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.execute.side_effect = Exception("Database error")
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.create_client('error@example.com', 'Error', 'Test')

        self.assertIsNone(result)
        mock_connection.rollback.assert_called_once()


class TestReservationRequests(unittest.TestCase):
    """Test reservation-related database requests"""

    @patch('src.db.requests._get_connection')
    def test_create_reservation_success(self, mock_conn):
        """Test creating a reservation"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (10,)
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.create_reservation(1, 5, 1)

        self.assertEqual(result, 10)
        mock_connection.commit.assert_called_once()

    @patch('src.db.requests._get_connection')
    def test_create_reservation_staff_vendor(self, mock_conn):
        """Test creating reservation with staff vendor"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (15,)
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.create_reservation(1, None, 2)

        self.assertEqual(result, 15)

    @patch('src.db.requests._get_connection')
    def test_cancel_reservation_success(self, mock_conn):
        """Test cancelling a reservation"""
        mock_cursor = Mock()
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.cancel_reservation(10)

        self.assertTrue(result)
        mock_connection.commit.assert_called_once()

    @patch('src.db.requests._get_connection')
    def test_delete_reservation_success(self, mock_conn):
        """Test deleting a reservation"""
        mock_cursor = Mock()
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.delete_reservation(10)

        self.assertTrue(result)
        self.assertEqual(mock_cursor.execute.call_count, 2)  # Delete tickets + reservation
        mock_connection.commit.assert_called_once()

    @patch('src.db.requests._get_connection')
    def test_get_need_reservation_for_event(self, mock_conn):
        """Test checking if event needs reservation"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (True,)
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_need_reservation_for_event(1)

        self.assertTrue(result)

    @patch('src.db.requests._get_connection')
    def test_get_need_reservation_default(self, mock_conn):
        """Test default value when event not found"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_need_reservation_for_event(999)

        self.assertTrue(result)  # Default to True


class TestTicketRequests(unittest.TestCase):
    """Test ticket-related database requests"""

    @patch('src.db.requests._get_connection')
    def test_add_ticket_success(self, mock_conn):
        """Test adding a ticket to reservation"""
        mock_cursor = Mock()
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.add_ticket_to_reservation(10, 1, 5, 'Normal')

        self.assertTrue(result)
        mock_connection.commit.assert_called_once()

    @patch('src.db.requests._get_connection')
    def test_add_ticket_exception(self, mock_conn):
        """Test handling exception when adding ticket"""
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("Seat already booked")
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.add_ticket_to_reservation(10, 1, 5, 'Normal')

        self.assertFalse(result)
        mock_connection.rollback.assert_called_once()

    @patch('src.db.requests._get_connection')
    def test_scan_ticket_success(self, mock_conn):
        """Test scanning a valid ticket"""
        mock_cursor = Mock()
        mock_cursor.fetchone.side_effect = [(1, 'paid'), None]  # Ticket exists and paid, not scanned
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.scan_ticket(1, 2, 'A')

        self.assertTrue(result['success'])
        self.assertIn('validé', result['message'])

    @patch('src.db.requests._get_connection')
    def test_scan_ticket_invalid(self, mock_conn):
        """Test scanning invalid ticket"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.scan_ticket(999, 2, 'A')

        self.assertFalse(result['success'])
        self.assertIn('invalide', result['message'])

    @patch('src.db.requests._get_connection')
    def test_scan_ticket_not_paid(self, mock_conn):
        """Test scanning unpaid ticket"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, 'pending')
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.scan_ticket(1, 2, 'A')

        self.assertFalse(result['success'])
        self.assertIn('non payé', result['message'])

    @patch('src.db.requests._get_connection')
    def test_scan_ticket_already_scanned(self, mock_conn):
        """Test scanning already scanned ticket"""
        mock_cursor = Mock()
        mock_cursor.fetchone.side_effect = [(1, 'paid'), (1,)]  # Exists and already scanned
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.scan_ticket(1, 2, 'A')

        self.assertFalse(result['success'])
        self.assertIn('déjà scanné', result['message'])


class TestPaymentRequests(unittest.TestCase):
    """Test payment-related database requests"""

    @patch('src.db.requests._get_connection')
    def test_create_payment_success(self, mock_conn):
        """Test creating a payment"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.create_payment(10, 100.50, 'card')

        self.assertEqual(result, 1)
        mock_connection.commit.assert_called_once()

    @patch('src.db.requests._get_connection')
    def test_create_payment_cash(self, mock_conn):
        """Test creating cash payment"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (2,)
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.create_payment(11, 50.00, 'cash')

        self.assertEqual(result, 2)

    @patch('src.db.requests._get_connection')
    def test_create_payment_twint(self, mock_conn):
        """Test creating Twint payment"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (3,)
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.create_payment(12, 75.00, 'twint')

        self.assertEqual(result, 3)


class TestAdminRequests(unittest.TestCase):
    """Test admin-related database requests"""

    @patch('src.db.requests._get_connection')
    def test_get_all_rooms_names(self, mock_conn):
        """Test fetching all room names"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [('ISC Room',), ('Main Hall',)]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_all_rooms_names()

        self.assertEqual(len(result), 2)
        self.assertIn('ISC Room', result)

    @patch('src.db.requests._get_connection')
    def test_get_all_config_names(self, mock_conn):
        """Test fetching all configuration names"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [('Main Floor',), ('Balcony',), ('Full Room',)]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_all_config_names()

        self.assertEqual(len(result), 3)
        self.assertIn('Full Room', result)

    @patch('src.db.requests._get_connection')
    def test_get_type_id(self, mock_conn):
        """Test getting type ID by name"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [(1,)]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_type_id('Concert')

        self.assertEqual(result, 1)

    @patch('src.db.requests._get_connection')
    def test_get_room_id(self, mock_conn):
        """Test getting room ID by name"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [(1,)]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_room_id('ISC Room')

        self.assertEqual(result, 1)

    @patch('src.db.requests._get_connection')
    def test_get_config_id(self, mock_conn):
        """Test getting configuration ID by name"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [(3,)]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_config_id('Full Room')

        self.assertEqual(result, 3)

    @patch('src.db.requests._get_connection')
    def test_create_event_success(self, mock_conn):
        """Test creating a new event"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (6,)
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        tarifs = [
            {'name': 'Normal', 'price': 50.00},
            {'name': 'Student', 'price': 35.00}
        ]

        result = requests.create_event(
            'New Event', 1,
            datetime(2026, 12, 1, 20, 0),
            datetime(2026, 12, 1, 22, 0),
            1, 1, tarifs
        )

        self.assertEqual(result, 6)
        self.assertEqual(mock_cursor.execute.call_count, 3)  # Event + 2 tarifs
        mock_connection.commit.assert_called_once()

    @patch('src.db.requests._get_connection')
    def test_get_type_of_event_details(self, mock_conn):
        """Test getting event type details"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, 'Concert', False, True)
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.get_type_of_event_details('Concert')

        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Concert')
        self.assertFalse(result['is_free'])
        self.assertTrue(result['need_reservation'])

    @patch('src.db.requests._get_connection')
    def test_add_staff_member(self, mock_conn):
        """Test adding a staff member"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (4,)
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection

        result = requests.add_staff_member('John Staff')

        self.assertEqual(result, 4)
        mock_connection.commit.assert_called_once()

    @patch('src.db.requests._get_connection')
    def test_get_all_staff(self, mock_conn):
        """Test getting all staff members"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (2, 'Delta'),
            (3, 'Echo')
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_all_staff()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], 'Delta')

    @patch('src.db.requests._get_connection')
    def test_get_event_statistics(self, mock_conn):
        """Test getting event statistics"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, 'Concert', datetime(2026, 7, 15, 20, 0), 'on_sale', 50, 30, 100)
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_event_statistics()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['tickets_sold'], 50)
        self.assertEqual(result[0]['tickets_scanned'], 30)
        self.assertEqual(result[0]['total_seats'], 100)

    @patch('src.db.requests._get_connection')
    def test_get_all_type_of_event_names(self, mock_conn):
        """Test getting all event type names"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ('Concert',), ('Exposition',), ('Festival',)
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = requests.get_all_type_of_event_names()

        self.assertEqual(len(result), 3)
        self.assertIn('Concert', result)
        self.assertIn('Festival', result)


if __name__ == '__main__':
    unittest.main(verbosity=2)