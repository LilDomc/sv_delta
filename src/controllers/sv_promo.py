from flask import request, redirect, render_template

import models.sv_promo

def insert_promo():
    if request.method == 'POST':
        koda = request.form['koda']
        vrednost = float(request.form['vrednost'])

        models.sv_promo.insert_promo_code(koda, vrednost)
        return redirect('/insert_promo')

    return render_template('sv_insert_promo.html')