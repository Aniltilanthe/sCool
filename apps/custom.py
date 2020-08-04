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


getFigureTypesOptions                   = constants.getFigureTypesOptions



#-----------------------------------Functions START ----------------------------------------
FeaturesCustom = ['SessionDuration', 'Points', 'Attempts', 'CollectedCoins', 'Difficulty']

FeaturesCustomPractice = ['NumberOfCoins', 'runsCount', 'runsErrorCount', 'runsSuccessCount', 'runsErrorSyntaxCount',
                                           'runsErrorNameCount', 'runsErrorTypeCount', 'runsLineOfCodeCountAvg',
                                           'tabsSwitchedCount', 'tabsSwitchedDescriptionCount', 'deletedCodesCount', 'robotCollisionsBoxCount']
FeaturesCustomTheory = ['playerShootCount', 'playerShootEndCount', 'playerShootEndEnemyHitCount',
                                         'playerShootEndEnemyMissedHitCount', 'enemysShootEndPlayerHitCount']


FigureTypes = constants.FigureTypes 


graphHeight         =  constants.graphHeight
graphHeight         =   graphHeight - 200


hoverData           =  ["CollectedCoins", "Result", "SessionDuration", "Attempts", "robotCollisionsBoxCount", "Points", "lineOfCodeCount", 'StudentId']


Feature1            = "Name"
Feature3Size        = "SessionDuration"

        
def BuildOptionsFeatures(options):  
    return [{'label': constants.feature2UserNamesDict.get(i) if i in constants.feature2UserNamesDict.keys() else i , 'value': i} for i in options]


#Student Interaction with Game - TIMELINE
def plotClassOverview(schoolKey, featureToPlot, selectedAxis, selectedFigureType, feature1 = Feature1, feature3 = Feature3Size ):

    graphs = []
    rows = []
    
    if (None == schoolKey) :
        return graphs
    
    if (None == featureToPlot) :
        return graphs
    
    studentDataDf = studentGrouped.getStudentsOfSchoolDF(schoolKey)
    
    print(' plotClassOverview got studentDataDf   ' )
    
        

    if 'studentDataDf' in locals()     and    ( studentDataDf is not None  )    and    ( featureToPlot in studentDataDf.columns )   :
        
        studentDataDf[constants.featureConceptsUsedDetailsStr]     = getPracticeConceptsUsedDetailsStr(studentDataDf)
                
        studentDataDfGrouped = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index = False)
    
#--------------------------------Total of each Features ----------------------------------     
        
        studentDataDfSum = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index=False).sum()        
        
#Default Horizontal Plots
        
        featureX2Plot = featureToPlot
        featureY2Plot = feature1
        
        
        plotTitle = ' Details of students ' 
        plotTitle = plotTitle + str( constants.feature2UserNamesDict.get(featureX2Plot) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot )
        plotTitle = plotTitle + ' vs ' + str( constants.feature2UserNamesDict.get(featureY2Plot) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot )
        
        
        hoverName = "Name"
        
        
        marginalX = ''
        marginalY = ''
        
        
        print('selectedFigureType   ' + str(selectedFigureType) + '   featureX2Plot   ' + str(featureX2Plot)  + '   featureY2Plot   ' + str(featureY2Plot) )
    
        
        try:
            if selectedFigureType == constants.FigureTypeScatter:
                
                if not None == selectedAxis and selectedAxis == constants.AxisV:
                    featureX2Plot = feature1
                    featureY2Plot = featureToPlot
                
                print('Scatter Chart figure   Check Numeric ! ' )
                if util.checkIsFeatureNumeric(studentDataDfSum, featureX2Plot):
                     marginalX = constants.MarginalPlotDefault
                     
                if util.checkIsFeatureNumeric(studentDataDfSum, featureY2Plot):
                     marginalY = constants.MarginalPlotDefault
                print('Scatter Chart figure   After  Check Numeric ! ' )
                
                
                figStudents = px.scatter(studentDataDfSum, x = featureX2Plot, y = featureY2Plot
                     , title        =   plotTitle
                     , labels       =   constants.feature2UserNamesDict # customize axis label
                     , hover_name   =   hoverName
                     , hover_data   =   hoverData
                     , marginal_x   =   marginalX
                     , marginal_y   =   marginalY
                     , height       =   graphHeight
                     , template     =   constants.graphTemplete
                    )
                figStudents.update_traces(marker=dict(size = 16
                                            , showscale    = False
                                            ,  line = dict(width=1,
                                                        color='DarkSlateGrey')),
                                  selector=dict(mode='markers'))
                figStudents.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)
                print('Scatter Chart figure   Made Success ! ' )
           
        
        
