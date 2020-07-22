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

import pandas as pd
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
                               children = [], 
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
                data                = dfTaskWiseSuccessFail.to_dict('records'),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi"
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
            
            
            combinedDataframeTaskCount = pd.concat([studentWiseDataOriginalTaskPerformed, studentWiseDataOriginalTaskPerformedTheory], ignore_index=True)
            figStudents = px.bar( combinedDataframeTaskCount
                                , x             =  countTaskCompletedByStudentFeature
                                , y             =  'Name'
                                , title         = 'Count of tasks completed by students '
                                , labels        = feature2UserNamesDict # customize axis label
                                , height        = constants.graphHeight
                                , template      = constants.graphTemplete                              
                                , orientation   = 'h'
                                , hover_data    = [featureTaskDesc]
                                , color         = 'TaskType'
                                , barmode       = 'group'
            )
            graphs.append(
                    dcc.Graph(
                        id='graphSchool-' + str(graphIndex),
                        figure= figStudents
                ))
            graphIndex = graphIndex + 1
            
            
        except Exception as e: 
            figStudents = px.bar( studentWiseDataOriginalTaskPerformed
                                , x             = countTaskCompletedByStudentFeature
                                , y             = 'Name'
                                , title         = '(Practice) Count of tasks completed by students '
                                , labels        = feature2UserNamesDict # customize axis label
                                , height        = constants.graphHeight
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
            print(e)
        
        

    except Exception as e: 
        print(e)


    return graphs        



    
#-------------------------------------------------
#GENERAL INFORMATION SECTION
#------------------------------------------------------
def plotSingleClassGeneral( titleTextAdd, school ):
    
    graphIndex = 1
    graphs = []
    
      
    featuresPractice            = dfPlayerStrategyPractice.columns
                             
    
        
    try :
        groupPractice = dfGroupedPractice.get_group(school)
        groupOriginal = dfGroupedOriginal.get_group(school)
        
        try :
            groupOriginalTheory = dfGroupedPlayerStrategyTheory.get_group(school)
        except Exception as e: 
            print(e)
        
#        CHECKED
    #            for concepts used
        featureX = 'Count (no. of times used)'
        featureY = 'Details'
        
        
        
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
                            , x             =   studentWiseDataConcepts[featureX]
                            , y             =   studentWiseDataConcepts[featureY]
                            , orientation   =  'h'
                            , height        =   constants.graphHeight - 100
                            , template      =   constants.graphTemplete   
                            , title         =   "(Practice) Concepts used by students of this class (no. of times students used a concept in code)"
                            , labels        =   feature2UserNamesDict # customize axis label
            )
        graphs.append(
                dcc.Graph(
                    id='graphSchool-' + str(graphIndex),
                    figure= figBar
            ))
        graphIndex = graphIndex + 1
        
        
        
        taskWiseConceptPracticeGrouped = dfGroupedPracticeTaskWise.get_group(school).groupby(['PracticeTaskId'])
                
        for groupKeyTaskId, groupTask in taskWiseConceptPracticeGrouped:
            
            
            taskTitle = str(groupKeyTaskId)
            try :
                taskTitle =  '(' + str(groupKeyTaskId) + ') ' +  dfPracticeTaskDetails[ dfPracticeTaskDetails['PracticeTaskId'] == int(groupKeyTaskId) ]['Title'].astype(str).values[0]
            except Exception as e: 
                print(e)
            
            studentWiseDataConceptsTask = groupTask.sum()
                   
            colY = hasFeatures
           
            studentWiseDataConceptsTask = pd.DataFrame(studentWiseDataConceptsTask)
            studentWiseDataConceptsTask[featureY] = studentWiseDataConceptsTask.index
            studentWiseDataConceptsTask = studentWiseDataConceptsTask.rename(columns={0: featureX})
            studentWiseDataConceptsTask.drop(studentWiseDataConceptsTask[~studentWiseDataConceptsTask[featureY].isin(colY)].index, inplace = True)
            
            studentWiseDataConceptsTask[featureY] = studentWiseDataConceptsTask[featureY].astype(str)
            studentWiseDataConceptsTask[featureY] = studentWiseDataConceptsTask[featureY].replace(
                    feature2UserNamesDict, regex=True)
            
            
            figBar = px.bar(studentWiseDataConceptsTask
                                , x             =   studentWiseDataConceptsTask[featureX]
                                , y             =   studentWiseDataConceptsTask[featureY]
                                , orientation   =  'h'
                                , height        =   constants.graphHeight - 100
                                , template      =   constants.graphTemplete   
                                , title         =   "(Practice) Concepts used by students in task " + str(taskTitle)  +   " (no. of times students used a concept in code)"
                                , labels        =   feature2UserNamesDict # customize axis label
                )
            graphs.append(
                    dcc.Graph(
                        id='graphSchool-' + str(graphIndex),
                        figure= figBar
                ))
            graphIndex = graphIndex + 1
        
        
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
            
        except Exception as e: 
                print(e)
        
    #            2. other features        
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

                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                 x              = studentWiseData[featuresPractice[first]] , y = studentWiseData[featuresPractice[second]] ,
                                name            = 'Practice',
                                text            = studentWiseData[featureDescription],
                                marker_color    = 'rgba(152, 0, 0, .8)',
                                marker_size     = 22
                            ))
                            fig.add_trace(go.Scatter(
                                x               = studentWiseDataTheory[featuresPractice[first]] , y = studentWiseDataTheory[featuresPractice[second]] ,
                                name            =  'Theory',
                                text            = studentWiseDataTheory[featureDescription],
                                marker_color    = 'rgb(73, 29, 29)',
                                marker_size     = 16
                            ))
                            fig.update_traces(mode='markers', 
                                    marker = dict(
                                        showscale = False
                            ))
                            fig.update_layout(
                                        height          =   constants.graphHeight, 
                                        title_text      = 'Details of students ' + titleFirst
                                             , yaxis = dict(
                                                title = featuresPractice[second],
                                                titlefont_size = 16,
                                                tickfont_size = 14,
                                            ), xaxis = dict(
                                                title = featuresPractice[first],
                                                titlefont_size = 16,
                                                tickfont_size = 14,
                            ))
                            
                            fig.update_yaxes(automargin=True)
                            
                            fig.update_yaxes(automargin=True)
                            
                            graphs.append(
                                    dcc.Graph(
                                        id='graphSchool-' + str(graphIndex),
                                        figure = fig
                                ))
                            graphIndex = graphIndex + 1

                         
