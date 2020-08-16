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


hoverData           =  constants.hoverData.copy()


Feature1            = "Student"
Feature3Size        = "SessionDuration"




featureGroupByOptions   = ['Student', 'Task', 'Skill', 'Course']
featureGroupByDefault   = 'Student'



#Student Interaction with Game - TIMELINE
def plotClassOverview(schoolKey, feature1, selectedAxis, selectedFigureType, 
                      feature2              = '', 
                      feature3              = '',
                      plotClassName         = " col-12 col-xl-12 ", 
                      selectedDistribution  = [],
                      selectedFeatureMulti  = [],
                      groupBy               = constants.STUDENT_ID_FEATURE,
                      groupBySub            = [] ,
                      hoverData             = hoverData.copy()       ) :
    

    graphs = []
    rows = []
    
    if (None == schoolKey) :
        return graphs
    
    
    print('plotClassOverview')
    print(hoverData)
    print(str(feature1) +  '  feature2 '  + str(feature2) + '  feature3 '  + str(feature3) + '  selectedFeatureMulti '   + str(selectedFeatureMulti) + '  selectedDistribution '  + str(selectedDistribution)  )
    print(str(schoolKey) +  '  groupBy '  + str(groupBy) + '  groupBySub '  + str(groupBySub))
    
    groupByAll = [ ]
    if groupBySub is None :
        groupBySub = []
    if selectedFeatureMulti is None:
        selectedFeatureMulti = []
    if selectedDistribution is None:
        selectedDistribution = []
    
    
    studentDataDf = studentGrouped.getStudentsOfSchoolDF(schoolKey, isOriginal = True)
    
    
    
    studentDataDf[constants.featureStudent]     =    studentDataDf['Name'].astype(str) + '-' + studentDataDf['StudentId'].astype(str)
#    studentDataDf[constants.featureGroup]       =    constants.TypeGroup + '-' + studentDataDf['GroupId'].astype(str)
    studentDataDf[constants.featureCourse]      =    constants.TypeCourse + '-' +  studentDataDf['CourseId'].astype(str)
    studentDataDf[constants.featureSkill]       =    constants.TypeSkill + '-' +  studentDataDf['SkillId'].astype(str)
    studentDataDf[constants.featureTask]        =    studentDataDf[constants.featureTaskId].astype(str)
    
    
    studentDataDf = studentDataDf.drop_duplicates(subset=[constants.featureStudent, constants.featureTask], keep='last')
    
    
    for hoverFeatureRemove in  featureGroupByOptions + [constants.featureTaskType]:
        if hoverFeatureRemove in hoverData:
            hoverData.remove( hoverFeatureRemove )
            
    print(' plotClassOverview got studentDataDf   ' )

    if 'studentDataDf' in locals()     and    ( studentDataDf is not None  )  :
        
        if selectedFeatureMulti is not None:
            selectedFeatureMulti = [groupBy] + groupBySub + selectedFeatureMulti
        
#        studentDataDf[constants.featureConceptsUsedDetailsStr]     = getPracticeConceptsUsedDetailsStr(studentDataDf)
                
        if    groupBy == constants.featureTask  :
            groupByAll = [ groupBy, constants.featureTaskType ]
            
            studentDataDfSum, hoverData, groupByAll = util.groupedBySelectedFeaturesDf(studentDataDf, 
                                                                   groupBy = groupBy  , 
                                                                   groupBySub = groupBySub  , 
                                                                   groupByAll = groupByAll  , 
                                                                   hoverData = hoverData.copy()   )
            hoverName   = groupBy
            groupBy     = constants.featureTaskType
            
            if selectedFeatureMulti is not None:
                selectedFeatureMulti = groupByAll + groupBySub + selectedFeatureMulti
            print('hoverData 2   ' +  str(hoverData) + '   hoverName ' + str(hoverName) + '   groupBy ' + str(groupBy))
        
        elif   groupBy  in  [ constants.featureSkill , constants.featureCourse , constants.featureStudent , ]  :
            
            studentDataDfSum, hoverData, groupByAll = util.groupedBySelectedFeaturesDf(studentDataDf, 
                                                                   groupBy = groupBy  , 
                                                                   groupBySub = groupBySub  , 
                                                                   groupByAll = groupByAll  , 
                                                                   hoverData = hoverData.copy()   )
            hoverName   = groupBy
#            color       = groupBy
            
            print('hoverData 3   ' +  str(hoverData) + '   hoverName ' + str(hoverName) + '   groupBy ' + str(groupBy))
            
        else  :
            studentDataDfSum = studentDataDf.groupby([ featureGroupByDefault ], as_index=False).sum()
            
            hoverName   = featureGroupByDefault
            groupBy     = featureGroupByDefault
            
            print('hoverData 4   ' +  str(hoverData) + '   hoverName ' + str(hoverName) + '   groupBy ' + str(groupBy))
                
                
        
        if not groupBy ==  constants.featureStudent :
            gameDataStudent = studentDataDf.groupby([groupBy] + [ constants.featureStudent ], as_index=False).sum()
        else :
            gameDataStudent = studentDataDf.groupby([ constants.featureStudent ], as_index=False).sum()
            
        
