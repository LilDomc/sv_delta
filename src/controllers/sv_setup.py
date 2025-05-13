from flask import request, render_template

import models.sv_contact_form
import models.sv_user

def setup_db():
    tables = {}
    tables['users'] = True == models.sv_user.setup_db() # Ja! ker primerjanje z True res doda tisto posebno noto... berljivost? Ne, hvala.
    tables['contact'] = models.sv_contact_form.setup_db()
    return render_template('sv_setup.html', tables=tables)

def reset_users():
    models.sv_user.reset_db()
    return setup_db()