#    Graphs only for PRACTICE
                        if ([featuresPractice[first], featuresPractice[second]] not in  featurePairsToPlotTheory):     
                            figStudents = px.scatter(studentWiseData, x=featuresPractice[first], y=featuresPractice[second] 
                                 , title  = ' (Practice)  Details of students ' + titleFirst
                                 , labels  =  feature2UserNamesDict # customize axis label
                                 , hover_name  =  "Name"
                                 , hover_data  =  ["CollectedCoins", "Result", "SessionDuration", "Attempts", "robotCollisionsBoxCount", "Points", "ConceptsUsedDetailsStr", "lineOfCodeCount", 'StudentId']
                                 , height       = constants.graphHeight
#                                 , color        = "StudentId" 
#                                 , color_continuous_scale=px.colors.sequential.Rainbow
                                 , template     = constants.graphTemplete
                                )
                            figStudents.update_traces(marker=dict(size = 16
                                                        , showscale    = False
                                                        ,  line = dict(width=1,
                                                                    color='DarkSlateGrey')),
                                              selector=dict(mode='markers'))
                            
                            
                            graphs.append(
                                    dcc.Graph(
                                        id='graphSchool-' + str(graphIndex),
                                        figure= figStudents
                                ))            
                            graphIndex = graphIndex + 1
    
    
    
