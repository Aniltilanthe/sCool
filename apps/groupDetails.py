# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 19:04:59 2020

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

TaskTypePractice                    = constants.TaskTypePractice
TaskTypeTheory                      = constants.TaskTypeTheory


hasFeatures =  studentGrouped.hasFeatures

#    [  X ,  Y   ]
featurePairsToPlotSingle = [
        ['Attempts', 'Name']
        , ['Points', 'Name']
        , ['robotCollisionsBoxCount', 'Name']
        , ['CollectedCoins', 'Name']
        , ['SessionDuration', 'Name']    
        ]

featurePairsToPlotTheory = [
        ['playerShootEndEnemyHitCount', 'Name']
        , ['Points', 'Name']  
        , ['SessionDuration', 'Name']  
        , ['Attempts', 'Name']  
        ]
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


#---------------------------------
# school selection
SchoolSelector_options                  = studentGrouped.GroupSelector_options 

StudentSelector_students = list()

#-----------------------------------


#--------------------------- helper functions -----------------------    
getTaskWiseSuccessFail                  =  studentGrouped.getTaskWiseSuccessFail
getStudentsOfSchool                     =  studentGrouped.getStudentsOfSchool


getPracticeDescription                  =  studentGrouped.getPracticeDescription
getTheoryDescription                     =  studentGrouped.getTheoryDescription



def getSuccessPieFig(groupData, taskId, dfTaskDetails, featureTaskId, typeOfTask):
    
    groupData = groupData.sort_values(['StudentId','Result'], ascending=False)

    taskTitle = ' missing '
    
    try :
        taskTitle =  dfTaskDetails[ dfTaskDetails[featureTaskId] == int(taskId) ]['Title'].values[0]
    except Exception as e: 
        print(e)
    
    pieFig = go.Figure(go.Pie(
                        values = [groupData[groupData['Result'] == 1].count()[0], 
                                  groupData[groupData['Result'] == 0].count()[0]],
                        labels = [constants.successPieFigClassSuccess, constants.successPieFigClassOthers],
                        text = ["Success", "Others"],
                        marker_colors =  [ constants.colorSuccess, constants.colorError ]
                    ))
    pieFig.update_layout(
            autosize =  False,
            title_text =  str(typeOfTask) + ' Task ' + ": " + str(taskTitle) + " (Id: " + str(taskId) + ")"
    )
    
    return pieFig

def convert_list_column_tostr_NL(val) :
    separator = ',<br>'
    return separator.join(val)




#--------------------------- helper functions  END -----------------------


#------------------------------------

def plotSingleClass( titleTextAdd, school ):
     
    graphIndex = 1
    graphs = []
    
        
    try :
        groupOriginal = dfGroupedOriginal.get_group(school)
        
        try :
            groupOriginalTheory = dfGroupedPlayerStrategyTheory.get_group(school)
        except Exception as e: 
            print(e)
        
        
        
        
#        -------------------------------------------
#            Task wise information
        
        
        graphs.append(html.Div(id='Task-Information',
                               children = [html.H2('Task Information')], 
                    style = {'padding' : '20px',
                             'padding-top' : '100px',
                             'font-size' : 'initial'}))        

