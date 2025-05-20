from flask import request, redirect, render_template
import models.sv_user

def obrazec_zaposlenih():
    return render_template('sv_zaposleni.html')

def shrani_zaposlenega():
    form = request.form
    models.sv_user.add_user(form)
    return redirect('/zaposleni')