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
    choices = question_instance.choices
    return render_template('question.html',
                           current_question=current_question,
                           choices=choices,
                           question_num=question_num)


@app.route('/answer', methods=['POST'])
def handle_answer():
    '''Takes in answer from user and adds value to responses[].
    Redirects user to next question unless they are at end of survey,
    then redirects to thank you page'''
    responses.append(request.form.get('answer'))
    print("responses =", responses)
    previous_question_num = int(request.form.get('question_num'))
    if previous_question_num < len(survey.questions)-1:
        next_question_num = previous_question_num + 1
        return redirect(f'/questions/{next_question_num}')
    else:
        return redirect('/thank_you')

# we are getting the number of the next question in order to create the
# route to redirect to (questions/next_quesiton_num). we will take the previous question number and
# increment by one. BUT if the question number is the lenght of the qustions
# list, then redirect to /thankyou


@app.route('/thank_you')
def say_thanks():
    return render_template('thank_you.html', survey_title=survey.title)
