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
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
                CREATE TYPE user_role AS ENUM ('user', 'employee');
            END IF;
        END
        $$;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employeeID SERIAL PRIMARY KEY,
            ime VARCHAR(50) NOT NULL,
            priimek VARCHAR(50) NOT NULL,
            email VARCHAR(100),
            naziv VARCHAR(100)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            userID SERIAL PRIMARY KEY,
            ime VARCHAR(50) NOT NULL,
            priimek VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            geslo VARCHAR(255) NOT NULL,
            role user_role NOT NULL DEFAULT 'user',
            employeeID INT,
            CONSTRAINT fk_employee
                FOREIGN KEY (employeeID)
                REFERENCES employees(employeeID)
                ON DELETE SET NULL
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    return True

