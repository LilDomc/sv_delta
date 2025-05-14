from flask import request, redirect, render_template, session
from models.sv_uporabnik import Uporabnik

def prikazi_registracijo():
    return render_template("sv_registracija.html")

def obdelaj_registracijo():
    ime = request.form.get("ime")
    priimek = request.form.get("priimek")
    email = request.form.get("email")
    geslo = request.form.get("geslo")

    if not ime or not priimek or not email or not geslo:
        return render_template("registracija.html", napaka="Vsa polja so obvezna.")

    if Uporabnik.registriraj(ime, priimek, email, geslo):
        session["uporabnik"] = {
            "ime": ime,
            "priimek": priimek,
            "email": email
        }
        return redirect("/")
    else:
        return render_template("registracija.html", napaka="Registracija ni uspela.")
