import logging
from uuid import uuid4
import requests
from logging.config import dictConfig

from flask import Flask
from flask import url_for
from requests_oauthlib import OAuth2Session
from flask import request
import jwt
from jwt import PyJWKClient
from jwt.exceptions import DecodeError
from werkzeug.exceptions import InternalServerError, Unauthorized

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config["SECRET_KEY"] = str(uuid4())


IDP_CONFIG = {
  "well_known_url": "http://172.27.0.1:8080/realms/master/.well-known/openid-configuration",
  "client_id": "account",
  "client_secret": "NEuQmakWzsV7v0R7rcBA2zYKEfnBgah4",
  "scope": ["profile", "email", "openid"]
}

IDP_CONFIG_LOCAL = {
  "well_known_url": "http://localhost:8080/realms/master/.well-known/openid-configuration",
  "client_id": "account",
  "client_secret": "NEuQmakWzsV7v0R7rcBA2zYKEfnBgah4",
  "scope": ["profile", "email", "openid"]
}

def get_well_known_metadata_local():
    logging.info('&requestingggg...'+ IDP_CONFIG_LOCAL["well_known_url"])
    response = requests.get(IDP_CONFIG_LOCAL["well_known_url"])
    logging.info('&&&&&&&&&&&&&'+ str(response.json()))
    response.raise_for_status()
    return response.json()

def get_well_known_metadata():
    logging.info('&requestingggg...'+ IDP_CONFIG["well_known_url"])
    response = requests.get(IDP_CONFIG["well_known_url"])
    logging.info('&&&&&&&&&&&&&'+ str(response.json()))
    response.raise_for_status()
    return response.json()


def get_oauth2_session(**kwargs):
    oauth2_session = OAuth2Session(IDP_CONFIG["client_id"],
                                   scope=IDP_CONFIG["scope"],
                                   redirect_uri=url_for(".callback", _external=True),
                                   **kwargs)
    return oauth2_session


from flask import redirect, session


@app.route("/login")
def login():
    logging.info('Hello, log')
    logging.info('checking.............')
    well_known_metadata = get_well_known_metadata()
    logging.info('******************', well_known_metadata)
    oauth2_session = get_oauth2_session()
    authorization_url, state = oauth2_session.authorization_url(well_known_metadata["authorization_endpoint"])
    session["oauth_state"] = state
    return redirect(authorization_url)
    # return 'dummy'

@app.route("/ll")
def login_local():
    logging.info('Hello, local')
    well_known_metadata = get_well_known_metadata_local()
    logging.info('******************', well_known_metadata)
    oauth2_session = get_oauth2_session()
    authorization_url, state = oauth2_session.authorization_url(well_known_metadata["authorization_endpoint"])
    session["oauth_state"] = state
    return redirect(authorization_url)


IDP_CONFIG_SIGNIN = {
  "token_endpoint": "http://127.0.0.1:8080/realms/master/protocol/openid-connect/token",
  "client_id": "account",
  "client_secret": "NEuQmakWzsV7v0R7rcBA2zYKEfnBgah4",
  "scope": ["profile", "email", "openid"]
}

@app.route('/signin')
def login_sign():
    logging.info('signing.....')
    resp = requests.post(
    IDP_CONFIG_SIGNIN["token_endpoint"],
    data={
            "client_id": IDP_CONFIG_SIGNIN["client_id"],
            "username": admin,
            "password": admin,
            "grant_type": "password",
        }
    )
    logging.info('&&&&&&&&&&&&&'+ str(resp.json()))
    resp.raise_for_status()
    return resp.json()


@app.route("/callback")
def callback():
    well_known_metadata = get_well_known_metadata()
    oauth2_session = get_oauth2_session(state=session["oauth_state"])
    tok = oauth2_session.fetch_token(well_known_metadata["token_endpoint"],
                                                        client_secret=IDP_CONFIG["client_secret"],
                                                        code=request.args["code"])
    app.logger.debug(tok)
    session["id_token"] = tok["id_token"]
    return "ok"

@app.route("/hello")
def get_user_token():
    return "<code>"+ session["id_token"] + "</code>"



# def get_jwks_client():
#     well_known_metadata = get_well_known_metadata()
#     jwks_client = PyJWKClient(well_known_metadata["jwks_uri"])
#     return jwks_client


# jwks_client = get_jwks_client()


# @app.before_request
# def verify_and_decode_token():
#     if request.endpoint not in {"login", "callback"}:
#         if "Authorization" in request.headers:
#             token = request.headers["Authorization"].split()[1]
#         elif "id_token" in session:
#             token = session["id_token"]
#         else:
#             return Unauthorized("Missing authorization token")

#         try:
#             signing_key = jwks_client.get_signing_key_from_jwt(token)
#             header_data = jwt.get_unverified_header(token)
#             request.user_data = jwt.decode(token,
#                                            signing_key.key,
#                                            algorithms=[header_data['alg']],
#                                            audience=IDP_CONFIG["client_id"])
#         except DecodeError:
#             return Unauthorized("Authorization token is invalid")
#         except Exception as e:
#             app.logger.error(e)
#             return InternalServerError("Error authenticating client")


@app.route("/user/id")
def get_user_id():
    return request.user_data


if __name__ == "__main__":
    app.run()
