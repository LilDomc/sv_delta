from flask import request, redirect, render_template
import models.sv_user

def obrazec_zaposlenih():
    return render_template('sv_zaposleni.html')

def shrani_zaposlenega():
    form = request.form
    models.sv_user.add_user(form)
    return redirect('/zaposleni')

def seznam_zaposlenih():
    zaposleni = models.sv_user.vsi_zaposleni()
    return render_template('/seznam_zaposlenih.html', zaposleni=zaposleni)