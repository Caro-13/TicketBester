from .connection import _get_connection

def get_all_events():
    connection = _get_connection()
    cursor = connection.cursor()

    # cursor.execute() ToDo Faire la requête pour les evenements

    rows = cursor.fetchall()

    # ToDo Traitement des données

    cursor.close()
    connection.close()
    return rows


def get_all_events_with_names():
    conn = _get_connection()
    cur = conn.cursor()

    query = """
            SELECT e."name", t."name", e."date", e."hour"
            FROM "event" e
                     JOIN "typeOfEvent" t ON e."typeId" = t."id"
            ORDER BY e."date" DESC \
            """

    try:
        cur.execute(query)
        rows = cur.fetchall()
    except Exception as e:
        print(f"SQL error: {e}")
        rows = []
    finally:
        cur.close()
        conn.close()

    return rows

def get_tarifs_for_event(event_id):
    pass