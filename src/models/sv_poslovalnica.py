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