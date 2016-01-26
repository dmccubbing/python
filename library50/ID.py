from flask import Flask, request, redirect, session
from flask.json import jsonify

import hashlib
import os
import re
import uuid

from requests_oauthlib import OAuth2Session

AUTH_URL = 'https://id.cs50.net/authorize'
TOKEN_URL = 'https://id.cs50.net/token'
OWNER_DETAILS = 'https://id.cs50.net/userinfo'

'''
Client for CS50 ID.
'''
class ID:
    '''
    Configures client for authorization server.
    '''
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        # Authorization server
        self.provider = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

    '''
    Authenticates user via CS50 ID. If user is returning from CS50 ID,
    returns dict of user's claims, else redirects to CS50 ID for
    authentication.

    @param  string  client_id
    @param  string  client_secret
    @param  string  scope

    @return dict    claims
    '''
    @staticmethod
    def authenticate(client_id, client_secret, scope=['openid profile']):
        # set environment variable to bypass SSL necessity
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        # validate scope
        # https://tools.ietf.org/html/rfc6749#appendix-A.4
        # if not re.match(r'/^[\x{21}\x{23}-\x{5B}\x{5D}-\x{7E}]([ \x{21}\x{23}-\x{5B}\x{5D}-\x{7E}])*$/', scope):
        #     raise Exception('Invalid scope!')

        # redirection URI
        redirect_uri = request.base_url

        # configure client
        id = ID(client_id, client_secret, redirect_uri, scope)

        # if user is returning from CS50 ID, return claims
        if request.args.get('code', '') and request.args.get('state'):
            return id.getUser(client_id, client_secret)

        # redirect to CS50 ID
        url, state = id.getLoginUrl()
        return redirect(url)

    '''
    Returns URL to which user should be redirected for authentication via CS50 ID.

    @return string url
    '''
    def getLoginUrl(self):
        # return OP endpoint URL with CSRF protection
        # create UUID and store it in Flask's session to be hashed and de-hashed later
        uuid_str = str(uuid.uuid4())
        session['id50'] = uuid_str

        return self.provider.authorization_url(AUTH_URL, state=hashlib.sha256(session['id50']))

    '''
    Gets claims from an Authorization Response.

    @return array|false claims
    '''
    def getUser(self, client_id, client_secret):
        # if returning from CS50 ID
        if not request.args.get('code', ''):
            raise Exception('Missing code!')

        # validate state to prevent CSRF
        if not request.args.get('state', ''):
            raise Exception('Missing state in request!')
            return False

        if request.args.get('state', '') != hashlib.sha256(session['id50']):
            raise Exception('Invalid state!')
            return False

        # exchange code for token
        try:
            token = self.provider.fetch_token(TOKEN_URL, client_secret=client_secret, authorization_response=request.url)
        except:
            print 'Error fetching token!'
            return False

        # get UserInfo with token
        try:
            self.provider = OAuth2Session(client_id, token=token)
            owner = jsonify(self.provider.get(OWNER_DETAILS).json())
            return owner
        except:
            print 'Error grabbing UserInfo!'
            return False

app = Flask(__name__)

client_id = 'http://127.0.0.1:5000/'
client_secret = 'cogden/cogden'

@app.route('/')
def main():
    return ID.authenticate(client_id, client_secret)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)
