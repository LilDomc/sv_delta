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