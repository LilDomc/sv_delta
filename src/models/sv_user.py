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
            employeeID INT,
            ime VARCHAR(50) NOT NULL,
            priimek VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            geslo VARCHAR(255) NOT NULL,
            role user_role NOT NULL DEFAULT 'user',
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

def insert_test_users():        #To se laho zakomentira, ko se bo testiralo vnašanje podatkov na spletni strani in isto zakomentirati klicno funkcijo na app.py!!!
    conn = db.get_connection()
    cursor = conn.cursor()
    employees = [
        ('Janez', 'Novak', 'janez.novak@example.com', 'Vodja prodaje'),
        ('Tina', 'Horvat', 'tina.horvat@example.com', 'Naziv za Tino'),
    ]

    employee_ids = {}
    for ime, priimek, email, naziv in employees:
        cursor.execute('''
            INSERT INTO employees (ime, priimek, email, naziv)
            VALUES (%s, %s, %s, %s)
            RETURNING employeeID;
        ''', (ime, priimek, email, naziv))
        emp_id = cursor.fetchone()[0]
        employee_ids[email] = emp_id

    test_users = [
        ('Ana', 'Kovač', 'ana.kovac@example.com', 'geslo123', 'user', None),
        ('Marko', 'Zupan', 'marko.zupan@example.com', '123456', 'user', None),
        ('Tina', 'Horvat', 'tina.horvat@example.com', 'securepass', 'employee', employee_ids.get('tina.horvat@example.com')),
        ('Janez', 'Novak', 'janez.novak@example.com', 'vodjageslo', 'employee', employee_ids.get('janez.novak@example.com')),
    ]

    for user in test_users:
        cursor.execute('''
            INSERT INTO users (ime, priimek, email, geslo, role, employeeID)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING;
        ''', user)

    conn.commit()
    cursor.close()
    conn.close()
