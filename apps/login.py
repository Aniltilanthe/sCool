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
                dcc.Location(id='login-url',refresh=True,pathname='/login'),
                html.Div(id='login-trigger',style=dict(display='none')),
                html.Div(id='login-alert'),
                dbc.FormGroup(
                    [

                        dbc.Input(id='login-username', autoFocus=True),
                        dbc.FormText('Email'),
                        
                        html.Br(),
                        dbc.Input(id='login-password', type='password'),
                        dbc.FormText('Password'),
                        
                        html.Br(),
                        dbc.Button('Submit',color='primary', id='login-button'),
                    ]
                )
            ],
            width=6
        )
    )



@app.callback(
    [Output('login-url', 'pathname'),
     Output('login-alert', 'children')
     ],
    [Input('login-button', 'n_clicks')],
    [State('login-username', 'value')]
)
def login_success(n_clicks, usernameId):
    '''
    logs in the user
    '''
    if not n_clicks is None and n_clicks > 0:
        print('login success user')
        userDB = studentGrouped.getUserFromUserId(usernameId)
        
        if  userDB is not None: 
            user = User(userDB['UserName'], userDB['Id'], active = True, isAdmin = userDB['IsAdmin'], securityStamp = userDB['SecurityStamp'] )
            print('login success user')
            print(userDB)
            print(user)
            if user:
                login_user(user)

                return constants.loginRedirect, success_alert
            else:
                return no_update, failure_alert
        else:
            return no_update, failure_alert
    else:
        return no_update, ''



# Adding this route allows us to use the POST method on our login app.
# It also allows us to implement HTTP Redirect when the login form is submitted.
@server.route('/login', methods=['POST'])
def login():
    print('in server route login')
    if request.method == 'POST':
        print('in server route login POST')
        if request.args.get('securityStamp')   :
            userDB = studentGrouped.getUserFromSecurityStamp( str(request.args.get('securityStamp'))  )
            
            print(userDB)
        
            if  userDB is not None:
                user = User(userDB['UserName'], userDB['Id'], active = True, isAdmin = userDB['IsAdmin'], securityStamp = userDB['SecurityStamp'] )
                if user:
                    login_user(user)
                    print(user)
                    print('login user')
                    return redirect(constants.loginRedirect)
                else:
                    return redirect('/login')
            else:
                return redirect('/login')
        else:
            return redirect('/login')
    else:
        return redirect('/login')



#
## Adding this route allows us to use the POST method on our login app.
## It also allows us to implement HTTP Redirect when the login form is submitted.
#@server.route('/login', methods=['POST'])
#def login():
#    print('in server route login')
#    if request.method == 'POST':
#        print('in server route login POST')
#        if request.args.get('usernameId')  and request.args.get('password') :
#            userDB = studentGrouped.getUserFromUserId( str(request.args.get('usernameId')), password = str(request.args.get('password')))            
#            
#            print(userDB)
#        
#            if  userDB is not None:            
#                user = User(userDB['UserName'], userDB['Id'], True)
#                if user:
#                    login_user(user)
#                    print(user)
#                    print('login user')
#                    return redirect(constants.loginRedirect)
#                else:
#                    return redirect('/login')
#            else:
#                return redirect('/login')
#        else:
#            return redirect('/login')
#    else:
#        return redirect('/login')










#import dash_html_components as html
#import dash_core_components as dcc
#import dash_bootstrap_components as dbc
#from dash.dependencies import Input, Output, State
#from dash import no_update, Dash
#from dash_flask_login import FlaskLoginAuth
#
#from flask import  Flask, request, redirect
#from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
#from werkzeug.security import generate_password_hash, check_password_hash
#
#
#from data import studentGrouped
#
#from app import app
#
## Setup the Flask server
#server = app.server
#
#
#login_manager = LoginManager()
#login_manager.init_app(server)
#login_manager.login_view = "/login"
#login_manager.login_message = u"Please log in to access this page."
#login_manager.refresh_view = "reauth"
#
#
## Create Login Dash App with a login form
#login_app = Dash(name='login-app', url_base_pathname='/login', server=server)
#
#
#login_app.layout = html.Div([
#    html.H1('Please log in to continue.', id='h1'),
#    html.Form(
#        method='Post',
#        children=[
#            dcc.Input(
#                placeholder='Enter your username',
#                type='text',
#                id='uname-box'
#            ),
#            dcc.Input(
#                placeholder='Enter your password',
#                type='password',
#                id='pwd-box'
#            ),
#            html.Button(
#                children='Login',
#                n_clicks=0,
#                type='submit',
#                id='submit-button'
#            ),
#
#        ]
#    ),
#    html.A(html.Button('app1'), href='/app1', style={'display':'none'}, id='hidden-link')
#]
#)
#        
## This callback to the login app should encapsulate the login functionality
## Set the output to a non-visible location
#@login_app.callback(
#            Output('h1', 'n_clicks'),
#            [Input('submit-button', 'n_clicks')],
#            [State('uname-box', 'value'),
#             State('pwd-box', 'value')]
#        )
#def login(n_clicks, uname, pwd):
#
#    if uname == 'user' and pwd == 'password':
#        login_user(load_user('peter.lerchbacher@schule.at'))
#
#    else:pass
#
#
#
#
#class User(UserMixin):
#    def __init__(self, name, Id, active=True):
#        self.name = name
#        self.id = Id
#        self.active = active
#
#    def is_active(self):
#        # Here you should write whatever the code is
#        # that checks the database if your user is active
#        return self.active
#
#    def is_anonymous(self):
#        return False
#
#    def is_authenticated(self):
#        return True
#    
#    
#    
#@login_manager.user_loader
#def load_user(username):
#     # 1. Fetch against the database a user by `id` 
#     # 2. Create a new object of `User` class and return it.
#    u = studentGrouped.getUserDetails(username)
#    return User(u['UserName'][0], u['Id'][0], True)
#
#
#
## Adding this route allows us to use the POST method on our login app.
## It also allows us to implement HTTP Redirect when the login form is submitted.
#@server.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        if request.args.get('next'):
#            return redirect(request.args.get('next'))
#        else:
#            return redirect('/login')
#    else:
#        return redirect('/login')
#    
#    
#    
#    
##LOGOUT
#
## Create logout Dash App
#logout_app = Dash(name='logout-app', url_base_pathname='/logout', server=server)
#
#logout_app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css',
#})
#
#logout_app.layout = html.Div([
#    html.H1('You have successfully logged out!', id='h1'),
#
#    # Since we've logged out, this will force a redirect to the login page with a next page of /app1
#    html.A(html.Button('Log Back In'), href='/app1', id='login-button'),
#]
#)
#
## This callback to the logout app simply logs the user out each time the logout page is loaded
#@logout_app.callback(
#            Output('h1', 'n_clicks'),
#            [Input('login-button', 'children')]
#        )
#def logout(children):
#    logout_user()
#    
#
## Create FlaskLoginAuth object to require login for Dash Apps
#auth = FlaskLoginAuth(app)
#
## Add logout app to FlaskLoginAuth
#auth.add_app(logout_app)
