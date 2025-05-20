import db

def get_trgovina():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT productID, Ime_produkta, Opis_produkta, Cena_produkta
        FROM products;
        ''')
    products = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return products

def get_rate(product_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT average_rating 
        FROM rate
        WHERE productID = %s;
    ''', (product_id,))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if result and result[0] is not None:
        return result[0]
    else:
        return None