#---------------------------        Datatable task wise success fail    ---------------------------
        dfTaskWiseSuccessFail = pd.DataFrame(index=np.arange(0, 1), columns=['Task', 'Success', 'Others', 'Type', 'TaskId'])
        
        
        pieDataTaskWisePractice = groupOriginal.groupby(['PracticeTaskId', 'StudentId'], as_index=False).sum()
        pieDataTaskWisePractice.loc[pieDataTaskWisePractice['Result'] > 0, 'Result'] = 1   
        pieDataTaskWisePracticeGrouped = pieDataTaskWisePractice.groupby(['PracticeTaskId'])
        
        
        index_dfTaskWiseSuccessFail = 0
        for groupKeyTaskId, groupTask in pieDataTaskWisePracticeGrouped:
            dfTaskWiseSuccessFail.loc[index_dfTaskWiseSuccessFail] =  getTaskWiseSuccessFail(groupTask, groupKeyTaskId,  dfPracticeTaskDetails, 'PracticeTaskId', 'Practice')
            index_dfTaskWiseSuccessFail += 1
                
        try :        
            pieDataTaskWiseTheory = groupOriginalTheory.groupby(['TheoryTaskId', 'StudentId'], as_index=False).sum()
            pieDataTaskWiseTheory.loc[pieDataTaskWiseTheory['Result'] > 0, 'Result'] = 1   
            pieDataTaskWiseTheoryGrouped = pieDataTaskWiseTheory.groupby(['TheoryTaskId'])
        
            for groupKeyTaskId, groupTask in pieDataTaskWiseTheoryGrouped:
                dfTaskWiseSuccessFail.loc[index_dfTaskWiseSuccessFail] =  getTaskWiseSuccessFail(groupTask, groupKeyTaskId,  dfTheoryTaskDetails, 'TheoryTaskId', 'Theory')
                index_dfTaskWiseSuccessFail += 1

        except Exception as e: 
                print('in the theory exception ')   
                print(e)   
        
        # convert column of DataFrame to Numeric Int
        dfTaskWiseSuccessFail["Success"] = pd.to_numeric(dfTaskWiseSuccessFail["Success"], downcast='integer')
        dfTaskWiseSuccessFail["Others"] = pd.to_numeric(dfTaskWiseSuccessFail["Others"], downcast='integer')
        
        print(dfTaskWiseSuccessFail.info())
        
        figStudents =  dash_table.DataTable(
                id='datatable-taskwise-successfail',
                columns=[
                    {"name": i, "id": i, "deletable": True, "selectable": True} for i in dfTaskWiseSuccessFail.columns
                ],
                data            =   dfTaskWiseSuccessFail.to_dict('records'),
                editable        =   True,
                filter_action   =   "native",
                sort_action     =   "native",
                sort_mode       =   "multi"
            )
            
        graphs.append(  
                html.Div([ figStudents ] ,
                    style = { 'font-size' : '1rem'  })
        )
        graphIndex = graphIndex + 1
        

        
    #            CHECKED     
    #            count of students completing a task
    
    
    #       if a student passed a task once, then he is Successfull OR Result = 1    
    
        pieData = groupOriginal.groupby(['PracticeTaskId', 'StudentId'], as_index=False).sum()
        
        pieData.loc[pieData['Result'] > 0, 'Result'] = 1
    
        taskData = pieData.groupby(['PracticeTaskId'], as_index=False).sum()
        taskData = taskData.rename(columns={"Result": countStudentCompletingTaskFeature})
        taskData = taskData.merge(right= dfPracticeTaskDetails
                                          , left_on='PracticeTaskId', right_on='PracticeTaskId'
                                            , left_index=False, right_index=False
                                            , how='inner')
        taskData[featurePracticeTaskDesc] = taskData['Title'] + ' (Id: ' + taskData['PracticeTaskId'].astype(str) + ')' 
    
        try :
            pieDataTheory = groupOriginalTheory.groupby(['TheoryTaskId', 'StudentId'], as_index=False).sum()
        
            pieDataTheory.loc[pieDataTheory['Result'] > 0, 'Result'] = 1
        
            taskDataTheory = pieDataTheory.groupby(['TheoryTaskId'], as_index=False).sum()
            taskDataTheory = taskDataTheory.rename(columns={"Result": countStudentCompletingTaskFeature})
            taskDataTheory = taskDataTheory.merge(right= dfTheoryTaskDetails
                                              , left_on='TheoryTaskId', right_on='TheoryTaskId'
                                                , left_index=False, right_index=False
                                                , how='inner')
            taskDataTheory[featureTheoryTaskDesc] = taskDataTheory['Title'] + ' (Id: ' + taskDataTheory['TheoryTaskId'].astype(str) + ')' 
        except Exception as e: 
                print(e)
    
        figStudents = px.bar(taskData
                            , x=  countStudentCompletingTaskFeature
                            , y=  featurePracticeTaskDesc
                            , title  = "(Practice)" +  ' No. of students completing a Task '
                            ,  labels= feature2UserNamesDict # customize axis label
#                            , height       = graphHeight
                            , template     = constants.graphTemplete
                            , hover_data = ['Title']                             
                            , orientation   = 'h'
        )
        graphs.append(
                dcc.Graph(
                    id='graphSchool-' + str(graphIndex),
                    figure= figStudents
            ))
        graphIndex = graphIndex + 1
        
        
        figStudents = px.bar(taskDataTheory
                            , x=  countStudentCompletingTaskFeature
                            , y=  featureTheoryTaskDesc
                            , title  = "(Theory)" + ' No. of students completing a Task '
                            ,  labels= feature2UserNamesDict # customize axis label
#                            , height       = graphHeight
                            , template     = constants.graphTemplete
                            , hover_data = ['Title']                             
                            , orientation   = 'h'
        )
        graphs.append(
                dcc.Graph(
                    id='graphSchool-' + str(graphIndex),
                    figure= figStudents
            ))
        graphIndex = graphIndex + 1
        
        
    #            CHECKED
    #            count of tasks completed by each student    
        graphTitle = '(Practice) Count of tasks completed by students'
        try: 
            studentWiseDataOriginalTaskPerformed = groupOriginal
            studentWiseDataOriginalTaskPerformed[featureTaskDesc] = studentWiseDataOriginalTaskPerformed['Title'] + ' (Id: ' + studentWiseDataOriginalTaskPerformed['PracticeTaskId'].astype(str) + ')' 
            studentWiseDataOriginalTaskPerformed = studentWiseDataOriginalTaskPerformed [ studentWiseDataOriginalTaskPerformed['Result'] == 1][['StudentId', 'PracticeTaskId'
                          , 'Result', 'Name', featureTaskDesc]].groupby(
                          ['StudentId', 'Name']).agg({'PracticeTaskId': ['nunique'], featureTaskDesc: ['unique']})
            studentWiseDataOriginalTaskPerformed = studentWiseDataOriginalTaskPerformed.reset_index()
            studentWiseDataOriginalTaskPerformed.rename(columns={'PracticeTaskId': countTaskCompletedByStudentFeature}, inplace=True)
            studentWiseDataOriginalTaskPerformed.columns = studentWiseDataOriginalTaskPerformed.columns.droplevel(1)
            
            studentWiseDataOriginalTaskPerformed[featureTaskDesc] = studentWiseDataOriginalTaskPerformed[featureTaskDesc].apply(convert_list_column_tostr_NL)
            studentWiseDataOriginalTaskPerformed[featureTaskType] = TaskTypePractice
            
            
            figStudents = px.bar( studentWiseDataOriginalTaskPerformed
                                    , x             = countTaskCompletedByStudentFeature
                                    , y             = 'Name'
                                    , title         = graphTitle
                                    , labels        = feature2UserNamesDict # customize axis label
    #                                , height        = constants.graphHeight
                                    , template      = constants.graphTemplete                              
                                    , orientation   = 'h'
                                    , hover_data    = [featureTaskDesc]
                )
            graphs.append(
                    dcc.Graph(
                        id='graphSchool-' + str(graphIndex),
                        figure= figStudents
                ))
            graphIndex = graphIndex + 1
        except Exception as e:             
            print( 'ERROR - ' + graphTitle )   
            print(e)
        
        graphTitle = '(Theory) Count of tasks completed by students'
        try: 
            studentWiseDataOriginalTaskPerformedTheory = groupOriginalTheory
            studentWiseDataOriginalTaskPerformedTheory = studentWiseDataOriginalTaskPerformedTheory.merge(right= dfTheoryTaskDetails
                                              , left_on='TheoryTaskId', right_on='TheoryTaskId'
                                                , left_index=False, right_index=False
                                                , how='inner')
            studentWiseDataOriginalTaskPerformedTheory[featureTaskDesc] = studentWiseDataOriginalTaskPerformedTheory['Title'] + ' (Id: ' + studentWiseDataOriginalTaskPerformedTheory['TheoryTaskId'].astype(str) + ')' 
            studentWiseDataOriginalTaskPerformedTheory = studentWiseDataOriginalTaskPerformedTheory [ studentWiseDataOriginalTaskPerformedTheory['Result'] == 1][['StudentId', 'TheoryTaskId'
                          , 'Result', 'Name', featureTaskDesc]].groupby(
                          ['StudentId', 'Name']).agg({'TheoryTaskId': ['nunique'], featureTaskDesc: ['unique']})
            studentWiseDataOriginalTaskPerformedTheory = studentWiseDataOriginalTaskPerformedTheory.reset_index()
            studentWiseDataOriginalTaskPerformedTheory.rename(columns={'TheoryTaskId': countTaskCompletedByStudentFeature}, inplace=True)
            studentWiseDataOriginalTaskPerformedTheory.columns = studentWiseDataOriginalTaskPerformedTheory.columns.droplevel(1)
            studentWiseDataOriginalTaskPerformedTheory[featureTaskDesc] = studentWiseDataOriginalTaskPerformedTheory[featureTaskDesc].apply(convert_list_column_tostr_NL)
            studentWiseDataOriginalTaskPerformedTheory[featureTaskType] = TaskTypeTheory
            
            
