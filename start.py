# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import abort
from flask import session
from flask import redirect
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


@app.route('/app')
def demo():
    if 'client_sess' in session:
        return api.render_tmp('demo.html')
    else:
        return redirect("/auth/page_login")


@app.route('/about')
def about():
    return api.render_tmp('about.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

app.run(port=5011)
