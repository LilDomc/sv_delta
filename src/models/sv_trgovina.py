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