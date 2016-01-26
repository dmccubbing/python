from flask import Flask, request, redirect, session
from flask.json import jsonify
from flask.wrappers import Request

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
        self.client_secret = client_secret
        self.client_id = client_id

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
        # validate scope
        # https://tools.ietf.org/html/rfc6749#appendix-A.4
        # if not re.match(r'/^[\x{21}\x{23}-\x{5B}\x{5D}-\x{7E}]([ \x{21}\x{23}-\x{5B}\x{5D}-\x{7E}])*$/', scope):
        #     raise Exception('Invalid scope!')

        # redirection URI
        redirect_uri = request.base_url

        # configure client
        id = ID(client_id, client_secret, redirect_uri, scope)

        # if user is returning from CS50 ID, return claims
        if request.args.get('code') and request.args.get('state'):
            return id.getUser(client_id, client_secret)

        # redirect to CS50 ID
        url, state = id.getLoginUrl()
        return redirect(url)

    '''
    Returns URL to which user should be redirected for authentication via CS50 ID.

    @return string url
    '''
    def getLoginUrl(self):
        # set environment variable to bypass SSL necessity
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        # return OP endpoint URL with CSRF protection
        # create UUID and store it in Flask's session to be hashed and de-hashed later
        uuid_str = str(uuid.uuid4())
        session['id50'] = uuid_str

        return self.provider.authorization_url(AUTH_URL, state=hashlib.sha256(session['id50']))

    '''
    Gets claims from an Authorization Response.

    @return array|false claims
    '''
    def getUser(self):
        # if returning from CS50 ID
        if not request.args.get('code'):
            raise Exception('Missing code!')

        # validate state to prevent CSRF
        if not request.args.get('state'):
            raise Exception('Missing state in request!')
            return False

        if request.args.get('state') != hashlib.sha256(session['id50']):
            raise Exception('Invalid state!')
            return False

        # exchange code for token
        try:
            token = self.provider.fetch_token(TOKEN_URL, client_secret=self.client_secret, authorization_response=request.url)
        except:
            print 'Error fetching token!'
            return False

        # get UserInfo with token
        try:
            self.provider = OAuth2Session(self.client_id, token=token)
            owner = jsonify(self.provider.get(OWNER_DETAILS).json())
            return owner
        except:
            print 'Error grabbing UserInfo!'
            return False

# http://stackoverflow.com/questions/19840051/mutating-request-base-url-in-flask
'''
Modifies base URL of request object if using SSL. Replaces regular Request object.
'''
class ProxiedRequest(Request):
    def __init__(self, environ, populate_request=True, shallow=False):
        super(Request, self).__init__(environ, populate_request, shallow)
        # Support SSL termination. Mutate the host_url within Flask to use https://
        # if the SSL was terminated.
        x_forwarded_proto = self.headers.get('X-Forwarded-Proto')
        if x_forwarded_proto == 'https':
            self.url = self.url.replace('http://', 'https://')
            self.host_url = self.host_url.replace('http://', 'https://')
            self.base_url = self.base_url.replace('http://', 'https://')
            self.url_root = self.url_root.replace('http://', 'https://')


app = Flask(__name__)
app.request_class = ProxiedRequest

client_id = 'http://127.0.0.1:5000/'
client_secret = 'cogden/cogden'

@app.route('/')
def main():
    return ID.authenticate(client_id, client_secret)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)
