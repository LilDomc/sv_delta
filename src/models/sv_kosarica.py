import db

def setup_db():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kosarica (
            kosaricaID SERIAL PRIMARY KEY,
            productID INT NOT NULL,
            ime_produkta varchar(255),
            cena_produkta varchar(255),
            stock INT NOT NULL DEFAULT 1,
            FOREIGN KEY (productID) REFERENCES products(productID)
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
    conn.commit()
    cursor.close()
    conn.close()
    return True

def dodaj_v_kosarico(product_id):
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
            WHERE productID = %s;
        ''', (productID,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute('''
                UPDATE kosarica
                SET Stock = Stock + 1
                WHERE productID = %s;
                ''', (productID,))
        else:
            cursor.execute('''
            INSERT INTO kosarica (productID, Ime_produkta, Cena_produkta, Stock)
            VALUES (%s, %s, %s, 1)
        ''', (productID, ime, cena))

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

def izpis_kosarice_iz_seje(seznam_id):
    if not seznam_id:
        return []

    conn = db.get_connection()
    cursor = conn.cursor()

    # Pretvori v tuple in uporabi SQL IN
    format_strings = ','.join(['%s'] * len(seznam_id))
    query = f'''
        SELECT productID, Ime_produkta, Cena_produkta 
        FROM products
        WHERE productID IN ({format_strings});
    '''
    cursor.execute(query, tuple(seznam_id))
    izdelki = cursor.fetchall()

    # Preštej količine
    from collections import Counter
    kolicine = Counter(seznam_id)
    izdelki_s_kolicino = [(id, ime, cena, kolicine[id]) for id, ime, cena in izdelki]

    cursor.close()
    conn.close()

    return izdelki_s_kolicino