import controllers.sv_contact
import controllers.sv_kosarica
from flask import Flask

import controllers.index
import controllers.sv_hello
import controllers.sv_setup
import controllers.sv_users
import controllers.sv_products
import models
import models.sv_backend
import models.sv_products
import models.sv_trgovina
import models.sv_kosarica
import models.sv_qa

f_app = Flask(__name__) # F stands for fu***ng
#tuki se napiše pot to controllers

if __name__ == "__main__":
    models.sv_backend.setup_all_db_tables()
    f_app.run(debug=True)


@f_app.get('/')
def home():
    return controllers.index.home()

@f_app.get('/hello')
def hello_ask():
    return controllers.sv_hello.ask_for_name()

@f_app.post('/hello')
def hello_greet():
    return controllers.sv_hello.greet_user()

@f_app.get('/setup')
def setup():
    return controllers.sv_setup.setup_db()

@f_app.get('/reset/users')
def reset_users():
    return controllers.sv_setup.reset_users()

@f_app.get('/users')
def users():
    return controllers.sv_users.show_users()

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
