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

featuresOverview = [constants.GROUPBY_FEATURE,'SessionDuration', 'Points', 'Attempts', 'itemsCollectedCount', constants.COUNT_STUDENT_FEATURE]

#Student Interaction with Game - TIMELINE
def plotClassOverview(schoolKey, schoolKeys2Compare):
    
    
    colors = ['mediumturquoise', 'gold', 'darkorange', 'lightgreen']
    graphs = []
    rows = []
    
    if (None == schoolKey) :
        return html.Div()
    
    if (None == schoolKeys2Compare) :
        schoolKeys2Compare = []
    
    students = getStudentsOfSchool(schoolKey)
        
    studentDataDf = studentGrouped.getStudentsOfSchoolDF(schoolKey)
    
    for sckoolKey2Com in schoolKeys2Compare:
        studentDataDf2Com = studentGrouped.getStudentsOfSchoolDF(sckoolKey2Com)
        studentDataDf = pd.concat([studentDataDf, studentDataDf2Com], ignore_index=True, sort=False)    


#   Sum of features
    studentDataDfSum = studentDataDf.groupby([constants.GROUPBY_FEATURE, constants.COUNT_STUDENT_FEATURE], as_index=False).sum()
    
    tableSum = dbc.Table.from_dataframe(studentDataDfSum[featuresOverview], striped=True, bordered=True, hover=True, className = "table-comparision")
    
    print(studentDataDf.columns)
        
    columns1 = []
    columns1.append(dbc.Col(
               html.Div( tableSum ) , align="center")
    )
    rows.append( dbc.Row( html.Div('Total') ) )
    rows.append( dbc.Row( columns1 ) )
    
#   Mean of comparision features    
    studentDataDfMean = studentDataDf.groupby([constants.GROUPBY_FEATURE], as_index=False).mean()
    
    tableMean = dbc.Table.from_dataframe(studentDataDfMean[featuresOverview].round(decimals=2), striped=True, bordered=True, hover=True, className = "table-comparision")
    columns2 = []
    columns2.append(dbc.Col(tableMean , align="center"))

    rows.append( dbc.Row( html.Div('Average') ) )
    rows.append( dbc.Row( columns2 ) )
    
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

            html.P("Select Group for Comparision"),
            dcc.Dropdown(
                id      ="group-selector-comparision-overview",
                options = GroupSelector_options,
                multi   = True,
            ),
            html.Div(
                id="reset-btn-outer",
                children =  
                        dbc.Button( "Reset", id="reset-btn", 
                           outline=True, color="primary", className="mr-1", n_clicks=0
                        ),
            ),
            html.Br(),
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


    html.Div(id='group-comparision-container', className = "row group-comparision-container" )
    
    
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
    Output("group-comparision-container", "children"),
    [
        Input("group-selector-main", "value"),
        Input("group-selector-comparision-overview", "value"),
    ],
)
def update_bar(groupMain, groupComparision ):
    print('anil')
    print(groupMain)
    print(groupComparision)
    
    graphs = []

    if groupMain is None or not int(groupMain) >= 0:
        return html.Div(graphs)
 
    graphs = plotClassOverview( int(groupMain), groupComparision )    

    return  html.Div(graphs)
    