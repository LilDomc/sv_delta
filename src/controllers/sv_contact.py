from flask import request, render_template

import models.sv_contact_form

def show_contact_form():
    return render_template("sv_contact_form.html") ## TODO actually create the frontend!!  

def save_contact_request():
    email = request.form.get('email')
    message = request.form.get('message')
    name = request.form.get('name')
    contact_form = models.sv_contact_form.ContactForm(email=email, message=message, name=name)
    contact_form.save()

    return render_template('sv_contact_form.html', response="Hvala ker ste nas kontaktirali! Odgovorili vam bomo v najkrajsem moznem času!")

def show_all_contact_requests():
    messages = models.sv_contact_form.get_contact_messages()
    return render_template('sv_contact_form_read.html', messages=messages)