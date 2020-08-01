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



import studentGrouped
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

hasFeatures =  studentGrouped.hasFeatures

#--------------------------------- Const values END ----------------------------


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
    school                              = dfGroupedOriginal.get_group(schoolKey)
    schoolStudent                       = school[school['StudentId'] == StudentId]
    schoolStudent['Finish']             = schoolStudent['CreatedAt'] 
    schoolStudent['Start']              = schoolStudent['Finish'] - pd.to_timedelta(schoolStudent[featureSessionDuration], unit='s')
    schoolStudent[featureDescription]   = getPracticeDescription(schoolStudent, False)   
    schoolStudent[featureDescription]   = '<b>Title</b>:' + schoolStudent['Title'].astype(str)  + '<br><br>'+ schoolStudent[featureDescription].astype(str)
    
#    codes = dfRuns[dfRuns['StudentId'].isin(schoolStudent['StudentId']) & dfRuns['PracticeStatisticsId'].isin(schoolStudent['PracticeStatisticsId']) ]
#        
#    codes = codes.merge(right= dfPracticeTaskDetails
#                                      , left_on='PracticeTaskId', right_on='PracticeTaskId'
#                                        , left_index=False, right_index=False
#                                        , how='inner')
#    codes.rename(columns = {featureDescription: 'PracticeTaskDescription'}, inplace = True)
#    
#    codes['RunsTime'] = pd.to_datetime(codes['RunsTime'])
#    
#    #codes['Finish'] = codes['RunsTime'].shift(-1)
#    codes['Start'] = codes['RunsTime']
#    codes['Start'] = pd.to_datetime(codes['Start'])
#    codes['Task'] =  'Practice-' + codes['PracticeTaskId'].astype(str)
#    codes['Code'] =  codes['RunsCode']
#    codes['Finish'] = codes.groupby('PracticeStatisticsId')['Start'].shift(-1)
#    
#    codes['IndexCol'] = 'Practice-' + codes['PracticeTaskId'].astype(str) + '-(Runs Code Error:' + codes['RunsError'].astype(int).astype(str) + ')'
#    
#    codes[featureDescription] = '<b>Runs code</b>'
#    codes[featureDescription] = codes[featureDescription] + '<br><b>Title</b>:' + codes['Title'].astype(str) + '<br><b>Code</b> : ' +  codes['Code'].astype(str)
#    codes[featureDescription] = codes[featureDescription] + '<br><b>Has Error</b>: ' + codes['RunsError'].astype(int).astype(str)
    

#    codes = pd.concat([codes, schoolStudent], ignore_index=True, sort =False)
#    codes = pd.concat([codes, schoolStudent[['PracticeTaskId', 'StudentId', 'PracticeStatisticsId', 'Finish', 'Start', 'Result', 'Code', 'Title', 'SessionDuration']]], ignore_index=True, sort =False)
    
    schoolStudent = schoolStudent.sort_values(by='Start')
    
    schoolStudent['IndexCol']  = 'Practice-' + schoolStudent['PracticeTaskId'].astype(str) + '-' + schoolStudent['Result'].astype('Int64').astype(str) 
#    schoolStudent['IndexCol'] = np.where(   schoolStudent['IndexCol'].isnull()  , ( 'Practice-' + schoolStudent['PracticeTaskId'].astype(str) + '-' + schoolStudent['Result'].astype('Int64').astype(str) )  ,   schoolStudent['IndexCol']  ) 

    
    schoolStudent['Finish'] = np.where(schoolStudent['Finish'].isnull(), schoolStudent['Start'].shift(-1), schoolStudent['Finish'])
    
    
    schoolStudent['Difference'] = (schoolStudent['Finish'] - schoolStudent['Start']).astype('timedelta64[s]')
     
    
#    schoolStudent['Description2'] = '<b>Title</b>:' + schoolStudent['Title'].astype(str) + '<br><b>Code</b> : ' +  schoolStudent['Code'].astype(str)
#    schoolStudent['Description2'] = schoolStudent['Description2'] + '<br><b>Result</b>: ' + schoolStudent['Result'].astype('Int64').astype(str)
    
    
#    schoolStudent[featureDescription] = np.where(schoolStudent[featureDescription].isnull(), schoolStudent['Description2'], schoolStudent[featureDescription])
#    schoolStudent[featureDescription] = schoolStudent[featureDescription] + '<br><b>Duration</b>: ' + schoolStudent['Difference'].astype(str) + ' s '

    
    studentData         = schoolStudent

    
    studentData[constants.featureTaskType] = [  constants.TaskTypePractice ] * studentData.shape[0]


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
        schoolTheoryStudent['Task'] = constants.TaskTypeTheory + '-' + schoolTheoryStudent['TheoryTaskId'].astype(str) 
        
        schoolTheoryStudent[featureDescription] = getTheoryDescription(schoolTheoryStudent, False)  
        schoolTheoryStudent[featureDescription] = '<b>Title</b>:' + schoolTheoryStudent['Title'].astype(str)  + '<br><br>'+ schoolTheoryStudent[featureDescription].astype(str) 
    
