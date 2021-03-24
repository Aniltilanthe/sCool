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


from data import studentGrouped
import constants
import util





idApp             = "home"





   
    

    
FeaturesCustom          = constants.FeaturesCustom

FeaturesCustomPractice  = constants.FeaturesCustomPractice
FeaturesCustomTheory    = constants.FeaturesCustomTheory


FigureTypes             = constants.FigureTypes 


graphHeight             =  constants.graphHeight
graphHeight             =   graphHeight - 200


hoverData               =  constants.hoverData.copy()
#hoverData.remove("lineOfCodeCount")



selectedColorGroupDefault    = "Name"



#--------------------- school selection START ----------------------
GroupSelector_options = studentGrouped.GroupSelector_options 
#--------------------- school selection END ----------------------



#--------------------------------- DataBase get data START ---------------------------
dfStudentDetails                        = studentGrouped.dfStudentDetails

dfSkillDetails                          = studentGrouped.dfSkillDetails
dfCourseDetails                         = studentGrouped.dfCourseDetails
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
                    util.generateCardBase([html.I(className="fas fa-clock m-right-small"),   'Game Time'], 
                                        '' + util.seconds_2_dhms(dfAllData['SessionDuration'].sum().round(decimals=2)), 
                                        )
#                   util.generateCardDetail([html.I(className="fas fa-clock m-right-small"),   'Game Time'], 
#                                        '' + util.seconds_2_dhms(dfAllData['SessionDuration'].sum().round(decimals=2)), 
#                                        '' + str(dfAllData['SessionDuration'].mean().round(decimals=2)) + 's', 
#                                        '' + str(dfAllData['SessionDuration'].std().round(decimals=2)) + 's', 
#                                        'total',
#                                        'mean',
#                                        'std',
#                                        )
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
                    
                util.generateCardBase('Points Collected', 
                                        '' + util.millify(dfAllData['Points'].sum().round(decimals=2)), 
                                        )
                    
#                   util.generateCardDetail('Points Collected', 
#                                        '' + util.millify(dfAllData['Points'].sum().round(decimals=2)), 
#                                        '' + str(dfAllData['Points'].mean().round(decimals=2)), 
#                                        '' + str(dfAllData['Points'].std().round(decimals=2)), 
#                                        'total',
#                                        'mean',
#                                        'std',
#                                        )
                ],            
                className="col-sm-4",
            ))

    plots.append(
            html.Div(children  = plotRow,                
                     className = "row")
    )
    
    return plots

featureGroupByOptions   = [constants.featureStudent, constants.featureTask, constants.featureGroup, constants.featureSkill, constants.featureCourse]



def getGroupByFilterOptions(selectedGroupBy = constants.featureGroup):
    
    if selectedGroupBy == constants.featureTask :
        
        return list(dfPracticeTaskDetails[constants.featureTask].unique()) +  list(dfTheoryTaskDetails[constants.featureTask].unique())
    
    elif selectedGroupBy == constants.featureGroup :
        return studentGrouped.getGroups()
    
    elif selectedGroupBy == constants.featureStudent:
        return dfStudentDetails[constants.featureStudent].unique()
    
    elif selectedGroupBy ==   constants.featureSkill :
        return dfSkillDetails[constants.featureSkill].unique()
    
    elif selectedGroupBy == constants.featureCourse :
        return dfCourseDetails[constants.featureCourse].unique()
    
    else:
        return []
    
    


def plotGamePlots (feature1 = '',  feature2 = '', feature3 = '', 
                   selectedAxis         = constants.AxisH, 
                   selectedFigureType   = constants.FigureTypeBar,
                   plotClassName        = " col-sm-12 ", 
                   selectedDistribution = [],
                   groupBy              = selectedColorGroupDefault  ,
                   groupBySub           = [],
                   groupByFilter        = [],
                   selectedFeatureMulti = [],
                   hoverData            = hoverData.copy() ):

    graphs = []
    rows = []
    
    print('   plotGamePlots  in home !!!! ' )
    
    hoverName   = groupBy
    color       = groupBy
    
    marginalX   = ''
    marginalY   = ''
        
    groupByAll = [ ]
    if groupBySub is None :
        groupBySub = []
    if selectedFeatureMulti is None:
        selectedFeatureMulti = []
    if selectedDistribution is None:
        selectedDistribution = []
    
        
    gameData = pd.concat([dfPlayerStrategyPracticeOriginal, dfPlayerStrategyTheory], ignore_index=True)
    
    gameData[constants.featureStudent]     =    gameData['Name'].astype(str) + '-' +   gameData['StudentId'].astype(str) 
    gameData[constants.featureGroup]       =    constants.TypeGroup  + '-' + gameData['LearningActivityId'].astype(str) 
    gameData[constants.featureCourse]      =    constants.TypeCourse  + '-' +   gameData['CourseId'].astype(str) 
    gameData[constants.featureSkill]       =    constants.TypeSkill  + '-' +   gameData['SkillId'].astype(str) 
    gameData[constants.featureTask]        =    gameData[constants.featureTaskId].astype(str)
            
    
    gameData = gameData.drop_duplicates(subset=[constants.featureStudent, constants.featureTask], keep='last')
    
    
    for hoverFeatureRemove in  featureGroupByOptions + [constants.featureTaskType]:
        if hoverFeatureRemove in hoverData:
            hoverData.remove( hoverFeatureRemove )
            
    
    if groupByFilter and len(groupByFilter) > 0:
        gameData = gameData[gameData[groupBy].isin(groupByFilter)]
        
    