#            Error when plotting pie charts !!!
#            elif selectedFigureType == FigureTypePie:
#                
#                print('Pie Chart figure   featureX2Plot  ' + str(featureX2Plot) + '   plotTitle   ' + str(plotTitle)  )
#    
#                figStudents = px.pie(studentDataDfSum, values = featureX2Plot
#                                     , names        =  'Name'
#                                     , title        =   plotTitle
#                                     , labels       =   constants.feature2UserNamesDict # customize axis label
#                                     , hover_name   =   hoverName
#                                     , hover_data   =   hoverData
#                                     , height       =   graphHeight
#                                     , template     =   constants.graphTemplete
#                                     )
#                figStudents.update_traces(textposition='inside', textinfo='percent+label+value')
#                figStudents.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)
#                    
#                print('Pie Chart figure   Made Success ' )
                
                
            elif selectedFigureType == constants.FigureTypeBar :
                orientation = constants.AxisH
                if not None == selectedAxis and selectedAxis == constants.AxisV:
                    featureX2Plot   = feature1
                    featureY2Plot   = featureToPlot
                    orientation     = constants.AxisV
                
                figStudents = px.bar( studentDataDfSum
                    , x             =   featureX2Plot
                    , y             =   featureY2Plot
                    , title         =   plotTitle
                    , labels        =   constants.feature2UserNamesDict # customize axis label
                    , template      =   constants.graphTemplete                              
                    , orientation   =   orientation
                    , hover_name    =   hoverName
                    , hover_data    =   hoverData
                    , height        =   graphHeight
                )
                figStudents.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)
                print('Baar Chart figure   Made Success ! ' )
            
            
            elif selectedFigureType == constants.FigureTypeBubble :
                
                if not None == selectedAxis and selectedAxis == constants.AxisV:
                    featureX2Plot   = feature1
                    featureY2Plot   = featureToPlot
                
                figStudents = px.scatter(studentDataDfSum, x = featureX2Plot, y = featureY2Plot
                     , title        =   plotTitle
                     , labels       =   constants.feature2UserNamesDict # customize axis label
                     , hover_name   =   hoverName
                     , hover_data   =   hoverData
                     , size         =   feature3
                     , color        =   "Name"
                     , size_max     =   60
                     , height       =   graphHeight
                     , template     =   constants.graphTemplete
                    )
                figStudents.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)
                
                rows.append( html.Div(children=[
                                html.P('Size is based on ' + ((constants.feature2UserNamesDict.get(feature3)) if feature3 in constants.feature2UserNamesDict.keys() else feature3 ) ),
                                ]) )
                
                
            elif selectedFigureType == constants.FigureTypeLine :

                if not None == selectedAxis and selectedAxis == constants.AxisV:
                    featureX2Plot   = feature1
                    featureY2Plot   = featureToPlot
                
                figStudents = px.line(studentDataDf
                    , x             =   featureX2Plot
                    , y             =   featureY2Plot
                    , color         =   "Name"
                    , hover_name    =   hoverName
                    , hover_data    =   hoverData
                    , height        =   graphHeight
                    , template      =   constants.graphTemplete                              
                )
                figStudents.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)
            
            
            
            
            rows.append( dbc.Row( dcc.Graph(
                    figure= figStudents,
                    className = "graph-small"
            ) ) )
            
            print('Before Mean and Std calculation ! ' )

            
            studentDataDfSumMean    = studentDataDfSum.mean().round(decimals=2)
            studentDataDfSumStd     = studentDataDfSum.std().round(decimals=2)

            print('After Mean and Std calculation ! ' )
            
            try :
                print('before Mean and Std calculation for 1 ! ' )
                if   not 'Name' == featureX2Plot   and  featureX2Plot is not None and featureX2Plot in studentDataDfSumMean:
                    rows.append( html.Div(children=[
                                html.P('Mean  ' + ((constants.feature2UserNamesDict.get(featureX2Plot)) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot )  + ' = ' + str(studentDataDfSumMean[featureX2Plot]) ),
                                html.P('Std. ' + ((constants.feature2UserNamesDict.get(featureX2Plot)) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot ) + ' = ' + str(studentDataDfSumStd[featureX2Plot]) ),
                                ]) )
                print('Added Mean and Std calculation for 1 ! ' )
            except Exception as e: 
                print('Exception Mean and Std calculation for 1 ! ' )
                print(e)
            try :
                print('before Mean and Std calculation for 2 ! ' )
                if  not 'Name' == featureY2Plot   and   featureY2Plot is not None and featureY2Plot in studentDataDfSumMean:
                    rows.append( html.Div(children=[
                                    html.P('Mean  ' + ((constants.feature2UserNamesDict.get(featureY2Plot)) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot )  + ' = ' + str(studentDataDfSumMean[featureY2Plot]) ),
                                    html.P('Std. ' + ((constants.feature2UserNamesDict.get(featureY2Plot)) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot ) + ' = ' + str(studentDataDfSumStd[featureY2Plot]) ),
                                    ]) )
                print('Added Mean and Std calculation for 2 ! ' )
            except Exception as e: 
                print('Exception Mean and Std calculation for 2 ! ' )
                print(e)
        
        except Exception as e: 
            print('Add Graph exception ! ' )
            print(e)
            
            
        graphs.append( html.Div( rows ) )

    return graphs




