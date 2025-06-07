from flask import render_template, request
from datetime import datetime, timedelta

def prikazi_dostavo():
    izbran_datum = None

    if request.method == "POST":
        izbran_datum = request.form.get("datum_dostave")

    min_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    return render_template("sv_dostava.html", min_date=min_date, izbran_datum=izbran_datum)
