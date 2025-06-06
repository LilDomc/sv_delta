import db

def insert_question_and_answer(vprasanje, odgovor):
    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        # 1. Vstavi vprašanje
        cursor.execute('''
            INSERT INTO vprasanja (vprasanje_tekst)
            VALUES (%s)
            RETURNING vprasanjeID
        ''', (vprasanje,))
        vprasanje_id = cursor.fetchone()[0]

        # 2. Vstavi odgovor (povezan z vprasanjeID)
        cursor.execute('''
            INSERT INTO odgovori (vprasanjeID, odgovor_tekst)
            VALUES (%s, %s)
        ''', (vprasanje_id, odgovor))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print("Napaka pri vnosu Q&A:", e)
        return False

    finally:
        cursor.close()
        conn.close()
