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
import plotly.express as px

import pandas as pd
import flask
import dash
from dash.dependencies import Input, Output, State
import dash_table
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
getPracticeConceptsUsedDetails          =  studentGrouped.getPracticeConceptsUsedDetails
getStudentWiseData                      =  studentGrouped.getStudentWiseData

#--------------------------- helper functions END -----------------------  



#-----------------------------------Functions START ----------------------------------------

featureAdderAvg = ' Avg.'
featuresOverview = [constants.GROUPBY_FEATURE,'SessionDuration', 'Points', 'Attempts', 'itemsCollectedCount', constants.COUNT_STUDENT_FEATURE ]
featuresOverviewAvg = [constants.GROUPBY_FEATURE, 'SessionDuration'+ featureAdderAvg, 'Points'+ featureAdderAvg
                       , 'Attempts'+ featureAdderAvg, 'itemsCollectedCount'+ featureAdderAvg ]
featuresOverviewAvgNames = {
        'SessionDuration': 'SessionDuration'+ featureAdderAvg,
                                      'Points': 'Points' + featureAdderAvg,
                                      'Attempts' : 'Attempts' + featureAdderAvg,
                                      'itemsCollectedCount' : 'itemsCollectedCount' + featureAdderAvg
                                      }
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
        
        if 'studentDataDf2Com' in locals()    and    studentDataDf2Com is not None :
            studentDataDf = pd.concat([studentDataDf, studentDataDf2Com], ignore_index=True, sort=False)
    

    if 'studentDataDf' in locals()     and    studentDataDf is not None  :
        
        studentDataDf[constants.GROUPBY_FEATURE]    = studentDataDf[constants.GROUPBY_FEATURE].apply(str)
        studentDataDf[constants.GROUPBY_FEATURE]    = 'Group-' + studentDataDf[constants.GROUPBY_FEATURE]
        studentDataDf[constants.featureConceptsUsedDetailsStr]     = getPracticeConceptsUsedDetails(studentDataDf)
                
        studentDataDfGrouped = studentDataDf.groupby([constants.GROUPBY_FEATURE], as_index = False)

        
    #   Sum of features
        studentDataDfSum = studentDataDf.groupby([constants.GROUPBY_FEATURE, constants.COUNT_STUDENT_FEATURE], as_index=False).sum()
        
    #    get the Mean DF and merge both DF
        studentDataDfMean = studentDataDf.groupby([constants.GROUPBY_FEATURE], as_index=False).mean()
        studentDataDfMean.rename(columns = featuresOverviewAvgNames, inplace=True)
        
#        studentDataDfOverview = pd.merge(studentDataDfSum[featuresOverview], studentDataDfMean[featuresOverviewAvg].round(decimals=2), 
#                                         how='inner', on = constants.GROUPBY_FEATURE, left_index=False, right_index=False )
        
        
    #   Mean of comparision features    
        studentDataDfMean = studentDataDf.groupby([constants.GROUPBY_FEATURE], as_index = False).mean()
        
        
        studentDataDfMeanFinal = studentDataDfMean
        
        ConceptsUsedGroupList = []
        ConceptsUsedDetailsGroupList = []
        for groupKey, group in studentDataDfGrouped :
            if 'ConceptsUsed' in group.columns and  group[ group['ConceptsUsed'].notnull() ].shape[0] > 0 :
                ConceptsUsedGroupList.append( ', '.join( group[ group['ConceptsUsed'].notnull() ].iloc[0]['ConceptsUsed'] )   )
#                ConceptsUsedDetailsGroupList.append( ', '.join( group[ group['ConceptsUsedDetails'].notnull() ].iloc[0]['ConceptsUsedDetails']   ) )
            else :
                ConceptsUsedGroupList.append(' ')
#                ConceptsUsedDetailsGroupList.append(' ')
                
        
    
        studentDataDfMean['ConceptsUsed'] = ConceptsUsedGroupList
