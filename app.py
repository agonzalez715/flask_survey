# This is app.py
# It should contain Flask imports, app instance, routes, and the server run command.

from flask import Flask, request, render_template, redirect, session
from surveys import satisfaction_survey, surveys  # Import surveys from surveys.py
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) # Generate a 32-character (16 bytes) secret key

# Now you can define your responses list and routes
responses = []

@app.route('/', methods=["GET", "POST"])
def survey_start():
    if request.method == "POST":
        session['responses'] = [] #to initialize the responses in session
        return redirect('/questions/0') #redirect to the first question

    title = satisfaction_survey.title
    instructions = satisfaction_survey.title
    return render_template('start.html', title=title, instructions=instructions)
    #this code checks if the request method is POST, and if so, it initializes the responses session variable as an empty list and redirects the user to the first question. otherwise, it renders the start page as before
    


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
    # Retrieve the selected answer from the form data
    selected_choice = request.form['answer']

    # Append the selected answer to the responses in session
    responses = session.get('responses', [])  # Retrieve the existing responses or an empty list
    responses.append(selected_choice)
    session['responses'] = responses  # Update the responses in session

    # Determine the next question ID
    next_question_id = len(responses)

    # Check if we have answered all questions
    if next_question_id == len(satisfaction_survey.questions):
        # If so, redirect to the survey completion page
        return redirect('/completion')
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/completion')
def survey_completion():
    return render_template('completion.html')

if __name__ == '__main__':
    app.run(debug=True)