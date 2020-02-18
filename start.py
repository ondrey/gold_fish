# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import abort
import api

app = Flask(__name__)
app.config.from_object('config.DevelopmentTemplateConfig')


@app.route('/<api_group>/<method_api>', methods=["GET", "POST"])
def run_api_method(api_group, method_api):
    if api_group in api.__dict__:
        obj = api.__dict__[api_group]()
        return obj.run_api_method(method_api)
    abort(404)


@app.route('/')
def index():
    return api.render_tmp('index.html')


@app.route('/demo')
def demo():
    return api.render_tmp('demo.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

app.run(port=5011)
