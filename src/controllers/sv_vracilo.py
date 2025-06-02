from flask import request, render_template
import models.sv_vracila
import models.sv_products

def show_vracilo():
    potrjeno = False

    # TODO fill this with  session info
    uporabnik = {
        'ime': '',
        'email': ''
    }

    izdelki = models.sv_products.get_all_products()

    if request.method == 'POST':
        ime = request.form.get('ime')
        email = request.form.get('email')
        izdelek = request.form.get('izdelek')
        razlog = request.form.get('razlog')

        print(f"Ime: {ime}, Email: {email}, Izdelek: {izdelek}, Razlog: {razlog}")
        models.sv_vracila.insert_vracilo(ime, email, izdelek, razlog)
        potrjeno = True

    return render_template('sv_vracilo.html', potrjeno=potrjeno, uporabnik=uporabnik, izdelki=izdelki)

