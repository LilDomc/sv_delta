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

def insert_test_data_qa():     #inserta če je tabela prazna
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM vprasanja;")
    count = cursor.fetchone()[0]
    if count > 0:
        cursor.close()
        conn.close()
        return  


    cursor.execute("""
        INSERT INTO vprasanja (vprasanjeID, vprasanje_tekst) VALUES
        (1, 'What is the capital of France?'),
        (2, 'What is 2 + 2?'),
        (3, 'Which planet is known as the Red Planet?');
    """)

    cursor.execute("""
        INSERT INTO odgovori (odgovoriID, vprasanjeID, odgovor_tekst) VALUES
        (1, 1, 'Paris'),
        (2, 1, 'London'),
        (3, 2, '4'),
        (4, 2, '5'),
        (5, 3, 'Mars'),
        (6, 3, 'Jupiter');
    """)

    conn.commit()
    cursor.close()
    conn.close()

def get_questions_answers():
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.vprasanjeID, v.vprasanje_tekst, o.odgovor_tekst
        FROM vprasanja v
        LEFT JOIN odgovori o ON v.vprasanjeID = o.vprasanjeID
        ORDER BY v.vprasanjeID, o.odgovoriID;
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    questions = {}
    for vprasanjeID, vprasanje_tekst, odgovor_tekst in rows:
        if vprasanjeID not in questions:
            questions[vprasanjeID] = {
                'text': vprasanje_tekst,
                'answers': []
            }
        if odgovor_tekst:
            questions[vprasanjeID]['answers'].append(odgovor_tekst)

    return questions


    