from flask import request, redirect, render_template
import models.sv_qa_insert

def insert_question():
    if request.method == 'POST':
        vprasanje = request.form['vprasanje']
        odgovor = request.form['odgovor']

        models.sv_qa_insert.insert_question_and_answer(vprasanje, odgovor)
        return redirect('/insert_qa')

    return render_template('sv_insert_qa.html')
