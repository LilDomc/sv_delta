from flask import request, redirect, url_for
import models.sv_kosarica

def add_to_cart():
    models.sv_kosarica.setup_db()
    product_id = request.form.get("productID")
    models.sv_kosarica.dodaj_v_kosarico(product_id)
    return redirect(url_for('trgovina'))
