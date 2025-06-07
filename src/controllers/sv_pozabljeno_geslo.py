import hashlib
import time
from flask import request, redirect, render_template, flash
from models.sv_uporabnik import Uporabnik
import traceback

def to_dict_list(reset_tokens):
    return [dict(zip(["token", "email", "created_at"], r)) for r in reset_tokens]
def zahtevaj_ponastavitev():
    try:
        email = request.form.get("reset_email")
        print(f"[DEBUG] Prejet email za ponastavitev: {email}")
        user = Uporabnik.najdi_po_emailu(email)
        print(f"[DEBUG] Rezultat iskanja uporabnika po emailu: {user}")

        if user:
            token = hashlib.sha256((email + str(time.time())).encode()).hexdigest()
            print(f"[DEBUG] Ustvarjen token: {token}")
            Uporabnik.shrani_reset_token(email, token)
            print(f"[DEBUG] Token shranjen v bazo.")

            reset_link = f"http://localhost:8080/ponastavi-geslo/{token}"
            return render_template("sv_prijava.html", alert_link=reset_link)
        else:
            print("[DEBUG] Uporabnik s tem emailom ne obstaja.")
            return render_template("sv_prijava.html", napaka="Uporabnik s tem emailom ne obstaja.")
    except Exception as e:
        print("[ERROR] Napaka v zahtevaj_ponastavitev:")
        traceback.print_exc()
        return render_template("sv_prijava.html", napaka="Prišlo je do napake. Poskusi ponovno.")

def prikazi_obrazec_za_nastavitev_gesla(token):
    try:
        print(f"[DEBUG] Prejet token za prikaz obrazca: {token}")
        reset_tokens = Uporabnik.vrni_vse_reset_token()
        print(f"[DEBUG] Reset tokeni iz baze: {reset_tokens}")

        # Če reset_tokens vsebujejo tuple (token, email)
        token_map = {r[0]: r[1] for r in reset_tokens}
        print(f"[DEBUG] Token map: {token_map}")

        if token not in token_map:
            print("[DEBUG] Token ni veljaven ali je potekel.")
            return "Neveljavna ali pretekla povezava", 403
        return render_template("sv_pozabljeno_geslo.html")
    except Exception as e:
        print("[ERROR] Napaka v prikazi_obrazec_za_nastavitev_gesla:")
        traceback.print_exc()
        return "Prišlo je do napake. Poskusi ponovno kasneje.", 500

def shrani_novo_geslo(token):
    try:
        print(f"[DEBUG] Prejet token za shranjevanje novega gesla: {token}")
        reset_tokens = Uporabnik.vrni_vse_reset_token()
        print(f"[DEBUG] Reset tokeni iz baze: {reset_tokens}")

        reset_tokens = to_dict_list(reset_tokens)  # <-- dodano
        token_map = {r['token']: r['email'] for r in reset_tokens}
        print(f"[DEBUG] Token map: {token_map}")

        if token not in token_map:
            print("[DEBUG] Token ni veljaven ali je potekel.")
            return "Povezava je neveljavna ali potekla.", 403

        novo = request.form.get("geslo")
        ponovljeno = request.form.get("ponovi_geslo")
        print(f"[DEBUG] Novo geslo: {novo}, Ponovljeno geslo: {ponovljeno}")

        if novo != ponovljeno:
            print("[DEBUG] Gesli se ne ujemata.")
            return render_template("sv_pozabljeno_geslo.html", napaka="Gesli se ne ujemata.")

        email = token_map[token]
        print(f"[DEBUG] Email povezan s tokenom: {email}")
        Uporabnik.spremeni_geslo(email, novo)
        print("[DEBUG] Geslo uspešno spremenjeno.")
        flash("Geslo je bilo uspešno spremenjeno.")
        return redirect("/prijava")
    except Exception as e:
        print("[ERROR] Napaka v shrani_novo_geslo:")
        traceback.print_exc()
        return render_template("sv_pozabljeno_geslo.html", napaka="Prišlo je do napake. Poskusi ponovno.")
