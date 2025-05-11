import os
import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname = os.environ.get('DBNAME', 'delta'),
        user = os.environ.get('DBUSER', 'admin'),
        password = os.environ.get('DBPASS', 'admin'),
        host = os.environ.get('DBHOST', 'localhost'),
        port = os.environ.get('DBPORT', '5432')
    )
    return conn
