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
    return sso.get_authorised_oauth()

@app.route("/oauth/userInfo")
def get_warwick_info():
    return sso.get_warwick_info()

@app.route("/oauth/tabula/events/")
def get_upcoming_events():
    return sso.get_upcoming_events()

@app.route("/oauth/tabula/assignments/")
def get_assignments():
    return sso.get_assignments()
