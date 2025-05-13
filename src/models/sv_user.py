import db

class User:

    def __init__(self, name):
        self.name = name
        self.save()

    def save(self):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name) VALUES (%s)', (self.name,))
        conn.commit()
        cursor.close()
        conn.close()


def setup_db():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            Ime_produkta varchar(255),
            Opis_produkta varchar(255),
            Cena_produkta varchar(255),
            Ocena_izdelka varchar(255),
            Komentar varchar(255),
            Stock INT
        )
    ''')                                #Ocena izdelka, ko bo input ustvarjen spremeni Ocena_izdelka, v avg rate of specific product
    conn.commit()
    cursor.close()
    conn.close()
    return True

def reset_db():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE users')
    conn.commit()
    cursor.close()
    conn.close()

def get_users():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def insert_test_data():     #inserta če je tabela prazna
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''
            DO
            $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM products LIMIT 1) THEN
                    INSERT INTO products (id, Ime_produkta, Opis_produkta, Cena_produkta, Ocena_izdelka, Komentar, Stock) VALUES
                    (1, 'Varovalka 100w', 'Description for product 1', '100', '5', 'Zelo dober izdelek!', '3'),
                    (2, 'Varovalka 200w', 'Description for product 2', '150', '4', 'Solidno', NULL),
                    (3, 'Varovalka 300w', 'Description for product 3', '200', '3', 'Zadovoljen, vendar sem pričakoval več', '1'),
                    (4, 'Varovalka 400w', 'Description for product 4', '600', '5', 'Dela kot je treba!', '2'),
                    (5, 'Varovalka 500w', 'Description for product 5', '700', '5', 'Dela kot je treba!', '5'),
                    (6, 'Varovalka 600w', 'Description for product 6', '800', '5', 'Dela kot je treba!', '10');
                END IF;
            END;
            $$;''')

    conn.commit()
    cursor.close()
    conn.close()

def get_products():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, Ime_produkta, Opis_produkta, Cena_produkta, Stock FROM products')
    products = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return products

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
