from .connection import _get_connection

def get_all_events():
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()
        
        query = """
            SELECT 
                e.id,
                e.name,
                t.name as type_name,
                e.start_at::date,
                e.start_at::time
            FROM event e
            JOIN type_of_event t ON e.type_id = t.id
            WHERE e.status = 'on_sale' or e.status = 'on_site' 
              AND e.start_at > NOW()
            ORDER BY e.start_at ASC
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        cursor.close()
        return rows
        
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []
    finally:
        if connection:
            connection.close()

def get_all_events_details(event_id):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()
        
        query = """
            SELECT 
                e.id,
                e.name,
                e.start_at,
                e.end_at,
                e.status,
                t.name as type_name,
                t.is_free,
                t.need_reservation,
                r.name as room_name,
                r.address as room_address
            FROM event e
            JOIN type_of_event t ON e.type_id = t.id
            JOIN room r ON e.room_id = r.id
            WHERE e.id = %s
        """
        
        cursor.execute(query, (event_id,))
        row = cursor.fetchone()
        
        if row:
            result = {
                'id': row[0],
                'name': row[1],
                'start_at': row[2],
                'end_at': row[3],
                'status': row[4],
                'type_name': row[5],
                'is_free': row[6],
                'need_reservation': row[7],
                'room_name': row[8],
                'room_address': row[9]
            }
        else:
            result = None
            
        cursor.close()
        return result
        
    except Exception as e:
        print(f"Error fetching event details: {e}")
        return None
    finally:
        if connection:
            connection.close()

def get_tarifs_for_event(event_id):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()
        
        query = """
            SELECT 
                t.id,
                t.name,
                t.price,
                d.value as discount_percent,
                d.code as discount_code
            FROM tarif t
            LEFT JOIN discount d ON t.discount_id = d.id
            WHERE t.event_id = %s
            ORDER BY t.price DESC
        """
        
        cursor.execute(query, (event_id,))
        rows = cursor.fetchall()
        
        tarifs = []
        for row in rows:
            tarif = {
                'id': row[0],
                'name': row[1],
                'price': float(row[2]) if row[2] else 0.0,
                'discount_percent': row[3] if row[3] else 0,
                'discount_code': row[4] if row[4] else None
            }
            tarifs.append(tarif)
        
        cursor.close()
        return tarifs
        
    except Exception as e:
        print(f"Error fetching tarifs: {e}")
        return []
    finally:
        if connection:
            connection.close()

def get_available_seats_for_event(event_id):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()
        
        query = """
            SELECT 
                s.id,
                s.name,
                ts.type as seat_type,
                sec.name as sector_name,
                sec.supplement as sector_supplement,
                es.status
            FROM event_seat es
            JOIN seat s ON es.seat_id = s.id
            JOIN type_of_seat ts ON s.type_id = ts.id
            JOIN sector sec ON s.sector_id = sec.id
            WHERE es.event_id = %s
              AND es.status = 'AVAILABLE'
            ORDER BY sec.name, s.name
        """
        
        cursor.execute(query, (event_id,))
        rows = cursor.fetchall()
        
        seats = []
        for row in rows:
            seat = {
                'id': row[0],
                'name': row[1],
                'type': row[2],
                'sector': row[3],
                'supplement': float(row[4]) if row[4] else 0.0,
                'status': row[5]
            }
            seats.append(seat)
        
        cursor.close()
        return seats
        
    except Exception as e:
        print(f"Error fetching available seats: {e}")
        return []
    finally:
        if connection:
            connection.close()

def get_seats_with_status_for_event(event_id):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
                SELECT s.id, \
                       s.name, \
                       ts.type        as seat_type, \
                       sec.name       as sector_name, \
                       sec.supplement as sector_supplement, \
                       es.status, \
                       es.hold_expires_at
                FROM event_seat es
                         JOIN seat s ON es.seat_id = s.id
                         JOIN type_of_seat ts ON s.type_id = ts.id
                         JOIN sector sec ON s.sector_id = sec.id
                WHERE es.event_id = %s
                ORDER BY sec.name, s.name \
                """

        cursor.execute(query, (event_id,))
        rows = cursor.fetchall()

        seats = []
        for row in rows:
            seat = {
                'id': row[0],
                'name': row[1],
                'type': row[2],
                'sector': row[3],
                'supplement': float(row[4]) if row[4] else 0.0,
                'status': row[5],
                'hold_expires_at': row[6]
            }
            seats.append(seat)

        cursor.close()
        return seats

    except Exception as e:
        print(f"Error fetching seats with status: {e}")
        return []
    finally:
        if connection:
            connection.close()

def create_client(email, firstname, lastname):
    """
    Create a new client or return existing client ID.
    Returns client_id or None on error.
    """
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()
        
        # Check if client exists
        check_query = "SELECT id FROM client WHERE mail = %s"
        cursor.execute(check_query, (email,))
        existing = cursor.fetchone()
        
        if existing:
            client_id = existing[0]
        else:
            # Create new client
            insert_query = """
                INSERT INTO client (mail, firstname, lastname)
                VALUES (%s, %s, %s)
                RETURNING id
            """
            cursor.execute(insert_query, (email, firstname, lastname))
            client_id = cursor.fetchone()[0]
            connection.commit()
        
        cursor.close()
        return client_id
        
    except Exception as e:
        print(f"Error creating client: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        if connection:
            connection.close()

def create_reservation(event_id, client_id, vendor_id=1):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()
        
        query = """
            INSERT INTO reservation (event_id, vendor, client_id, status)
            VALUES (%s, %s, %s, 'pending')
            RETURNING id
        """
        
        cursor.execute(query, (event_id, vendor_id, client_id))
        reservation_id = cursor.fetchone()[0]
        connection.commit()
        
        cursor.close()
        return reservation_id
        
    except Exception as e:
        print(f"Error creating reservation: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        if connection:
            connection.close()

def add_ticket_to_reservation(reservation_id, event_id, seat_id, tarif_name):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()
        
        # Insert ticket
        ticket_query = """
            INSERT INTO ticket (reservation_id, event_id, seat_id, tarif_name)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        cursor.execute(ticket_query, (reservation_id, event_id, seat_id, tarif_name))
        
        # Update seat status to HOLD
        seat_query = """
            UPDATE event_seat
            SET status = 'HOLD',
                hold_expires_at = NOW() + INTERVAL '15 minutes'
            WHERE event_id = %s AND seat_id = %s
        """
        cursor.execute(seat_query, (event_id, seat_id))
        
        connection.commit()
        cursor.close()
        return True
        
    except Exception as e:
        print(f"Error adding ticket: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            connection.close()

def create_payment(reservation_id, total, method='card'):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
                INSERT INTO payment (reservation_id, total, method)
                VALUES (%s, %s, %s)
                RETURNING id \
                """

        cursor.execute(query, (reservation_id, total, method))
        payment_id = cursor.fetchone()[0]
        connection.commit()

        cursor.close()
        return payment_id

    except Exception as e:
        print(f"Error creating payment: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        if connection:
            connection.close()


