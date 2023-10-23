import json
import logging

from flask import Flask, g, render_template
from flask_oidc import OpenIDConnect
import requests

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False, # Si vrai cookie envoyé que sous https
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True, # si vrai, le client peut accéder à des infos utilisateur
    'OIDC_SCOPES': ['openid', 'email', 'profile', 'roles'], # précise les informations qui vont être accessible par le client
    'OIDC_OPENID_REALM': 'primx',
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_TOKEN_TYPE_HINT': 'access_token'
})

oidc = OpenIDConnect(app)


@app.route('/')
def hello_world():
    if oidc.user_loggedin:
        return render_template('index.html', login = "true", name = oidc.user_getfield('preferred_username'))
    else:
        return render_template('index.html', login = "false")


@app.route('/private')
@oidc.require_login
def hello_me():
    """Example for protected endpoint that extracts private information from the OpenID Connect id_token.
       Uses the accompanied access_token to access a backend service.
    """

    info = oidc.user_getinfo(['preferred_username', 'email', 'sub', 'name', 'phone number'])
    token = oidc.get_cookie_id_token()

    username = info.get('preferred_username')
    email = info.get('email')
    user_id = info.get('sub')
    name = info.get('name')
    groups = info.get('phone number')
    if user_id in oidc.credentials_store:
        from oauth2client.client import OAuth2Credentials
        access_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).access_token
        print( 'access_token=<%s>' % access_token)
        headers = {'Authorization': 'Bearer %s' % (access_token)}
        # YOLO
        print( "Could not access greeting-service")
        greeting = "Hello %s (%s)" % (name, username)


    return render_template('private.html', greeting = greeting, email = email, uid = user_id, grp=groups, tkn= json.dumps(token,sort_keys = False, indent=4, separators = (',', ': ')))


@app.route('/api', methods=['POST'])
@oidc.accept_token(require_token=True, scopes_required=['openid'])
def hello_api():
    """OAuth 2.0 protected API endpoint accessible via AccessToken"""

    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})


@app.route('/logout')
def logout():
    """Performs local logout by removing the session cookie."""

    oidc.logout()
    return render_template('logout.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')