#--------------------------------Total of each Features ----------------------------------     
    
        
    if selectedFeatureMulti is not None:
        selectedFeatureMulti = [groupBy] + groupBySub + selectedFeatureMulti
        
    
    if    groupBy == constants.featureTask  :
        groupByAll = [ groupBy, constants.featureTaskType ]
        gameDataDfGroupedSum, hoverData, groupByAll = util.groupedBySelectedFeaturesDf(gameData, 
                                                               groupBy = groupBy  , 
                                                               groupBySub = groupBySub  , 
                                                               groupByAll = groupByAll  , 
                                                               hoverData = hoverData   )
        hoverName   = groupBy
        groupBy     = constants.featureTaskType
        
        if selectedFeatureMulti is not None:
            selectedFeatureMulti = groupByAll + groupBySub + selectedFeatureMulti
    
    elif   groupBy  in  [ constants.featureGroup, constants.featureSkill , constants.featureCourse , constants.featureStudent     ]  :
        
        gameDataDfGroupedSum, hoverData, groupByAll = util.groupedBySelectedFeaturesDf(gameData, 
                                                               groupBy = groupBy  , 
                                                               groupBySub = groupBySub  , 
                                                               groupByAll = groupByAll  , 
                                                               hoverData = hoverData   )
        hoverName   = groupBy
        color       = groupBy
        
        
    else  :
        groupByAll = [constants.GROUPBY_FEATURE, constants.featureGroup, 
                                                 constants.featureStudent ]
        gameDataDfGroupedSum = gameData.groupby(groupByAll, as_index=False).sum()
        
        for hoverFeature in groupBySub:
            if hoverFeature in hoverData:
                hoverData.remove(hoverFeature)
                
        if not constants.featureStudent in hoverData:
            hoverData.append(constants.featureStudent)
        if not constants.featureGroup in hoverData:
            hoverData.append(constants.featureGroup)
            
    
    if not constants.featureStudent in groupByAll :
        gameDataStudent = gameData.groupby(groupByAll + [constants.featureStudent], as_index=False).sum().round(decimals=2)
    else:    
        gameDataStudent = gameData.groupby(groupByAll, as_index=False).sum()

    dfOriginalMean = gameDataStudent.groupby(groupByAll, as_index = False).mean().round(decimals=2)
    dfOriginalMedian = gameDataStudent.groupby(groupByAll, as_index = False).median().round(decimals=2)
    
    try:
        dfOriginalStd = gameDataStudent.groupby(groupByAll, as_index = False).agg([np.std])
        dfOriginalStd.reset_index(level=0, inplace=True)
        dfOriginalStd = dfOriginalStd.round(decimals=2)
        dfOriginalStd.columns = dfOriginalStd.columns.droplevel(1)
    except Exception as e: 
        
        print(e)
        try:
            list_df = []
            for key, group in gameDataStudent.groupby(groupByAll, as_index = False):
                list_df.append(
                    group.apply([np.std])
                )

            dfOriginalStd = pd.concat(list_df)
            dfOriginalStd.reset_index(level=0, inplace=True)
            dfOriginalStd = dfOriginalStd.round(decimals=2)
            dfOriginalStd.columns = dfOriginalStd.columns.droplevel(1)
        except Exception as e: 
            print('plotGamePlots exception in second trial of creating dfOriginalStd !!!! ')
            print(e)
    
        
    if 'gameDataDfGroupedSum' in locals()     and    ( gameDataDfGroupedSum is not None  )    and   ( not  gameDataDfGroupedSum.empty )   :
        
            
        plotTitle   = ' Details of students ' 
        plotTitle   = plotTitle + str( constants.feature2UserNamesDict.get(feature1) if feature1 in constants.feature2UserNamesDict.keys() else feature1 )
        plotTitle   = plotTitle + ' vs ' + str( constants.feature2UserNamesDict.get(feature2) if feature2 in constants.feature2UserNamesDict.keys() else feature2 )
        
        rows = util.getCustomPlot(
                          df                    = gameDataDfGroupedSum, 
                          dfOriginal            = gameDataStudent,
                          dfOriginalMean        = dfOriginalMean, 
                          dfOriginalMedian      = dfOriginalMedian,
                          dfOriginalStd         = dfOriginalStd,                          
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
                          groupBy               = groupBy,
                          selectedDistribution  = selectedDistribution,
                          selectedFeatureMulti  = selectedFeatureMulti,
                          isThemeSizePlot       = True,
            )
       
        graphs.append( html.Div( rows ,
                                className = plotClassName ) )
        

    return graphs



