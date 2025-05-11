from flask import Flask

import controllers.index
import controllers.sv_hello
import controllers.sv_setup
import controllers.sv_users
import controllers.sv_products

f_app = Flask(__name__)
#tuki se napiše pot to controllers

if __name__ == "__main__":
    setup_db()
    app.run(debug=True)

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

@f_app.get('/products')
def products():
    return controllers.sv_products.show_products()




