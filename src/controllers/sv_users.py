from flask import request, render_template

import models.sv_user

def show_users():
    users = models.sv_user.get_users()
    return render_template('sv_users.html', users=users)