#            combinedDataframeTaskCount = pd.concat([studentWiseDataOriginalTaskPerformed, studentWiseDataOriginalTaskPerformedTheory], ignore_index=True)
            figStudents = px.bar( studentWiseDataOriginalTaskPerformedTheory
                                , x             =  countTaskCompletedByStudentFeature
                                , y             =  'Name'
                                , title         = graphTitle
                                , labels        = feature2UserNamesDict # customize axis label
#                                , height        = constants.graphHeight
                                , template      = constants.graphTemplete                              
                                , orientation   = 'h'
                                , hover_data    = [featureTaskDesc]
#                                , color         = 'TaskType'
#                                , barmode       = 'group'
            )
            graphs.append(
                    dcc.Graph(
                        id='graphSchool-' + str(graphIndex),
                        figure= figStudents
                ))
            graphIndex = graphIndex + 1
            
            
        except Exception as e: 
            print( 'ERROR - ' + graphTitle )  
            print(e)
        
        

    except Exception as e: 
        print( 'ERROR - plotSingleClass ')  
        print(e)


    return graphs        



    
#-------------------------------------------------
#GENERAL INFORMATION SECTION
#------------------------------------------------------

#        CHECKED
#            for concepts used
featureX = 'Count (no. of times used)'
featureY = 'Details'
featurePracticeTaskGroup = 'Task-Id'            

