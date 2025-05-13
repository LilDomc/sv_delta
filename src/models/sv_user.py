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