#    Graphs only for THEORY
        for rowTheory in featurePairsToPlotTheory : 
            if (rowTheory not in featurePairsToPlotSingle) :
    
                try :
                #                           for setting title  
                    titleFirst = rowTheory[0]
                    if rowTheory[0] in feature2UserNamesDict:
                        titleFirst = feature2UserNamesDict.get(rowTheory[0])
    
                    figStudents = px.scatter ( studentWiseDataTheory, x = rowTheory[0], y = rowTheory[1] 
                                         , title        = ' (Theory) Details of students ' + titleFirst
                                         , labels       =  feature2UserNamesDict # customize axis label
                                         , hover_name   =  "Name"
                                         , hover_data   =  ["Points", "Result", "SessionDuration", "Attempts", "Points", "itemsCollectedCount", "playerShootEndEnemyHitCount", 'StudentId']
                                         , height       = constants.graphHeight
#                                         , color        = "StudentId" 
#                                         , color_continuous_scale   = px.colors.sequential.Rainbow
                                         , template     = constants.graphTemplete
                                        )
                    figStudents.update_traces(marker=dict(size = 16
                                                        , showscale    = False
                                                        ,  line = dict(width=1,
                                                                    color='DarkSlateGrey')),
                                              selector=dict(mode='markers'))
                    graphs.append(
                            dcc.Graph(
                                id='graphSchool-' + str(graphIndex),
                                figure= figStudents
                        ))
                    graphIndex = graphIndex + 1
                except Exception as e: 
                    print(e)


    except Exception as e: 
        print(e)


    return graphs        


#Student Interaction with Game - TIMELINE
def plotStudent(StudentId, schoolKey):
    
    graphs = []
    graphIndex = 1
    

    school              = dfGroupedOriginal.get_group(schoolKey)
    school              = school[school['StudentId'] == StudentId]
    school['Start']     = school['CreatedAt']
    school['Finish']    = school['CreatedAt'] + pd.to_timedelta(school['SessionDuration'], unit='s')
    
    
    codes = dfRuns[dfRuns['StudentId'].isin(school['StudentId']) & dfRuns['PracticeStatisticsId'].isin(school['PracticeStatisticsId']) ]
        
    codes = codes.merge(right= dfPracticeTaskDetails
                                      , left_on='PracticeTaskId', right_on='PracticeTaskId'
                                        , left_index=False, right_index=False
                                        , how='inner')
    codes.rename(columns = {'Description': 'PracticeTaskDescription'}, inplace = True)
    
    codes['RunsTime'] = pd.to_datetime(codes['RunsTime'])
    
    #codes['Finish'] = codes['RunsTime'].shift(-1)
    codes['Start'] = codes['RunsTime']
    codes['Start'] = pd.to_datetime(codes['Start'])
    codes['Task'] =  'Practice-' + codes['PracticeTaskId'].astype(str)
    codes['Code'] =  codes['RunsCode']
    codes['Finish'] = codes.groupby('PracticeStatisticsId')['Start'].shift(-1)
    
    codes['IndexCol'] = 'Practice-' + codes['PracticeTaskId'].astype(str) + '-(Runs Code Error:' + codes['RunsError'].astype(int).astype(str) + ')'
    
    codes['Description'] = '<b>Runs code</b>'
    codes['Description'] = codes['Description'] + '<br><b>Title</b>:' + codes['Title'].astype(str) + '<br><b>Code</b> : ' +  codes['Code'].astype(str)
    codes['Description'] = codes['Description'] + '<br><b>Has Error</b>: ' + codes['RunsError'].astype(int).astype(str)
    
    

    codes = pd.concat([codes, school[['PracticeTaskId', 'StudentId', 'PracticeStatisticsId', 'Finish', 'Start', 'Result', 'Code', 'Title']]], ignore_index=True, sort =False)
    
    codes = codes.sort_values(by='Start')
    
    
    codes['Finish'] = np.where(codes['Finish'].isnull(), codes['Start'].shift(-1), codes['Finish'])
    
    
    codes['Difference'] = (codes['Finish'] - codes['Start']).astype('timedelta64[s]')
        
    codes['IndexCol'] = np.where(   codes['IndexCol'].isnull()  , ( 'Practice-' + codes['PracticeTaskId'].astype(str) + '-' + codes['Result'].astype('Int64').astype(str) )  ,   codes['IndexCol']  ) 
    
    
    codes['Description2'] = '<b>Title</b>:' + codes['Title'].astype(str) + '<br><b>Code</b> : ' +  codes['Code'].astype(str)
    codes['Description2'] = codes['Description2'] + '<br><b>Result</b>: ' + codes['Result'].astype('Int64').astype(str)
    
    
    codes['Description'] = np.where(codes['Description'].isnull(), codes['Description2'], codes['Description'])
    
    codes['Description'] = codes['Description'] + '<br><b>Duration</b>: ' + codes['Difference'].astype(str) + ' s '
    
    
    studentData         = codes
    

    try :
        schoolTheory = dfGroupedPlayerStrategyTheory.get_group(schoolKey)
        schoolTheoryStudent = schoolTheory[schoolTheory['StudentId'] == StudentId]
        
        schoolTheoryStudent['Start']   =   schoolTheoryStudent['CreatedAt']
        schoolTheoryStudent            =   schoolTheoryStudent.sort_values(by='Start')
        schoolTheoryStudent['Finish'] = schoolTheoryStudent.groupby([schoolTheoryStudent['Start'].dt.date , 'StudentId'])['Start'].shift(-1)
        
        schoolTheoryStudent.loc[schoolTheoryStudent['Finish'].isna(), 'Finish'] = schoolTheoryStudent[schoolTheoryStudent['Finish'].isna()][
                'Start'] + pd.to_timedelta(schoolTheoryStudent[schoolTheoryStudent['Finish'].isna()]['SessionDuration'], unit='s')
        
        
        
        schoolTheoryStudent['Difference'] = (schoolTheoryStudent['Finish'] - schoolTheoryStudent['Start']).astype('timedelta64[s]')
        
        schoolTheoryStudent.loc[schoolTheoryStudent['Difference'] > schoolTheoryStudent['SessionDuration'], 'Difference'] =  schoolTheoryStudent[
                schoolTheoryStudent['Difference'] > schoolTheoryStudent['SessionDuration'] ]['SessionDuration']
        schoolTheoryStudent['Finish'] =  schoolTheoryStudent['Start'] + pd.to_timedelta(schoolTheoryStudent['Difference'], unit='s')
        