def plotGroupTaskWiseConcepts(groupId, isGrouped = True) :
    
    graphs = []
    
    try :
        taskWiseConceptPracticeGrouped = dfGroupedPracticeTaskWise.get_group(groupId).groupby(['PracticeTaskId'])
        
        studentWiseTaskWiseConceptPractice = pd.DataFrame()    
        
        
        for groupKeyTaskId, groupTask in taskWiseConceptPracticeGrouped:
            
            studentWiseDataConceptsTask = groupTask.sum()
            
            colY = hasFeatures
           
            studentWiseDataConceptsTask = pd.DataFrame(studentWiseDataConceptsTask)
            studentWiseDataConceptsTask['PracticeTaskId'] = groupKeyTaskId
            studentWiseDataConceptsTask['Title'] = dfPracticeTaskDetails[ dfPracticeTaskDetails['PracticeTaskId'] == int(groupKeyTaskId) ]['Title'].astype(str).values[0]
            studentWiseDataConceptsTask[featurePracticeTaskGroup] = constants.TaskTypePractice + '-' + str(groupKeyTaskId)
            studentWiseDataConceptsTask[featureY] = studentWiseDataConceptsTask.index
            studentWiseDataConceptsTask = studentWiseDataConceptsTask.rename(columns={0: featureX})
            studentWiseDataConceptsTask.drop(studentWiseDataConceptsTask[~studentWiseDataConceptsTask[featureY].isin(colY)].index, inplace = True)
            
            studentWiseDataConceptsTask[featureY] = studentWiseDataConceptsTask[featureY].astype(str)
            studentWiseDataConceptsTask[featureY] = studentWiseDataConceptsTask[featureY].replace(
                    feature2UserNamesDict, regex=True)
            
            if studentWiseTaskWiseConceptPractice is None or studentWiseTaskWiseConceptPractice.empty:
                studentWiseTaskWiseConceptPractice = studentWiseDataConceptsTask
            else:
                studentWiseTaskWiseConceptPractice = pd.concat([studentWiseTaskWiseConceptPractice, studentWiseDataConceptsTask], ignore_index=True)


            taskTitle = str(groupKeyTaskId)
            try :
                taskTitle =  dfPracticeTaskDetails[ dfPracticeTaskDetails['PracticeTaskId'] == int(groupKeyTaskId) ]['Title'].astype(str).values[0]
            except Exception as e: 
                print(e)
                
            figBar = px.bar(studentWiseDataConceptsTask
                                , x             =   featureX
                                , y             =   featureY
                                , orientation   =  'h'
                                , height        =   constants.graphHeight - 100
                                , template      =   constants.graphTemplete   
                                , title         =   "(Practice) Concepts used by students in task " + str(groupKeyTaskId) + '(TaskId)'+ "<br>" + str(taskTitle)  +   " (no. of times students used a concept in code)"
                                , labels        =   feature2UserNamesDict # customize axis label
                )
            graphs.append(
                    dcc.Graph(
                        figure= figBar
                )) 
        
        if isGrouped:
            figGroupedTaskConcepts = px.bar(studentWiseTaskWiseConceptPractice
                                , x             =   featureY
                                , y             =   featureX
                                , height        =   constants.graphHeight - 100
                                , hover_data  =  [ 'Title', 'PracticeTaskId',  ]
                                , template      =   constants.graphTemplete   
                                , title         =   "(Practice) Concepts used by students in each task <br> (no. of times students used a concept in code for a task)"
                                , labels        =   feature2UserNamesDict # customize axis label
                                , color         =   featurePracticeTaskGroup
                                , barmode       =   'group'
                )
            return figGroupedTaskConcepts
                
        return graphs
    except Exception as e: 
        print(e)               


