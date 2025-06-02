from flask import request, render_template
import models.sv_poslovalnica

def show_store_form():
    return render_template('sv_poslovalnica.html')

def save_store():
    ime = request.form.get('ime')
    naslov = request.form.get('naslov')
    telefon = request.form.get('telefon')
    models.sv_poslovalnica.insert_store(ime, naslov, telefon)
    return render_template('sv_poslovalnica.html', response="Poslovalnica uspešno dodana!")