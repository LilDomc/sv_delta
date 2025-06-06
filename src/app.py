from flask import Flask, session, redirect, url_for, request
from functools import wraps

import controllers.sv_contact
import controllers.sv_kosarica
import controllers.sv_vracilo
import controllers.index
import controllers.sv_qa
import controllers.sv_setup
import controllers.sv_products
import controllers.sv_registracija
import controllers.sv_prijava
import controllers.sv_odjava
import controllers.sv_zaposleni
import controllers.sv_menjava_gesla
import controllers.sv_profil
import controllers.sv_narocila
import controllers.sv_promo
import controllers.sv_qa_insert

import controllers.sv_poslovalnica
from controllers import sv_pozabljeno_geslo

import models
import models.sv_backend
import models.sv_products
import models.sv_trgovina
import models.sv_kosarica
import models.sv_qa
import models.sv_narocila
import models.sv_prihodi_odhodi
import models.sv_promo
import models.sv_qa_insert
from models import sv_uporabnik


f_app = Flask(__name__) # F stands for fu***ng

# to bi mogl bit znotrej main funkcije se mi zdi ... sej ta koda se ne bo uporabljala
# kot module tko da naceloma ne bi smelo biti problema ampak samo za dobro prakso :) 
models.sv_backend.setup_all_db_tables()     
models.sv_user.insert_test_users()      #zakomentirati če se zakomentira funkcija v sv_users
models.sv_products.insert_test_data()

if __name__ == "__main__":
    f_app.run(debug=True)

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = session.get('user')
            if user is None:
                return redirect(url_for('prijava_get'))  # redirect to login page
            if role and user.get('role') != role:
                return "Access denied", 403
            return f(*args, **kwargs)
        return wrapped
    return decorator


@f_app.get('/')
def home():
    return controllers.index.home()

@f_app.get('/kontakt')
def kontakt():
    return controllers.sv_contact.show_contact_form()

@f_app.post('/kontakt')
def kontakt_post():
    return controllers.sv_contact.save_contact_request()


@f_app.get('/products')
@login_required(role='employee')
def products():
    return controllers.sv_products.show_products()


@f_app.route('/rate', methods=['POST'])
@login_required()  # Locked to logged-in users (any role)
def rate():
    return controllers.sv_products.rate_product()

@f_app.get('/trgovina')
def trgovina():
    return controllers.sv_products.show_trgovina()

@f_app.route('/trgovina', methods=['POST'])
@login_required()  # Locked to logged-in users (any role)
def trgovina_post():
    return controllers.sv_kosarica.add_to_cart()

@f_app.get('/vprasanja')
def qa():
    return controllers.sv_qa.show_questions()

@f_app.get('/registracija')
def registracija_get():
    return controllers.sv_registracija.prikazi_registracijo()

@f_app.post('/registracija')
def registracija_post():
    return controllers.sv_registracija.obdelaj_registracijo()

@f_app.get('/prijava')
def prijava_get():
    return controllers.sv_prijava.prikazi_prijavo()

@f_app.post('/prijava')
def prijava_post():
    return controllers.sv_prijava.obdelaj_prijavo()

@f_app.get('/odjava')
@login_required()  # user must be logged in to log out
def odjava():
    return controllers.sv_odjava.odjava()

f_app.secret_key = "delta2secure"

@f_app.route('/insert_product', methods=['GET', 'POST'])
@login_required(role='employee')  # employee only
def insert_product():
    return controllers.sv_products.insert_product()

@f_app.get('/izpis_kosarice')
@login_required()  # logged-in users only
def izpis_kosarice():
    return controllers.sv_kosarica.izpis_kosarice()

@f_app.route('/zaposleni', methods=['GET'])
@login_required(role='employee')  # employee only
def zaposleni_get():
    return controllers.sv_zaposleni.obrazec_zaposlenih()

@f_app.route('/zaposleni', methods=['POST'])
@login_required(role='employee')  # employee only
def zaposleni_post():
    return controllers.sv_zaposleni.shrani_zaposlenega()

@f_app.get('/menjava_gesla')
@login_required()  # logged-in users only
def menjava_gesla_get():
    return controllers.sv_menjava_gesla.prikazi_menjava_gesla()

@f_app.post('/menjava_gesla')
@login_required()  # logged-in users only
def menjava_gesla_post():
    return controllers.sv_menjava_gesla.obdelaj_menjava_gesla()

