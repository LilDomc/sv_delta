from flask import request, redirect, url_for, render_template
import models.sv_kosarica

def add_to_cart():
    product_id = request.form.get("productID")
    models.sv_kosarica.dodaj_v_kosarico(product_id)
    return redirect(url_for('trgovina'))

def izpis_kosarice():
    izdelki = models.sv_kosarica.izpis_kosarice()
    return render_template('sv_izpis_kosarice.html', izdelki=izdelki)
