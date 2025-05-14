from flask import redirect, session
from models.sv_uporabnik import Uporabnik

def odjava():
    Uporabnik.odjavi()
    session.pop("uporabnik", None)
    return redirect("/")