#        schoolTheoryStudent['Finish'] = np.where(   schoolTheoryStudent['Difference'] == 0  , ( schoolTheoryStudent['Finish'] + pd.to_timedelta(10, unit='s') )  ,   schoolTheoryStudent['Finish']  )
        
        
        schoolTheoryStudent = schoolTheoryStudent.merge(right= dfTheoryTaskDetails[ ['TheoryTaskId', 'Title', 'Description' ] ]
                                          , left_on='TheoryTaskId', right_on='TheoryTaskId'
                                            , left_index=False, right_index=False
                                            , how='inner')
        schoolTheoryStudent.rename(columns={'Description': 'TheoryTaskDescription'}, inplace=True)
        schoolTheoryStudent['Task'] = 'Theory-' + schoolTheoryStudent['TheoryTaskId'].astype(str) 
        
        schoolTheoryStudent['Description'] = '<b>Title</b>:' + schoolTheoryStudent['Title'].astype(str) + '<br><b>Solution</b>: ' +  schoolTheoryStudent['Solution'].astype(str)
        schoolTheoryStudent['Description'] = schoolTheoryStudent['Description'] + '<br><b>Result</b> : '+ schoolTheoryStudent['Result'].astype(str)
        schoolTheoryStudent['Description'] = schoolTheoryStudent['Description'] + '<br><b>Duration</b>: ' + schoolTheoryStudent['Difference'].astype(str) + ' s '
        
        
        schoolTheoryStudent['IndexCol'] = 'Theory-' + schoolTheoryStudent['TheoryTaskId'].astype(str) + '-' + schoolTheoryStudent['Result'].astype(str)
    
        if schoolTheoryStudent.empty == False :
            studentData = pd.concat([studentData, schoolTheoryStudent], ignore_index=True)
    except Exception as e: 
        print(e)

        
    studentData                     = studentData.sort_values(by='Start')
    studentData['StartStr']         = '@' + studentData['Start'].astype(str) + '-' + studentData['IndexCol'].astype(str)
    
    studentData['color']                                            =   constants.colorError
    studentData.loc[studentData['Result']  == 1, 'color']           =   constants.colorSuccess
    studentData.loc[studentData['RunsError']  == False, 'color']    =   'rgb(51, 204, 255)'
    
    

