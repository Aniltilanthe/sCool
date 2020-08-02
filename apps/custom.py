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




#-----------------------------------Functions START ----------------------------------------
FeaturesCustom = ['SessionDuration', 'Points', 'Attempts', 'CollectedCoins', 'Difficulty']

FeaturesCustomPractice = ['NumberOfCoins', 'runsCount', 'runsErrorCount', 'runsSuccessCount', 'runsErrorSyntaxCount',
                                           'runsErrorNameCount', 'runsErrorTypeCount', 'runsLineOfCodeCountAvg',
                                           'tabsSwitchedCount', 'tabsSwitchedDescriptionCount', 'deletedCodesCount', 'robotCollisionsBoxCount']
FeaturesCustomTheory = ['playerShootCount', 'playerShootEndCount', 'playerShootEndEnemyHitCount',
                                         'playerShootEndEnemyMissedHitCount', 'enemysShootEndPlayerHitCount']


keyLabel                    = 'label'
keyHref                     = 'href'
keySubmenu                  = 'submenu'
keyValue                    = 'value'
keyIsAxisEnabled            = 'isAxisEnabled'
keyIsFeature3Enabled        = 'isFeature3Enabled'
keyScrollTo                 = 'scrollTo'
keyClassName                = 'className'

FigureTypeScatter           = 'Scatter'
FigureTypePie               = 'Pie'
FigureTypeBar               = 'Bar'
FigureTypeLine              = 'Line'
FigureTypeBubble            = 'Bubble'
FigureTypes = {
     FigureTypeBar      : { keyLabel      : FigureTypeBar, 
                   keyValue     : FigureTypeBar,
                  keyIsAxisEnabled : True,
                  keyIsFeature3Enabled : False }
    ,   
     FigureTypeScatter : { keyLabel           : FigureTypeScatter, 
                  keyValue      : FigureTypeScatter,
                  keyIsAxisEnabled : True,
                  keyIsFeature3Enabled : False  }
    ,   
     FigureTypePie      : { keyLabel      : FigureTypePie, 
                   keyValue     : FigureTypePie,
                  keyIsAxisEnabled : False,
                  keyIsFeature3Enabled : False  }
    ,   
     FigureTypeBubble     : { keyLabel       : FigureTypeBubble, 
                   keyValue     : FigureTypeBubble,
                  keyIsAxisEnabled : True,
                  keyIsFeature3Enabled : True  }
    ,   
     FigureTypeLine     : { keyLabel       : FigureTypeLine, 
                   keyValue     : FigureTypeLine,
                  keyIsAxisEnabled : True,
                  keyIsFeature3Enabled : False  }
}
     
AxisV               = 'v'
AxisH               = 'h'
MarginalPlot        = 'box'


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
        

    if 'studentDataDf' in locals()     and    ( studentDataDf is not None  )    and    ( featureToPlot in studentDataDf.columns )   :
        
        studentDataDf[constants.featureConceptsUsedDetailsStr]     = getPracticeConceptsUsedDetailsStr(studentDataDf)
                
        studentDataDfGrouped = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index = False)
    
#--------------------------------Total of each Features ----------------------------------     
        
        studentDataDfSum = studentDataDf.groupby([constants.STUDENT_ID_FEATURE, 'Name'], as_index=False).sum()
        
        
#        studentDataDfFeaturesInterpreted2 = pd.DataFrame(columns = [constants.STUDENT_ID_FEATURE, 'ConceptsUsed'])
#        for groupKey, group in studentDataDfGrouped :   
#            conceptsUsedStr = ' '
#            if 'ConceptsUsed' in group.columns and  group[ group['ConceptsUsed'].notnull() & (group['ConceptsUsed']  !=  u'') ].shape[0] > 0 :
#                conceptsUsedStr = ', '.join(  util.get_unique_ConceptsUsed_items(group)  )
#                
#            studentDataDfFeaturesInterpreted2 = studentDataDfFeaturesInterpreted2.append({constants.STUDENT_ID_FEATURE : groupKey,
#                                                                                        'ConceptsUsed' : conceptsUsedStr },  
#                                                                                ignore_index = True)
#            
#        
#        studentDataDfSum = studentDataDfSum.merge(right= studentDataDfFeaturesInterpreted2
#                                          , left_on = constants.STUDENT_ID_FEATURE, right_on = constants.STUDENT_ID_FEATURE
#                                            , left_index=False, right_index=False
#                                            , how='inner')
#        
#        ConceptsUsedGroupList = []
#        ConceptsUsedDetailsGroupList = []
#        for groupKey, group in studentDataDfGrouped :
#            if 'ConceptsUsed' in group.columns and  group[ group['ConceptsUsed'].notnull() ].shape[0] > 0 :
#                ConceptsUsedGroupList.append( ', '.join( util.get_unique_list_items(group[ group['ConceptsUsed'].notnull() ]['ConceptsUsed']) )   )
#                ConceptsUsedDetailsGroupList.append( ', '.join( util.get_unique_list_items(group[ group['ConceptsUsedDetails'].notnull() ]['ConceptsUsedDetails'])  )   )
#            else :
#                ConceptsUsedGroupList.append(' ')
#                ConceptsUsedDetailsGroupList.append(' ')
#        studentDataDfSum['ConceptsUsed'] = ConceptsUsedGroupList
#        studentDataDfSum['ConceptsUsedDetails']     = ConceptsUsedDetailsGroupList
        
#        studentDataDfSum['ConceptsUsedDetailsStr']  = studentDataDfSum['ConceptsUsedDetails'].apply(lambda x: x[1:-1])