#        schoolTheoryStudent['Description'] = '<b>Title</b>:' + schoolTheoryStudent['Title'].astype(str) + '<br><b>Solution</b>: ' +  schoolTheoryStudent['Solution'].astype(str)
#        schoolTheoryStudent['Description'] = schoolTheoryStudent['Description'] + '<br><b>Result</b> : '+ schoolTheoryStudent['Result'].astype(str)
#        schoolTheoryStudent['Description'] = schoolTheoryStudent['Description'] + '<br><b>SessionDuration</b>: ' + schoolTheoryStudent['SessionDuration'].astype(str) + ' s '
        
        
        schoolTheoryStudent['IndexCol'] = 'Theory-' + schoolTheoryStudent['TheoryTaskId'].astype(str) + '-' + schoolTheoryStudent['Result'].astype(str)
        
        schoolTheoryStudent[constants.featureTaskType] = [  constants.TaskTypeTheory ] * schoolTheoryStudent.shape[0]
        
        
        if schoolTheoryStudent is not None and schoolTheoryStudent.empty == False :
            studentData = pd.concat([studentData, schoolTheoryStudent], ignore_index=True)
    except Exception as e: 
        print(e)
        
    
    if     None is not selectedDate         and         not selectedDate == ''     and   util.is_valid_date(selectedDate) :
        studentDataGroupedDate  = studentData.groupby(  [studentData['Start'].dt.date] )
        studentData = studentDataGroupedDate.get_group(selectedDate)
    
    
    studentData['StartStr']         = '@' + studentData['Start'].dt.strftime('%Y-%m-%d %H:%M:%S') + '-' + studentData['IndexCol'].astype(str)
    
    return studentData


#Check if Student is in a Group
def isStudentInGroup(StudentId, groupId) :
    groupStudents = getStudentsOfSchool(groupId)
    
    if not StudentId in groupStudents:
        return False
    
    return True



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
                html.H2('Has no game interactions')
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
                          height =   graphHeightRows  
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




#-----------------------------------------
# Layout-------------------------
#-------------------------------------------

layout = [
        html.Div([

     dbc.Row([
            dbc.Col(
                html.Div(id='Student-Information', children = [
                    html.H3('Student Information'),
                        ], 
                               className = "c-container p_medium", 
                )
      )])
    , dbc.Row([
            dbc.Col(
              html.Div([
                    dcc.Dropdown(
                            id ='StudentSelector-Dropdown', 
                            placeholder = "Select Student", 
                        )
                    ],
                    className = "c-container"
               )
                , width=8
            ),
            dbc.Col(
                html.Div([
                    dcc.Dropdown(
                            id='StudentSelector-Date-Dropdown', 
                            placeholder = "Select Date",
                        )
                    ],
                    className = "c-container"
                )
                , width=3
            ),
            dbc.Col(
                html.Div([
                    dcc.Dropdown(
                            id = 'StudentSelector-Direction-Dropdown',
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
                , width=1
            )
    ])

    , dbc.Row([
            dbc.Col( 
                    html.A(children=[html.I(className="fas fa-download font-size_medium p_small"),
                       "download data : Student",],  id = "details_download_student_link", className = "hidden" ,
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
@app.callback(Output('StudentSelector-Dropdown', 'options'), [Input('group-selector-main', 'value')])
def setStudentOptions(schoolSelected):
        
    if schoolSelected is None or not int(schoolSelected) >= 0:
        return []
    
    students = getStudentsOfSchool(int(schoolSelected))
    
    return [{'label': row['Name'], 'value': row['StudentId'] } for index, row  in dfStudentDetails[dfStudentDetails['StudentId'].isin( students)][['StudentId', 'Name']].iterrows() ]

@app.callback(
         Output('StudentSelector-Date-Dropdown', 'options'), 
              [Input('StudentSelector-Dropdown', 'value') , Input('group-selector-main', 'value')    ], 
)
def setStudentDateOptions(studentSelected, groupSelected):
    defaultValue = []
    
    if groupSelected is None or not int(groupSelected) >= 0  or studentSelected is None or not int(studentSelected) >= 0:
        return defaultValue
    
    if not isStudentInGroup(studentSelected, groupSelected) :
        return defaultValue


    dfStudentData                     = getStudentData(int(studentSelected), int(groupSelected))
    
    return [{'label': d, 'value': d } for d  in dfStudentData['Start'].dt.date.unique() ]

@app.callback(
         Output('StudentSelector-Date-Dropdown', 'value'), 
         [Input('StudentSelector-Dropdown', 'value') , Input('group-selector-main', 'value')   ],
)
def setStudentDateOptionsClear(studentSelected, groupSelected):        
    if groupSelected is None or not int(groupSelected) >= 0  or studentSelected is None or not int(studentSelected) >= 0:
        return ''   
    
    if not isStudentInGroup(studentSelected, groupSelected) :
        return ''




@app.callback(Output('Student-Container', 'children'),               
              [Input('StudentSelector-Dropdown', 'value') , 
               Input('StudentSelector-Date-Dropdown', 'value') ,
               Input('StudentSelector-Direction-Dropdown', 'value') ,
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









#--------------------- data download callbacks 
@app.callback(
    [ Output('details_download_student_link', 'href'),
     Output('details_download_student_link', 'className'),
     ],
    [ Input('StudentSelector-Dropdown', 'value')  , Input('StudentSelector-Date-Dropdown', 'value') ],               
    state=[ State(component_id='group-selector-main', component_property='value')
            ]   
)
def update_download_link__details_student( studentSelected, studentSelectedDate, groupMain ):
    defaultValues = ["", "hidden"]
    
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
