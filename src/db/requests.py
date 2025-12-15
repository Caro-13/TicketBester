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