def generateControlCard():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card-custom",
        children=[

            html.P("Select Features")
            
            
            , dbc.Row([
                    dbc.Col(
                      html.Div([
                                dcc.Dropdown(
                                    id      = "form-feature-selector-custom",
                                    options = BuildOptionsFeatures( FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory ),
                                )
                            ],
                            className = "c-container"
                       )
                        , width=6
                    ),
                    dbc.Col(
                        html.Div([
                            dcc.Dropdown(
                                    id              = 'form-feature-selector-1-custom', 
                                    placeholder     = "Select feature",
                                    options = BuildOptionsFeatures( [Feature1] + FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory ),
                                    value   = Feature1
                                )
                            ],
                            className = "c-container"
                        )
                        , width=3
                    ),
                    dbc.Col(
                        html.Div([
                            dcc.Dropdown(
                                    id              = 'form-feature-selector-3-size-custom', 
                                    placeholder     = "Select Size",
                                    options = BuildOptionsFeatures( FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory ),
                                    value   = Feature3Size
                                )
                            ],
                            className = "c-container"
                        )
                        , width=3
                    )
            ])
            
            , dcc.RadioItems(
                id          = "form-figure-type-custom",
                options     = getFigureTypesOptions(),
                value       = constants.FigureTypeBar ,
                labelStyle  = {'display': 'inline-block'},
                className   = "radio-items-inline"
            ), 
            dcc.RadioItems(
                id      ="form-feature-axis-custom",
                options=[
                    {'label': 'Horizontal (x-axis)', 'value': constants.AxisH},
                    {'label': 'Vertical (y-axis)', 'value': constants.AxisV},
                ],
                value       = constants.AxisH,
                labelStyle  = {'display': 'inline-block'},
                className   = "radio-items-inline"
            ), 
            html.Button(children=[
                    html.I(className="fas fa-plus font-size_medium p-right_xx-small"),
                    'Add Plot',  ], 
                        id='form-submit-btn-custom', 
                        className="c-button button w3-btn w3-xlarge", n_clicks=0),
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
    ])

    , html.Div(id='custom-main-container', className = "row custom-main-container" )
    
    , html.A(children=[html.I(className="fas fa-download font-size_medium p_small"),
                       "download data",], 
                    id = "custom_download_main_link", className = "hidden" ,
                                               href="", target="_blank",
                                               download='data.csv' )
]



