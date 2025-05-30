from flask import request, redirect, render_template

import models.sv_products
import models.sv_trgovina

def show_products():
    sort = request.args.get("sort", "name_asc")
    sort_by, order = sort.split("_")
    stock_filter = request.args.get("stock_filter", "all")

    products = models.sv_products.get_products(sort_by, order, stock_filter)
    return render_template("sv_products.html", products=products, sort_by=sort_by, order=order, stock_filter=stock_filter)

def rate_product():
    product_id = int(request.form['product_id'])
    rating_value = int(request.form['rating'])
    models.sv_products.add_rating(product_id, rating_value)
    return redirect('/trgovina')

def show_trgovina():
    sort = request.args.get("sort", "name_asc")
    sort_by, order = sort.split("_")
    #models.sv_trgovina.get_rate()
    trgovina = models.sv_trgovina.get_trgovina(sort_by, order)
    trgovina_test = []

    for p in trgovina: 
        product_id = p[0]
        ime = p[1]
        opis = p[2]
        cena = p[3]
        avg_rating = models.sv_trgovina.get_rate(product_id)
        trgovina_test.append((product_id, ime, opis, cena, avg_rating)) 
    return render_template('sv_trgovina.html', products=trgovina_test, sort_by=sort_by, order=order)

def insert_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        models.sv_products.insert_product(name, description, price, stock)
        return redirect('/products')

    return render_template('sv_insert_product.html')

def show_checkout():
    trgovina = models.sv_trgovina.get_trgovina()
    return render_template('sv_checkout.html', products=trgovina)

def show_best_selling():
    products = models.sv_products.get_best_selling_products()
    return render_template("sv_best_selling.html", products=products)

def search_products():
    query = request.args.get("query", "").strip()

    if query:
        products = models.sv_products.search_products(query)
    else:
        products = []  

    return render_template(
        "sv_products.html",
        products=products,
        query=query
    )