def plotGroupConceptDetails(groupId):
    
    graphs = []
    
      
    try :
        groupPractice = dfGroupedPractice.get_group(groupId)
        
    #        sum - to get count of students who used the concept
        studentWiseDataConcepts = groupPractice.sum()
               
        colY = hasFeatures
       
        studentWiseDataConcepts = pd.DataFrame(studentWiseDataConcepts)
        studentWiseDataConcepts[featureY] = studentWiseDataConcepts.index
        studentWiseDataConcepts = studentWiseDataConcepts.rename(columns={0: featureX})
        studentWiseDataConcepts.drop(studentWiseDataConcepts[~studentWiseDataConcepts[featureY].isin(colY)].index, inplace = True)
        
        studentWiseDataConcepts[featureY] = studentWiseDataConcepts[featureY].astype(str)
        studentWiseDataConcepts[featureY] = studentWiseDataConcepts[featureY].replace(
                feature2UserNamesDict, regex=True)
        
        
        figBar = px.bar(studentWiseDataConcepts
                            , x             =   featureX
                            , y             =   featureY
                            , orientation   =  'h'
                            , height        =   constants.graphHeight - 100
                            , template      =   constants.graphTemplete   
                            , title         =   "(Practice) Concepts used by students of this class (no. of times students used a concept in code)"
                            , labels        =   feature2UserNamesDict # customize axis label
            )
        graphs.append(
                dcc.Graph(
                    figure= figBar
            ))
        
#        Task wise concepts used - grouped together
        try :
            figBar = plotGroupTaskWiseConcepts(groupId, True)
            graphs.append(
                    dcc.Graph(
                        figure= figBar
                ))

            graphs.append(  html.Div([
                    dbc.Button(
                        "Show Task Wise Concept Used",
                        id          = "collapse-taskwise-concept-button",
                        color       = "primary",
                        n_clicks    = 0
                    ),
                    dbc.Tooltip(
                        "Click to View/Hide",
                        target      = "collapse-taskwise-concept-button",
                        style       = { 'font-size' : 'initial'  }
                    ),
                    dbc.Collapse(
                        children = [] ,
                        id = "collapse-taskwise-concept",
                        is_open = False
                    ),
                ] ,
                className = "c-container"
            ))
            
        except Exception as e: 
                print('Task Concepts used')
                print(e)                
      
    except Exception as e: 
            print(e)  
            
    return graphs        


def plotSingleClassGeneral( titleTextAdd, school ):
    
    graphs = []
    
      
    featuresPractice            = dfPlayerStrategyPractice.columns
                             
    
        
    try :
        groupPractice = dfGroupedPractice.get_group(school)
        groupOriginal = dfGroupedOriginal.get_group(school)
        
        try :
            groupOriginalTheory = dfGroupedPlayerStrategyTheory.get_group(school)
        except Exception as e: 
            print(e)
        
        
        #            2. other features    
        #   Combined Plots         
        
