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
            Cena_produkta varchar(255)
        )
    ''')
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

#Po prvem zagonu zakomentiraj def insert_data
def insert_test_data():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (Ime_produkta, Opis_produkta, Cena_produkta) VALUES
        ('Varovalka 100w', 'Description for product 1', '100'),
        ('Varovalka 200w', 'Description for product 2', '150'),
        ('Varovalka 300w', 'Description for product 3', '200'),
        ('Varovalka 400w', 'Description for product 4', '600');
    ''')

    conn.commit()
    cursor.close()
    conn.close()
#--------------------------------------------


def get_products():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return products

