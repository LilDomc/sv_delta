from flask import render_template
import models.sv_products

def home():
    top_products = models.sv_products.get_best_selling_products(limit=3)
    return render_template("index.html", top_products=top_products)
