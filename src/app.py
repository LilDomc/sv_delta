import controllers.sv_contact
import controllers.sv_kosarica
from flask import Flask

import controllers.index
import controllers.sv_qa
import controllers.sv_setup
import controllers.sv_products
import models
import models.sv_backend
import models.sv_products
import models.sv_trgovina
import models.sv_kosarica
import models.sv_qa
import models.sv_narocila

import controllers.sv_registracija
import controllers.sv_prijava
import controllers.sv_odjava
import controllers.sv_zaposleni
import controllers.sv_narocila

f_app = Flask(__name__) # F stands for fu***ng

# to bi mogl bit znotrej main funkcije se mi zdi ... sej ta koda se ne bo uporabljala
# kot module tko da naceloma ne bi smelo biti problema ampak samo za dobro prakso :) 
models.sv_backend.setup_all_db_tables()     #zakomentirati če se zakomentira funkcija v sv_users
models.sv_user.insert_test_users()
models.sv_products.insert_test_data()

if __name__ == "__main__":
    f_app.run(debug=True)


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
def products():
    return controllers.sv_products.show_products()

@f_app.route('/rate', methods=['POST'])
def rate():
    return controllers.sv_products.rate_product()

@f_app.get('/trgovina')
def trgovina():
    return controllers.sv_products.show_trgovina()

@f_app.route('/trgovina', methods=['POST'])
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
def odjava():
    return controllers.sv_odjava.odjava()

f_app.secret_key = "delta2secure" #NUJNO POTREBEN SUPER SKRIVNI KLJUČ, ZA DELOVANJE SEJ ~ Luka Drofenik

@f_app.route('/insert_product', methods=['GET', 'POST'])
def insert_product():
    return controllers.sv_products.insert_product()
 
@f_app.get('/izpis_kosarice')
def izpis_kosarice():
    return controllers.sv_kosarica.izpis_kosarice()

@f_app.route('/zaposleni', methods=['GET'])
def zaposleni_get():
    return controllers.sv_zaposleni.obrazec_zaposlenih()

@f_app.route('/zaposleni', methods=['POST'])
def zaposleni_post():
    return controllers.sv_zaposleni.shrani_zaposlenega()

@f_app.route('/najbolj_prodajani', methods=['GET', 'POST'])
def najbolj_prodajani():
    return controllers.sv_products.show_best_selling()

@f_app.get('/products/search')
def products_search():
    return controllers.sv_products.search_products() 

@f_app.get('/kontakt_prebrano')
def kontakt_prebrano():
    return controllers.sv_contact.show_all_contact_requests()

@f_app.route('/seznam_zaposlenih')
def seznam_zaposlenih():
    return controllers.sv_zaposleni.seznam_zaposlenih()

@f_app.route('/vpogled_narocila/<int:narocilo_id>', methods=['GET', 'POST'])
def vpogled_narocila(narocilo_id):
    return controllers.sv_narocila.izpis_narocila(narocilo_id)
