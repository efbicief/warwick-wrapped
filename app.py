# pylint: disable=missing-function-docstring
from flask import Flask, render_template , make_response
import sso
import dataFormat
import sys

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


@app.route("/")
def home():
    return render_template('homepage.html')

@app.route("/start")
def start():
    return render_template('start.html')

@app.route("/PrivacyPolicy")
def privacy():
    return render_template('PrivacyPolicy.html')

@app.route("/oauth/info")
def oauthInfo():
    return render_template('OAuthInfo.html')

@app.route("/oauth/begin")
def get_begin_oauth():
    return sso.get_begin_oauth()

@app.route("/oauth/authorised")
def get_authorised_oauth():
    uuid = sso.get_authorised_oauth()
    response = make_response( render_template("uuid.html") )
    print(uuid, file=sys.stderr)
    response.set_cookie( "uuid",uuid )
    return response


@app.route("/oauth/endpoint")
def get_endpoint():
    uuid = sso.get_cookie_uuid()
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

@app.route("/results")
def renderResults():
    uuid = sso.get_cookie_uuid()
    data = dataFormat.UserData(None)
    return render_template('Results.html'
                           ,user_name=data.user_info.name
                           ,year_of_study=data.user_info.year_of_study
                            ,degree=data.user_info.degree)


# @app.route("/oauth/tabula/assignments/")
# def get_assignments(uuid):
#     return sso.get_assignments(uuid)

if __name__ == "__main__":
    app.run(debug=True)