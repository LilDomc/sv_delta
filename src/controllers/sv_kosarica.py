from flask import request, redirect, url_for, render_template, session
import models.sv_kosarica
import models.sv_products
from datetime import datetime
import random

def add_to_cart():
    user = session.get("user")
    if not user:
        return redirect("/prijava")

    user_id = user["userID"]
    product_id = request.form.get("product_id")
    if not product_id:
        return "Manjka product_id", 400

    models.sv_products.povecaj_klike(product_id)
    models.sv_kosarica.dodaj_v_kosarico(product_id, user_id)

    return redirect(url_for("trgovina"))


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

#def izpis_kosarice():
#    postnina = None
#    drzava = request.args.get('drzava')
#    regija = request.args.get('regija')
#    nacin = request.args.get('nacin')
#
#    print("request.arg", request.args, flush=True)
#
#    if drzava and regija and nacin:
#        postnina = izracunaj_postnino(drzava, regija, nacin)
#
#    izdelki = models.sv_kosarica.izpis_kosarice()
#    return render_template('sv_izpis_kosarice.html', izdelki=izdelki, postnina=postnina)

def izpis_kosarice():
    postnina = None
    drzava = request.args.get('drzava')
    nacin = request.args.get('nacin')

    if drzava  and nacin:
        postnina = izracunaj_postnino(drzava, nacin)

    user = session.get("user")
    if not user:
        return render_template("sv_izpis_kosarice.html", izdelki=[], postnina=postnina)

    user_id = user["userID"]
    izdelki = models.sv_kosarica.izpis_kosarice_iz_baze(user_id)

    return render_template('sv_izpis_kosarice.html', izdelki=izdelki, postnina=postnina)

def izpis_racuna():
    drzava = request.args.get('drzava', 'ni izbrano')
    regija = request.args.get('regija', 'ni izbrano')
    nacin = request.args.get('nacin', 'ni izbrano')

    kosarica = session.get('kosarica', [])
    izdelki_raw = models.sv_kosarica.izpis_kosarice_iz_seje(kosarica)

    izdelki = []
    skupna_cena = 0

    for productID, ime, cena, kolicina in izdelki_raw:
        try:
            cena_float = float(cena)
        except ValueError:
            cena_float = 0.0

        skupaj = round(cena_float * kolicina, 2)
        skupna_cena += skupaj

        izdelki.append({
            'ime': ime,
            'cena': cena_float,
            'kolicina': kolicina,
            'skupaj': skupaj
        })

    # Poštnina
    postnina_str = izracunaj_postnino(drzava, regija, nacin)
    try:
        postnina_value = float(postnina_str.replace("Informativna poštnina:", "").replace("EUR", "").strip())
    except:
        postnina_value = 0.0

    skupna_cena_z_postnino = round(skupna_cena + postnina_value, 2)

    datum_cas = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    stevilka_racuna = random.randint(100000, 999999)

    return render_template('sv_izpis_racuna.html',
                           cas=datum_cas,
                           stevilka_racuna=stevilka_racuna,
                           drzava=drzava,
                           regija=regija,
                           nacin=nacin,
                           izdelki=izdelki,
                           skupna_cena=f"{skupna_cena:.2f}",
                           postnina=f"{postnina_value:.2f}",
                           skupna_cena_z_postnino=f"{skupna_cena_z_postnino:.2f}")

def dodaj_na_wishlist():
    user = session.get("user")
    if not user:
        return redirect("/prijava")

    product_id = request.form.get("product_id")
    if not product_id:
        return "Manjka product_id", 400

    user_id = user["userID"]
    models.sv_kosarica.dodaj_na_wishlist(product_id, user_id)

    return redirect(url_for("prikazi_wishlist"))


def prikazi_wishlist():
    user = session.get("user")
    if not user:
        return redirect("/prijava")

    user_id = user["userID"]
    izdelki = models.sv_kosarica.pridobi_wishlist_izdelke(user_id)

    return render_template("sv_wishlist.html", wishlist=izdelki)


def odstrani_iz_wishlist():
    user = session.get("user")
    if not user:
        return redirect("/prijava")

    product_id = request.form.get("product_id")
    if not product_id:
        return "Manjka product_id", 400

    user_id = user["userID"]
    models.sv_kosarica.odstrani_iz_wishlist(user_id, product_id)
    return redirect(url_for("prikazi_wishlist"))