@f_app.get('/profil')
@login_required()  # logged-in users only
def profil():
    return controllers.sv_profil.prikazi_profil()

@f_app.route("/pozabljeno_geslo/<token>", methods=["GET"])
def obrazec_ponastavi(token):
    return sv_pozabljeno_geslo.prikazi_obrazec_za_nastavitev_gesla(token)

@f_app.route("/pozabljeno_geslo/<token>", methods=["POST"])
def shrani_novo_geslo(token):
    return sv_pozabljeno_geslo.shrani_novo_geslo(token)

@f_app.route("/pozabljeno_geslo", methods=["POST"])
def pozabljeno_geslo():
    return sv_pozabljeno_geslo.zahtevaj_ponastavitev()

@f_app.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    print(f"[DEBUG] Prejeti token iz URL-ja: {token}")
    email = sv_uporabnik.Uporabnik.preveri_reset_token(token)
    print(f"[DEBUG] Vrnjeni email iz baze: {email}")
    if email is None:
        return "Token ne obstaja ali je potekel"
    # nadaljuj ...

@f_app.route('/najbolj_prodajani', methods=['GET', 'POST'])
def najbolj_prodajani():
    return controllers.sv_products.show_best_selling()

@f_app.get('/products/search')
def products_search():
    return controllers.sv_products.search_products()

@f_app.get('/kontakt_prebrano')
@login_required(role='employee')  # employee only
def kontakt_prebrano():
    return controllers.sv_contact.show_all_contact_requests()

@f_app.route('/seznam_zaposlenih')
@login_required(role='employee')  # employee only
def seznam_zaposlenih():
    return controllers.sv_zaposleni.seznam_zaposlenih()

@f_app.route('/vpogled_narocila/<int:narocilo_id>', methods=['GET', 'POST'])
@login_required()  # logged-in users only
def vpogled_narocila(narocilo_id):
    return controllers.sv_narocila.izpis_narocila(narocilo_id)

@f_app.get('/vracila')
@login_required(role='user')  # ✅ Only regular users
def show_vracilo():
    return controllers.sv_vracilo.show_vracilo()


@f_app.get('/stores')
@login_required(role='employee')  # employee only
def stores_get():
    return controllers.sv_poslovalnica.show_store_form()

@f_app.post('/stores')
@login_required(role='employee')  # employee only
def stores_post():
    return controllers.sv_poslovalnica.save_store()

@f_app.route('/arrived', methods=['POST'])
@login_required(role='employee')  # employee only
def arrived():
    user = session.get('user')
    employee_id = user.get('employeeID')
    if employee_id:
        models.sv_prihodi_odhodi.log_arrival(employee_id)
    else:
        print("[ERROR] employeeID not found in session!")
    return redirect(url_for('home'))

@f_app.route('/left', methods=['POST'])
@login_required(role='employee')  # employee only
def left():
    user = session.get('user')
    employee_id = user.get('employeeID')
    if employee_id:
        models.sv_prihodi_odhodi.log_departure(employee_id)
    else:
        print("[ERROR] employeeID not found in session!")
    return redirect(url_for('home'))

@f_app.get('/order_history')
@login_required()  # logged-in users only
def order_history():
    return controllers.sv_narocila.order_history()

@f_app.get('/izpis_racuna')
@login_required()  # logged-in users only
def izpis_racuna():
    return controllers.sv_kosarica.izpis_racuna()

@f_app.route("/wishlist/odstrani", methods=["POST"])
@login_required()  # logged-in users only
def wishlist_odstrani():
    return controllers.sv_kosarica.odstrani_iz_wishlist()

@f_app.route("/wishlist/dodaj", methods=["POST"])
@login_required()  # logged-in users only
def dodaj_na_wishlist():
    return controllers.sv_kosarica.dodaj_na_wishlist()

@f_app.route("/wishlist", methods=["GET"])
@login_required()  # logged-in users only
def prikazi_wishlist():
    return controllers.sv_kosarica.prikazi_wishlist()

@f_app.route('/insert_promo', methods=['GET', 'POST'])
@login_required(role='employee')  # employee only
def insert_promo():
    return controllers.sv_promo.insert_promo()

@f_app.get('/vracila')
@login_required(role='employee')  # employee only
def show_all_vracila():
    return controllers.sv_vracilo.show_all_vracila()

@f_app.route('/insert_qa', methods=['GET', 'POST'])
@login_required(role='employee')  # employee only
def insert_qa():
    return controllers.sv_qa_insert.insert_question()