from flask import render_template, redirect, session
from models.sv_uporabnik import Uporabnik

def prikazi_profil():
    if not Uporabnik.je_prijavljen():
        return redirect("/prijava")

    uporabnik = Uporabnik.pridobi_trenutnega_uporabnika()
    return render_template("sv_profil.html", uporabnik=uporabnik)
