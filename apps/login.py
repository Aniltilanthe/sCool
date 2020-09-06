# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 21:51:30 2020

@author: tilan
"""
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import no_update

from flask import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from data import studentGrouped


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"


class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    
    
@login_manager.user_loader
def load_user(username):
     # 1. Fetch against the database a user by `id` 
     # 2. Create a new object of `User` class and return it.
    u = studentGrouped.getUserDetails(username)
    return User(u.name,u.id,u.active)