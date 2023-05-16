# pylint: disable=missing-function-docstring
from flask import Flask, render_template
import sso

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('homepage.html')

@app.route("/start")
def start():
    return render_template('start.html')

@app.route("/oauth/begin")
def get_begin_oauth():
    return sso.get_begin_oauth()

@app.route("/oauth/authorised")
def get_authorised_oauth():
    uuid = sso.get_authorised_oauth()
    assignments = sso.get_assignments(uuid)

    assignment_names = []
    for item in assignments['enrolledAssignments']:
        assignment_names.append(item['name'])
    for item in assignments['historicAssignments']:
        assignment_names.append(item['name'])

    return render_template('assignments.html', assignments=assignment_names)

@app.route("/oauth/userInfo")
def get_warwick_info():
    return sso.get_warwick_info()

@app.route("/oauth/tabula/events/")
def get_upcoming_events():
    return sso.get_upcoming_events()

# @app.route("/oauth/tabula/assignments/")
# def get_assignments(uuid):
#     return sso.get_assignments(uuid)
