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

def get_sector_supplements_for_event(event_id):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
            SELECT DISTINCT sec.name       as sector_name, \
                            sec.supplement as sector_supplement
            FROM event_seat es
                     JOIN seat s ON es.seat_id = s.id
                     JOIN sector sec ON s.sector_id = sec.id
            WHERE es.event_id = %s
              AND sec.supplement IS NOT NULL
              AND sec.supplement > 0
            ORDER BY sec.name
        """

        cursor.execute(query, (event_id,))
        rows = cursor.fetchall()

        supplements = {}
        for row in rows:
            sector_name = row[0]
            supplement = float(row[1]) if row[1] else 0.0
            if supplement > 0:
                supplements[sector_name] = supplement

        cursor.close()
        return supplements

    except Exception as e:
        print(f"Error fetching sector supplements: {e}")
        return {}
    finally:
        if connection:
            connection.close()


""" Admin functions"""
#event
def get_all_rooms_names():
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
                SELECT  r.name 
                FROM room r
                ORDER BY name
                """
        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        return [row[0] for row in rows]
    except Exception as e:
        print(f"Error fetching room names: {e}")
        return []
    finally:
        if connection:
            connection.close()

def get_all_config_names():
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
                SELECT c.name
                FROM configuration c
                ORDER BY name \
                """
        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        return [row[0] for row in rows]
    except Exception as e:
        print(f"Error fetching room names: {e}")
        return []
    finally:
        if connection:
            connection.close()

def get_type_id(type_name):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
                SELECT toe.id
                FROM type_of_event toe
                WHERE toe.name = %s\
                """
        cursor.execute(query,(type_name,))
        rows = cursor.fetchall()

        cursor.close()
        return rows[0][0]
    except Exception as e:
        print(f"Error fetching type id: {e}")
        return []
    finally:
        if connection:
            connection.close()

def get_room_id(room_name):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
                SELECT r.id
                FROM room r
                WHERE r.name = %s\
                """
        cursor.execute(query,(room_name,))
        rows = cursor.fetchall()

        cursor.close()
        return rows[0][0]
    except Exception as e:
        print(f"Error fetching room id: {e}")
        return []
    finally:
        if connection:
            connection.close()

def get_config_id(config_name):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
                SELECT c.id
                FROM configuration c
                WHERE c.name = %s\
                """
        cursor.execute(query,(config_name,))
        rows = cursor.fetchall()

        cursor.close()
        return rows[0][0]
    except Exception as e:
        print(f"Error fetching configuration id: {e}")
        return []
    finally:
        if connection:
            connection.close()

def create_event(name, type_id, start_at, end_at, room_id, config_id, status='on_sale'):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
                INSERT INTO event (type_id, name, start_at, end_at, room_id, config_id, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id \
                """
        cursor.execute(query, (type_id, name, start_at, end_at, room_id, config_id, status))
        event_id = cursor.fetchone()[0]
        connection.commit()

        cursor.close()
        return event_id
    except Exception as e:
        print(f"Error creating event: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        if connection:
            connection.close()

#staff
def add_staff_member(name):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = "INSERT INTO staff (name) VALUES (%s) RETURNING id"
        cursor.execute(query, (name,))
        staff_id = cursor.fetchone()[0]
        connection.commit()

        cursor.close()
        return staff_id
    except Exception as e:
        print(f"Error adding staff: {e}")
        if connection:
            connection.rollback()
        return None
    finally:
        if connection:
            connection.close()

#stats
def get_event_statistics():
    """Get statistics for all events."""
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
                SELECT e.id, \
                       e.name, \
                       e.start_at, \
                       e.status, \
                       COUNT(DISTINCT t.id)       as tickets_sold, \
                       COUNT(DISTINCT st.id)      as tickets_scanned, \
                       COUNT(DISTINCT es.seat_id) as total_seats
                FROM event e
                         LEFT JOIN ticket t ON e.id = t.event_id
                         LEFT JOIN scan_ticket st ON t.id = st.ticket_id
                         LEFT JOIN event_seat es ON e.id = es.event_id
                GROUP BY e.id, e.name, e.start_at, e.status
                ORDER BY e.start_at DESC \
                """

        cursor.execute(query)
        rows = cursor.fetchall()

        stats = []
        for row in rows:
            stats.append({
                'id': row[0],
                'name': row[1],
                'start_at': row[2],
                'status': row[3],
                'tickets_sold': row[4],
                'tickets_scanned': row[5],
                'total_seats': row[6]
            })

        cursor.close()
        return stats
    except Exception as e:
        print(f"Error fetching statistics: {e}")
        return []
    finally:
        if connection:
            connection.close()

def get_all_type_of_event_names():
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = """
                SELECT te.name
                FROM type_of_event te
                """

        cursor.execute(query)
        rows = cursor.fetchall()

        type_of_events = []
        for row in rows:
            type_of_events.append(row[0])

        cursor.close()
        return type_of_events
    except Exception as e:
        print(f"Error getting all type_of_events names: {e}")
        return []
    finally:
        if connection:
            connection.close()

# Staff functions
def get_all_staff():
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        query = "SELECT id, name FROM staff WHERE id != 1 ORDER BY name"
        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        return rows
    except Exception as e:
        print(f"Error fetching staff: {e}")
        return []
    finally:
        if connection:
            connection.close()

def scan_ticket(ticket_id, staff_id, door):
    connection = None
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        # Check if ticket exists and is valid
        check_query = """
                      SELECT t.id, r.status
                      FROM ticket t
                               JOIN reservation r ON t.reservation_id = r.id
                      WHERE t.id = %s \
                      """
        cursor.execute(check_query, (ticket_id,))
        result = cursor.fetchone()

        if not result:
            return {"success": False, "message": "Billet invalide"}

        if result[1] != 'paid':
            return {"success": False, "message": "Billet non payé"}

        # Check if already scanned
        scan_check = "SELECT id FROM scan_ticket WHERE ticket_id = %s"
        cursor.execute(scan_check, (ticket_id,))
        if cursor.fetchone():
            return {"success": False, "message": "Billet déjà scanné"}

        # Record scan
        insert_query = """
                       INSERT INTO scan_ticket (staff_id, door, ticket_id)
                       VALUES (%s, %s, %s) \
                       """
        cursor.execute(insert_query, (staff_id, door, ticket_id))
        connection.commit()

        cursor.close()
        return {"success": True, "message": f"Billet #{ticket_id} validé"}
    except Exception as e:
        print(f"Error scanning ticket: {e}")
        if connection:
            connection.rollback()
        return {"success": False, "message": "Erreur système"}
    finally:
        if connection:
            connection.close()