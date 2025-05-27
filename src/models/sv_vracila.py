import db

def setup_db():
    print("Seting up vracila database", flush=True)
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vracila (
            vraciloID SERIAL PRIMARY KEY,
            ime VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            izdelek VARCHAR(100) NOT NULL,
            razlog TEXT NOT NULL,
            datum_vnosa TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    return True

def insert_vracilo(ime, email, izdelek, razlog):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vracila (ime, email, izdelek, razlog)
        VALUES (%s, %s, %s, %s)
    ''', (ime, email, izdelek, razlog))
    conn.commit()
    cursor.close()
    conn.close()
    