import db
from datetime import datetime

def log_arrival(user_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prihodi_odhodi (employeeID, prihod)
        VALUES (%s, %s)
    """, (user_id, datetime.now()))
    cursor.close()
    conn.close()

def log_departure(user_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prihodi_odhodi (employeeID, odhod)
        VALUES (%s, %s)
    """, (user_id, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()