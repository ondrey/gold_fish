# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

app.config.from_object('config.DevelopmentConfig')

app.run(port=5011)
