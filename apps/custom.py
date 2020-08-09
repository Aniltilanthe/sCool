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




from data import studentGrouped
import constants
import util




idApp             = "custom"


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
FeaturesCustom          = constants.FeaturesCustom

FeaturesCustomPractice  = constants.FeaturesCustomPractice
FeaturesCustomTheory    = constants.FeaturesCustomTheory


FigureTypes             = constants.FigureTypes 


graphHeight         =  constants.graphHeight
graphHeight         =   graphHeight - 200


hoverData           =  constants.hoverData


Feature1            = "Name"
Feature3Size        = "SessionDuration"

#Student Interaction with Game - TIMELINE
def plotClassOverview(schoolKey, feature1, selectedAxis, selectedFigureType, feature2 = Feature1, feature3 = Feature3Size,
                      plotClassName = " col-sm-6 ", selectedDistribution = [] ):

    graphs = []
    rows = []
    
    if (None == schoolKey) :
        return graphs
    
    if (None == feature1) :
        return graphs
    
    studentDataDf = studentGrouped.getStudentsOfSchoolDF(schoolKey)
    
    print(' plotClassOverview got studentDataDf   ' )

    if 'studentDataDf' in locals()     and    ( studentDataDf is not None  )    and    ( feature1 in studentDataDf.columns )   :
        
        studentDataDf[constants.featureConceptsUsedDetailsStr]     = getPracticeConceptsUsedDetailsStr(studentDataDf)
                
        studentDataDfGrouped = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index = False)
    
#--------------------------------Total of each Features ----------------------------------     
        
        studentDataDfSum = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index=False).sum()

        
        plotTitle   = ' Details of students ' 
        plotTitle   = plotTitle + str( constants.feature2UserNamesDict.get(feature1) if feature1 in constants.feature2UserNamesDict.keys() else feature1 )
        plotTitle   = plotTitle + ' vs ' + str( constants.feature2UserNamesDict.get(feature2) if feature2 in constants.feature2UserNamesDict.keys() else feature2 )
        
        
        hoverName   = "Name"
        color       = "Name"
        
        marginalX   = ''
        marginalY   = ''
        
        print('selectedFigureType   ' + str(selectedFigureType) + '   feature1   ' + str(feature1)  + '   feature2   ' + str(feature2) )
        
        rows = util.getCustomPlot(
                          df                    = studentDataDfSum, 
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
                          color                 = color,
                          selectedDistribution  = selectedDistribution
            )
       
        graphs.append( html.Div( rows ,
                                className = plotClassName ) )
        

    return graphs




def generateControlCardCustomPlotForm():
    
    return util.generateControlCardCustomPlotForm(
            idApp                   = idApp, 
            feature1Options         = FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory , 
            feature2Options         = [Feature1] + FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory, 
            feature3Options         = FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory, 
            feature1ValueDefault    = "",
            feature2ValueDefault    = Feature1,
            feature3ValueDefault    = Feature3Size,
            colorGroupIsDisabled    = True
    )

#------------------------------------------------------------------------------------------------
#---------------------------LAYOUT --------------------------------------------------------------


layout = [

    dbc.Row([
            dbc.Col(
                # Left column
                html.Div(
                    id= idApp + "-row-control-main",
                    className="",
                    children=[ generateControlCardCustomPlotForm() ]
                ),
        ),
    ])

    , html.Div(id = idApp + "-main-container", className = "row custom-main-container m-top_small" )
    
    , html.A(children=[html.I(className="fas fa-download font-size_medium p_small"),
                       "download data",], 
                    id = idApp + "-download-main-link", className = "disabled" ,
                                               href="", target =  "_blank",
                                               download='data.csv' )
]



#----------------------------------------------------------------------------------------------
#                    CALL BACK
#----------------------------------------------------------------------------------------------
    
    
# Form Submission  - Update plot container with new selected plot
@app.callback(
    Output( idApp + "-main-container", "children"),
    [
        Input( idApp + "-form-submit-btn", "n_clicks")
    ],
     state=[ State(component_id  =  'group-selector-main', component_property='value'),
                State(component_id = idApp + "-form-feature-1", component_property='value'),
                State(component_id = idApp + "-form-feature-2", component_property='value'),
                State(component_id = idApp + "-form-feature-3", component_property='value'),
                State(component_id = idApp + "-form-feature-axis", component_property='value'),
                State(component_id = idApp + "-form-figure-type", component_property='value'),
                State(component_id = idApp + "-form-feature-distribution", component_property='value'),
                State(component_id = idApp + "-main-container", component_property='children'),
                ]
)
def update_bar(n_clicks, groupMain, selectedFeature, selectedFeature1, selectedFeature3, selectedAxis, selectedFigureType, 
               selectedDistribution,
               containerChildren 
               ):    
    graphs = []
    
    print('update_bar')
    print(selectedDistribution)
    
    if n_clicks == 0 or groupMain is None or not int(groupMain) >= 0  or None is selectedFeature or '' == selectedFeature:
        return html.Div(graphs)
    
    if selectedFeature1 is None or  '' == selectedFeature1:
        selectedFeature1 = Feature1
    
    if selectedFeature3 is None or '' == selectedFeature3:
        selectedFeature3 = ''
        
    print('groupMain   ' + str(groupMain) + '   selectedFeature   ' + str(selectedFeature)  + '   selectedAxis   ' + str(selectedAxis) )
    print('selectedFigureType   ' + str(selectedFigureType) + '   selectedFeature1   ' + str(selectedFeature1)  + '     selectedFeature3   ' + str(selectedFeature3) )
    
    graphs = plotClassOverview( int(groupMain), selectedFeature, selectedAxis, selectedFigureType, selectedFeature1, selectedFeature3,
                               selectedDistribution = selectedDistribution)
    
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


@app.callback(
    Output(idApp + "-form-feature-distribution", "className"),
    [
        Input(idApp + "-form-figure-type", "value")
    ],
    state=[ State(component_id = idApp +"-form-feature-distribution", component_property='className') ]
)
def update_feature_distribution_disabled(selectedFigureType, initialClass):   
    if None is selectedFigureType or '' == selectedFigureType:
        return initialClass

    initialClassS = set()
    
    if not None is initialClass:
        initialClassS = set(initialClass.split(' '))

    if selectedFigureType in FigureTypes and   not FigureTypes.get(selectedFigureType).get(constants.keyIsDistributionEnabled):
        initialClassS.add('disabled')
    else:
        initialClassS.discard('disabled')

    return  ' '.join(initialClassS)












@app.callback(
    [ Output(idApp + "-download-main-link", 'href'),
     Output(idApp + "-download-main-link", 'className'),
     ],
    [ Input("group-selector-main", "value") ],
)
def update_download_link_custom_group(groupMain):
    if groupMain is None or not int(groupMain) >= 0 or groupMain == "":
        return "", "disabled"
    
    csv_string = util.get_download_link_data_uri( studentGrouped.getStudentsOfSchoolDF(int(groupMain)) )
    return csv_string, ""

