import json
import urllib
import urllib.parse
import uuid

from flask import redirect, jsonify, request, Response
from oauthlib.oauth1 import SIGNATURE_HMAC, SIGNATURE_TYPE_AUTH_HEADER, Client
from requests_oauthlib import OAuth1Session

from .db import Database
from .config import CONFIG

from pprint import pprint as pp

CONSUMER_SECRET = CONFIG.CONSUMER_SECRET
CONSUMER_KEY = CONFIG.CONSUMER_KEY

ACCESS_TOKEN_URL = "https://websignon.warwick.ac.uk/oauth/accessToken"
AUTHORISE_URL = "https://websignon.warwick.ac.uk/oauth/authorise?"
REQUEST_TOKEN_URL = "https://websignon.warwick.ac.uk/oauth/requestToken?"

SCOPES = "urn:websignon.warwick.ac.uk:sso:service urn:tabula.warwick.ac.uk:tabula:service"

db_data = Database("db.sqlite3")


class CustomClient(Client):
    def _render(self, request, formencode=False, realm=None):
        request.headers["User-Agent"] = "A useful user agent for ITS"
        return super()._render(request, formencode, realm)


# @app.route("/oauth/begin")
def get_begin_oauth():
    base_url = get_base_url()
    return get_redirect_to_authorise_url("%s/oauth/authorised" % base_url)


def get_base_url():
    return "http://localhost:5000"


def get_redirect_to_authorise_url(callback, expiry="forever"):
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET,
                          signature_method=SIGNATURE_HMAC,
                          signature_type=SIGNATURE_TYPE_AUTH_HEADER, client_class=CustomClient,
                          callback_uri=callback)
    resp = oauth.fetch_request_token(
        url=REQUEST_TOKEN_URL + urllib.parse.urlencode({"scope": SCOPES, "expiry": expiry}))

    db_data.add_secret_for_token(resp['oauth_token'], resp['oauth_token_secret'])
    authorise_qs = urllib.parse.urlencode({"oauth_token": resp['oauth_token']})
    return redirect(AUTHORISE_URL + authorise_qs, code=302)


# @app.route("/oauth/authorised")
def get_authorised_oauth():
    generated_uuid = generate_and_store_uuid()
    # uuid_data = {"uuid": generated_uuid}
    return generated_uuid


def generate_and_store_uuid():
    last_secret = db_data.get_secret_for_token(request.args.get("oauth_token"))
    if last_secret is None:
        raise Exception("Couldn't find that OAuth token")
    last_secret = str(last_secret)
    oauth = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, resource_owner_secret=last_secret, client_class=CustomClient)
    oauth.parse_authorization_response(request.url)
    access = oauth.fetch_access_token(ACCESS_TOKEN_URL)
    generated_uuid = str(uuid.uuid1())
    db_data.add_token_for_uuid(generated_uuid, access['oauth_token'])
    db_data.add_secret_for_token(access['oauth_token'], access['oauth_token_secret'])

    return generated_uuid


# @app.route("/oauth/userInfo")
def get_warwick_info():
    oauth = _get_oauth_session_for_request()
    end_data = get_warwick_data_using_oauth(oauth)
    return jsonify(end_data)


def get_warwick_data_using_oauth(oauth):
    resp = oauth.request("POST", "https://websignon.warwick.ac.uk/oauth/authenticate/attributes")
    content = str(resp.content, "UTF-8").strip()
    end_data = {"data": {}}
    for item in content.split("\n"):
        if "=" not in item:
            continue
        name = item[0:item.find("=")]
        value = item[item.find("=") + 1:]
        end_data["data"][name] = value
    return end_data


# @app.route("/oauth/tabula/events/")
def get_upcoming_events():
    oauth = _get_oauth_session_for_request()
    url_reqd = "https://tabula.warwick.ac.uk/api/v1/member/me/timetable/events"
    resp = oauth.request("GET", url_reqd)
    print(resp.text)
    end_data = resp.json()['events']

    print(json.dumps(end_data))
    return Response(json.dumps(end_data), mimetype='application/json')

# @app.route("/oauth/tabula/assignments/")
def get_assignments(oauth_uuid=None):
    oauth = _get_oauth_session_for_request(oauth_uuid)

    url_reqd = "https://tabula.warwick.ac.uk/api/v1/member/me/assignments"
    resp = oauth.request("GET", url_reqd)
    end_data = resp.json()

    return end_data
    # return Response(json.dumps(end_data), mimetype='application/json')

def get_user_info(oauth_uuid=None):
    oauth = _get_oauth_session_for_request(oauth_uuid)

    url_reqd = "https://tabula.warwick.ac.uk/api/v1/member/me"
    resp = oauth.request("GET", url_reqd)
    end_data = resp.json()
    member = end_data["member"]

    return member

def get_attendance(begin:int, end:int, oauth_uuid=None):
    oauth = _get_oauth_session_for_request(oauth_uuid)

    end_data = []
    for year in range(begin, end):
        url_reqd = f"https://tabula.warwick.ac.uk/api/v1/member/me/attendance/{year}"
        resp = oauth.request("GET", url_reqd)
        end_data.append(resp.json())

    print("attendance")
    pp(end_data)
    print()

    return end_data

def _get_oauth_session_for_request(oauth_uuid=None):
    if oauth_uuid is None:
        if "uuid" not in request.args:
            raise Exception("No user UUID provided")
        this_uuid = request.args.get("uuid")
    else:
        this_uuid = oauth_uuid
    access_token = db_data.get_token_for_uuid(this_uuid)
    if access_token is None:
        raise Exception("Couldn't find an associated access token for that UUID")
    access_token = str(access_token)
    access_token_secret = db_data.get_secret_for_token(access_token)
    if access_token_secret is None:
        raise Exception("Couldn't find secret")
    access_token_secret = str(access_token_secret)

    oauth = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, resource_owner_key=access_token,
                    resource_owner_secret=access_token_secret, client_class=CustomClient)
    return oauth

def get_uuid_from_cookie():
    return request.cookies.get("uuid")