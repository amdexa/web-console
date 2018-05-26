#!/usr/bin/env python3

from gevent import monkey
monkey.patch_all()
from flask import Flask
from flask import render_template
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

server = WSGIServer(('0.0.0.0', 80), app)
server.serve_forever()
