from flask import Blueprint,request, redirect, render_template
from models.sv_user import get_products

import models.sv_user

sv_products_bp = Blueprint("sv_products", __name__)
@sv_products_bp.route("/products")

def show_products():
    sort = request.args.get("sort", "name_asc")
    sort_by, order = sort.split("_")

    models.sv_user.insert_test_data()  # keep this if needed
    products = get_products(sort_by, order)
    return render_template("sv_products.html", products=products, sort_by=sort_by, order=order)

def rate_product():
    product_id = int(request.form['product_id'])
    rating_value = int(request.form['rating'])
    models.sv_user.add_rating(product_id, rating_value)
    return redirect('/products')

def show_trgovina():
    trgovina = models.sv_user.get_trgovina()
    return render_template('sv_trgovina.html', trgovina=trgovina)