#----------------------------------------------------------------------------------------------
#                    CALL BACK
#----------------------------------------------------------------------------------------------
# Form Submission  - Update plot container with new selected plot
@app.callback(
    Output("custom-main-container", "children"),
    [
        Input("form-submit-btn-custom", "n_clicks")
    ],
     state=[ State(component_id='group-selector-main', component_property='value'),
                State(component_id='form-feature-selector-custom', component_property='value'),
                State(component_id='form-feature-selector-1-custom', component_property='value'),
                State(component_id='form-feature-selector-3-size-custom', component_property='value'),
                State(component_id='form-feature-axis-custom', component_property='value'),
                State(component_id='form-figure-type-custom', component_property='value'),
                State(component_id='custom-main-container', component_property='children'),
                ]
)
def update_bar(n_clicks, groupMain, selectedFeature, selectedFeature1, selectedFeature3, selectedAxis, selectedFigureType, 
               containerChildren 
               ):    
    graphs = []
    
    print('update_bar')
    
    if n_clicks == 0 or groupMain is None or not int(groupMain) >= 0  or None is selectedFeature or '' == selectedFeature:
        return html.Div(graphs)
    
    if selectedFeature1 is None or  '' == selectedFeature1:
        selectedFeature1 = Feature1
    
    if selectedFeature3 is None or '' == selectedFeature3:
        selectedFeature3 = ''
        
    print('groupMain   ' + str(groupMain) + '   selectedFeature   ' + str(selectedFeature)  + '   selectedAxis   ' + str(selectedAxis) )
    print('selectedFigureType   ' + str(selectedFigureType) + '   selectedFeature1   ' + str(selectedFeature1)  + '     selectedFeature3   ' + str(selectedFeature3) )
    
    graphs = plotClassOverview( int(groupMain), selectedFeature, selectedAxis, selectedFigureType, selectedFeature1, selectedFeature3 )
    
    if not(None is containerChildren):
        if isinstance(containerChildren, list):
            print(' isinstance(containerChildren, list) ')
            graphs = graphs + containerChildren 
        else :
            if isinstance(containerChildren, dict) and 'props' in containerChildren.keys():
                print(' isinstance(containerChildren, dict) and props in containerChildren.keys() ')
                graphs = graphs + containerChildren.get('props').get('children')

    print(' graphs to plot ! ')

    return   graphs 




# Form Submission  - Update plot container with new selected plot
@app.callback(
    Output("form-feature-axis-custom", "className"),
    [
        Input("form-figure-type-custom", "value")
    ],
    state=[ State(component_id='form-feature-axis-custom', component_property='className') ]
)
def update_axis_selector_disabled(selectedFigureType, initialClass):   
    if None is selectedFigureType or '' == selectedFigureType:
        return initialClass
 
    initialClassS = set()
    
    if not None is initialClass:
        initialClassS = set(initialClass.split(' '))  
    
    if selectedFigureType in FigureTypes   and   not FigureTypes.get(selectedFigureType).get(constants.keyIsAxisEnabled):
        initialClassS.add('disabled')  
    else:
        initialClassS.discard('disabled') 

    return  ' '.join(initialClassS)


@app.callback(
    Output("form-feature-selector-3-size-custom", "className"),
    [
        Input("form-figure-type-custom", "value")
    ],
    state=[ State(component_id='form-feature-selector-3-size-custom', component_property='className') ]
)
def update_feature_size_disabled(selectedFigureType, initialClass):   
    if None is selectedFigureType or '' == selectedFigureType:
        return initialClass

    initialClassS = set()
    
    if not None is initialClass:
        initialClassS = set(initialClass.split(' ')) 

    if selectedFigureType in FigureTypes and   not FigureTypes.get(selectedFigureType).get(constants.keyIsFeature3Enabled):
        initialClassS.add('disabled') 
    else:
        initialClassS.discard('disabled') 

    return  ' '.join(initialClassS)




@app.callback(
    [ Output('custom_download_main_link', 'href'),
     Output('custom_download_main_link', 'className'),
     ],
    [ Input("group-selector-main", "value") ],
)
def update_download_link_custom_group(groupMain):
    if groupMain is None or not int(groupMain) >= 0 or groupMain == "":
        return "", "hidden"
    
    csv_string = util.get_download_link_data_uri( studentGrouped.getStudentsOfSchoolDF(int(groupMain)) )
    return csv_string, ""

