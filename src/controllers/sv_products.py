from flask import request, redirect, render_template

import models.sv_user

def show_products():
    models.sv_user.insert_test_data()

    products = models.sv_user.get_products()
    return render_template('sv_products.html', products=products)

def rate_product():
    product_id = int(request.form['product_id'])
    rating_value = int(request.form['rating'])
    models.sv_user.add_rating(product_id, rating_value)
    return redirect('/products')

def show_trgovina():
    trgovina = models.sv_user.get_trgovina()
    return render_template('sv_trgovina.html', trgovina=trgovina)
