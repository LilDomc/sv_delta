from flask import request, redirect, url_for, render_template
import models.sv_kosarica
from datetime import datetime

def add_to_cart():
    product_id = request.form.get("productID")
    models.sv_kosarica.dodaj_v_kosarico(product_id)
    return redirect(url_for('trgovina'))

#def izpis_kosarice():
#    izdelki = models.sv_kosarica.izpis_kosarice()
#    return render_template('sv_izpis_kosarice.html', izdelki=izdelki)

def izpis_kosarice():
    podatki = models.sv_kosarica.izpis_kosarice()
    if not podatki:
        return render_template('sv_izpis_kosarice.html', izdelki=[], skupna_vsota=0)
    
    return render_template(
        'sv_izpis_kosarice.html',
        izdelki=podatki["izdelki"],
        skupna_vsota=podatki["skupna_vsota"]
    )

def racun():
    podatki = models.sv_kosarica.izpis_kosarice()
    if not podatki:
        izdelki = []
        skupna_vsota = 0
    else:
        izdelki = podatki["izdelki"]
        skupna_vsota = podatki["skupna_vsota"]

    now = datetime.now()
    datum_cas = now.strftime("%d.%m.%Y ob %H:%M")

    return render_template('sv_racun.html', izdelki=izdelki, skupna_vsota=skupna_vsota, datum_cas=datum_cas)
