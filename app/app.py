from functools import wraps
from dotenv import load_dotenv

from flask import Flask, redirect, render_template, request, session, jsonify, send_from_directory
from flask_wtf.csrf import CsrfProtect

import os
import json
import requests
import config

app = Flask(__name__)
csrf = CsrfProtect()
app.config.from_pyfile('config.py')
app.debug = True

# session stuff
# Generated by doing the following:
# import os
# os.urandom(24)
app.secret_key='mF)\xa8\x9b\x9c\xaf\xb0t\x0ckj\xf9\xf4\x86\xd5\x06?\x88\xe6\x13\xc6\x83\xd6'
app.config['SESSION_TYPE'] = 'filesystem'

# load env
env = None

# Loading config.py to enviroment variable
dotenv_path = os.path.join(os.path.dirname(__file__), 'config.py')
load_dotenv(dotenv_path)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)

    return decorated

# The default landing page
@app.route('/')
def home():
    return render_template('index.html', env=os.environ)

@app.route("/dashboard")
@requires_auth
def dashboard():
    return render_template('dashboard.html', user=session['profile'])

# This code is provided by auth0 when you set up the client
@app.route("/callback")
def callback():
    code = request.args.get('code')

    json_header = {'content-type': 'application/json'}

    token_url = "https://{domain}/oauth/token".format(domain=app.config["DOMAIN"])

    token_payload = {
        'client_id':     app.config["CLIENT_ID"],
        'client_secret': app.config["CLIENT_SECRET"],
        'redirect_uri':  app.config["CALLBACK_URL"],
        'code':          code,
        'grant_type':    'authorization_code'
    }

    token_info = requests.post(token_url, data=json.dumps(token_payload), headers = json_header).json()

    user_url = "https://{domain}/userinfo?access_token={access_token}" \
            .format(domain=app.config['DOMAIN'], access_token=token_info['access_token'])

    user_info = requests.get(user_url).json()

    # We're saving all user information into the session
    session['profile'] = user_info

    # Redirect to the User logged in page that you want here
    # In our case it's /dashboard
    return redirect('/dashboard')

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(host='0.0.0.0', port=8080)
