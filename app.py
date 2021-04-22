from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_homepage():
    title = survey.title
    instructions = survey.instructions
    return render_template('survey_start.html',
                           survey_title=title,
                           survey_instructions=instructions)

@app.route('/questions/<question_num>')
def show_question(question_num):
    question_list = survey.questions
    question_instance = question_list[int(question_num)]
    current_question = question_instance.question
    print('current question: ', current_question)
    return render_template('question.html',
                           current_question=current_question)
