#!/usr/bin/env python3

from gevent import monkey
monkey.patch_all()
from flask import Flask
from flask import request
from flask import Response
from flask import render_template
from functools import wraps
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

def check_auth(username, password):
    return username == 'admin' and password == 'admin'

def authenticate():
    return Response(
    'Authorization required to access web-console.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
  return render_template("index.html")

server = WSGIServer(('0.0.0.0', 80), app)
server.serve_forever()