def generateControlCardCustomPlot():
    
#    featureGroupByOptionsCopyFeatures = featureGroupByOptions.copy()
#    featureGroupByOptionsCopyFeatures = featureGroupByOptionsCopyFeatures.remove('Student')
    
    return util.generateControlCardCustomPlotForm(
            idApp                   = idApp, 
            feature1Options         = FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory , 
            feature2Options         = featureGroupByOptions + FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory, 
            feature3Options         = FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory, 
            feature1ValueDefault    = "",
            feature2ValueDefault    = "",
            feature3ValueDefault    = "",
            figureTypeDefault       = constants.FigureTypeScatter,
            featureMultiOptions     = featureGroupByOptions + FeaturesCustom + FeaturesCustomPractice + FeaturesCustomTheory,
            featureGroupByDefault   = constants.featureGroup ,
            featureGroupByOptions   = featureGroupByOptions, 
            featureGroupByFilterOptionsDefault  = ['Group-1', 'Group-2', 'Group-3', 'Group-4','Group-5', 'Group-15',]
    )

#----------------------------------Functions END --------------------------------------------



layout = [
            
    dbc.Row([
            dbc.Col(
                # Left column
                html.Div(
                    id="game-main-overview",
                    className="",
                    children=  [html.H2("Game Overview")]  ,
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
                    className=" ",
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
                State(component_id = idApp + "-form-feature-distribution", component_property='value'),
                State(component_id = idApp + "-form-feature-color-group", component_property='value'),
                State(component_id = idApp + "-form-feature-color-group-sub", component_property='value'),
                State(component_id = idApp + "-form-feature-color-group-filter", component_property='value'),
                State(component_id = idApp + "-form-feature-multi", component_property='value'),
                State(component_id = idApp + "-custom-plot-container", component_property='children'),
                ]
)
def update_bar(n_clicks, selectedFeature1, selectedFeature2, selectedFeature3, selectedAxis, selectedFigureType,  
               selectedDistribution, 
               selectedFeatureColorGroupBy,
               selectedFeatureColorGroupBySub,
               selectedFeatureColorGroupByFilter,
               selectedFeatureMulti,
               containerChildren 
               ):    
    graphs = []
    
    if n_clicks == 0:
        return html.Div(graphs)
    
    if not selectedFeature1 :
        selectedFeature1 = ''
    
    if not  selectedFeature2 :
        selectedFeature2 = ''
    
    if not selectedFeature3 :
        selectedFeature3 = ''
    
    
    graphs = plotGamePlots( feature1            = selectedFeature1, 
                           feature2             = selectedFeature2, 
                           feature3             = selectedFeature3,
                           selectedAxis         = selectedAxis, 
                           selectedFigureType   = selectedFigureType, 
                           plotClassName        = " col-sm-12 ",
                           selectedDistribution = selectedDistribution,
                           groupBy              = selectedFeatureColorGroupBy,
                           groupBySub           = selectedFeatureColorGroupBySub,
                           groupByFilter        = selectedFeatureColorGroupByFilter, 
                           selectedFeatureMulti = selectedFeatureMulti   )
    
    if not(None is containerChildren):
        if isinstance(containerChildren, list):
            graphs = graphs + containerChildren 
        else :
            if isinstance(containerChildren, dict) and 'props' in containerChildren.keys():
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
    [Output(idApp + "-form-feature-color-group-filter", "value"),
     Output(idApp + "-form-feature-color-group-filter", "options"),
     ],
    [
        Input(idApp + "-form-feature-color-group", "value")
    ],
)
def update_feature_groupby_filter_option_reset(selectedGroupBy):
    
    return "", util.BuildOptions( getGroupByFilterOptions(selectedGroupBy) ) 


              