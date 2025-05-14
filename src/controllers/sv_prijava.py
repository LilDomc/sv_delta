from flask import request, redirect, render_template, session
from models.sv_uporabnik import Uporabnik

def prikazi_prijavo():
    return render_template("sv_prijava.html")

def obdelaj_prijavo():
    email = request.form.get("email")
    geslo = request.form.get("geslo")

    if Uporabnik.prijavi(email, geslo):
        session["uporabnik"] = {
            "email": email
            # Lahko dodaš več info iz baze kasneje
        }
        return redirect("/")
    else:
        return render_template("prijava.html", napaka="Napačen email ali geslo.")
