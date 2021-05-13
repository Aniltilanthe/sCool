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

from flask import  Flask, request, redirect
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
import time
import base64

from data import studentGrouped

from app import app, User, server

import constants





dfUser                  =  studentGrouped.dfUser


success_alert = dbc.Alert(
    'Logged in successfully. Taking you home!',
    color='success',
    dismissable=True
)
failure_alert = dbc.Alert(
    'Login unsuccessful. Try again.',
    color='danger',
    dismissable=True
)
already_login_alert = dbc.Alert(
    'User already logged in. Taking you home!',
    color='warning',
    dismissable=True
)


layout = dbc.Row(
        dbc.Col(
            [
                html.H1('Login from main app only'),
            ],
            width=6
        )
    )




# Adding this route allows us to use the POST method on our login app.
# It also allows us to implement HTTP Redirect when the login form is submitted.
@server.route('/login', methods=['POST'])
def login():
    print('in server route login')
    if request.method == 'POST':
        print('in server route login POST')
        if request.args.get('securityStamp')   :
            userDB = studentGrouped.getUserFromSecurityStamp( str(request.args.get('securityStamp'))  )
                    
            if  userDB is not None:
                user = User(userDB['UserName'], userDB['Id'], active = True, isAdmin = userDB['IsAdmin'], securityStamp = userDB['SecurityStamp'], 
                        isAuthenticated = True )
                if user:
                    login_user(user)
                    return redirect(constants.loginRedirect)
                else:
                    return redirect('/login')
            else:
                return redirect('/login')
        else:
            return redirect('/login')
    else:
        return redirect('/login')