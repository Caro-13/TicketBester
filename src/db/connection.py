# Connect to db

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Accessible uniquement depuis requests.py
def _get_connection():
    return psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
