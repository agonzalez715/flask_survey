# This is app.py
# It should contain Flask imports, app instance, routes, and the server run command.

from flask import Flask, request, render_template, redirect
from surveys import satisfaction_survey, surveys  # Import surveys from surveys.py

app = Flask(__name__)

# Now you can define your responses list and routes
responses = []

@app.route('/')
def survey_start():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('start.html', title=title, instructions=instructions)


# in app.py add a new route that will display the current question based on the question_id provided in the URL
@app.route('/questions/<int:question_id>')
def show_question(question_id):
 # check if tryinf to access questions out of order
    if question_id != len(responses):
     # Redirect to the current question
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[question_id]
    return render_template('question.html', question=question)



@app.route('/answer', methods=["POST"])
def handle_answer():
    # retreive the selected answer from the form data
    selected_choice = request.form['answer']

    # append the selected answer to the responses list
    responses.append(selected_choice)

    # determine the next question id
    next_question_id = len(responses)

    # check if we have answered all questions
    if next_question_id == len(satisfaction_survey.questions):
        # if so redirect to the survey completion page
        return redirect('/completion')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/completion')
def survey_completion():
    return render_template('completion.html')

if __name__ == '__main__':
    app.run(debug=True)