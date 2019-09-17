# -*- coding: utf-8 -*-
from flask import current_app as app


class AuthSession:
    def __init__(self):
        self.admin = app.config["ADMIN_ACCOUNT"]
        pass

    def login(self):

        return False