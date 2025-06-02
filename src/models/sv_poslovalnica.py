import db

def setup_db():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS poslovalnice (
            poslovalnicaID SERIAL PRIMARY KEY,
            ime_poslovalnica varchar(100) NOT NULL,
            naslov_poslovalnica varchar(255) NOT NULL,
            telefonska_st varchar(20)
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    return True

def insert_store(ime, naslov, telefon):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO poslovalnice (ime_poslovalnica, naslov_poslovalnica, telefonska_st)
        VALUES (%s, %s, %s)
    ''', (ime, naslov, telefon))
    conn.commit()
    cursor.close()
    conn.close()
    
def get_all_stores():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM poslovalnice")
    stores = cursor.fetchall()
    cursor.close()
    conn.close()
    return stores