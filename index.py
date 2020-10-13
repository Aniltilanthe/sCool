# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 18:04:10 2020

@author: tilan
"""

# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly import graph_objs as go

from flask import redirect
from flask_login import logout_user, current_user, LoginManager, UserMixin

from app import app, server, login_manager, User
from apps import groups, groupDetails, groupStudents, custom, home, sidebar, login
from data import studentGrouped

import constants




#--------------------- school selection START ----------------------
GroupSelector_options   = studentGrouped.GroupSelector_options 
dfUser                  =  studentGrouped.dfUser
#--------------------- school selection END ----------------------


    
@login_manager.user_loader
def load_user(usernameOrId):
     # 1. Fetch against the database a user by `id` 
     # 2. Create a new object of `User` class and return it.
 
    userDB = studentGrouped.getUserFromUserId(usernameOrId)
    print(userDB['UserName'])
    
    if  userDB is not None:        
        return User(userDB['UserName'], userDB['Id'], True)



print( GroupSelector_options )


def getUserLA():
    print('index getUserLA current user')
    print(current_user)
    if current_user and current_user is not None   and   not isinstance(current_user, type(None))  and    current_user.is_authenticated:
        currentUserId = current_user.id
        print('getUserLA isAdmin or not userDB')
        print(currentUserId)
        
        userDB = studentGrouped.getUserFromUserId(currentUserId)
        
        print(userDB)
        
        if  userDB is not None:        
            if userDB['IsAdmin']:
                print('In IsAdmin part')
                return studentGrouped.dfLearningActivityDetails[constants.GROUPBY_FEATURE].unique().astype(str)
            else:
                print('In Not Admin Else Part')
                return studentGrouped.dfLearningActivityDetails[studentGrouped.dfLearningActivityDetails['User_Id'] == 
                                                                currentUserId][constants.GROUPBY_FEATURE].unique().astype(str)


    return studentGrouped.dfLearningActivityDetails[constants.GROUPBY_FEATURE].unique()




def getUserLAOptions():
    print('index  getUserLAOptions')
    userLA = getUserLA()
    print(userLA)
    
    return studentGrouped.BuildOptionsLA( [ groupId for groupId in  np.append(userLA, [0])  ]  )


def generateControlCard():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card-index",
        children=[
            html.P(constants.labelSelectLA),
            dcc.Dropdown(
                id = "group-selector-main",
                options = getUserLAOptions(),
                className = "dropdown-main",
            ),
        ]
    )


content = html.Div(
        children=[
        
            dbc.Navbar(
                children = [
                        dbc.Row([
                                dbc.Col(
                                    # Left column
                                    html.Div(
                                        id="row-control-main-index",
                                        className="",
                                        children=[ generateControlCard() ]
                                        + [
                                            html.Div(
                                                ["initial child"], id="row-control-main-output-clientside-index", style={"display": "none"}
                                            )
                                        ],
                                    ),
                            ),
                        ],
                            className = "row w-100  selector-main-row"
                        ),                
                ],
                id="page-topbar", 
                sticky          = "top" ,
                light           = False ,
                className       = "navbar-main hidden",
            ),

            # Page content
            html.Div(id="page-content", className="page-content "),
                    
    ],
        
    id="page-main", 
    className = "  page-main "
)
                                        
                                        
userInfoLayout = html.Div(
        children=[
        dcc.Input(id="user-info-username", type="text", placeholder=""),
        dcc.Input(id="user-info-id", type="text", placeholder=""),
    ],
    className = " hidden "
)



app.layout = html.Div([dcc.Location(id="url"), sidebar.sidebar, content,
                       userInfoLayout ],
                       className = constants.THEME
                       )




@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    
    if pathname == '/login':
        if not current_user.is_authenticated:
            return login.layout
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
        

    if current_user.is_authenticated:
        if pathname in ["/", "/Home"]:
            return home.layout
        if pathname in ["/Overview", "/Groups"]:
            return groups.layout
        elif pathname == "/Details":
            return groupDetails.layout
        elif pathname == "/Custom":
            return custom.layout
        elif pathname == "/Students":
            return groupStudents.layout        

        return groupDetails.layout

    
    # DEFAULT NOT LOGGED IN: /login
    return login.layout



#@app.callback(Output('group-selector-main', 'options'), 
#              [Input("url", "pathname")])
#def update_group_select_options(pathname):    
#    if pathname in  ["/login"] :
#        return []
#    else:
#        return studentGrouped.getUserLAOptions()




# Update bar plot
@app.callback(
    Output("page-topbar", "className"),
    [
        Input("url", "pathname")
    ],
     state=[ State(component_id='page-topbar', component_property='className')
                ]
)
def show_hide_topbar(pathname, currentClasses):
    currentClassesS = set()
    
    if not (None is currentClasses) and not ('' == currentClasses) :
        currentClassesS = set(currentClasses.split(' '))

    currentClassesS.discard('hidden')
    
    if pathname in  ["/", "/Home", "/login"] :
        currentClassesS.add('hidden')
        
    return  ' '.join(currentClassesS)





# Update bar plot
@app.callback(
    Output("page-sidebar", "className"),
    [
        Input("url", "pathname")
    ],
     state=[ State(component_id='page-sidebar', component_property='className')
                ]
)
def show_hide_sidebar(pathname, currentClasses):
    currentClassesS = set()
    
    if not (None is currentClasses) and not ('' == currentClasses) :
        currentClassesS = set(currentClasses.split(' '))

    currentClassesS.discard('hidden')
    
    if  pathname in  ["/login"]    or   not  ( current_user and current_user is not None   and   not isinstance(current_user, type(None))  and    current_user.is_authenticated) :
        currentClassesS.add('hidden')
        
    return  ' '.join(currentClassesS) 





@app.callback(
    Output("group-selector-main", "options"),
    [
        Input("user-info-id", "value")
    ],
)
def on_login_update_group_selector_options(usernameOrId):
    
    return studentGrouped.getUserLAOptions()






#if __name__ == "__main__":
#    app.run_server(port=8888, debug=True)

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)