#              Practice Data
        studentWiseData = groupPractice.groupby(['StudentId'], as_index=False).sum()
        
        studentWiseData = studentWiseData.merge(right= dfPlayerStrategyPractice[['StudentId', "Result", 'ConceptsUsed', 'ConceptsUsedDetails', 'Name', "lineOfCodeCount", "Code"]]
                                                , left_index=False, right_index=False
                                                , how='inner')
        
        studentWiseData['ConceptsUsedDetailsStr']= studentWiseData['ConceptsUsedDetails'].apply(lambda x: x[1:-1])
        studentWiseData.reset_index(drop=True, inplace=True)
        
        studentWiseData[countTaskCompletedByStudentFeature] = studentWiseData['Result']
        
        del studentWiseData['Attempts']
        del studentWiseData['SessionDuration']
        del studentWiseData['Result']
        
        studentWiseDataOriginal = groupOriginal.groupby(['StudentId'], as_index=False).sum()
        studentWiseData = studentWiseData.merge(right= studentWiseDataOriginal[['StudentId', "Attempts", 'SessionDuration', 'Result']]
                                                , left_on='StudentId', right_on='StudentId'
                                                , left_index=False, right_index=False
                                                , how='inner')  
        
        
        studentWiseData[featureDescription] = getPracticeDescription(studentWiseData)
        studentWiseData[constants.featureTaskType] = constants.TaskTypePractice
        
        
        
        try :
            studentWiseDataTheory =  groupOriginalTheory.groupby(['StudentId'], as_index=False).sum()
            studentWiseDataTheory.reset_index(drop=True, inplace=True)
            
            studentWiseDataTheory[countTaskCompletedByStudentFeature] = studentWiseDataTheory['Result']
            
            studentWiseDataTheory = studentWiseDataTheory.merge(right= dfStudentDetails[['StudentId', 'Name']]
                                            , left_on='StudentId', right_on='StudentId'
                                            , left_index=False, right_index=False
                                            , how='inner')
            
#            if need to add a MEAN column values
#            studentWiseDataTheoryMean =  groupOriginalTheory.groupby(['StudentId'], as_index=False).sum()
#            studentWiseDataTheory['Attempts'] = studentWiseDataTheory['StudentId'].map(studentWiseDataTheoryMean.set_index('StudentId')['Attempts'])
            
            studentWiseDataTheory[featureDescription] = getTheoryDescription(studentWiseDataTheory)
            studentWiseDataTheory[constants.featureTaskType] = constants.TaskTypeTheory
            
        except Exception as e: 
                print(e)
        
    #            2. other features        
    
        hoverDataPractice   = ["SessionDuration", "Points", "Attempts", "Result", "CollectedCoins", "robotCollisionsBoxCount", "ConceptsUsedDetailsStr", "lineOfCodeCount", 'StudentId']
        hoverDataTheory     = ["SessionDuration", "Points", "Attempts", "Result", "itemsCollectedCount", "playerShootEndEnemyHitCount", 'StudentId']
                                          
        for first in range(featuresPractice.size):
                
            for second in  range(featuresPractice.size):
                if ([featuresPractice[first], featuresPractice[second]] in featurePairsToPlotSingle):                
            
                    if featuresPractice[first] != featuresPractice[second] :            
    
    #                           for setting title        
                        titleFirst = featuresPractice[first]
                        if featuresPractice[first] in feature2UserNamesDict:
                            titleFirst = feature2UserNamesDict.get(featuresPractice[first])
                        
                        #    Graphs for both THEORY & PRACTICE                        
                        if ([featuresPractice[first], featuresPractice[second]] in  featurePairsToPlotTheory):  
                            
                            
                            fig = px.bar( studentWiseData
                                , x             =  featuresPractice[first]
                                , y             =  featuresPractice[second]
                                , title         = '(Practice) Details of students ' + titleFirst
                                , labels        = feature2UserNamesDict # customize axis label
                                , template      = constants.graphTemplete                              
                                , orientation   = 'h'
                                , hover_name    =  "Name"
                                , hover_data    =  hoverDataPractice
                                , marginal    =  "box" 
                            )
                            graphs.append(
                                    dcc.Graph(
                                        figure = fig
                                ))
                            
                            fig = px.bar( studentWiseDataTheory
                                , x             =  featuresPractice[first]
                                , y             =  featuresPractice[second]
                                , title         = '(Theory) Details of students ' + titleFirst
                                , labels        = feature2UserNamesDict # customize axis label
                                , template      = constants.graphTemplete                              
                                , orientation   = 'h'
                                , hover_name    =  "Name"
                                , hover_data    =  hoverDataTheory
                                , color         = constants.featureTaskType
                                , color_discrete_sequence = [constants.colorTheory]
                                , marginal    =  "box" 
                            )                                                       
                            graphs.append(
                                    dcc.Graph(
                                        figure = fig
                                ))
                         
#    Graphs only for PRACTICE
                        if ([featuresPractice[first], featuresPractice[second]] not in  featurePairsToPlotTheory):     
                            fig = px.bar( studentWiseData
                                , x             =  featuresPractice[first]
                                , y             =  featuresPractice[second]
                                , title         = '(Practice) Details of students ' + titleFirst
                                , labels        = feature2UserNamesDict # customize axis label
                                , template      = constants.graphTemplete                              
                                , orientation   = 'h'
                                , hover_name  =  "Name"
                                , hover_data  =  hoverDataPractice
                                , marginal    =  "box" 
                            )
                            graphs.append(
                                    dcc.Graph(
                                        figure = fig
                                ))
    
