from flask import request, redirect, url_for, render_template
import models.sv_kosarica

def add_to_cart():
    product_id = request.form.get("productID")
    models.sv_kosarica.dodaj_v_kosarico(product_id)
    return redirect(url_for('trgovina'))

def izracunaj_postnino(drzava, nacin):
    # Base price
    base_price = 2.0

    # Country multiplier
    if drzava == "tujina":
        base_price += 5.0
    elif drzava == "slo":
        base_price += 1.0

    # Delivery method adjustment
    if nacin == "obicajno":
        base_price += 0
    elif nacin == "prednostno":
        base_price += 1.5
    elif nacin == "expres":
        base_price += 3.0

    return f"Informativna poštnina: {base_price:.2f} EUR"

def izpis_kosarice():
    postnina = None
    drzava = request.args.get('drzava')
    nacin = request.args.get('nacin')

    print("request.arg", request.args, flush=True)

    if drzava  and nacin:
        postnina = izracunaj_postnino(drzava, nacin)

    izdelki = models.sv_kosarica.izpis_kosarice()
    return render_template('sv_izpis_kosarice.html', izdelki=izdelki, postnina=postnina)

