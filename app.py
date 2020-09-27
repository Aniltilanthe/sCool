# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 19:06:08 2020

@author: tilan
"""

# -*- coding: utf-8 -*-
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from flask import request

from dash.dependencies import Input, Output, State

from flask_login import LoginManager, UserMixin


import numpy as np
import pandas as pd
#from data import studentGrouped


FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
MATERIAL_CSS = "https://fonts.googleapis.com/icon?family=Material+Icons"

external_stylesheets = [
                        dbc.themes.BOOTSTRAP,
                        dbc.themes.MATERIA,
                        FA,
#                        MATERIAL_CSS
                        ]



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

server = app.server
app.title = 'sCool Data Analysis App'



# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# config
server.config.update(
    SECRET_KEY='SCOOLSECRET@HEREITIS',
)



class User(UserMixin):
    def __init__(self, name, Id, active=True):
        self.name = name
        self.id = Id
        self.active = active

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True



#VALID_USERNAME_PASSWORD_PAIRS = {
#    'peter.lerchbacher@schule.at': 'peter.lerchbacher@schule.at',
#    'a.kojic@live.com' : 'a.kojic@live.com'
#}
#
#
#
#auth = dash_auth.BasicAuth(
#    app,
#    VALID_USERNAME_PASSWORD_PAIRS
#)