#    Graphs only for THEORY
        for rowTheory in featurePairsToPlotTheory : 
            if (rowTheory not in featurePairsToPlotSingle) :
    
                try :
                #                           for setting title  
                    titleFirst = rowTheory[0]
                    if rowTheory[0] in feature2UserNamesDict:
                        titleFirst = feature2UserNamesDict.get(rowTheory[0])
                    
                    fig = px.bar( studentWiseDataTheory
                                , x             =  rowTheory[0]
                                , y             =  rowTheory[1] 
                                , title         = '(Theory) Details of students ' + titleFirst
                                , labels        = feature2UserNamesDict # customize axis label
                                , template      = constants.graphTemplete                              
                                , orientation   = 'h'
                                , hover_name  =  "Name"
                                , hover_data   =  hoverDataTheory
                                , color         = constants.featureTaskType
                                , color_discrete_sequence = [constants.colorTheory]
                                , marginal_x    =  "box" 
                            )
                    graphs.append(
                            dcc.Graph(
                                figure = fig
                        ))
                except Exception as e: 
                    print(e)


    except Exception as e: 
        print(e)


    return graphs        



#Student Interaction with Game - TIMELINE
def plotClassOverview(schoolKey):
    
    graphs = []
    rows = []
    columns = []

    features2Plot = ['Name', 'SessionDuration', 'PracticeSessionDuration', 'TheorySessionDuration', 
                     'Attempts', 'Points' 
                     ]
        
    studentDataDf = studentGrouped.getStudentsOfSchoolDF(schoolKey)
    studentDataDfSum = studentDataDf.groupby(['StudentId', 'Name'], as_index=False).sum()
    
    studentDataDfSumTask = studentDataDf.groupby(['StudentId', 'Name', constants.TASK_TYPE_FEATURE
                                               ], as_index=False)

    studentDataDfFeaturesInterpreted = pd.DataFrame(columns = ['StudentId', 'PracticeSessionDuration', 'TheorySessionDuration']) 
    for groupKey, group in studentDataDfSumTask :        
        practiceSessionDuration = group[group[constants.TASK_TYPE_FEATURE] ==  constants.TaskTypePractice ]['SessionDuration'].sum()        
        theorySessionDuration =  group[group[constants.TASK_TYPE_FEATURE] == constants.TaskTypeTheory ]['SessionDuration'].sum()            
        studentDataDfFeaturesInterpreted = studentDataDfFeaturesInterpreted.append({'StudentId' : groupKey[0], 
                                                                                    'PracticeSessionDuration' : practiceSessionDuration, 
                                                                                    'TheorySessionDuration' : theorySessionDuration},  
                                                                            ignore_index = True)       
    studentDataDfFeaturesInterpreted = studentDataDfFeaturesInterpreted.groupby(['StudentId'],  as_index=False).sum()
        
    studentDataDfSum = studentDataDfSum.merge(right= studentDataDfFeaturesInterpreted
                                      , left_on='StudentId', right_on='StudentId'
                                        , left_index=False, right_index=False
                                        , how='inner')
    
    rows.append( dbc.Row( html.Div([
                html.H3('Overview'), 
            ]) ) )
    fig1Table = dash_table.DataTable(
        columns=[
            {"name": constants.feature2UserNamesDict.get(i) if i in constants.feature2UserNamesDict.keys() else i , "id": i, "deletable": True, "selectable": True} for i in studentDataDfSum[features2Plot].columns
        ],
        data            = studentDataDfSum[features2Plot].to_dict('records'),
        editable        = True,
        filter_action       = "native",
        sort_action         = "native",
        sort_mode           = "multi",
        style_data_conditional=([
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
         ] 
        ),
        style_header = constants.THEME_TABLE_HEADER_STYLE
    )
    columns.append(dbc.Col(
                    fig1Table , align="center"
    ))
    rows.append( dbc.Row( columns ) )
    
#    ---------------------------------------------
        
    
    graphs.append(html.Div(  rows  ))
    
    return graphs



#-----------------------------------------
# Layout-------------------------
#-------------------------------------------

