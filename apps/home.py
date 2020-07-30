# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 19:13:32 2020

@author: tilan
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 18:16:48 2020

@author: tilan
"""
import numpy as np
import plotly.express as px

import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import chart_studio.plotly as py
from plotly import graph_objs as go



from app import app


import studentGrouped
import constants
import util

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
dfPracticeDB                            = studentGrouped.dfPracticeDB


dfPlayerStrategyTheory                  = studentGrouped.dfPlayerStrategyTheory
dfGroupedPlayerStrategyTheory           = studentGrouped.dfGroupedPlayerStrategyTheory

#--------------------------------- DataBase get data END ---------------------------



#-----------------------------------Functions START ----------------------------------------
featuresCombined       =   constants.featuresCombined

    
def plotGameOverview():
    
    allGroups       = dfStudentDetails[constants.GROUPBY_FEATURE].unique()
    allStudents     =  dfStudentDetails[constants.STUDENT_ID_FEATURE].unique()
    
    plots = []
    
    plotRow = []
    plotRow.append(html.Div([
                                util.generateCardBase([html.I(className="fas fa-globe m-right-small"),   'No of Groups'], len(allGroups))
                            ],
                            className="col-sm-6",
                        ))
    plotRow.append( html.Div([
                                util.generateCardBase([html.I(className="fas fa-users m-right-small"),   'No of Students'], len(allStudents))
                            ],
                            className="col-sm-6",
                        ))
    plots.append(
            html.Div(children  = plotRow,                
                     className = "row")
    )


    dfAllData = pd.concat([dfPracticeDB[featuresCombined] , dfPlayerStrategyTheory[featuresCombined]], ignore_index=True, sort =False)

    plotRow = []    
    plotRow.append(
            html.Div([
                   util.generateCardDetail([html.I(className="fas fa-clock m-right-small"),   'Game Time'], 
                                        '' + util.seconds_2_dhms(dfAllData['SessionDuration'].sum().round(decimals=2)), 
                                        '' + str(dfAllData['SessionDuration'].mean().round(decimals=2)) + 's', 
                                        '' + str(dfAllData['SessionDuration'].std().round(decimals=2)) + 's', 
                                        'total',
                                        'mean',
                                        'std',
                                        )
                ],
                className="col-sm-4",
            ))
    
    plotRow.append(
            html.Div([
                   util.generateCardDetail('Points Collected', 
                                        '' + util.millify(dfAllData['Points'].sum().round(decimals=2)), 
                                        '' + str(dfAllData['Points'].mean().round(decimals=2)), 
                                        '' + str(dfAllData['Points'].std().round(decimals=2)), 
                                        'total',
                                        'mean',
                                        'std',
                                        )
                ],            
                className="col-sm-4",
            ))

    plotRow.append(
            html.Div([
                   util.generateCardDetail2([html.I(className="fas fa-clock m-right-small"),   'Game Time Spent - Practice vs Theory'], 
                                        '' + util.seconds_2_dhms(dfPracticeDB['SessionDuration'].sum().round(decimals=2)), 
                                        '' + util.seconds_2_dhms(dfPlayerStrategyTheory['SessionDuration'].sum().round(decimals=2)), 
                                        'Practice',
                                        'Theory'
                                        )
                ],
                className="col-sm-4",
            ))
    plots.append(
            html.Div(children  = plotRow,                
                     className = "row")
    )
    
    return plots

    


#----------------------------------Functions END --------------------------------------------






layout = [
            
    dbc.Row([
            dbc.Col(
                # Left column
                html.Div(
                    id="game-main-overview",
                    className="",
                    children=  [html.H1("sCool"),
                                html.H2("Game Overview")]  ,
                ),
        ),
    ]),
    dbc.Row([
            dbc.Col(
                # Left column
                html.Div(
                    className="game-overview m-bottom_medium",
                    children=  plotGameOverview()  ,
                ),
        ),
    ]),    
]
                
      