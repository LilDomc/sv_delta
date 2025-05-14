import db

def setup_db():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vprasanja (
            vprasanjeID SERIAL PRIMARY KEY,
            vprasanje_tekst varchar(255)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS odgovori (
            odgovoriID SERIAL PRIMARY KEY,
            vprasanjeID INT NOT NULL,
            odgovor_tekst varchar(255),
            FOREIGN KEY (vprasanjeID) REFERENCES vprasanja(vprasanjeID)
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    return True