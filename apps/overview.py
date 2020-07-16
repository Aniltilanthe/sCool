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



import studentGrouped
import constants

#--------------------- school selection START ----------------------
GroupSelector_options = studentGrouped.GroupSelector_options 
#--------------------- school selection END ----------------------



#--------------------------------- DataBase get data START ---------------------------
dfStudentDetails                        = studentGrouped.dfStudentDetails


dfPracticeTaskDetails                   = studentGrouped.dfPracticeTaskDetails
dfTheoryTaskDetails                     = studentGrouped.dfTheoryTaskDetails


dfGroupedPractice                       = studentGrouped.dfGroupedPractice
dfGroupedOriginal                       = studentGrouped.dfGroupedOriginal
dfPlayerStrategyPractice                = studentGrouped.dfPlayerStrategyPractice  
dfGroupedPracticeTaskWise               = studentGrouped.dfGroupedPracticeTaskWise
dfGroupedPracticeDB                     = studentGrouped.dfGroupedPracticeDB
dfRuns                                  = studentGrouped.dfRuns


dfPlayerStrategyTheory                  = studentGrouped.dfPlayerStrategyTheory
dfGroupedPlayerStrategyTheory           = studentGrouped.dfGroupedPlayerStrategyTheory

#--------------------------------- DataBase get data END ---------------------------

#--------------------------- helper functions START -----------------------    
getTaskWiseSuccessFail                  =  studentGrouped.getTaskWiseSuccessFail
getStudentsOfSchool                     =  studentGrouped.getStudentsOfSchool

#--------------------------- helper functions END -----------------------  



#-----------------------------------Functions START ----------------------------------------

#Student Interaction with Game - TIMELINE
def plotClassOverview(schoolKey):
    
    
    colors = ['mediumturquoise', 'gold', 'darkorange', 'lightgreen']
    graphs = []
    rows = []
    columns = []
    
    students = getStudentsOfSchool(schoolKey)
    
    
    
    try :
        schoolPractice = dfGroupedPracticeDB.get_group(schoolKey)
        schoolPractice['TaskId'] = 'Theory' + schoolPractice['PracticeTaskId']
        studentData = schoolPractice
    except Exception as e:
        print(e)

    try :
        schoolTheory = dfGroupedPlayerStrategyTheory.get_group(schoolKey)
        schoolTheory['TaskId'] = 'Theory' + schoolTheory['TheoryTaskId']
        studentData = schoolTheory
    except Exception as e:
        print(e)

    try :
        if schoolTheory.empty == False :
            studentData = pd.concat([schoolPractice, schoolTheory], ignore_index=True)
    except Exception as e:
        print(e)
    
    
#    fig1 = go.Figure(data=[go.Pie(labels=['No. of Students'],
#                                 values=[  len(students)   ])])
#    fig1.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=20,
#                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))
#    
#    fig1.update_layout(
#            height =  500
#    )
#    
#    columns.append(dbc.Col(
#                dcc.Graph(
#                    figure= fig1
#            ) , align="center")
#    )
    
#    ---------------------------------------------
    parentsText = "<b>" + str(schoolKey) + "<br>No. of Students: " + str(len(students)) + "</b>"
    
    labels = [parentsText]
    labels = labels + dfStudentDetails[dfStudentDetails['StudentId'].isin( students)]['Name'].tolist()
    labels = [str(i) for i in labels]
    
    parents = [parentsText] * len(labels)
    parents[0] = ""
    
    fig2 = go.Figure(go.Sunburst(
        labels      =  labels,
        parents     =  parents,
        values      = [1] * len(labels),
    ))
    fig2.update_layout(
            height =  constants.graphHeight + 300
    )
    
    
    columns.append(dbc.Col(
                dcc.Graph(
                    figure= fig2
            ) , align="center")
    )
        
    rows.append( dbc.Row( columns ) )
    
    graphs.append(html.Div(  rows  ))
    
    return graphs




#----------------------------------Functions END --------------------------------------------




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
        Input("group-selector-main", "value"),
        Input("group-selector-comparision-overview", "value"),
    ],
)
def update_bar(groupMain, groupComparision ):
    print('anil')
    print(groupMain)
    print(groupComparision)
    