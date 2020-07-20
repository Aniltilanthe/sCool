# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 18:16:48 2020

@author: tilan
"""
import math
import json
import datetime
import numpy as np
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

featureAdderAvg = '(Avg.)'
featuresOverview = [constants.GROUPBY_FEATURE,'SessionDuration', 'Points', 'Attempts', 'itemsCollectedCount', constants.COUNT_STUDENT_FEATURE ]
featuresOverviewAvg = [constants.GROUPBY_FEATURE, 'SessionDuration' + featureAdderAvg, 'Points' + featureAdderAvg
                       , 'Attempts' + featureAdderAvg, 'itemsCollectedCount' + featureAdderAvg ]
featuresOverviewAvgNames = {'SessionDuration': 'SessionDuration'+ featureAdderAvg,
                                      'Points': 'Points' + featureAdderAvg,
                                      'Attempts' : 'Attempts' + featureAdderAvg,
                                      'itemsCollectedCount' : 'itemsCollectedCount' + featureAdderAvg }
featuresOverviewGeneralNames = {'CountOfStudents': 'No. of Students'}

def get_merge_list(values):
    return list(set([a for b in values.tolist() for a in b]))

#Student Interaction with Game - TIMELINE
def plotClassOverview(schoolKey, schoolKeys2Compare):
    
    
    colors = ['mediumturquoise', 'gold', 'darkorange', 'lightgreen']
    graphs = []
    rows = []
    
    if (None == schoolKey) :
        return html.Div()
    
    if (None == schoolKeys2Compare) :
        schoolKeys2Compare = []
    
    studentDataDf = studentGrouped.getStudentsOfSchoolDF(schoolKey)
    
    for sckoolKey2Com in schoolKeys2Compare:
        studentDataDf2Com = studentGrouped.getStudentsOfSchoolDF(sckoolKey2Com)
        
        if 'studentDataDf2Com' in locals():
            studentDataDf = pd.concat([studentDataDf, studentDataDf2Com], ignore_index=True, sort=False)    


    if 'studentDataDf' in locals():
        print('Initial List of Columns after adding all DF')
        print(studentDataDf.columns)
        
    #   Sum of features
        studentDataDfSum = studentDataDf.groupby([constants.GROUPBY_FEATURE, constants.COUNT_STUDENT_FEATURE], as_index=False).sum()
        
    #    get the Mean DF and merge both DF
        studentDataDfMean = studentDataDf.groupby([constants.GROUPBY_FEATURE], as_index=False).mean()
        studentDataDfMean.rename(columns = featuresOverviewAvgNames, inplace=True)
        
        studentDataDfOverview = pd.merge(studentDataDfSum[featuresOverview], studentDataDfMean[featuresOverviewAvg].round(decimals=2), 
                                         how='inner', on = constants.GROUPBY_FEATURE, left_index=False, right_index=False )
        
    #    tableSum = dbc.Table.from_dataframe(studentDataDfOverview, striped=True, bordered=True, hover=True, className = "table-comparision")
    #
    #    columns1 = []
    #    columns1.append(dbc.Col(
    #               html.Div( tableSum ) , align="center")
    #    )
    #    rows.append( dbc.Row( html.Div('Overview') ) )
    #    rows.append( dbc.Row( columns1 ) )
    #
    #    tableSum = dbc.Table.from_dataframe(studentDataDfSum[featuresOverview], striped=True, bordered=True, hover=True, className = "table-comparision")
    #    
    #    columns1 = []
    #    columns1.append(dbc.Col(
    #               html.Div( tableSum ) , align="center")
    #    )
    #    rows.append( dbc.Row( html.Div('Total') ) )
    #    rows.append( dbc.Row( columns1 ) )
        
    #   Mean of comparision features    
        studentDataDfMean = studentDataDf.groupby([constants.GROUPBY_FEATURE], as_index = False).mean()
        
        studentDataDfGrouped = studentDataDf.groupby([constants.GROUPBY_FEATURE], as_index = False)
        
        studentDataDfMeanFinal = studentDataDfMean
        
        ConceptsUsedGroupList = []
        ConceptsUsedDetailsGroupList = []
        for groupKey, group in studentDataDfGrouped :
            if 'ConceptsUsed' in group.columns and  group[ group['ConceptsUsed'].notnull() ].shape[0] > 0 :
                ConceptsUsedGroupList.append( ', '.join( group[ group['ConceptsUsed'].notnull() ].iloc[0]['ConceptsUsed'] )   )
                ConceptsUsedDetailsGroupList.append( ', '.join( group[ group['ConceptsUsedDetails'].notnull() ].iloc[0]['ConceptsUsedDetails']   ) )
            else :
                ConceptsUsedGroupList.append(' ')
                ConceptsUsedDetailsGroupList.append(' ')
                
        
    
        studentDataDfMean['ConceptsUsed'] = ConceptsUsedGroupList
        studentDataDfMean['ConceptsUsedDetails'] = ConceptsUsedDetailsGroupList
        
        studentDataDfMeanToPlot = studentDataDfMean[featuresOverview + ['ConceptsUsed', 'ConceptsUsedDetails']].round(decimals=2)
        studentDataDfMeanToPlot.rename(columns = featuresOverviewAvgNames, inplace=True)
        studentDataDfMeanToPlot.rename(columns = featuresOverviewGeneralNames, inplace=True)
        
        tableMean = dbc.Table.from_dataframe(studentDataDfMeanToPlot, 
                                             striped=True, bordered=True, hover=True, className = "table-comparision")
        columns2 = []
        columns2.append(dbc.Col(tableMean , align="center"))
    
        rows.append( dbc.Row( html.Div('Overview') ) )
        rows.append( dbc.Row( columns2 ) )
        
        graphs.append(html.Div(  rows  ))
        
    return graphs




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


#----------------------------------Functions END --------------------------------------------






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

    # indicators row
#    html.Div(
#        [
#            indicator("#00cc96", "Won opportunities", "left_opportunities_indicator"),
#            indicator(
#                "#119DFF", "Open opportunities", "middle_opportunities_indicator"
#            ),
#            indicator("#EF553B", "Lost opportunities", "right_opportunities_indicator"),
#        ],
#        className="row",
#    ),


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
    