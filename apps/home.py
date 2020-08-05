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





idApp             = "home"


#--------------------- school selection START ----------------------
GroupSelector_options = studentGrouped.GroupSelector_options 
#--------------------- school selection END ----------------------



#--------------------------------- DataBase get data START ---------------------------
dfStudentDetails                        = studentGrouped.dfStudentDetails


dfPracticeTaskDetails                   = studentGrouped.dfPracticeTaskDetails
dfTheoryTaskDetails                     = studentGrouped.dfTheoryTaskDetails


dfPlayerStrategyPracticeOriginal        = studentGrouped.dfPlayerStrategyPracticeOriginal

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
                   util.generateCardDetail2([html.I(className="fas fa-clock m-right-small"),   'Game Time Spent - Practice vs Theory'], 
                                        '' + util.seconds_2_dhms(dfPracticeDB['SessionDuration'].sum().round(decimals=2)), 
                                        '' + util.seconds_2_dhms(dfPlayerStrategyTheory['SessionDuration'].sum().round(decimals=2)), 
                                        'Practice',
                                        'Theory'
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

    plots.append(
            html.Div(children  = plotRow,                
                     className = "row")
    )
    
    return plots


def plotGamePlots (feature1 = '',  feature2 = '', feature3 = '', 
                   selectedAxis = constants.AxisH, 
                   selectedFigureType = constants.FigureTypeBar,
                   plotClassName = " col-sm-6 ") :

    graphs = []
    rows = []
    
    if (None == feature1   or  '' == feature1  or '' == feature2 ) :
        return graphs
    
    
    gameData = pd.concat([dfPlayerStrategyPracticeOriginal, dfPlayerStrategyTheory], ignore_index=True)
            
#--------------------------------Total of each Features ----------------------------------     
    
    gameDataDfGroupedStudent = gameData.groupby([constants.GROUPBY_FEATURE, 
                                                 constants.STUDENT_ID_FEATURE], as_index=False).sum()

    gameDataDfGroupedStudent = gameDataDfGroupedStudent.merge(
            dfStudentDetails[['StudentId', 'Name']]
            , how='inner', on=['StudentId'], left_index=False, right_index=False)
    

    if 'gameDataDfGroupedStudent' in locals()     and    ( gameDataDfGroupedStudent is not None  )    and    ( feature1 in gameDataDfGroupedStudent.columns ) and (feature2 in gameDataDfGroupedStudent.columns)   :
        
        
        plotTitle   = ' Details of students ' 
        plotTitle   = plotTitle + str( constants.feature2UserNamesDict.get(feature1) if feature1 in constants.feature2UserNamesDict.keys() else feature1 )
        plotTitle   = plotTitle + ' vs ' + str( constants.feature2UserNamesDict.get(feature2) if feature2 in constants.feature2UserNamesDict.keys() else feature2 )
        
        hoverName   = "Name"
        color       = "Name"
        
        marginalX   = ''
        marginalY   = ''
        
        print('selectedFigureType   ' + str(selectedFigureType) + '   feature1   ' + str(feature1)  + '   feature2   ' + str(feature2) )
        
        rows = util.getCustomPlot(
                          df                    = gameDataDfGroupedStudent, 
                          featureX              = feature1, 
                          featureY              = feature2, 
                          feature3              = feature3, 
                          selectedFigureType    = selectedFigureType, 
                          selectedAxis          = selectedAxis, 
                          plotTitle             = plotTitle,
                          hoverName             = hoverName,
                          marginalX             = marginalX,
                          marginalY             = marginalY,
                          hoverData             = hoverData,
                          color                 = color
            )
       
        graphs.append( html.Div( rows ,
                                className = plotClassName ) )
        

    return graphs

   
    

    
FeaturesCustom          = constants.FeaturesCustom

FeaturesCustomPractice  = constants.FeaturesCustomPractice
FeaturesCustomTheory    = constants.FeaturesCustomTheory


FigureTypes             = constants.FigureTypes 


graphHeight         =  constants.graphHeight
graphHeight         =   graphHeight - 200


hoverData           =  constants.hoverData
hoverData.remove("lineOfCodeCount")



def generateControlCardCustomPlot():
    
    return util.generateControlCardCustomPlotForm(
            idApp                   = idApp, 
            feature1Options         = FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory , 
            feature2Options         = FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory, 
            feature3Options         = FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory, 
            feature1ValueDefault    = "",
            feature2ValueDefault    = "",
            feature3ValueDefault    = "",
            figureTypeDefault       = constants.FigureTypeScatter
    )

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
    ])
    ,  dbc.Row([
            dbc.Col(
                # Left column
                html.Div(
                    className="game-overview m-bottom_medium",
                    children=  plotGameOverview()  ,
                ),
        ),
    ])    
                        
                        
    , dbc.Row([
            dbc.Col(
                # Left column
                html.Div(
                    id= idApp + "-custom-plot-form",
                    className=" m_small",
                    children=[ generateControlCardCustomPlot() ]
                ),
        ),
    ])

    , html.Div(id = idApp + "-custom-plot-container", className = "row custom-main-container m-top_small" )

]
                
      
        
        
        
#----------------------------------------------------------------------------------------------
#                    CALL BACK
#----------------------------------------------------------------------------------------------
# Form Submission  - Update plot container with new selected plot
@app.callback(
    Output( idApp + "-custom-plot-container", "children"),
    [
        Input( idApp + "-form-submit-btn", "n_clicks")
    ],
     state=[    State(component_id = idApp + "-form-feature-1", component_property='value'),
                State(component_id = idApp + "-form-feature-2", component_property='value'),
                State(component_id = idApp + "-form-feature-3", component_property='value'),
                State(component_id = idApp + "-form-feature-axis", component_property='value'),
                State(component_id = idApp + "-form-figure-type", component_property='value'),
                State(component_id = idApp + "-custom-plot-container", component_property='children'),
                ]
)
def update_bar(n_clicks, selectedFeature1, selectedFeature2, selectedFeature3, selectedAxis, selectedFigureType, 
               containerChildren 
               ):    
    graphs = []
    
    if n_clicks == 0 or None is selectedFeature1 or '' == selectedFeature1:
        return html.Div(graphs)
    
    if selectedFeature2 is None or  '' == selectedFeature2:
        selectedFeature1 = ''
    
    if selectedFeature3 is None or '' == selectedFeature3:
        selectedFeature3 = ''
        
    print('   selectedFeature2   ' + str(selectedFeature2)  + '   selectedAxis   ' + str(selectedAxis) )
    print('selectedFigureType   ' + str(selectedFigureType) + '   selectedFeature1   ' + str(selectedFeature1)  + '     selectedFeature3   ' + str(selectedFeature3) )
    
    graphs = plotGamePlots( feature1 = selectedFeature1, 
                           feature2 = selectedFeature2, 
                           feature3 = selectedFeature3,
                           selectedAxis = selectedAxis, 
                           selectedFigureType = selectedFigureType, 
                           plotClassName = " col-sm-12 ")
    
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
    Output(idApp + "-form-feature-axis", "className"),
    [
        Input(idApp + "-form-figure-type", "value")
    ],
    state=[ State(component_id = idApp + "-form-feature-axis", component_property='className') ]
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
    Output(idApp + "-form-feature-3", "className"),
    [
        Input(idApp + "-form-figure-type", "value")
    ],
    state=[ State(component_id = idApp +"-form-feature-3", component_property='className') ]
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

