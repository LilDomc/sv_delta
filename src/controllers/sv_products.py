from flask import request, render_template

import models.sv_user

def show_products():
    models.sv_user.insert_test_data()

    products = models.sv_user.get_products()
    return render_template('sv_products.html', products=products)
