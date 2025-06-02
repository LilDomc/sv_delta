import db

def insert_promo_code(koda, vrednost):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO promo_kode (koda, vrednost_kode)
        VALUES (%s, %s)
    ''', (koda, vrednost))
    conn.commit()
    cursor.close()
    conn.close()
    return True