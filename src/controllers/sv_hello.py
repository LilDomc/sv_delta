from flask import request, render_template

import models.sv_user

def ask_for_name():
    return render_template("sv_hello.html")

def greet_user():
    name = request.form.get('name')
    user = models.sv_user.User(name)
    greeting = f"Hej, {user.name}!"
    return render_template('sv_hello.html', pozdrav=greeting)
