# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 10:34:38 2020

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
getPracticeConceptsUsedDetailsStr          =  studentGrouped.getPracticeConceptsUsedDetailsStr
getStudentWiseData                      =  studentGrouped.getStudentWiseData


BuildOptions                            =  studentGrouped.BuildOptions

#--------------------------- helper functions END -----------------------  




#-----------------------------------Functions START ----------------------------------------
FeaturesCustom = ['SessionDuration', 'Points', 'Attempts', 'CollectedCoins', 'Difficulty']

FeaturesCustomPractice = ['NumberOfCoins', 'runsCount', 'runsErrorCount', 'runsSuccessCount', 'runsErrorSyntaxCount',
                                           'runsErrorNameCount', 'runsErrorTypeCount', 'runsLineOfCodeCountAvg',
                                           'tabsSwitchedCount', 'tabsSwitchedDescriptionCount', 'deletedCodesCount', 'robotCollisionsBoxCount']
FeaturesCustomTheory = ['playerShootCount', 'playerShootEndCount', 'playerShootEndEnemyHitCount',
                                         'playerShootEndEnemyMissedHitCount', 'enemysShootEndPlayerHitCount']



#Student Interaction with Game - TIMELINE
def plotClassOverview(schoolKey, featureToPlot, selectedAxis):

    graphs = []
    rows = []
    
    if (None == schoolKey) :
        return graphs
    
    if (None == featureToPlot) :
        return graphs
    
    studentDataDf = studentGrouped.getStudentsOfSchoolDF(schoolKey)
        

    if 'studentDataDf' in locals()     and    studentDataDf is not None  :
        
        studentDataDf[constants.featureConceptsUsedDetailsStr]     = getPracticeConceptsUsedDetailsStr(studentDataDf)
                
        studentDataDfGrouped = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index = False)

        
    #   Sum of features
        studentDataDfStudentSum = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index=False).sum()
        
        
    
#--------------------------------Total of each Features ----------------------------------     
        
        studentDataDfSum = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index=False).sum()
        
        ConceptsUsedGroupList = []
        ConceptsUsedDetailsGroupList = []
        for groupKey, group in studentDataDfGrouped :
            if 'ConceptsUsed' in group.columns and  group[ group['ConceptsUsed'].notnull() ].shape[0] > 0 :
                ConceptsUsedGroupList.append( ', '.join( group[ group['ConceptsUsed'].notnull() ].iloc[0]['ConceptsUsed'] )   )
                ConceptsUsedDetailsGroupList.append( ', '.join( group[ group['ConceptsUsedDetails'].notnull() ].iloc[0]['ConceptsUsedDetails'] )   )
            else :
                ConceptsUsedGroupList.append(' ')
                ConceptsUsedDetailsGroupList.append(' ')
        studentDataDfSum['ConceptsUsed'] = ConceptsUsedGroupList
        studentDataDfSum['ConceptsUsedDetails'] = ConceptsUsedDetailsGroupList
        
        studentDataDfSum['ConceptsUsedDetailsStr']= studentDataDfSum['ConceptsUsedDetails'].apply(lambda x: x[1:-1])

#Default Horizontal Plots
        featureX2Plot = featureToPlot
        featureY2Plot = 'Name'
        
        if not None == selectedAxis and selectedAxis == 'Vertical':
            featureX2Plot = 'Name'
            featureY2Plot = featureToPlot
        
        figStudents = px.scatter(studentDataDfSum, x = featureX2Plot, y = featureY2Plot
             , title  = ' Details of students ' + featureToPlot
             , labels  =  constants.feature2UserNamesDict # customize axis label
             , hover_name  =  "Name"
             , hover_data  =  ["CollectedCoins", "Result", "SessionDuration", "Attempts", "robotCollisionsBoxCount", "Points", "ConceptsUsedDetailsStr", "lineOfCodeCount", 'StudentId']
#             , marginal_x  = "box"
             , height       = constants.graphHeight
             , template     = constants.graphTemplete
            )
        figStudents.update_traces(marker=dict(size = 16
                                    , showscale    = False
                                    ,  line = dict(width=1,
                                                color='DarkSlateGrey')),
                          selector=dict(mode='markers'))
        figStudents.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)
        
#        columns3 = []
#        columns3.append(dbc.Col(
#                dcc.Graph(
#                        figure= figStudents
#                    ) , align="center"))    
#        rows.append( dbc.Row( columns3 ) ) 
#        rows.append( html.Br() )       
#        graphs.append(html.Div(  rows,
#                     className = "width-100"  ))

        
        graphs.append(
            dcc.Graph(
                figure= figStudents,
                className = "graph-small"
        ))

    return graphs




def generateControlCard():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card-custom",
        children=[

            html.P("Select Features"),
            dcc.Dropdown(
                id      ="form-feature-selector-custom",
                options = BuildOptions( FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory ),
            ),
            dcc.RadioItems(
                id      ="form-feature-axis-custom",
                options=[
                    {'label': 'Horizontal (x-axis)', 'value': 'Horizontal'},
                    {'label': 'Vertical (y-axis)', 'value': 'Vertical'},
                ],
                value       = 'Horizontal',
                labelStyle  = {'display': 'inline-block'},
                className   = "radio-items-inline"
            ),  
            html.Button('Submit', id='form-submit-btn-custom', className="button", n_clicks=0),
            html.Br(),
        ],
        className = "form"
    )


#------------------------------------------------------------------------------------------------
#---------------------------LAYOUT --------------------------------------------------------------


layout = [

    dbc.Row([
            dbc.Col(
                # Left column
                html.Div(
                    id="row-control-main-custom",
                    className="",
                    children=[ generateControlCard() ]
                    + [
                        html.Div(
                            ["initial child"], id="row-control-main-output-clientside-custom", style={"display": "none"}
                        )
                    ],
                ),
        ),
    ]),

    html.Div(id='custom-main-container', className = "row custom-main-container" )
]



#----------------------------------------------------------------------------------------------
#                    CALL BACK
#----------------------------------------------------------------------------------------------
@app.callback(
    [ 
         Output("feature-selector-custom", "value"), 
    ],
    [
        Input("reset-btn-custom", "n_clicks")
    ],
)
def on_reset(reset_click):
    # Find which one has been triggered
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "reset-btn" and reset_click:
            return [""]
            
    return [""]



# Update bar plot
@app.callback(
    Output("custom-main-container", "children"),
    [
        Input("form-submit-btn-custom", "n_clicks")
    ],
     state=[ State(component_id='group-selector-main', component_property='value'),
                State(component_id='form-feature-selector-custom', component_property='value'),
                State(component_id='form-feature-axis-custom', component_property='value'),
                State(component_id='custom-main-container', component_property='children')]
)
def update_bar(n_clicks, groupMain, selectedFeature, selectedAxis, containerChildren ):    
    graphs = []

    if n_clicks == 0 or groupMain is None or not int(groupMain) >= 0  or None is selectedFeature or '' == selectedFeature:
        return html.Div(graphs)
    
    graphs = plotClassOverview( int(groupMain), selectedFeature, selectedAxis )    
    
    if not(None is containerChildren):
        if isinstance(containerChildren, list):
            graphs = graphs + containerChildren 
        else :
            if isinstance(containerChildren, dict) and 'props' in containerChildren.keys():
                graphs = graphs + containerChildren.get('props').get('children')

    return  graphs