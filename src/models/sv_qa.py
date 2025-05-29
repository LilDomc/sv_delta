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
        (1, 'Kako oddam naročilo?'),
        (2, 'Kaj naj naredim, če prejmem poškodovano varovalko ali napačen izdelek?'),
        (3, 'Kako preverim, ali je določena varovalka trenutno na zalogi?');
    """)

    cursor.execute("""
        INSERT INTO odgovori (odgovoriID, vprasanjeID, odgovor_tekst) VALUES
        (1, 1, 'Izberite željen izdelek, nastavite količino in kliknite »Dodaj v košarico«. Ko zaključite z izbiro, nadaljujete na spletni blagajni, kamor vnesete podatke za dostavo in izberete način plačila.'),
        (2, 2, 'Takoj nas kontaktirajte po e-pošti in priložite fotografije poškodbe ter embalaže. Po potrditvi bomo organizirali brezplačno zamenjavo ali vračilo. Napako je treba prijaviti najkasneje v 3 dneh po prejemu pošiljke.'),
        (3, 3, 'Na strani vsakega izdelka je navedeno, ali je varovalka na zalogi in v kakšni količini. Če izdelek ni na zalogi, lahko vpišete svoj e-mail za obvestilo ob ponovni dobavi.');
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


    