#Default Horizontal Plots
        
        featureX2Plot = featureToPlot
        featureY2Plot = feature1
        
        plotTitle = ' Details of students ' + constants.feature2UserNamesDict.get(featureToPlot) if featureToPlot in constants.feature2UserNamesDict.keys() else featureToPlot
        
        hoverName = "Name"
        
        marginalX = ''
        marginalY = ''
        
        
        try:
            if selectedFigureType == FigureTypeScatter:
                
                if not None == selectedAxis and selectedAxis == AxisV:
                    featureX2Plot = feature1
                    featureY2Plot = featureToPlot
                
                if util.checkIsFeatureNumeric(studentDataDfSum, featureX2Plot):
                     marginalX = MarginalPlot
                     
                if util.checkIsFeatureNumeric(studentDataDfSum, featureY2Plot):
                     marginalY = MarginalPlot
                
                
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
            
        
        
            
            elif selectedFigureType == FigureTypePie:
                
                figStudents = px.pie(studentDataDfSum, values = featureX2Plot
                                     , names        =  'Name'
                                     , title        =   plotTitle
                                     , labels       =   constants.feature2UserNamesDict # customize axis label
                                     , hover_name   =   hoverName
                                     , hover_data   =   hoverData
                                     , height       =   graphHeight
                                     , template     =   constants.graphTemplete
                                     )
                figStudents.update_traces(textposition='inside', textinfo='percent+label+value')
                figStudents.update_layout(constants.THEME_CYAN_EXPRESS_LAYOUT)
                    
                
                
            elif selectedFigureType == FigureTypeBar :
                orientation = AxisH
                if not None == selectedAxis and selectedAxis == AxisV:
                    featureX2Plot = feature1
                    featureY2Plot = featureToPlot
                    orientation = AxisV
                
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
            
            
            elif selectedFigureType == FigureTypeBubble :
                
                if not None == selectedAxis and selectedAxis == AxisV:
                    featureX2Plot = feature1
                    featureY2Plot = featureToPlot
                
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
                                html.P('Size is based on ' + ((constants.feature2UserNamesDict.get(featureY2Plot)) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot ) ),
                                ]) )
                
                
            elif selectedFigureType == FigureTypeLine :

                if not None == selectedAxis and selectedAxis == AxisV:
                    featureX2Plot = feature1
                    featureY2Plot = featureToPlot
                
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
            
            
            
            studentDataDfSumMean    = studentDataDfSum.mean().round(decimals=2)
            studentDataDfSumStd     = studentDataDfSum.std().round(decimals=2)
            
            try :
                if featureX2Plot is not None and featureX2Plot in studentDataDfSumMean:
                    rows.append( html.Div(children=[
                                html.P('Mean  ' + ((constants.feature2UserNamesDict.get(featureX2Plot)) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot )  + ' = ' + str(studentDataDfSumMean[featureX2Plot]) ),
                                html.P('Std. ' + ((constants.feature2UserNamesDict.get(featureX2Plot)) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot ) + ' = ' + str(studentDataDfSumStd[featureX2Plot]) ),
                                ]) )
            except Exception as e: 
                print(e)
            try :
                if featureY2Plot is not None and featureY2Plot in studentDataDfSumMean:
                    rows.append( html.Div(children=[
                                    html.P('Mean  ' + ((constants.feature2UserNamesDict.get(featureY2Plot)) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot )  + ' = ' + str(studentDataDfSumMean[featureY2Plot]) ),
                                    html.P('Std. ' + ((constants.feature2UserNamesDict.get(featureY2Plot)) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot ) + ' = ' + str(studentDataDfSumStd[featureY2Plot]) ),
                                    ]) )
            except Exception as e: 
                print(e)
        
        except Exception as e: 
            print(e)
            
            
        graphs.append(dbc.Col(rows , align="center", width = 6))

    return graphs



def getFigureTypesOptions():
    return [{'label': FigureTypes.get(i).get(keyLabel) , 'value': FigureTypes.get(i).get(keyValue)} for i in FigureTypes]


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
                value       = FigureTypeBar ,
                labelStyle  = {'display': 'inline-block'},
                className   = "radio-items-inline"
            ), 
            dcc.RadioItems(
                id      ="form-feature-axis-custom",
                options=[
                    {'label': 'Horizontal (x-axis)', 'value': AxisH},
                    {'label': 'Vertical (y-axis)', 'value': AxisV},
                ],
                value       = AxisH,
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
def update_bar(n_clicks, groupMain, selectedFeature, selectedFeature1, selectedFeature3, selectedAxis, selectedFigureType, containerChildren ):    
    graphs = []
        
    if n_clicks == 0 or groupMain is None or not int(groupMain) >= 0  or None is selectedFeature or '' == selectedFeature:
        return html.Div(graphs)
    
    if selectedFeature1 is None or  '' == selectedFeature1:
        selectedFeature1 = Feature1
    
    if selectedFeature3 is None or '' == selectedFeature3:
        selectedFeature3 = ''
    
    graphs = plotClassOverview( int(groupMain), selectedFeature, selectedAxis, selectedFigureType, selectedFeature1, selectedFeature3 )
    
    if not(None is containerChildren):
        if isinstance(containerChildren, list):
            graphs = graphs + containerChildren 
        else :
            if isinstance(containerChildren, dict) and 'props' in containerChildren.keys():
                graphs = graphs + containerChildren.get('props').get('children')

    return  graphs




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
    
    if selectedFigureType in FigureTypes   and   not FigureTypes.get(selectedFigureType).get(keyIsAxisEnabled):
        initialClassS.add('hidden')  
    else:
        initialClassS.discard('hidden') 

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

    if selectedFigureType in FigureTypes and   not FigureTypes.get(selectedFigureType).get(keyIsFeature3Enabled):
        initialClassS.add('hidden') 
    else:
        initialClassS.discard('hidden') 

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

