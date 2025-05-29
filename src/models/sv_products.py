import db

def setup_db():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            productID SERIAL PRIMARY KEY,
            ime_produkta varchar(255),
            opis_produkta varchar(255),
            cena_produkta NUMERIC(10, 2),
            komentar varchar(255),
            stock INT,
            prodano INT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS promo_kode (
            promo_kodeID SERIAL PRIMARY KEY,
            productID INT NOT NULL,
            koda varchar(255),
            vrednost_kode NUMERIC(5, 2) NOT NULL CHECK (vrednost_kode >= 0 AND vrednost_kode <= 100),
            uporaba BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (productID) REFERENCES products(productID)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_products(sort_by="Ime_produkta", order="asc", stock_filter="all"):
    conn = db.get_connection()
    cursor = conn.cursor()
    sort_columns = {
        "name": "Ime_produkta",
        "price": "CAST(Cena_produkta AS INT)",
        "stock": "Stock"
    }
    directions = ["asc", "desc"]

    column = sort_columns.get(sort_by, "Ime_produkta")
    direction = order if order in directions else "asc"
    nulls = "NULLS FIRST" if sort_by == "stock" and order == "asc" else \
            "NULLS LAST" if sort_by == "stock" and order == "desc" else ""

    # Filter pogoj
    where_clause = ""
    if stock_filter == "in_stock":
        where_clause = "WHERE Stock > 0"
    elif stock_filter == "out_of_stock":
        where_clause = "WHERE Stock = 0 OR Stock IS NULL"

    query = f'''
        SELECT productID, Ime_produkta, Opis_produkta, Cena_produkta, Stock
        FROM products
        {where_clause}
        ORDER BY {column} {direction} {nulls};
    '''
    cursor.execute(query)
    products = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return products

def insert_test_data():     #inserta če je tabela prazna
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
            cursor.executemany('''
                INSERT INTO products (Ime_produkta, Opis_produkta, Cena_produkta, Komentar, Stock, Prodano)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', [
                ('Varovalka 100w', 'Description for product 1', '100', 'Zelo dober izdelek!', 3, 4),
                ('Varovalka 200w', 'Description for product 2', '150', 'Solidno', None, 1),
                ('Varovalka 300w', 'Description for product 3', '200', 'Zadovoljen, vendar sem pričakoval več', 1, 5),
                ('Varovalka 400w', 'Description for product 4', '600', 'Dela kot je treba!', 2, 10),
                ('Varovalka 500w', 'Description for product 5', '700', 'Dela kot je treba!', 5, 2),
                ('Varovalka 600w', 'Description for product 6', '800', 'Dela kot je treba!', 10, 3)
            ])

    conn.commit()
    cursor.close()
    conn.close()

def get_product_avg_rate(product_id):
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            "1_star", "2_star", "3_star", "4_star", "5_star"
        FROM rate
        WHERE productID = %s;
    ''', (product_id,))
    row = cursor.fetchone()

    if row:
        one, two, three, four, five = row
        total_votes = one + two + three + four + five
        if total_votes > 0:
            total_score = one*1 + two*2 + three*3 + four*4 + five*5
            avg = round(total_score / total_votes, 2)
        else:
            avg = None

        cursor.execute('''
            UPDATE rate
            SET average_rating = %s
            WHERE productID = %s;
        ''', (avg, product_id))

    conn.commit()
    cursor.close()
    conn.close()

def add_rating(product_id, star_value):
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT rateID FROM rate WHERE productID = %s', (product_id,))
    if cursor.fetchone() is None:
        cursor.execute('''
            INSERT INTO rate (productID, "1_star", "2_star", "3_star", "4_star", "5_star")
            VALUES (%s, 0, 0, 0, 0, 0)
        ''', (product_id,))

    star_column = f'"{star_value}_star"'
    cursor.execute(f'''
        UPDATE rate
        SET {star_column} = {star_column} + 1
        WHERE productID = %s
    ''', (product_id,))

    conn.commit()
    cursor.close()
    conn.close()

    get_product_avg_rate(product_id)

def insert_product(name, description, price, stock):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (Ime_produkta, Opis_produkta, Cena_produkta, Komentar, Stock)
        VALUES (%s, %s, %s, NULL, %s)
    ''', (name, description, price, stock))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_best_selling_products(limit=5):
    conn = db.get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT productID, Ime_produkta, Opis_produkta, Cena_produkta, Stock, Prodano
        FROM products
        ORDER BY Prodano DESC
        LIMIT %s;
    '''
    cursor.execute(query, (limit,))
    products = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    return products


def get_all_products():
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Ime_produkta
        FROM products
        ORDER BY Ime_produkta ASC
    ''')

    products = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    return products

def search_products(query):
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT productID, Ime_produkta, Opis_produkta, Cena_produkta, Stock
        FROM products
        WHERE Ime_produkta ILIKE %s
        ORDER BY Ime_produkta ASC
    ''', (f"%{query}%",))

    products = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    return products 