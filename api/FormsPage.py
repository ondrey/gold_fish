# -*- coding: utf-8 -*-

from hashlib import md5
from random import choice
from uuid import uuid4

from flask import jsonify
from flask import abort
from flask import request
from flask import session
from flask import redirect, url_for
from flask import current_app as app
from flask_mail import Mail

from ObjectAPI import ObjectAPI
from ObjectAPI import render_tmp
from ObjectDb import ObjectDb


