# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 18:04:10 2020

@author: tilan
"""

# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import flask
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly import graph_objs as go
import math

from app import app
from apps import overview, groupDetails, custom, home

from sidebar import sidebar


import constants

import studentGrouped



#--------------------- school selection START ----------------------
GroupSelector_options = studentGrouped.GroupSelector_options 
#--------------------- school selection END ----------------------





def generateControlCard():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card-index",
        children=[
            html.P("Select Group"),
            dcc.Dropdown(
                id = "group-selector-main",
                options = GroupSelector_options,
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
            html.Div(id="page-content", className="page-content"),
                    
    ],
        
    id="page-main", 
    style =  constants.CONTENT_STYLE,
    className = constants.THEME
)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])




@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/Home"]:
        return home.layout
    if pathname in ["/Overview"]:
        return overview.layout
    elif pathname == "/Details":
        return groupDetails.layout
    elif pathname == "/Custom":
        return custom.layout
    elif pathname == "/page-2/2":
        return html.P("No way! This is page 2.2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

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
    
    if pathname in  ["/", "/Home"]:
        currentClassesS.add('hidden')
        
    return  ' '.join(currentClassesS) 
    


#if __name__ == "__main__":
#    app.run_server(port=8888, debug=True)

if __name__ == "__main__":
    app.run_server(debug=True)