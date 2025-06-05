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

def insert_test_data_qa():
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM vprasanja;")
    count = cursor.fetchone()[0]
    if count > 0:
        cursor.close()
        conn.close()
        return

    # Vstavi vprašanja
    cursor.execute("""
        INSERT INTO vprasanja (vprasanje_tekst) VALUES
        ('Kako oddam naročilo?'),
        ('Kaj naj naredim, če prejmem poškodovano varovalko ali napačen izdelek?'),
        ('Kako preverim, ali je določena varovalka trenutno na zalogi?')
        RETURNING vprasanjeID;
    """)
    vprasanja_ids = cursor.fetchall()

    # Vstavi odgovore z uporabo ustreznih ID-jev
    cursor.execute("""
        INSERT INTO odgovori (vprasanjeID, odgovor_tekst) VALUES
        (%s, 'Izberite željen izdelek, nastavite količino in kliknite »Dodaj v košarico«. Ko zaključite z izbiro, nadaljujete na spletni blagajni, kamor vnesete podatke za dostavo in izberete način plačila.'),
        (%s, 'Takoj nas kontaktirajte po e-pošti in priložite fotografije poškodbe ter embalaže. Po potrditvi bomo organizirali brezplačno zamenjavo ali vračilo. Napako je treba prijaviti najkasneje v 3 dneh po prejemu pošiljke.'),
        (%s, 'Na strani vsakega izdelka je navedeno, ali je varovalka na zalogi in v kakšni količini. Če izdelek ni na zalogi, lahko vpišete svoj e-mail za obvestilo ob ponovni dobavi.');
    """, (vprasanja_ids[0][0], vprasanja_ids[1][0], vprasanja_ids[2][0]))

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


    