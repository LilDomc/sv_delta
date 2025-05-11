from flask import request, render_template

import models.sv_user

def setup_db():
    tables = dict()
    tables['users'] = True == models.sv_user.setup_db()
    return render_template('sv_setup.html', tables=tables)

def reset_users():
    models.sv_user.reset_db()
    return setup_db()

