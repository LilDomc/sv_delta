from flask import request, redirect, render_template
import models.sv_qa

def show_questions():
    models.sv_qa.insert_test_data_qa()
    questions = models.sv_qa.get_questions_answers()
    return render_template('qa.html', questions=questions)
