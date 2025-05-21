import db

def get_trgovina(sort_by="name", order="asc"):
    conn = db.get_connection()
    cursor = conn.cursor()

    sort_columns = {
        "name": "Ime_produkta",
        "price": "CAST(Cena_produkta AS INT)"
    }
    directions = ["asc", "desc"]

    column = sort_columns.get(sort_by, "Ime_produkta")
    direction = order if order in directions else "asc"

    query = f'''
        SELECT productID, Ime_produkta, Opis_produkta, Cena_produkta
        FROM products
        ORDER BY {column} {direction};
    '''
    cursor.execute(query)
    products = cursor.fetchall()
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