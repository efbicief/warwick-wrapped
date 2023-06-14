"""
This is the main file for the web application. 
It contains the routes for the webpages and the functions that are
called when the user visits a page.
"""
from flask import Flask, render_template ,redirect,make_response,url_for
import sso
import middleware
from dataFormat import User
from charts import load_chart

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

@app.route("/")
def home():
    """Homepage the first page visited."""
    return render_template('homepage.html')

@app.route("/PrivacyPolicy")
def privacy():
    """Privacy Policy page."""
    return render_template('PrivacyPolicy.html')

@app.route("/oauth/info")
def oauth_info():
    """Imformation about OAuth."""
    return render_template('OAuthInfo.html')

@app.route("/oauth/begin")
def get_begin_oauth():
    """Redirects to the OAuth page."""
    return sso.get_begin_oauth()

@app.route("/oauth/authorised")
def get_authorised_oauth():
    """Recieves the OAuth token and redirects to the results page."""
    uuid = sso.get_authorised_oauth()
    response = redirect("/results", code=302)
    response.set_cookie( "uuid",uuid )
    return response


@app.route("/oauth/endpoint")
def get_endpoint():
    """A temporary page to test the OAuth endpoint."""
    uuid = sso.get_uuid_from_cookie()
    assignments = sso.get_assignments(uuid)
    member = sso.get_user_info(uuid)
    user_submissions = sso.get_assignments(uuid)

    print("print_debug", middleware.get_data(uuid))

    assignment_names = []
    for item in assignments['enrolledAssignments']:
        assignment_names.append(item['name'])
    for item in assignments['historicAssignments']:
        assignment_names.append(item['name'])

    return render_template('assignments.html',\
                        assignments=assignment_names,\
                        member=member,\
                        submissions=user_submissions)

@app.route("/oauth/tabula/events/")
def get_upcoming_events():
    """temporary page to test the upcoming events endpoint."""
    return sso.get_upcoming_events()

@app.route("/results")
def loading():
    """Renders the laodin page that calls /api/results."""
    return render_template('loading.html')

@app.route("/api/results")
def render_results():
    """The primary page of the web application."""
    try:
        uuid = sso.get_uuid_from_cookie()
    except TypeError:
        return redirect("/", code=302)
    if uuid is None:
        return redirect("/", code=302) 
    user_data:User=middleware.convert_to_page(middleware.get_data(uuid))
    # try:
    #     userData=middleware.convert_to_page(middleware.get_data(uuid))
    # except:
    #     return redirect("/", code=302) 

    return render_template('Results.html',userData=user_data)

@app.route("/charts/<chart_id>")
def get_chart(chart_id:str):
    """Returns a chart."""
    image_bytes = load_chart(chart_id)
    response = make_response(image_bytes)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'attachment', filename=f'{chart_id}.png')
    return response



if __name__ == "__main__":
    app.run(debug=True)