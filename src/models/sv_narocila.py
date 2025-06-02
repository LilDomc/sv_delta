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

def get_orders_by_user(user_id):
    conn = db.get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT n.narociloID, n.datum_narocila, n.status_narocila, n.kolicina,
               p.ime_produkta, p.opis_produkta, p.cena_produkta
        FROM narocila n
        JOIN products p ON n.productID = p.productID
        WHERE n.userID = %s
        ORDER BY n.datum_narocila DESC
    """, (user_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders

def shrani_narocilo(user_id, izdelki, u_ime, u_priimek, status="V obdelavi"):
    conn = db.get_connection()
    cursor = conn.cursor()

    for izdelek in izdelki:
        productID = izdelek['productID']
        kolicina = izdelek['kolicina']
        cena = izdelek['cena']
        opis = izdelek.get('opis', '')

        cursor.execute('''
            INSERT INTO narocila (productID, userID, u_ime, u_priimek, kolicina, p_cena_produkta, p_opis_produkta, status_narocila)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (productID, user_id, u_ime, u_priimek, kolicina, cena, opis, status)
        )
    conn.commit()
    cursor.close()
    conn.close()