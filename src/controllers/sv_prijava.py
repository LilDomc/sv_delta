import uuid
import urllib.parse

from flask import request, redirect, render_template, session, flash, url_for
from models.sv_uporabnik import Uporabnik
#import sv_send

# začasen slovar za shranjevanje tokenov (v praksi uporabi DB ali Redis)
reset_tokens = {}

def prikazi_prijavo():
    return render_template("sv_prijava.html")

def obdelaj_prijavo():
    action = request.form.get("action")

    if action == "login":
        email = request.form.get("email")
        geslo = request.form.get("geslo")

        if Uporabnik.prijavi(email, geslo):
            return redirect("/")
        else:
            return render_template("sv_prijava.html", napaka="Napačen email ali geslo.")

    elif action == "reset":
        reset_email = request.form.get("reset_email")
        uporabnik = Uporabnik.poisci_po_emailu(reset_email)

        if uporabnik:
            token = str(uuid.uuid4())
            Uporabnik.shrani_reset_token(reset_email, token)
            povezava = url_for('obrazec_ponastavi', token=token, _external=True)

            base_url = "https://drofenik.eu/faks"
            geslo = "f2ddd40837baa505b8db98b88a73ba222c4034f988dd86890dd9aca9b14835f0"

            email = reset_email#"nameless9876543@gmail.com"
            subject = f"Pozabljeno geslo [{Uporabnik.getTokenID(token)}]"
            message = (
                "Pozdravljeni!\n\n"
                "Spodaj imate obnovitveni url naslov, da si lahko nastavite novo geslo. "
                "Naslov je veljaven 1 uro od poslane zahteve.\n"
                f"{povezava}\n\n"
                "Hvala za zaupanje in lep pozdrav!\nEkipa Delta"
            )

            # URL-enkodiraj vse parametre posebej
            email_enc = urllib.parse.quote(email, safe='')
            subject_enc = urllib.parse.quote(subject, safe='')
            message_enc = urllib.parse.quote(message, safe='')

            # Sestavi URL z zakodiranimi parametri
            url = f"{base_url}/{geslo}/{email_enc}/{subject_enc}/{message_enc}"

            # Pošlji GET zahtevek (ker je tvoj PHP API verjetno GET preko URL)
            response = requests.get(url)

            # Izpiši rezultat
            print("Status code:", response.status_code)
            print("Response:", response.text)
            #############################
            flash("Na e-mail smo vam poslali obnovitveni url naslov")
        else:
            flash("Uporabnik s tem e-mail naslovom ne obstaja.")

        return render_template("sv_prijava.html")

