import db

def get_trgovina():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Ime_produkta, Opis_produkta, Cena_produkta
        FROM products;
        ''')
    products = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return products