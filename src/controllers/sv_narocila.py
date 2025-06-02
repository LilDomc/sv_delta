from flask import redirect, request, session, render_template, url_for, session
import models.sv_kosarica
import models.sv_narocila

def shrani_narocilo():
    user = session.get('user')
    if not user:
        return redirect(url_for('/prijava'))
    
    user_id = user.get('userID')
    u_ime = user.get('ime')
    u_priimek = user.get('priimek')


    kosarica_izdelki = models.sv_kosarica.izpis_kosarice_iz_baze(user_id)

    izdelki = []
    for productID, ime_produkta, cena_produkta, kolicina in kosarica_izdelki:
        izdelki.append({
            'productID': productID,
            'kolicina': kolicina,
            'cena': cena_produkta,
            'ime': ime_produkta
        })
    if not izdelki:
        return redirect(url_for('izpis_kosarice'))
    
    models.sv_narocila.shrani_narocilo(user_id, izdelki, u_ime, u_priimek)
    return redirect(url_for('order_history'))

def izpis_narocila(narocilo_id):
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'potrdi':
            models.sv_narocila.spremeni_status(narocilo_id, 'Potrjeno')
        elif action == 'zavrni':
            models.sv_narocila.spremeni_status(narocilo_id, 'Zavrnjeno')
        return redirect(url_for('vpogled_narocila', narocilo_id=narocilo_id))

    izdelki, status, total_price = models.sv_narocila.vpogled_narocila(narocilo_id)
    return render_template("sv_vpogled_narocila.html", izdelki=izdelki, narocilo={'order_id': narocilo_id, 'status': status}, total_price=total_price)

def order_history():
    user = session.get('user')
    if not user:
        return redirect(url_for('prijava_get'))

    user_id = user.get('userID')
    orders = models.sv_narocila.get_orders_by_user(user_id)
    return render_template("sv_order_history.html", orders=orders)