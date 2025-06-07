import db
from flask import request

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
            datum_rojstva DATE NOT NULL,
            naslov VARCHAR(100) NOT NULL,
            placa INT NOT NULL,
            email VARCHAR(100),
            naziv VARCHAR(100),
            datum_zaposlitve DATE NOT NULL DEFAULT CURRENT_DATE
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prihodi_odhodi (
            prihodi_odhodiID SERIAL PRIMARY KEY,
            employeeID INT,
            datum DATE DEFAULT CURRENT_DATE,        /*DEAFULT get it xD*/
            prihod TIME DEFAULT CURRENT_TIME,
            odhod TIME DEFAULT CURRENT_TIME,
            FOREIGN KEY (employeeID) REFERENCES employees(employeeID)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_reset_token (
            tokenID SERIAL PRIMARY KEY,
            token varchar(64) NOT NULL,
            email varchar(100) NOT NULL,
            ustvarjeno TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (email) REFERENCES users(email))
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    return True

def insert_test_users():        #To se laho zakomentira, ko se bo testiralo vnašanje podatkov na spletni strani in isto zakomentirati klicno funkcijo na app.py!!!
    conn = db.get_connection()
    cursor = conn.cursor()

    employees = [
        ('Janez', 'Novak', '19801215', 'Trg republike 1, Ljubljana', 2500, 'janez.novak@example.com', 'Vodja prodaje'),
        ('Tina', 'Horvat', '19900322', 'Celovška cesta 10, Ljubljana', 2200, 'tina.horvat@example.com', 'Junior designer'),
        ('Admin', 'Admin', '19850422', 'Trg nimam blage 69', 5000, 'admin@delta.com', 'Administrator'),
    ]

    employee_ids = {}
    for ime, priimek, datum_rojstva, naslov, placa, email, naziv in employees:
        cursor.execute('''
            INSERT INTO employees (ime, priimek, datum_rojstva, naslov, placa, email, naziv)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING employeeID;
        ''', (ime, priimek, datum_rojstva, naslov, placa, email, naziv))
        emp_id = cursor.fetchone()[0]
        employee_ids[email] = emp_id

    test_users = [
        ('Ana', 'Kovač', 'ana.kovac@example.com', 'geslo123', 'user', None),
        ('Marko', 'Zupan', 'marko.zupan@example.com', '123456', 'user', None),
        ('Tina', 'Horvat', 'tina.horvat@example.com', 'securepass', 'employee', employee_ids.get('tina.horvat@example.com')),
        ('Janez', 'Novak', 'janez.novak@example.com', 'vodjageslo', 'employee', employee_ids.get('janez.novak@example.com')),
        ('Admin', 'Admin', 'admin@delta.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'employee', employee_ids.get('admin@delta.com')),
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

def add_user(form):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (ime, priimek, datum_rojstva, naslov, placa, email, naziv)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (
        form['ime'],
        form['priimek'],
        form['datum_rojstva'],
        form['naslov'],
        int(form['placa']),
        form.get('email'),
        form.get('naziv')
    ))
    conn.commit()
    cursor.close()
    conn.close()

def vsi_zaposleni():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ime, priimek, datum_rojstva, naslov, placa, email, naziv, datum_zaposlitve
        FROM employees
        ORDER BY ime, priimek;
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return rows

def isci_zaposlene(iskanje):
    conn = db.get_connection()
    cur = conn.cursor()

    query = """
        SELECT ime, priimek, datum_rojstva, naslov, placa, email, naziv, datum_zaposlitve
        FROM employees
        WHERE LOWER(ime) LIKE %s OR LOWER(priimek) LIKE %s
    """
    param = f"%{iskanje.lower()}%"
    cur.execute(query, (param, param))

    rezultati = cur.fetchall()
    cur.close()
    conn.close()
    return rezultati