#  do this here - finish should always less than equal to next start !!! error in 2019-08-26 Player5383        
#    studentData['Difference'] = (studentData['Finish'] - studentData['Start']).astype('timedelta64[s]')
#    
#    studentData.loc[studentData['Difference'] > studentData['SessionDuration'], 'Difference'] =  studentData[
#            studentData['Difference'] > studentData['SessionDuration'] ]['SessionDuration']
#    studentData['Finish'] =  studentData['Start'] + pd.to_timedelta(studentData['Difference'], unit='s')
    
    
    
    graphHeightRows =  ( studentData.shape[0] * 30 )    
    graphHeightRows = graphHeightRows if (graphHeightRows > 500) else 500  
    
    #type 2 
    fig = go.Figure()
    fig.add_traces(go.Bar(
                    x               =  studentData['Difference'],
                    y               = studentData['StartStr'] ,
                    text            = studentData['Difference']    , 
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
    
    
    
    studentData['Task'] = studentData['IndexCol']
    fig = ff.create_gantt(studentData, title = 'Student Schedule' ,
                          show_colorbar = True , bar_width = 0.8 , showgrid_x = True , showgrid_y = True,
                          show_hover_fill = True , height =   graphHeightRows  )
    
    graphs.append(
            dcc.Graph(
                id='graphStudent-' + str(graphIndex),
                figure= fig
        ))
    graphIndex = graphIndex + 1
    
    
    
    return graphs




#Student Interaction with Game - TIMELINE
def plotClassOverview(schoolKey):
    
    
    colors = ['mediumturquoise', 'gold', 'darkorange', 'lightgreen']
    graphs = []
    rows = []
    columns = []
    
    
    students = getStudentsOfSchool(schoolKey)
        
    studentData = studentGrouped.getStudentsOfSchoolDF(schoolKey)
    
    
    fig1 = go.Figure(data=[go.Pie(labels=['No. of Students'],
                                 values=[  len(students)   ])])
    fig1.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    
    fig1.update_layout(
            height =  500
    )
    
    columns.append(dbc.Col(
                dcc.Graph(
                    figure= fig1
            ) , align="center")
    )
    
#    ---------------------------------------------
    parentsText = "<b>" + str(schoolKey) + "<br>No. of Students: " + str(len(students)) + "</b>"
    
    labels = [parentsText]
    labels = labels + dfStudentDetails[dfStudentDetails['StudentId'].isin( students)]['Name'].tolist()
    labels = [str(i) for i in labels]
    
    parents = [parentsText] * len(labels)
    parents[0] = ""
    
    fig2 = go.Figure(go.Sunburst(
        labels      =  labels,
        parents     =  parents,
        values      = [1] * len(labels),
    ))
    fig2.update_layout(
            height =  constants.graphHeight + 300
    )
    
    
    columns.append(dbc.Col(
                dcc.Graph(
                    figure= fig2
            ) , align="center")
    )
        
    rows.append( dbc.Row( columns ) )
    
    graphs.append(html.Div(  rows  ))
    
    return graphs



#-----------------------------------------
# Layout-------------------------
#-------------------------------------------

layout = [
        html.Div([
                
                
                         
#    html.Div([
#            dcc.Dropdown(
#                    id='SchoolSelector-Dropdown',                    
#                    options =  SchoolSelector_options,
##                    value  =   '2018-03-01' 
#                    )
#          ], 
#                    style = {'padding' : '20px',
#                             'font-size' : 'initial'}
#    )
#    
#    , 
    
    html.Div(id='Class-Overview-Container')
    
    
    , html.Div(id='Class-Container')
    
    
    
    , html.Div(id='General-Information',
                               children = [
                                           html.H3('General Information'),
                                           ], 
                    style = {'padding' : '20px',
                             'padding-top' : '100px',
                             'font-size' : 'initial'})
    , html.Div(id='Class-Container-General')
    
    
    
    , html.Div(id='Student-Information', children = [
            html.H3('Student Information'),
            ], 
                    style = {'padding' : '20px',
                             'font-size' : 'initial'})
    ,   html.Div([
            dcc.Dropdown(
                    id='StudentSelector-Dropdown' )
          ], 
                    style = {'padding' : '20px',
                             'font-size' : 'initial'}
    )
    
    
    , html.Div(id='Student-Container', 
                    style = {'padding-bottom' : '200px',
                             'font-size' : 'initial'})
                
                ])
        
        ]


#-----------------------------------------
# callback functions---------------------
#        ---------------------------------
@app.callback(Output('Class-Container', 'children'), [Input('group-selector-main', 'value')])
def display_graphs(schoolSelected):
    graphs = []
    
    if schoolSelected is None or not int(schoolSelected) >= 0 :
        return html.Div(graphs)
    
#    graphs = plotSingleClass('School', format(schoolSelected) )
    graphs = plotSingleClass('School', int(schoolSelected) )
    
    return html.Div(graphs)


@app.callback(Output('Class-Container-General', 'children'), [Input('group-selector-main', 'value')])
def display_class_general(schoolSelected):
    graphs = []
    
    if schoolSelected is None or not int(schoolSelected) >= 0 :
        return html.Div(graphs)
    
#    graphs = plotSingleClass('School', format(schoolSelected) )
    graphs = plotSingleClassGeneral('School', int(schoolSelected) )
    
    return html.Div(graphs)
#----------------------------------------


@app.callback(Output('StudentSelector-Dropdown', 'options'), [Input('group-selector-main', 'value')])
def setStudentOptions(schoolSelected):
        
    if schoolSelected is None or not int(schoolSelected) >= 0:
        return []
    
    students = getStudentsOfSchool(int(schoolSelected))
    
    return [{'label': row['Name'], 'value': row['StudentId'] } for index, row  in dfStudentDetails[dfStudentDetails['StudentId'].isin( students)][['StudentId', 'Name']].iterrows() ]



@app.callback(Output('Class-Overview-Container', 'children'), [Input('group-selector-main', 'value')])
def setClassOverview(schoolSelected):
    graphs = []

    if schoolSelected is None or not int(schoolSelected) >= 0:
        return html.Div(graphs)
    
#    graphs = plotClassOverview( format(schoolSelected) )    
    graphs = plotClassOverview( int(schoolSelected) )    

    return  html.Div(graphs)
    


@app.callback(Output('Student-Container', 'children'), [Input('StudentSelector-Dropdown', 'value')  , Input("group-selector-main", "value")   ])
def display_graphs_student(studentSelected, schoolSelected):
    graphs = []
    
    if schoolSelected is None or not int(schoolSelected) >= 0 or studentSelected is None or not int(studentSelected) >= 0:
        return html.Div(graphs)
    
    if ( studentSelected is not None ) and int( studentSelected ) >= 0 :
#    if ( studentSelected is not None ) and ( studentSelected in getStudentsOfSchool(schoolSelected) ) :
#        graphs = plotStudent( int( studentSelected ) , format(schoolSelected) )
        graphs = plotStudent( int( studentSelected ) , int(schoolSelected) )
    
    return html.Div(graphs)


@app.callback(
    Output("collapse-task", "is_open"),
    [Input("collapse-task-button", "n_clicks")],
    [State("collapse-task", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
