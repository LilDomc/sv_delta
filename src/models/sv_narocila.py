import db
from flask import request, redirect, render_template
from psycopg2.extras import RealDictCursor

def vpogled_narocila(narocilo_id):
    conn = db.get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT n.*, p.ime_produkta, p.opis_produkta, p.cena_produkta
        FROM narocila n
        JOIN products p ON n.productID = p.productID
        WHERE narociloID = %s
    """, (narocilo_id,))
    postavke = cursor.fetchall()

    if not postavke:
        status_narocila = "Ni podatkov"
        skupna_cena = 0.0
    else:
        status_narocila = postavke[0]['status_narocila']
        skupna_cena = sum(int(p['kolicina']) * float(p['p_cena']) for p in postavke)
    
    cursor.close()
    conn.close()

    return postavke, status_narocila, skupna_cena

def spremeni_status(narocilo_id, nov_status):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE narocila SET status_narocila = %s WHERE narociloID = %s
    """, (nov_status, narocilo_id))
    conn.commit()
    cursor.close()
    conn.close()
