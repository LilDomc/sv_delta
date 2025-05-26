from flask import render_template, request, redirect, session
from models.sv_uporabnik import Uporabnik

def prikazi_menjava_gesla():
    if not Uporabnik.je_prijavljen():
        return redirect("/prijava")
    return render_template("sv_menjava_gesla.html")

def obdelaj_menjava_gesla():
    if not Uporabnik.je_prijavljen():
        return redirect("/prijava")

    staro_geslo = request.form.get("staro_geslo")
    novo_geslo = request.form.get("novo_geslo")
    novo_geslo2 = request.form.get("novo_geslo2")

    if novo_geslo != novo_geslo2:
        return render_template("sv_menjava_gesla.html", napaka="Novo geslo se ne ujema.")

    uporabnik = Uporabnik.pridobi_trenutnega_uporabnika()
    if not Uporabnik.menjava_gesla(uporabnik['email'], staro_geslo, novo_geslo):
        return render_template("sv_menjava_gesla.html", napaka="Staro geslo je napačno.")

    return redirect("/profil")
