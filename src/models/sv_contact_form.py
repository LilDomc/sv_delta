import db

class ContactForm:
    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message
        
    def save(self):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)',
            (self.name, self.email, self.message)
        )
        conn.commit()
        cursor.close()
        conn.close()


def setup_db():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_contact_messages():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contact_messages ORDER BY created_at DESC')
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return messages