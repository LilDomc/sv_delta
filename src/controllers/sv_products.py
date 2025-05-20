from flask import request, redirect, render_template

import models.sv_products
import models.sv_trgovina

def show_products():
    sort = request.args.get("sort", "name_asc")
    sort_by, order = sort.split("_")

    models.sv_products.insert_test_data()
    products = models.sv_products.get_products(sort_by, order)
    return render_template("sv_products.html", products=products, sort_by=sort_by, order=order)

def rate_product():
    product_id = int(request.form['product_id'])
    rating_value = int(request.form['rating'])
    models.sv_products.add_rating(product_id, rating_value)
    return redirect('/products')

def show_trgovina():
    sort = request.args.get("sort", "name_asc")
    sort_by, order = sort.split("_")
    products = models.sv_trgovina.get_trgovina(sort_by, order)
    return render_template("sv_trgovina.html", products=products, sort_by=sort_by, order=order)

def insert_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        models.sv_products.insert_product(name, description, price, stock)
        return redirect('/products')

    return render_template('sv_insert_product.html')

