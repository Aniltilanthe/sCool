# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 18:16:48 2020

@author: tilan
"""
import math
import json
import datetime
from datetime import date
from datetime import datetime as dt
import dateutil.parser

import pandas as pd
import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import chart_studio.plotly as py
from plotly import graph_objs as go
import os

from app import app, indicator, millify



import studentGroupedPerformance
import studentGroupedPerformanceTheory
import studentGroupedGeneral


#--------------------- school selection START ----------------------
GroupSelector_options = studentGroupedGeneral.GroupSelector_options 
#--------------------- school selection END ----------------------



#--------------------------------- DataBase get data START ---------------------------
dfStudentDetails = studentGroupedGeneral.dfStudentDetails
dfStudentDetails = dfStudentDetails.drop_duplicates(subset=['StudentId'], keep='first')


dfPracticeTaskDetails = studentGroupedPerformance.dfPracticeTaskDetails
dfTheoryTaskDetails   = studentGroupedPerformanceTheory.dfTheoryTaskDetails


dfGroupedPractice                       = studentGroupedPerformance.dfGrouped
dfGroupedOriginal                       = studentGroupedPerformance.dfGroupedOriginal
dfPlayerStrategyPractice                = studentGroupedPerformance.dfPlayerStrategyPractice  
dfGroupedPracticeTaskWise               = studentGroupedPerformance.dfGroupedPracticeTaskWise
dfGroupedPracticeDB  = studentGroupedPerformance.dfPractice.groupby(  [studentGroupedPerformance.dfPractice['GroupId']] )



dfPlayerStrategyTheory = pd.concat([studentGroupedPerformanceTheory.dfPlayerStrategyNN, studentGroupedPerformanceTheory.dfPlayerStrategyN], ignore_index=True, sort =False)
dfGroupedPlayerStrategyTheory = dfPlayerStrategyTheory.groupby(  [dfPlayerStrategyTheory['GroupId']] )

#--------------------------------- DataBase get data END ---------------------------



def generateControlCard():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="Control-Card-Overview",
        children=[
#            html.P("Select Group"),
#            dcc.Dropdown(
#                id = "group-selector-main-overview",
#                options = GroupSelector_options,
#            ),
#            html.Br(),
#            html.Br(),
#            html.Br(),
            html.P("Select Group for Comparision"),
            dcc.Dropdown(
                id="group-selector-comparision-overview",
                options = GroupSelector_options,
#                value = GroupSelector_options[:],
                multi = True,
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=  
                        dbc.Button( "Reset", id="reset-btn", 
                           outline=True, color="primary", className="mr-1", n_clicks=0
                        ),
            ),
        ],
    )



layout = [
        
    dbc.Row([
            dbc.Col(
                # Left column
                html.Div(
                    id="row-control-main-overview",
                    className="",
                    children=[ generateControlCard() ]
                    + [
                        html.Div(
                            ["initial child"], id="row-control-main-output-clientside-overview", style={"display": "none"}
                        )
                    ],
                ),
        ),
    ]),

        
    # top controls
    dbc.Row(
        [
            dbc.Col(  html.Div(
                dcc.Dropdown(
                    id="converted_opportunities_dropdown",
                    options=[
                        {"label": "By day", "value": "D"},
                        {"label": "By week", "value": "W-MON"},
                        {"label": "By month", "value": "M"},
                    ],
                    value="D",
                    clearable=False,
                ), 
                
                
#                dcc.Dropdown(
#                    id='SchoolSelector-Dropdown',                    
#                    options =  SchoolSelector_options,
#                    value  =   '2018-03-01' )
                
            ),
                width = { "size" : 2} 
            ),
            dbc.Col(  html.Div(
                dcc.Dropdown(
                    id="heatmap_dropdown",
                    options=[
                        {"label": "All stages", "value": "all_s"},
                        {"label": "Cold stages", "value": "cold"},
                        {"label": "Warm stages", "value": "warm"},
                        {"label": "Hot stages", "value": "hot"},
                    ],
                    value="all_s",
                    clearable=False,
                ),
            ),
                width = { "size" : 2} 
            ),
            dbc.Col(  html.Div(
                dcc.Dropdown(
                    id="source_dropdown",
                    options=[
                        {"label": "All sources", "value": "all_s"},
                        {"label": "Web", "value": "Web"},
                        {"label": "Word of Mouth", "value": "Word of mouth"},
                        {"label": "Phone Inquiry", "value": "Phone Inquiry"},
                        {"label": "Partner Referral", "value": "Partner Referral"},
                        {"label": "Purchased List", "value": "Purchased List"},
                        {"label": "Other", "value": "Other"},
                    ],
                    value="all_s",
                    clearable=False,
                ),
            ),
                width = { "size" : 2} 
            ),
            # add button
            
            dbc.Col(  html.Div(
                html.Span(
                    "Add new",
                    id="new_opportunity",
                    n_clicks=0,
                    className="button button--primary add",
                ),
            ),
                width = { "size" : 2} 
            ),
        ],
        style={"marginBottom": "10"},
    ),
    # indicators row
    html.Div(
        [
            indicator("#00cc96", "Won opportunities", "left_opportunities_indicator"),
            indicator(
                "#119DFF", "Open opportunities", "middle_opportunities_indicator"
            ),
            indicator("#EF553B", "Lost opportunities", "right_opportunities_indicator"),
        ],
        className="row",
    ),
    # charts row div
    html.Div(
        [
            html.Div(
                [
                    html.P("Converted Opportunities count"),
                    dcc.Graph(
                        id="converted_count",
                        style={"height": "90%", "width": "98%"},
                        config=dict(displayModeBar=False),
                    ),
                ],
                className="four columns chart_div",
            ),
            html.Div(
                [
                    html.P("Probabilty heatmap per Stage and Type"),
                    dcc.Graph(
                        id="heatmap",
                        style={"height": "90%", "width": "98%"},
                        config=dict(displayModeBar=False),
                    ),
                ],
                className="eight columns chart_div",
            ),
        ],
        className="row",
        style={"marginTop": "5px"},
    ),
]
                
                
                                
@app.callback(
    [ 
         Output("group-selector-comparision-overview", "value"), 
    ],
    [
        Input("reset-btn", "n_clicks")
    ],
)
def on_reset(reset_click):
    # Find which one has been triggered
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "reset-btn" and reset_click:
            return [""]
            
#    return [GroupSelector_options[0]['value']]
    return [""]



# Update bar plot
@app.callback(
    Output("row-control-main-output-clientside-overview", "figure"),
    [
        Input("group-selector-main-index", "value"),
        Input("group-selector-comparision-overview", "value"),
    ],
)
def update_bar(groupMain, groupComparision ):
    print('anil')
    print(groupMain)
    print(groupComparision)
    