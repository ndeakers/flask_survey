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
    session["responses"] = []
    #session["questions_already_answered"] = []
    title = survey.title
    instructions = survey.instructions
    return render_template('survey_start.html',
                           survey_title=title,
                           survey_instructions=instructions)


#if the current question_num is greater than length of questions_already_answered,
#  or quesiotns in survery (-1),
# check if their list starts with 0, if so, redirect them to the appropirate question number
# page. use the length of questions_Alraedy_asnwered as the url to redirect.

@app.route('/questions/<int:question_num>')
def show_question(question_num):
    # answered_list = session["questions_already_answered"]
    # answered_length = len(answered_list)
    # if answered_length != question_num:
    #     return redirect(f'/questions/{answered_length}')
    # else:
        question_list = survey.questions
        question_instance = question_list[question_num]
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

    responses = session['responses']
    answer = request.form['answer']
    responses.append(answer)
    session['responses'] = responses

    print("session[responses] =", session["responses"])

    previous_question_num = int(request.form['question_num']) #don't be safe when you don't need it. let it crash
    if previous_question_num < len(survey.questions) - 1: #flip this
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
