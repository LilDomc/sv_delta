import db

class User:
    def __init__(self, name):
        self.name = name
        self.save() # TODO Po mojem mnenju je to slab design, boljše bi bilo da se save kliče posebej, da je koda bolj berljiva ...

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
            userID SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS products (
            productID SERIAL PRIMARY KEY,
            Ime_produkta varchar(255),
            Opis_produkta varchar(255),
            Cena_produkta varchar(255),
            Komentar varchar(255),
            Stock INT
        );
        CREATE TABLE IF NOT EXISTS rate (
            rateID SERIAL PRIMARY KEY,
            productID INT NOT NULL,
            "5_star" INT,
            "4_star" INT,
            "3_star" INT,
            "2_star" INT,
            "1_star" INT,
            average_rating DECIMAL(3,2),
            FOREIGN KEY (productID) REFERENCES products(productID)
        );
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
                    INSERT INTO products (productID, Ime_produkta, Opis_produkta, Cena_produkta, Komentar, Stock) VALUES
                    (1, 'Varovalka 100w', 'Description for product 1', '100', 'Zelo dober izdelek!', '3'),
                    (2, 'Varovalka 200w', 'Description for product 2', '150', 'Solidno', NULL),
                    (3, 'Varovalka 300w', 'Description for product 3', '200', 'Zadovoljen, vendar sem pričakoval več', '1'),
                    (4, 'Varovalka 400w', 'Description for product 4', '600', 'Dela kot je treba!', '2'),
                    (5, 'Varovalka 500w', 'Description for product 5', '700', 'Dela kot je treba!', '5'),
                    (6, 'Varovalka 600w', 'Description for product 6', '800', 'Dela kot je treba!', '10');
                END IF;
            END;
            $$;''')

    conn.commit()
    cursor.close()
    conn.close()

def get_products():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT productID, Ime_produkta, Opis_produkta, Cena_produkta, Stock FROM products')
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
