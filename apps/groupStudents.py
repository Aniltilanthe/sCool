# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 10:55:10 2020

@author: tilan
"""

# -*- coding: utf-8 -*-
import math
import json
from datetime import date
import dateutil.parser
import numpy as np
import pandas as pd
from dateutil.parser import parse

import flask
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.figure_factory as ff
import chart_studio.plotly as py
from plotly import graph_objs as go
import os

from app import app



from data import studentGrouped
import constants
import util





#fig = studentGroupedPerformance.figBar


#--------------------------------- Const values START ----------------------------


feature2UserNamesDict               = constants.feature2UserNamesDict
countStudentCompletingTaskFeature   = constants.countStudentCompletingTaskFeature
countTaskCompletedByStudentFeature  = constants.countTaskCompletedByStudentFeature
featurePracticeTaskDesc             = constants.featurePracticeTaskDesc
featureTheoryTaskDesc               = constants.featureTheoryTaskDesc
featureTaskDesc                     = constants.featureTaskDesc
featureTaskType                     = constants.featureTaskType
featureDescription                  = constants.featureDescription
featureSessionDuration              = constants.featureSessionDuration

TaskTypePractice                    = constants.TaskTypePractice
TaskTypeTheory                      = constants.TaskTypeTheory



sortOrderDescending                 = constants.sortOrderDescending
sortOrderAscending                  = constants.sortOrderAscending

hasFeatures                         =  studentGrouped.hasFeatures

#--------------------------------- Const values END ----------------------------


#--------------------------------- DataBase get data START ---------------------------

dfStudentDetails                        = studentGrouped.dfStudentDetails


dfPracticeTaskDetails                   = studentGrouped.dfPracticeTaskDetails
dfTheoryTaskDetails                     = studentGrouped.dfTheoryTaskDetails


#dfGroupedPractice                       = studentGrouped.dfGroupedPractice
dfGroupedOriginal                       = studentGrouped.dfGroupedOriginal
dfPlayerStrategyPractice                = studentGrouped.dfPlayerStrategyPractice  
dfGroupedPracticeTaskWise               = studentGrouped.dfGroupedPracticeTaskWise
dfGroupedPracticeDB                     = studentGrouped.dfGroupedPracticeDB
dfRuns                                  = studentGrouped.dfRuns


dfPlayerStrategyTheory                  = studentGrouped.dfPlayerStrategyTheory
dfGroupedPlayerStrategyTheory           = studentGrouped.dfGroupedPlayerStrategyTheory

#--------------------------------- DataBase get data END ---------------------------


#--------------------------- helper functions -----------------------    
getTaskWiseSuccessFail                  =  studentGrouped.getTaskWiseSuccessFail
getStudentsOfSchool                     =  studentGrouped.getStudentsOfSchool


getPracticeDescription                  =  studentGrouped.getPracticeDescription
getTheoryDescription                     =  studentGrouped.getTheoryDescription



def convert_list_column_tostr_NL(val) :
    separator = ',<br>'
    return separator.join(val)




#--------------------------- helper functions  END -----------------------


#------------------------------------



def getStudentData(StudentId, schoolKey, selectedDate = ''):
    
    print('getStudentData')
    
    studentData = pd.DataFrame()
    
    try :
        school                            = dfGroupedOriginal.get_group(schoolKey)
        studentData                       = school[school['StudentId'] == StudentId]
        studentData['Finish']             = studentData['CreatedAt'] 
        studentData['Start']              = studentData['Finish'] - pd.to_timedelta(studentData[featureSessionDuration], unit='s')
        
        studentData['CodeDesc']           = studentData['Code'].str.replace('\n','<br>')
        
        studentData[featureDescription]   = getPracticeDescription(studentData, False)   
        studentData[featureDescription]   = '<b>Title</b>:' + studentData['Title'].astype(str)  + '<br>'+ studentData[featureDescription].astype(str)
        studentData[featureDescription]   = studentData[featureDescription].astype(str) + '<br><b>Code</b>:' + studentData['CodeDesc'].astype(str) 
        
        studentData = studentData.sort_values(by='Start')
        
        studentData['Task']       = constants.TaskTypePractice + '-' + studentData['PracticeTaskId'].astype(str) 
        studentData['IndexCol']   = studentData['Task'] + '-' + studentData['Result'].astype('Int64').astype(str) 
        
        studentData['Finish'] = np.where(studentData['Finish'].isnull(), studentData['Start'].shift(-1), studentData['Finish'])
        
        studentData['Difference'] = (studentData['Finish'] - studentData['Start']).astype('timedelta64[s]')
        
        studentData[constants.featureTaskType] = constants.TaskTypePractice
    except Exception as e: 
        print(e)


    try :
        schoolTheory = dfGroupedPlayerStrategyTheory.get_group(schoolKey)
        schoolTheoryStudent = schoolTheory[schoolTheory['StudentId'] == StudentId]
        
        
        schoolTheoryStudent['Finish']   =   schoolTheoryStudent['CreatedAt']
        schoolTheoryStudent['Start']    =   schoolTheoryStudent['Finish'] - pd.to_timedelta(schoolTheoryStudent[featureSessionDuration], unit='s')
        schoolTheoryStudent             =   schoolTheoryStudent.sort_values(by='Start')
        
        
        schoolTheoryStudent['Difference'] = (schoolTheoryStudent['Finish'] - schoolTheoryStudent['Start']).astype('timedelta64[s]')
        
        schoolTheoryStudent.loc[schoolTheoryStudent['Difference'] > schoolTheoryStudent[featureSessionDuration], 'Difference'] =  schoolTheoryStudent[
                schoolTheoryStudent['Difference'] > schoolTheoryStudent[featureSessionDuration] ][featureSessionDuration]        
        
        schoolTheoryStudent = schoolTheoryStudent.merge(right= dfTheoryTaskDetails[ ['TheoryTaskId', 'Title', 'Description' ] ]
                                          , left_on='TheoryTaskId', right_on='TheoryTaskId'
                                            , left_index=False, right_index=False
                                            , how='inner')
        schoolTheoryStudent.rename(columns={'Description': 'TheoryTaskDescription'}, inplace=True)
        
        schoolTheoryStudent[featureDescription] = getTheoryDescription(schoolTheoryStudent, False)  
        schoolTheoryStudent[featureDescription] = '<b>Title</b>:' + schoolTheoryStudent['Title'].astype(str)  + '<br>'+ schoolTheoryStudent[featureDescription].astype(str) 
    
        schoolTheoryStudent['Task'] = constants.TaskTypeTheory + '-' + schoolTheoryStudent['TheoryTaskId'].astype(str) 
        schoolTheoryStudent['IndexCol'] = schoolTheoryStudent['Task'] + '-' + schoolTheoryStudent['Result'].astype(str)
        
        schoolTheoryStudent[constants.featureTaskType] = [  constants.TaskTypeTheory ] * schoolTheoryStudent.shape[0]
        
        
        if schoolTheoryStudent is not None and schoolTheoryStudent.empty == False :
            studentData = pd.concat([studentData, schoolTheoryStudent], ignore_index=True)
    except Exception as e: 
        print(e)
        
    
    if studentData is None         or     studentData.empty   :
        return studentData
    
    
    if     None is not selectedDate         and         not selectedDate == ''     and   util.is_valid_date(selectedDate) :
        studentDataGroupedDate  = studentData.groupby(  [studentData['Start'].dt.date] )
        studentData = studentDataGroupedDate.get_group(selectedDate)
    
    
    studentData['StartStr']         = '@' + studentData['Start'].dt.strftime('%Y-%m-%d %H:%M:%S') + '-' + studentData['IndexCol'].astype(str)
        
    return studentData


#Check if Student is in a Group
def isStudentInGroup(StudentId, groupId) :
    groupStudents = getStudentsOfSchool(groupId)
    
    if  not StudentId in groupStudents:
        return False
    
    return True


studentOverviewFeaturesDefault =   {
        constants.featureCollectedCoins : {
                constants.keyClassName : 'fas fa-coins ',
                constants.keyHasMeanStd : False,                
        }
        , constants.featureItemsCollectedCount : {
                constants.keyClassName : 'fas fa-memory ',
                constants.keyHasMeanStd : False,                
        }
        , constants.featureLineOfCodeCount : {
                constants.keyClassName : 'fas list-ol ',
                constants.keyHasMeanStd : False,                
        }
}



def plotStudentOverview(StudentId, groupId):
    
    graphs = []
    
    
#    the student is not in the group
    if not isStudentInGroup(StudentId, groupId) :
        return graphs
    
    

    studentDataDf                     = getStudentData(StudentId, groupId)
    
    if studentDataDf is None or studentDataDf.empty == True :
        graphs.append(
                util.getNoDataMsg()
        )
        return graphs
    
    
    studentDataDf.fillna(0, inplace=True)
    graphs = util.plotStudentOverview(studentDataDf , classes = "c-card-small" )
    
    
    
    plotRow = []
    
    
    
    groupOriginal                           = dfGroupedOriginal.get_group(groupId)
    
    groupOriginal['ConceptsUsed']           = groupOriginal['Code'].apply( studentGrouped.getAllNodeTypesUsefull )
    groupOriginal["ConceptsUsedDetails"]    = groupOriginal['ConceptsUsed'].replace(
                                                    constants.ProgramConceptsUsefull2UserNames, regex=True )
    
    
    studentWiseData                         = groupOriginal.groupby(['StudentId'], as_index=False).sum()
    studentDataDfPractice                   = studentWiseData[studentWiseData['StudentId'] == StudentId]
    
    
    
    studentDataDfSuccess                    =     studentDataDf[studentDataDf['Result'].astype('Int64') > 0 ]
    
    if studentDataDfSuccess is not None and studentDataDfSuccess.empty is False  and 'Task' in studentDataDfSuccess.columns:        
        plotRow.append( html.Div([  
                
                                    util.generateCardDetail([html.I(className="fas fa-cubes m-right-small"),   'No. of Tasks completed'], 
                                        '' + util.millify(len(studentDataDfSuccess['Task'].unique())), 
                                        '' + str(  len(studentDataDfSuccess[studentDataDfSuccess[constants.featureTaskType] == constants.TaskTypePractice ]['Task'].unique()) ), 
                                        '' + str(  len(studentDataDfSuccess[studentDataDfSuccess[constants.featureTaskType] == constants.TaskTypeTheory ]['Task'].unique()) ), 
                                        constants.labelTotal  ,
                                        constants.TaskTypePractice,
                                        constants.TaskTypeTheory ,
                                        classes = "c-card-small" 
                                        )
                                ],
                                className="col-sm-4",
                        ))
    
        
    for feature2OKey in studentOverviewFeaturesDefault.keys():
        currentFeatureO = studentOverviewFeaturesDefault.get(feature2OKey)
        
        if constants.keyHasMeanStd in currentFeatureO.keys() and   currentFeatureO.get(constants.keyHasMeanStd):
            plotRow.append( html.Div([
                                    util.generateCardDetail(
                                                [html.I(className =  html.I(className=  currentFeatureO.get(constants.keyClassName)) +  " m-right-small"), 
                                                 ((constants.feature2UserNamesDict.get(feature2OKey)) if feature2OKey in constants.feature2UserNamesDict.keys() else feature2OKey ) ], 
                                                studentDataDf[feature2OKey].sum().round(decimals=2) ,
                                                studentDataDf[feature2OKey].mean().round(decimals=2) , 
                                                studentDataDf[feature2OKey].std().round(decimals=2) , 
                                                constants.labelTotal  ,
                                                constants.labelMean ,
                                                constants.labelStd ,
                                                classes = "c-card-small" )
                                    ],
                                    className="col-sm-4",
                            ))


            
        else :
            if feature2OKey in studentDataDfPractice.columns :
                plotRow.append( html.Div([
                                            util.generateCardBase(
                                                    [   html.I(className=  currentFeatureO.get(constants.keyClassName) +  " m-right-small"), 
                                                         ((constants.feature2UserNamesDict.get(feature2OKey)) if feature2OKey in constants.feature2UserNamesDict.keys() else feature2OKey ) ], 
                                                    studentDataDfPractice[feature2OKey].sum() ,
                                                    classes = "c-card-small" )
                                        ],
                                        className="col-sm-4",
                                ))
            elif feature2OKey in studentDataDf.columns :
                plotRow.append( html.Div([
                                            util.generateCardBase(
                                                    [   html.I(className=  currentFeatureO.get(constants.keyClassName) +  " m-right-small"), 
                                                         ((constants.feature2UserNamesDict.get(feature2OKey)) if feature2OKey in constants.feature2UserNamesDict.keys() else feature2OKey ) ], 
                                                    studentDataDf[feature2OKey].sum() ,
                                                    classes = "c-card-small" )
                                        ],
                                        className="col-sm-4",
                                ))
    
        
    if groupOriginal[groupOriginal['StudentId'] == StudentId] is not None  and groupOriginal[groupOriginal['StudentId'] == StudentId]['ConceptsUsedDetails'].shape[0] > 0 :
        ConceptsUsedUnique                      = util.get_unique_list_feature_items(groupOriginal[groupOriginal['StudentId'] == StudentId], 'ConceptsUsedDetails')
        
        if     ConceptsUsedUnique is not None  :        
            
            ConceptsUsedUniqueUserReadable = set()
            for conceptUsed in ConceptsUsedUnique:
                ConceptsUsedUniqueUserReadable.add(  constants.ProgramConceptsUsefull2UserNames.get(conceptUsed) if 
                                                      conceptUsed in constants.ProgramConceptsUsefull2UserNames 
                                                      else 
                                                      conceptUsed  )
            
            plotRow.append( html.Div([
                                        util.generateCardBase(
                                                 [html.I(className="fas fa-code m-right-small"),   'Concepts Used', ], 
                                                ', '.join(ConceptsUsedUniqueUserReadable) ,
                                                classes = "c-card-small" )
                                    ],
                                    className="col-sm-6",
                            ))
    
    
        
        
    graphs.append(
            html.Div(children  = plotRow,                
                     className = "row")
    )

    
    return graphs




def plotStudentOverviewFeatures( StudentId, groupId, features2Overview ):
    if (None == groupId) :
        return html.Div()
    
    if (None == features2Overview) :
        features2Overview = [] 
        
    
    graphs = []
    plotRow = []    
    
#    the student is not in the group
    if not isStudentInGroup(StudentId, groupId) :
        return graphs
    
    

    studentDataDf                     = getStudentData(StudentId, groupId)
    
    if studentDataDf is None or studentDataDf.empty == True :
        graphs.append(
                util.getNoDataMsg()
        )
        return graphs
    
    
    studentDataDf.fillna(0, inplace=True)
    
    try:
        studentDataDfMean    = studentDataDf.mean().round(decimals=2)
        studentDataDfStd    = studentDataDf.std().round(decimals=2)
        
        studentDataDfMean.fillna(0, inplace=True)
        studentDataDfStd.fillna(0, inplace=True)
    
        for feature2O in features2Overview :
            
            plotRow.append(
                html.Div([
                       util.generateCardDetail( 
                               ((constants.feature2UserNamesDict.get(feature2O)) if feature2O in constants.feature2UserNamesDict.keys() else feature2O ) 
                                , 
                                            '' + util.millify( studentDataDf[ feature2O ].sum().round(decimals=2) ), 
                                            '' + str( studentDataDfMean[ feature2O ] ), 
                                            '' + str( studentDataDfStd[ feature2O ] ), 
                                            'total',
                                            'mean',
                                            'std',
                                            classes = "c-card-small"
                                            )
                    ],            
                    className="col-sm-4",
                ))
    except Exception as e: 
        print(e)
        
      
    graphs.append(
            html.Div(children  = plotRow,                
                     className = "row")
    )
    
    return graphs
        

#Student Interaction with Game - TIMELINE
def plotStudent(StudentId, schoolKey, studentSelectedDate = '', studentGraphDirection = sortOrderDescending ):
    
    graphs = []
    graphIndex = 1
    
    
#    the student is not in the group
    if not isStudentInGroup(StudentId, schoolKey) :
        return graphs
    

    studentData                     = getStudentData(StudentId, schoolKey, studentSelectedDate)

    if studentData is None or studentData.empty == True :
        graphs.append(
                util.getNoDataMsg()
        )
        return graphs
    
        
#    studentData                     = studentData.sort_values(by='Start')
        
    isAscending = True
    if None is not studentGraphDirection and not studentGraphDirection == '' and studentGraphDirection == sortOrderDescending :
        isAscending = False
        
    studentData.sort_values(by = 'Start', inplace=True, ascending = isAscending )
    
#    studentData['color']                                            =   constants.colorError
#    studentData.loc[studentData['Result']  == 1, 'color']           =   constants.colorSuccess
    studentData.loc[studentData[constants.featureTaskType]  == constants.TaskTypePractice, 'color']      =   constants.colorPractice
    studentData.loc[studentData[constants.featureTaskType]  == constants.TaskTypeTheory, 'color']        =   constants.colorTheory
    studentData.loc[studentData['Result']  == 0, 'color']                                                =   constants.colorError

    studentData['Task'] = studentData['IndexCol']
    studentData['Text'] = studentData['Difference'].astype(str) + 's for ' + studentData[constants.featureTaskType].astype(str) + ' Task : ' +  studentData['Title' ]  + ' Result : ' +  studentData['Result'].astype(str)

    colors  = { 
            constants.TaskTypePractice  : constants.colorPractice,
            constants.TaskTypeTheory : constants.colorTheory,
            constants.TaskTypePractice + '-1' : constants.colorPractice,
            constants.TaskTypeTheory + '-1' : constants.colorTheory,
            constants.TaskTypePractice + '-0' : constants.colorError,
            constants.TaskTypeTheory + '-0' : constants.colorError,
    }
    
    studentData['IndexSuccFail'] = studentData[constants.featureTaskType] + '-' + studentData['Result'].astype(str)
    
    
    graphHeightRows =  ( studentData.shape[0] * 35 )    
    graphHeightRows = graphHeightRows if (graphHeightRows > 500) else 500  
    
    
    #type 2 
    fig = go.Figure()
    fig.add_traces(go.Bar(
                    x               =  studentData['Difference'],
                    y               = studentData['StartStr'] ,
                    text            = studentData['Text'] , 
                    textposition    = 'auto'  ,    
                    orientation     = 'h',
                    marker          =  dict( color = studentData['color']   ) ,
                    customdata      = np.stack(( studentData['Title'],
                                            studentData['Description'] 
                            ), axis=-1) ,
                    hovertemplate   = "<br>" +
                                  "%{customdata[1]}<br>"                         
                                )
                    )
    fig.update_layout(
                                        height          =   graphHeightRows , 
                                        title_text      = 'Details of student\'s game interactions'
                                             , yaxis = dict(
                                                title = 'Time',
                                                titlefont_size = 16,
                                                tickfont_size = 14,
                                            ), xaxis = dict(
                                                title = 'Duration (s)',
                                                titlefont_size = 16,
                                                tickfont_size = 14,
                            ))
    graphs.append(
            dcc.Graph(
                id='graphStudent-' + str(graphIndex),
                figure= fig
        ))
    graphIndex = graphIndex + 1
    
    
    
#    gantt chart for timeline 
#    if studentData is not None and studentData.empty == False :
    fig = ff.create_gantt(studentData, title = 'Student Schedule' , colors = colors, index_col= 'IndexSuccFail' , 
                          show_colorbar = True , 
                          bar_width = 0.8 , 
                          showgrid_x = True , showgrid_y = True,
                          height =   graphHeightRows ,
                         # width = 2000 
                          )
    
    graphs.append(
            dcc.Graph(
                id='graphStudent-' + str(graphIndex),
                figure= fig
        ))
    graphIndex = graphIndex + 1

# **** IMPORTANT - ff.create_gantt is deprecated -> moved to px.timeline 
#    studentData['StartStr'] = studentData['Start'].dt.strftime('%Y-%m-%d %H:%M:%S')
#    studentData['FinishStr'] = studentData['Finish'].dt.strftime('%Y-%m-%d %H:%M:%S')
#    
#    fig = px.timeline(studentData, x_start="StartStr", x_end="FinishStr", y="Task"
#                      , color = constants.featureTaskType,   
#                        hover_data    = ['Description', 'Start', 'StartStr', 'Finish', 'FinishStr'] ,                   
#                        height =   graphHeightRows 
#    )
#    graphs.append(
#            dcc.Graph(
#                id='graphStudent-' + str(graphIndex),
#                figure= fig
#        ))
#    graphIndex = graphIndex + 1
    
    
    
    return graphs



featureOptionsOverview = [
     'Result',
     'Points',
     'SessionDuration',
     'Attempts',
     'CollectedCoins',
     'Difficulty',
     'NumberOfCoins',
     'NumberOfHidden',
     'lineOfCodeCount',
     'runsCount',
     'runsErrorCount',
     'runsSuccessCount',
     'runsErrorSyntaxCount',
     'runsErrorNameCount',
     'runsErrorTypeCount',
     'runsErrorAttribiteCount',
     'runsHasLoopCount',
     'runsHasNestedLoopCount',
     'runsHasConditionCount',
     'runsHasVariableCount',
     'runsHasExpressionsCount',
     'runsHasAsyncOrAwaitCount',
     'runsHasFunctionClassCount',
     'runsHasControlFlowCount',
     'runsHasImportsCount',
     'runsHasStatementsCount',
     'runsHasComprehensionsCount',
     'runsHasSubscriptingCount',
     'runsLineOfCodeCountAvg',
     'draggedCount',
     'tabsSwitchedCount',
     'tabsSwitchedDescriptionCount',
     'tabsSwitchedCodeCount',
     'tabsSwitchedOutputCount',
     'deletedCodesCount',
     'robotCollisionsBoxCount',
     'coinCollectedCount',
     'keyboardKeyPressedCount',
     'studentAttemptsTotal',
     'enemiesCount',
     'playerShootCount',
     'playerShootEndCount',
     'playerShootEndEnemyHitCount',
     'playerShootEndEnemyMissedHitCount',
     'enemysShootEndPlayerHitCount',
     'enemysShootEndPlayerNotHitCount',
     'itemsCollectedCount'
 ]

def getFeatureOptions():
    
#    numericFeaturesPracticeS = set(util.getNumericFeatures(dfGroupedOriginal.median()))
#    numericFeaturesTheoryS = set(util.getNumericFeatures(dfPlayerStrategyTheory))
#    
#    print('get feature options')
#    print( numericFeaturesPracticeS  )
#    print( numericFeaturesTheoryS )
#    
#    return util.BuildOptionsFeatures( numericFeaturesPracticeS.union(numericFeaturesTheoryS) )
    
    return util.BuildOptionsFeatures( featureOptionsOverview )
    



#-----------------------------------------
# Layout-------------------------
#-------------------------------------------

layout = [
        html.Div([

     dbc.Row([
            dbc.Col(
                html.Div(id='student-information', children = [
                    html.H3('Student Information'),
                        ], 
                               className = "c-container", 
                )
      )])
    , dbc.Row([
            dbc.Col(
              html.Div([
                    dcc.Dropdown(
                            id ='student-selector-dropdown', 
                            placeholder = "Select Student", 
                        )
                    ],
                    className = " "
               )
                , width = 12
            ),  
    ])

    , dbc.Row([
            dbc.Col(
                html.Div(id='student-overview-container', 
                           className = "c-container m_small")
      )])
             

    , dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Dropdown(
                            id='student-feature-overview-dropdown', 
                            placeholder = "Select Overview Features",
                            options = getFeatureOptions(),
                            multi   = True,
                        )
                    ],
                    className = "  "
                )
                , width = 12
            ),
    ])
                
    , dbc.Row([
            dbc.Col(
                html.Div(id='student-features-overview-container', 
                           className = "c-container m_small")
      )])
             
            
    , dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Dropdown(
                            id='student-date-dropdown', 
                            placeholder = "Select Date",
                        )
                    ],
                    className = "c-container"
                )
                , width = 6
            ),
            dbc.Col(
                html.Div([
                    dcc.Dropdown(
                            id = 'student-sort-order-dropdown',
                            options=[
                                {'label': sortOrderAscending, 'value': sortOrderAscending},
                                {'label': sortOrderDescending, 'value': sortOrderDescending},
                            ],
                            value = sortOrderAscending , 
                            placeholder = "Order",
                    )
                ], 
                className = "c-container", 
                )
                , width  =  6
            )
    ])
                    
    , dbc.Row([
            dbc.Col( 
                    html.A(children=[html.I(className="fas fa-download font-size_medium p_small"),
                       "download data : Student",],  id = "student_details_download_link", className = "hidden" ,
                                               href="", target="_blank",
                                               download='student.csv' )
        )])    
     
    , dbc.Row([
            dbc.Col(
                html.Div(id='Student-Container', 
                           className = "c-container p-bottom_15")
      )])
        
                
                
    
    ])    
]


#-----------------------------------------
# callback functions---------------------
#        ---------------------------------


#-------- Students-------------
@app.callback(Output('student-selector-dropdown', 'options'), [Input('group-selector-main', 'value')])
def setStudentOptions(schoolSelected):
        
    if schoolSelected is None or not int(schoolSelected) >= 0:
        return []
    
    students = getStudentsOfSchool(int(schoolSelected))
    
    return [{'label': row['Name'], 'value': row['StudentId'] } for index, row  in dfStudentDetails[dfStudentDetails['StudentId'].isin( students)][['StudentId', 'Name']].iterrows() ]
    

@app.callback(
         Output('student-date-dropdown', 'options'), 
              [ Input('student-selector-dropdown', 'value') ],
        state = [ State(component_id='group-selector-main', component_property='value') ]   
)
def setStudentDateOptions(studentSelected, groupSelected):
    defaultValue = []
    
    if groupSelected is None or not int(groupSelected) >= 0  or studentSelected is None or not int(studentSelected) >= 0:
        return defaultValue
    
    if not isStudentInGroup(studentSelected, groupSelected) :
        return defaultValue


    dfStudentData                     = getStudentData(int(studentSelected), int(groupSelected))
    
    
    if dfStudentData is None        or     dfStudentData.empty == True :
        return defaultValue
    
    
    return [{'label': d, 'value': d } for d  in dfStudentData['Start'].dt.date.unique() ]



@app.callback(
         Output('student-date-dropdown', 'value'), 
         [  Input('student-selector-dropdown', 'value') , ],
        state = [ State(component_id='group-selector-main', component_property='value') ] 
)
def setStudentDateOptionsClear(studentSelected, groupSelected):        
    if groupSelected is None or not int(groupSelected) >= 0  or studentSelected is None or not int(studentSelected) >= 0:
        return ''   
    
    if not isStudentInGroup(studentSelected, groupSelected) :
        return ''




@app.callback(Output('Student-Container', 'children'),               
              [Input('student-selector-dropdown', 'value') , 
               Input('student-date-dropdown', 'value') ,
               Input('student-sort-order-dropdown', 'value') ,
               ],               
        state=[ State(component_id='group-selector-main', component_property='value')
                ]             
)
def display_graphs_student(studentSelected, studentSelectedDate, studentGraphDirection, schoolSelected):
    graphs = []
    
    if schoolSelected is None or not int(schoolSelected) >= 0 or studentSelected is None or not int(studentSelected) >= 0:
        return html.Div(graphs)
    
    if studentSelectedDate is None  or  studentSelectedDate == '':
        studentSelectedDate = ''
    
    graphs = plotStudent( int( studentSelected ) , int(schoolSelected) , format(studentSelectedDate), studentGraphDirection  )
    
    return html.Div(graphs)




@app.callback(
         Output('student-overview-container', 'children'), 
         [  Input('student-selector-dropdown', 'value') , ],
        state = [ State(component_id='group-selector-main', component_property='value') ] 
)
def display_graphs_student_overview(studentSelected, groupSelected):        
    graphs = []
    
    if groupSelected is None or not int(groupSelected) >= 0 or studentSelected is None or not int(studentSelected) >= 0:
        return html.Div(graphs)
    
    if not isStudentInGroup(studentSelected, groupSelected) :
        return graphs
    
    graphs = plotStudentOverview( int( studentSelected ) , int(groupSelected)  )
    
    return html.Div(graphs)

    


# Update bar plot
@app.callback(
    Output("student-features-overview-container", "children"),
    [
        Input("student-feature-overview-dropdown", "value"),
        Input("student-selector-dropdown", "value"),
    ],
     state = [ 
        State(component_id='group-selector-main', component_property='value'),
    ]
)
def onSelectFeatureOverview(selectedFeatures, studentSelected, groupSelected ):
    graphs = []

    if groupSelected is None or not int(groupSelected) >= 0    or   studentSelected is None   or not int(studentSelected) >= 0:
        return html.Div(graphs)
 
    graphs = plotStudentOverviewFeatures( int( studentSelected ) , int(groupSelected), selectedFeatures )    
    
    return  html.Div(graphs)
    



@app.callback(
    [    Output("student-date-dropdown", "className"),  
         Output("student-sort-order-dropdown", "className"),
         Output("student-feature-overview-dropdown", "className"), 
     ],
    [
        Input("student-selector-dropdown", "value")
    ],
    state=[ State(component_id='student-date-dropdown', component_property='className'),
           State(component_id='student-sort-order-dropdown', component_property='className'),
           State(component_id='student-feature-overview-dropdown', component_property='className'),
           ]
)
def update_no_student_selectors_class_disabled(studentSelected, initialClassDate, initialClassDir, initialClassFeatures, ):  
    initialClassDateS = set()
    initialClassDirS = set()
    initialClassFeaturesS = set()
    
    if not None is initialClassDate:
        initialClassDateS = set(initialClassDate.split(' ')) 
    if not None is initialClassDir:
        initialClassDirS = set(initialClassDir.split(' ')) 
    if not None is initialClassFeatures:
        initialClassFeaturesS = set(initialClassFeatures.split(' ')) 

    
    if   studentSelected is None   or not int(studentSelected) >= 0:
        initialClassDateS.add('disabled') 
        initialClassDirS.add('disabled') 
        initialClassFeaturesS.add('disabled') 

    else:
        initialClassDateS.discard('disabled') 
        initialClassDirS.discard('disabled') 
        initialClassFeaturesS.discard('disabled') 

    return ' '.join(initialClassDateS), ' '.join(initialClassDirS), ' '.join(initialClassFeaturesS)





#--------------------- data download callbacks 
@app.callback(
    [ Output('student_details_download_link', 'href'),
     Output('student_details_download_link', 'className'),
     ],
    [ Input('student-selector-dropdown', 'value')  , Input('student-date-dropdown', 'value') ],               
    state=[ State(component_id='group-selector-main', component_property='value')
            ]   
)
def update_download_link__details_student( studentSelected, studentSelectedDate, groupMain ):
    defaultValues = ["", "disabled"]
    
    if (groupMain is None or not int(groupMain) >= 0 or groupMain == "" ) or ( 
            studentSelected is None or not int(studentSelected) >= 0 or studentSelected == "" ):
        return defaultValues
    
    if studentSelectedDate is None  or  studentSelectedDate == '':
        studentSelectedDate = ''
        
    #    the student is not in the group
    if not isStudentInGroup(studentSelected, groupMain) :
        return defaultValues
        
    csv_string = util.get_download_link_data_uri( getStudentData(int(studentSelected), int(groupMain) , format(studentSelectedDate)  ))
    
    return csv_string, ""