#        studentDataDfMean['ConceptsUsedDetails'] = ConceptsUsedDetailsGroupList
        
        studentDataDfMeanToPlot = studentDataDfMean[featuresOverview + ['ConceptsUsed'
#                                                                        , 'ConceptsUsedDetails'
                                                                        ]].round(decimals=2)
        studentDataDfMeanToPlot.rename(columns = featuresOverviewAvgNames, inplace=True)
        studentDataDfMeanToPlot.rename(columns = featuresOverviewGeneralNames, inplace=True)
                
        tableMean = dash_table.DataTable(
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in studentDataDfMeanToPlot.columns
            ],
            data            = studentDataDfMeanToPlot.to_dict('records'),
            editable        = True,
            filter_action       = "native",
            sort_action             = "native",
            sort_mode           = "multi",
            style_data_conditional=([
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
             ] +  
            [
                {
                    'if': {
                        'filter_query'  : '{{SessionDuration Avg.}} = {}'.format(i),
                        'column_id'     : 'SessionDuration Avg.',
                    },
                    'backgroundColor': constants.ERROR_COLOR,
                    'color': 'white'
                }
                for i in studentDataDfMeanToPlot['SessionDuration Avg.'].nsmallest(1)
            ] + 
            [
                {
                    'if': {
                        'filter_query'  : '{{Points Avg.}} = {}'.format(i),
                        'column_id'     : 'Points Avg.',
                    },
                    'backgroundColor': constants.ERROR_COLOR,
                    'color': 'white'
                }
                for i in studentDataDfMeanToPlot['Points Avg.'].nsmallest(1)        
            ] + 
            [
                {
                    'if': {
                        'filter_query'  : '{{Attempts Avg.}} = {}'.format(i),
                        'column_id'     : 'Attempts Avg.',
                    },
                    'backgroundColor': constants.ERROR_COLOR,
                    'color': 'white'
                }
                for i in studentDataDfMeanToPlot['Attempts Avg.'].nsmallest(1)        
            ] + 
            [
                {
                    'if': {
                        'filter_query'  : '{{itemsCollectedCount Avg.}} = {}'.format(i),
                        'column_id'     : 'itemsCollectedCount Avg.',
                    },
                    'backgroundColor': constants.ERROR_COLOR,
                    'color': 'white'
                }
                for i in studentDataDfMeanToPlot['itemsCollectedCount Avg.'].nsmallest(1)        
            ] + 
            [
                {
                    'if': {
                        'filter_query': '{{GroupId}} = {}'.format(i),
                    },
                    'backgroundColor': constants.THEME_CYAN_COLOR,
                    'color': 'white'
                }
                for i in [ schoolKey ]
            ]
            ),
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        ),
        
        
#        tableMean = dbc.Table.from_dataframe(studentDataDfMeanToPlot, 
#                                             striped=True, bordered=True, hover=True, className = "table-comparision")
        columns2 = []
        columns2.append(dbc.Col(tableMean , align="center"))
    

        rows.append( dbc.Row( html.Div([
                    html.H3('Overview'), 
                ]) ) )
        rows.append( dbc.Row( columns2 ) )
        
        
        
#        -------------------
#        the Quantile Plots - distribution for each feature
        rows.append( html.Br() )
        rows.append( dbc.Row( html.Div([
                    html.H3('Distributions'), 
                ]) ) )


        studentDataDfStudentSum = studentDataDf.groupby([constants.GROUPBY_FEATURE, constants.COUNT_STUDENT_FEATURE, 
                                                         constants.STUDENT_ID_FEATURE, "Name" ], as_index=False).sum()
        

#Session duration
        figQuantile = px.box(studentDataDfStudentSum, x="GroupId", y="SessionDuration", points="all",
                             title="Distribution of Session Duration",
                             hover_data=[constants.STUDENT_ID_FEATURE, "Name", "SessionDuration", "Attempts", "Points"]
#                             , marker_color = 'rgb(214,12,140)'
                             )   
        figQuantile.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)         
        columns3 = []
        columns3.append(dbc.Col(
                dcc.Graph(
                        figure= figQuantile
                    ) , align="center"))    
        rows.append( dbc.Row( columns3 ) ) 
        rows.append( html.Br() )       