layout = [
        html.Div([
                   
    html.Div(id='Details-Group-Overview-Container')
    , dbc.Row([
            dbc.Col( 
                    html.A(children=[html.I(className="fas fa-download font-size_medium p_small"),
                       "download data : Group",], id = "details_download_group_overview_link", className = "hidden" ,
                                               href="", target="_blank",
                                               download='group-overview.csv' )
      )])
    
    , dbc.Row([
            dbc.Col( 
                    html.Div(id='Details-Group-Container')
        )])
    
    
    , dbc.Row([
            dbc.Col( 
                    html.Div(id='Concept-Information',
                               children = [
                                           html.H3('Concept Used'),
                                           ], 
                   className = "c-container p_medium p-top_xx-large", )
       )])
    , dbc.Row([
            dbc.Col( 
                html.Div(id='Details-Group-Concept-Container')
       )])
    
    , dbc.Row([
            dbc.Col( 
                    html.Div(id='General-Information',
                               children = [
                                           html.H3('General Information'),
                                           ], 
                   className = "c-container p_medium p-top_xx-large", )
       )])
    , dbc.Row([
            dbc.Col( 
                html.Div(id='Details-Group-General-Container')
       )])
    
    
    ])    
]


#-----------------------------------------
# callback functions---------------------
#        ---------------------------------
@app.callback(Output('Details-Group-Container', 'children'), [Input('group-selector-main', 'value')])
def display_graphs(schoolSelected):
    graphs = []
    
    if schoolSelected is None or not int(schoolSelected) >= 0 :
        return html.Div(graphs)
    
#    graphs = plotSingleClass('School', format(schoolSelected) )
    graphs = plotSingleClass('School', int(schoolSelected) )
    
    return html.Div(graphs)


@app.callback(Output('Details-Group-General-Container', 'children'), [Input('group-selector-main', 'value')])
def display_class_general(schoolSelected):
    graphs = []
    
    if schoolSelected is None or not int(schoolSelected) >= 0 :
        return html.Div(graphs)
    
#    graphs = plotSingleClass('School', format(schoolSelected) )
    graphs = plotSingleClassGeneral('School', int(schoolSelected) )
    
    return html.Div(graphs)


@app.callback(Output('Details-Group-Concept-Container', 'children'), [Input('group-selector-main', 'value')])
def display_class_concept(schoolSelected):
    graphs = []
    
    if schoolSelected is None or not int(schoolSelected) >= 0 :
        return html.Div(graphs)
    
    graphs = plotGroupConceptDetails(int(schoolSelected) )
    
    return html.Div(graphs)
#----------------------------------------

@app.callback(Output('Details-Group-Overview-Container', 'children'), [Input('group-selector-main', 'value')])
def setClassOverview(schoolSelected):
    graphs = []

    if schoolSelected is None or not int(schoolSelected) >= 0:
        return html.Div(graphs)
    
    graphs = plotClassOverview( int(schoolSelected) )    

    return  html.Div(graphs)
    

@app.callback(
    [Output("collapse-taskwise-concept", "is_open") , 
     Output("collapse-taskwise-concept", "children"),
     ],
    [Input("collapse-taskwise-concept-button", "n_clicks")],
    [State("collapse-taskwise-concept", "is_open"),
     State('group-selector-main', 'value'),
     State('collapse-taskwise-concept', 'children'),
     ],
)
def show_taskwise_concept(n, is_open, groupSelected, collapseCurrentChildren):
    
    print('taskwise concepts collapseCurrentChildren')
    graphs = []
    
    if n  and groupSelected is not None and int(groupSelected) >= 0:
        
        if isinstance(collapseCurrentChildren, list):
            graphs = plotGroupTaskWiseConcepts( int(groupSelected), isGrouped = False )  
            graphs = graphs 
        elif isinstance(collapseCurrentChildren, dict) and 'props' in collapseCurrentChildren.keys():
                graphs = graphs + collapseCurrentChildren.get('props').get('children')
                
        
        return not is_open,  html.Div(graphs)
    
    return is_open, graphs







#--------------------- data download callbacks 
@app.callback(
    [ Output('details_download_group_overview_link', 'href'),
     Output('details_download_group_overview_link', 'className'),
     ],
    [ Input("group-selector-main", "value"), ])
def update_download_link__details_group(groupMain):
    if groupMain is None or not int(groupMain) >= 0 or groupMain == "":
        return "", "hidden"
    
    csv_string = util.get_download_link_data_uri( studentGrouped.getStudentsOfSchoolDF(int(groupMain)) )
    return csv_string, ""