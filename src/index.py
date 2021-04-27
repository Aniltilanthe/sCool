# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 18:04:10 2020

@author: tilan
"""

# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from flask_login import logout_user, current_user, LoginManager, UserMixin

from app import app, server, login_manager, User
from apps import groups, learningActivityDetails, groupStudents, custom, home, sidebar, login
from data import studentGrouped

import constants




#--------------------- school selection START ----------------------
GroupSelector_options   = studentGrouped.GroupSelector_options 
dfUser                  =  studentGrouped.dfUser
#--------------------- school selection END ----------------------


    
@login_manager.user_loader
def load_user(usernameOrId):
    userDB = studentGrouped.getUserFromUserId(usernameOrId)
    
    if  userDB is not None:        
        return User(userDB['UserName'], userDB['Id'], active = True, isAdmin = userDB['IsAdmin'], securityStamp = userDB['SecurityStamp'] )




def getUserLA():
    if current_user and current_user is not None   and   not isinstance(current_user, type(None))  and    current_user.is_authenticated:
        currentUserId = current_user.id
        
        if  current_user.isAdmin : 
            return studentGrouped.dfLearningActivityDetails[constants.GROUPBY_FEATURE].unique().astype(str)
        else:
            return studentGrouped.dfLearningActivityDetails[studentGrouped.dfLearningActivityDetails['User_Id'] == 
                                                            currentUserId][constants.GROUPBY_FEATURE].unique().astype(str)


    return studentGrouped.dfLearningActivityDetails[constants.GROUPBY_FEATURE].unique()




def getUserLAOptions():
    userLA = getUserLA()
    
    if current_user and current_user is not None   and   not isinstance(current_user, type(None))  and    current_user.is_authenticated:
        return studentGrouped.BuildOptionsLA( [ groupId for groupId in  userLA  ] , isAdmin =  current_user.isAdmin ) 
    
    return studentGrouped.BuildOptionsLA( [ groupId for groupId in  userLA  ] , isAdmin = True  )




def generateControlCard():
    """
    :return: A Div containing Learning Analytics Selection.
    """
    return html.Div(
        id="control-card-index",
        children=[
            html.P(constants.labelSelectLA),
            dcc.Dropdown(
                id = "group-selector-main",
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
   



app.layout = html.Div([dcc.Location(id="url"), sidebar.sidebar, content,
                       ],
                       className = constants.THEME
                       )






@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    
    if pathname == '/login':
        if current_user and not current_user.is_authenticated:
            return login.layout
    elif pathname == '/logout':
        if current_user and current_user.is_authenticated:
            logout_user()
        

    if current_user and current_user.is_authenticated:
        if pathname in ["/Home"]:
            return home.layout
        if pathname in ["/Overview", "/Groups"]:
            return groups.layout
        elif pathname  in ["/", "/Details"]:
            return learningActivityDetails.layout
        elif pathname == "/Custom":
            return custom.layout
        elif pathname == "/Students":
            return groupStudents.layout        

        return learningActivityDetails.layout

    
    # DEFAULT NOT LOGGED IN: /login
    return login.layout




@app.callback( [Output("group-selector-main", "options") , Output("group-selector-main", "value") ], 
                [Input("url", "pathname")],
                state=[ State(component_id = "group-selector-main", component_property='options'),
                State(component_id = "group-selector-main", component_property='value') ]
    )
def render_main_selector_content(pathname,
               selectorOptions, selectorValue ):
    
    if current_user.is_authenticated  :
        userOptions = getUserLAOptions()
        value = ''

        if selectorOptions and selectorValue:
           return selectorOptions, selectorValue
        
        if len(userOptions) == 1:
            value = userOptions[0]['value']
        
        return userOptions, value
    
    
    return [], ''


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
    
    if pathname in  ["/Home", "/login"]  or   not  ( current_user and current_user is not None   and   not isinstance(current_user, type(None))  and    current_user.is_authenticated) :
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




# For Debug Mode
#if __name__ == "__main__":
#    app.run_server(port=8090, debug=True)

# For deployment
if __name__ == "__main__":
    app.run_server(port=8090, host="0.0.0.0", debug=False)