#Attempts
        figQuantile = px.box(studentDataDfStudentSum, x="GroupId", y="Attempts", points="all",
                             title="Distribution of Attempts",
                             hover_data=["StudentId", "Name", "SessionDuration", "Attempts", "Points"]
                             )       
        figQuantile.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)            
        columns3 = []
        columns3.append(dbc.Col(
                dcc.Graph(
                        figure= figQuantile
                    ) , align="center"))    
        rows.append( dbc.Row( columns3 ) )      
        rows.append( html.Br() )         
        
#Points
        figQuantile = px.box(studentDataDfStudentSum, x="GroupId", y="Points", points="all",
                             title="Distribution of Points",
                             hover_data=["StudentId", "Name", "SessionDuration", "Attempts", "Points"]
                             )     
        figQuantile.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)                      
        columns3 = []
        columns3.append(dbc.Col(
                dcc.Graph(
                        figure= figQuantile
                    ) , align="center"))    
        rows.append( dbc.Row( columns3 ) )       
        rows.append( html.Br() )           

#Items Collected
        figQuantile = px.box(studentDataDfStudentSum, x="GroupId", y="itemsCollectedCount", points="all",
                             title="Distribution of Items Collected",
                             hover_data=["StudentId", "Name", "SessionDuration", "Attempts", "Points"]
                             )    
        figQuantile.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)                           
        columns3 = []
        columns3.append(dbc.Col(
                dcc.Graph(
                        figure= figQuantile
                    ) , align="center"))    
        rows.append( dbc.Row( columns3 ) )      
        rows.append( html.Br() )             


        fig = go.Figure()        
        for groupId, group in studentDataDfStudentSum.groupby([constants.GROUPBY_FEATURE], as_index=False):
#            print(group[constants.featureDescription])
            groupDataStudent = getStudentWiseData(group)
            fig.add_trace(go.Box(
                y               = groupDataStudent['itemsCollectedCount'],                    
                marker_color    = 'rgb(214,12,140)',
                name            = groupId,
                boxpoints       = 'all',
                text            = groupDataStudent['Name'],
            ))
        
        fig.update_layout(
            title           ='Distribution of Items Collected',
            paper_bgcolor   = 'rgb(243, 243, 243)',
            plot_bgcolor    = 'rgb(243, 243, 243)',
            yaxis_title     ='Item Collected Count', 
            xaxis_title     = 'Group',
        )
        columns3 = []
        columns3.append(dbc.Col(
                                dcc.Graph(
                                        figure = fig
                                )  , align="center"))    
        rows.append( dbc.Row( columns3 ) )  


        
#        standard deviation and for each group
        
#        df.std(axis = 0, skipna = True) 
        
        studentDataDfMeanStd = studentDataDfMeanToPlot.std(axis = 0, skipna = True) 
        studentDataDfMeanStdToPlot = pd.concat([studentDataDfMeanStd], axis=1)
        
        
        print('studentDataDfMeanStdToPlot')
        print(studentDataDf.std(axis = 0, skipna = True) )
        print(studentDataDfMeanStd)
        print(studentDataDfMeanStdToPlot)
        print(studentDataDfMeanStdToPlot.columns)
        
        tableMean = dbc.Table.from_dataframe(studentDataDfMeanStdToPlot, 
                                             striped=True, bordered=True, hover=True, className = "table-comparision")
        columns3 = []
        columns3.append(dbc.Col(tableMean , align="center"))
    
        rows.append( dbc.Row( html.Div('Overview') ) )
        rows.append( dbc.Row( columns3 ) )
        
        
        graphs.append(html.Div(  rows,
                     className = "width-100"  ))
        
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

    return  html.Div(graphs,
                     className = "width-100")
    