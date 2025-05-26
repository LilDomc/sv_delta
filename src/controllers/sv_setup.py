from flask import request, render_template

import models.sv_backend

def setup_db():
    models.sv_backend.setup_all_db_tables()
    return render_template('sv_setup.html', tables=tables)

def reset_users():
    models.sv_user.reset_db()
    return setup_db()