#        if groupBy == 'Task':
#            
##            studentDataDfGrouped = studentDataDf.groupby(['TaskId',
##                                                          constants.STUDENT_ID_FEATURE, 'Name'
##                                                          ], as_index = False)
#            studentDataDfSum = studentDataDf.groupby(['TaskId',
#                                                      constants.STUDENT_ID_FEATURE, 'Name'
#                                                      ], as_index=False).sum()
#            
#            hoverName   = "TaskId"
#            groupBy     = "TaskId"
#            
#        else:
##            studentDataDfGrouped = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index = False)
#        
#    #--------------------------------Total of each Features ----------------------------------     
#            
#            studentDataDfSum = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index=False).sum()
#
#            hoverName   = "Name"
#            groupBy     = "Name"
        
        plotTitle   = ' Details of students ' 
        plotTitle   = plotTitle + str( constants.feature2UserNamesDict.get(feature1) if feature1 in constants.feature2UserNamesDict.keys() else feature1 )
        plotTitle   = plotTitle + ' vs ' + str( constants.feature2UserNamesDict.get(feature2) if feature2 in constants.feature2UserNamesDict.keys() else feature2 )
        
        
#        hoverName   = "Name"
#        groupBy     = "Name"
        
        marginalX   = ''
        marginalY   = ''
        
        print('selectedFigureType   ' + str(selectedFigureType) + '   feature1   ' + str(feature1)  + '   feature2   ' + str(feature2) )
        
        rows = util.getCustomPlot(
                          df                    = studentDataDfSum, 
                          dfOriginal            = gameDataStudent, 
                          featureX              = feature1, 
                          featureY              = feature2, 
                          feature3              = feature3, 
                          selectedFigureType    = selectedFigureType, 
                          selectedAxis          = selectedAxis, 
                          plotTitle             = plotTitle,
                          marginalX             = marginalX,
                          marginalY             = marginalY,
                          hoverData             = hoverData,
                          hoverName             = hoverName,
                          groupBy               = groupBy,
                          selectedDistribution  = selectedDistribution,
                          selectedFeatureMulti  = selectedFeatureMulti,
                          isThemeSizePlot       = True,
            )
        
        
        if (constants.keyClassName in constants.FigureTypes.get(selectedFigureType)   ):
            plotClassName = constants.FigureTypes.get(selectedFigureType).get(constants.keyClassName)
        
       
        graphs.append( html.Div( rows ,
                                className = plotClassName ) )
        

    return graphs


def generateControlCardCustomPlotForm():
    
    return util.generateControlCardCustomPlotForm(
            idApp                   = idApp , 
            feature1Options         = FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory , 
            feature2Options         = featureGroupByOptions + FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory , 
            feature3Options         = FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory , 
            feature1ValueDefault    = "" ,
            feature2ValueDefault    = "" ,
            feature3ValueDefault    = Feature3Size ,
            featureMultiOptions     = FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory ,
            featureGroupByDefault   = featureGroupByDefault ,
            featureGroupByOptions   = featureGroupByOptions ,
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
                State(component_id = idApp + "-form-feature-color-group", component_property='value'),
                State(component_id = idApp + "-form-feature-color-group-sub", component_property='value'),
                State(component_id = idApp + "-form-feature-multi", component_property='value'),
                State(component_id = idApp + "-main-container", component_property='children'),
                ]
)
def update_bar(n_clicks, groupMain, selectedFeature, selectedFeature1, selectedFeature3, selectedAxis, 
               selectedFigureType, 
               selectedDistribution,
               selectedFeatureColorGroupBy,
               selectedFeatureColorGroupBySub,
               selectedFeatureMulti,
               containerChildren 
               ):    
    graphs = []
    
    print('update_bar')
    print(selectedDistribution)
    
    if n_clicks == 0 or groupMain is None or not int(groupMain) >= 0:
        return html.Div(graphs)
    
    if   not ( selectedFeature1 ) :
        selectedFeature1 = ''
    
    if   not ( selectedFeature3 ) :
        selectedFeature3 = ''
        
    print('groupMain   ' + str(groupMain) + '   selectedFeature   ' + str(selectedFeature)  + '   selectedAxis   ' + str(selectedAxis) )
    print('selectedFigureType   ' + str(selectedFigureType) + '   selectedFeature1   ' + str(selectedFeature1)  + '     selectedFeature3   ' + str(selectedFeature3) )
    
    graphs = plotClassOverview( int(groupMain), selectedFeature, selectedAxis, selectedFigureType, selectedFeature1, selectedFeature3,
                               selectedDistribution         = selectedDistribution,
                               selectedFeatureMulti         = selectedFeatureMulti,
                               groupBy  = selectedFeatureColorGroupBy, 
                               groupBySub                   = selectedFeatureColorGroupBySub,   )
    
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
    return util.updateSelectorDisabled(selectedFigureType, initialClass, constants.keyIsAxisEnabled) 


@app.callback(
    Output(idApp + "-form-feature-3", "className"),
    [
        Input(idApp + "-form-figure-type", "value")
    ],
    state=[ State(component_id = idApp +"-form-feature-3", component_property='className') ]
)
def update_feature_size_disabled(selectedFigureType, initialClass):   
    return util.updateSelectorDisabled(selectedFigureType, initialClass, constants.keyIsFeature3Enabled)


@app.callback(
    Output(idApp + "-form-feature-distribution", "className"),
    [
        Input(idApp + "-form-figure-type", "value")
    ],
    state=[ State(component_id = idApp +"-form-feature-distribution", component_property='className') ]
)
def update_feature_distribution_disabled(selectedFigureType, initialClass):   
    return util.updateSelectorDisabled(selectedFigureType, initialClass, constants.keyIsDistributionEnabled)


@app.callback(
    Output(idApp + "-form-feature-multi", "className"),
    [
        Input(idApp + "-form-figure-type", "value")
    ],
    state=[ State(component_id = idApp + "-form-feature-multi", component_property='className') ]
)
def update_feature_multi_disabled(selectedFigureType, initialClass): 
    return util.updateSelectorDisabled(selectedFigureType, initialClass, constants.keyIsMultiFeatureEnabled)















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

