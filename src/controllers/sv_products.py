from flask import request, redirect, render_template

import models.sv_products
import models.sv_trgovina

def show_products():
    #models.sv_qa.setup_db()        #TO SE KLIČE V SVOJEM KONTROLERJU ZA VPRAŠANJA IN ODGOVORE!!!!
    models.sv_products.setup_db()
    models.sv_products.insert_test_data()

    products = models.sv_products.get_products()
    return render_template('sv_products.html', products=products)

def rate_product():
    product_id = int(request.form['product_id'])
    rating_value = int(request.form['rating'])
    models.sv_products.add_rating(product_id, rating_value)
    return redirect('/products')

def show_trgovina():
    trgovina = models.sv_trgovina.get_trgovina()

    return render_template('sv_trgovina.html', products=trgovina)


# def show_best_selling():
#     products = models.sv_products.get_best_selling_products()
#     return render_template("sv_best_selling.html", products=products)

