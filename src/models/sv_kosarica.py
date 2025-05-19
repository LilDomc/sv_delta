import db

def setup_db():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kosarica (
            kosaricaID SERIAL PRIMARY KEY,
            productID INT NOT NULL,
            Ime_produkta varchar(255),
            Cena_produkta varchar(255),
            Stock INT NOT NULL DEFAULT 1,
            FOREIGN KEY (productID) REFERENCES products(productID)
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    return True

def dodaj_v_kosarico(product_id):
    conn = db.get_connection()
    cursor = conn.cursor()

    # Pridobi podatke o izdelku
    cursor.execute('''
        SELECT productID, Ime_produkta, Cena_produkta 
        FROM products WHERE productID = %s;
    ''', (product_id,))
    row = cursor.fetchone()

    if row:
        productID, ime, cena = row
        # Vstavi v kosarico
        cursor.execute('''
            INSERT INTO kosarica (productID, Ime_produkta, Cena_produkta)
            VALUES (%s, %s, %s)
        ''', (productID, ime, cena))

    conn.commit()
    cursor.close()
    conn.close()

def izpis_kosarice():
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT productID, Ime_produkta, Cena_produkta, Stock 
        FROM kosarica;
    ''')
    izdelki = cursor.fetchall()

    cursor.close()
    conn.close()

    if not izdelki:
        print("Košarica je prazna.")
        return

    return izdelki