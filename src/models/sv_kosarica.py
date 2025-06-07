import db

def setup_db():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kosarica (
            kosaricaID SERIAL PRIMARY KEY,
            productID INT NOT NULL,
            userID INT NOT NULL,
            ime_produkta varchar(255),
            cena_produkta varchar(255),
            stock INT NOT NULL DEFAULT 1,
            FOREIGN KEY (productID) REFERENCES products(productID),
            FOREIGN KEY (userID) REFERENCES users(userID)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS narocila (
            narociloID SERIAL PRIMARY KEY,
            productID INT NOT NULL,
            userID INT NOT NULL,
            u_ime varchar(255),
            u_priimek varchar(255),
            kolicina INT NOT NULL,
            p_cena_produkta DECIMAL(10, 2),
            p_opis_produkta varchar(255),
            datum_narocila DATE NOT NULL DEFAULT CURRENT_DATE,
            status_narocila varchar,
            FOREIGN KEY (productID) REFERENCES products(productID),
            FOREIGN KEY (userID) REFERENCES users(userID)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wishlist (
            wishlistID SERIAL PRIMARY KEY,
            userID INT NOT NULL,
            productID INT NOT NULL,
            FOREIGN KEY (userID) REFERENCES users(userID),
            FOREIGN KEY (productID) REFERENCES products(productID)
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    return True

def dodaj_v_kosarico(product_id, user_id):
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT productID, Ime_produkta, Cena_produkta 
        FROM products
        WHERE productID = %s;
    ''', (product_id,))
    row = cursor.fetchone()

    if row:
        productID, ime, cena = row
        cursor.execute('''
            SELECT Stock
            FROM kosarica
            WHERE productID = %s AND userID = %s;
        ''', (productID, user_id))
        existing = cursor.fetchone()

        if existing:
            cursor.execute('''
                UPDATE kosarica
                SET Stock = Stock + 1
                WHERE productID = %s AND userID = %s;
            ''', (productID, user_id))
        else:
            cursor.execute('''
                INSERT INTO kosarica (productID, userID, Ime_produkta, Cena_produkta, Stock)
                VALUES (%s, %s, %s, %s, 1)
            ''', (productID, user_id, ime, cena))

    conn.commit()
    cursor.close()
    conn.close()


#def izpis_kosarice():
#    conn = db.get_connection()
#    cursor = conn.cursor()
#
#    cursor.execute('''
#        SELECT productID, Ime_produkta, Cena_produkta, Stock 
#        FROM kosarica;
#    ''')
#    izdelki = cursor.fetchall()
#
#    cursor.close()
#    conn.close()
#
#    if not izdelki:
#        print("Košarica je prazna.")
#        return
#
#    return izdelki

def izpis_kosarice_iz_baze(user_id):
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT productID, Ime_produkta, Cena_produkta, Stock
        FROM kosarica
        WHERE userID = %s;
    ''', (user_id,))
    izdelki = cursor.fetchall()

    cursor.close()
    conn.close()
    return izdelki

def dodaj_na_wishlist(product_id, user_id):
    conn = db.get_connection()
    cursor = conn.cursor()

    # Preveri, če je že v wishlist
    cursor.execute('''
        SELECT 1 FROM wishlist
        WHERE userID = %s AND productID = %s;
    ''', (user_id, product_id))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute('''
            INSERT INTO wishlist (userID, productID)
            VALUES (%s, %s);
        ''', (user_id, product_id))

    conn.commit()
    cursor.close()
    conn.close()


def pridobi_wishlist_izdelke(user_id):
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.productID, p.Ime_produkta, p.Opis_produkta, p.Cena_produkta
        FROM wishlist w
        JOIN products p ON w.productID = p.productID
        WHERE w.userID = %s;
    ''', (user_id,))
    izdelki = cursor.fetchall()

    cursor.close()
    conn.close()
    return izdelki

def odstrani_iz_wishlist(user_id, product_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM wishlist
        WHERE userID = %s AND productID = %s;
    ''', (user_id, product_id))
    conn.commit()
    cursor.close()
    conn.close()
    
""" def vstavi_placeholder_kode():
    conn = db.get_connection()
    cursor = conn.cursor()

    kode = [
        ("WELCOME10", 10.00),
        ("SUMMER15", 15.00),
        ("SAVE5", 5.00),
    ]

    for koda, vrednost in kode:
        cursor.execute('''
            INSERT INTO promo_kode (koda, vrednost_kode)
            SELECT %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM promo_kode WHERE koda = %s
            )
        ''', (koda, vrednost, koda))

    conn.commit() """

def pridobi_kosarico(user_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT k.productID, k.ime_produkta, k.cena_produkta, p.kolicina
            FROM kosarica k
            JOIN products p ON k.productID = p.productID
            WHERE k.userID = %s
        ''', (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


