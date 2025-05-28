from flask import render_template
import models.sv_products
import models.sv_poslovalnica

def home():
    top_products = models.sv_products.get_best_selling_products(limit=3)
    stores = models.sv_poslovalnica.get_all_stores()
    return render_template("index.html", top_products=top_products, stores=stores)