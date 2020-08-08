# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 13:51:24 2020

@author: Anil
"""


#import pyodbc
import numpy as np
import pandas as pd
import xlwt as xls_write
#import time

import plotly as plotly
from plotly.offline import plot 
import plotly.express as px

import dash
import dash_html_components as html

#main library
from data import main
import constants
#from main import PythonParser


#used for missing data fixes
#from sklearn.preprocessing import Imputer
#from sklearn.preprocessing import normalize
#from sklearn.preprocessing import StandardScaler

# visual libraries
from matplotlib import pyplot as plt
#import seaborn as sns
#from mpl_toolkits.mplot3d import Axes3D 
plt.style.use('ggplot')
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Fixing random state for reproducibility
np.random.seed(19680801)



featuresToInt = ['coinCollectedCount', 'keyboardKeyPressedCount', 'robotCollisionsBoxCount'
              , 'deletedCodesCount', 'tabsSwitchedCodeCount', 'tabsSwitchedDescriptionCount', 'tabsSwitchedCount'
              , 'draggedCount', 'runsHasVariableCount', 'runsHasConditionCount', 'runsHasNestedLoopCount'
              , 'runsHasLoopCount'
              , 'runsErrorAttribiteCount'
              , 'runsErrorTypeCount', 'runsErrorNameCount', 'runsErrorSyntaxCount'
              , 'runsSuccessCount', 'runsErrorCount', 'runsCount'
              , 'NumberOfBoxes', 'NumberOfCoins', 'NumberOfHidden', 'CollectedCoins'
              , 'lineOfCodeCount', 'runsLineOfCodeCountAvg'
              
              
              , 'runsHasExpressionsCount'
              , 'runsHasAsyncOrAwaitCount', 'runsHasFunctionClassCount'
              , 'runsHasControlFlowCount', 'runsHasImportsCount'
              , 'runsHasStatementsCount', 'runsHasComprehensionsCount'
              , 'runsHasSubscriptingCount'
              ]

                    
hasFeatures = ['hasLoop',
       'hasNestedLoop', 'hasCondition', 'hasVariable', 'hasExpressions',
       'hasAsyncOrAwait', 'hasFunctionClass', 'hasControlFlow', 'hasImports',
       'hasStatements', 'hasComprehensions', 'hasSubscripting']

featuresToInt = featuresToInt + hasFeatures







dfPractice = main.getPracticeData()

dfPracticeTaskDetails = main.getPracticeTaskDetails()
dfPracticeTaskDetails = dfPracticeTaskDetails.drop_duplicates(subset=['PracticeTaskId'], keep='first')


dfStudentDetails = main.getStudentDetails()
dfStudentDetails = dfStudentDetails.drop_duplicates(subset=['StudentId'], keep='first')




#----------------
# ----- Runs -----------
#---------------
#Data frames of JSON Features  - ALL OF THEM 
dfRuns = main.getDfFromJsonFeature('Runs', dfPractice, ['PracticeStatisticsId', 'PracticeTaskId', 'StudentId'])
main.toFormatStringToBoolean(dfRuns, 'Runs'+ '' +'Error')
#No of Times ran code
runsCount = dfRuns.PracticeStatisticsId.value_counts()
#No of Times ran Error
runsErrorCount = dfRuns[dfRuns.RunsError == True].PracticeStatisticsId.value_counts()
#No of Times ran Success
runsSuccessCount = dfRuns[dfRuns.RunsError == False].PracticeStatisticsId.value_counts()
#No of Times ran Error Syntax error
runsErrorSyntaxCount = dfRuns[dfRuns['RunsOutput'].str.contains("Syntax") & (dfRuns.RunsError == True ) ].PracticeStatisticsId.value_counts()
#No of Times ran Error Name Error
runsErrorNameCount = dfRuns[dfRuns['RunsOutput'].str.contains("NameError") & (dfRuns.RunsError == True ) ].PracticeStatisticsId.value_counts()
#No of Times ran Error Type Error
runsErrorTypeCount = dfRuns[dfRuns['RunsOutput'].str.contains("TypeError") & (dfRuns.RunsError == True ) ].PracticeStatisticsId.value_counts()
#No of Times ran Error Attribute Error
runsErrorAttribiteCount = dfRuns[dfRuns['RunsOutput'].str.contains("AttributeError") & (dfRuns.RunsError == True ) ].PracticeStatisticsId.value_counts()
#A new feature to store the complexity points



#----------------
# ----- Code -----------
#---------------
#dfRuns = main.calculateConceptComplexityPoints(dfRuns, 'RunsCode', 'RunsError', 'ConceptComplexityPoints')
#runsConceptPointsCount = dfRuns.groupby('PracticeStatisticsId')['ConceptComplexityPoints'].sum()


dfRuns = main.getConceptFeaturesFromCode(dfRuns, 'RunsCode', 'RunsError', 'ConceptComplexityPoints')
#dfRuns = dfRuns.merge(conceptFeatures, how='left')

dfRuns = dfRuns.dropna()

dfRuns[hasFeatures] =  dfRuns[hasFeatures].astype(np.int64)







#No of Times ran code with Loop
runsHasLoopCount = dfRuns[dfRuns.hasLoop == 1].PracticeStatisticsId.value_counts()
#No of Times ran code with nested loop
runsHasNestedLoopCount = dfRuns[dfRuns.hasNestedLoop == 1].PracticeStatisticsId.value_counts()
#No of Times ran code with condition
runsHasConditionCount = dfRuns[dfRuns.hasCondition == 1].PracticeStatisticsId.value_counts()
#No of Times ran code with variable
runsHasVariableCount = dfRuns[dfRuns.hasVariable == 1].PracticeStatisticsId.value_counts()


#generic programming concepts python ast parser
#https://docs.python.org/dev/library/ast.html
runsHasExpressionsCount = dfRuns[dfRuns.hasExpressions == 1].PracticeStatisticsId.value_counts()
runsHasAsyncOrAwaitCount = dfRuns[dfRuns.hasAsyncOrAwait == 1].PracticeStatisticsId.value_counts()
runsHasFunctionClassCount = dfRuns[dfRuns.hasFunctionClass == 1].PracticeStatisticsId.value_counts()
runsHasControlFlowCount = dfRuns[dfRuns.hasControlFlow == 1].PracticeStatisticsId.value_counts()
runsHasImportsCount = dfRuns[dfRuns.hasImports == 1].PracticeStatisticsId.value_counts()
runsHasStatementsCount = dfRuns[dfRuns.hasStatements == 1].PracticeStatisticsId.value_counts()
runsHasComprehensionsCount = dfRuns[dfRuns.hasComprehensions == 1].PracticeStatisticsId.value_counts()
runsHasSubscriptingCount = dfRuns[dfRuns.hasSubscripting == 1].PracticeStatisticsId.value_counts()





#line of code count for each code run - AVERAGE line of code per run
runsLineOfCodeCountAvg = dfRuns.groupby('PracticeStatisticsId')['lineOfCodeCount'].mean()



#lines of code
conceptFeaturesLines = main.getConceptFeaturesFromCodeLines(dfPractice, 'Code')
#dfPractice = dfPractice.join(conceptFeaturesLines) 
dfPractice = dfPractice.merge(conceptFeaturesLines, how='left')




#remove all features which have no meaning -
#which do not affect a student performance e.g. StudentId !!!
to_drop2After = [           
#           if these columns are still present - duplicate columns
           'Skill_SkillId', 'Course_CourseId', 'Student_StudentId', 'PracticeTask_PracticeTaskId'
           
           ]


dfPractice.drop(to_drop2After, inplace=True, axis=1)
dfPractice.fillna(0, inplace=True)







#----------------
# ----- DraggedOptions -----------
#---------------
dfDraggedOptions = main.getDfFromJsonFeature('DraggedOptions', dfPractice, ['PracticeStatisticsId', 'StudentId'])
#No of Times dragged
draggedCount = dfDraggedOptions.PracticeStatisticsId.value_counts()



#----------------
# ----- Tabs -----------
#---------------
dfTabs = main.getDfFromJsonFeature('Tabs', dfPractice, ['PracticeStatisticsId', 'StudentId'])
#No of Times tabs switched
tabsSwitchedCount = dfTabs.PracticeStatisticsId.value_counts()
#No of Times tabs switched to description - how clear is the task/description for the subject
tabsSwitchedDescriptionCount = dfTabs[dfTabs['TabsName'] == "Description"].PracticeStatisticsId.value_counts()
#No of Times tabs switched
tabsSwitchedCodeCount = dfTabs[dfTabs['TabsName'] == "Code"].PracticeStatisticsId.value_counts()
#No of Times tabs switched
tabsSwitchedOutputCount = dfTabs[dfTabs['TabsName'] == "Output"].PracticeStatisticsId.value_counts()


#----------------
# ----- Deleted codes -----------
#---------------
dfDeletedCodes = main.getDfFromJsonFeature('DeletedCodes', dfPractice, ['PracticeStatisticsId', 'StudentId'])
#No of Times deleted code
deletedCodesCount = dfDeletedCodes.PracticeStatisticsId.value_counts()


dfObstacles = main.getDfFromJsonFeature('Obstacles', dfPractice, ['PracticeStatisticsId', 'StudentId'])


#----------------
# ----- RobotCollisions -----------
#---------------
dfRobotCollisions = main.getDfFromJsonFeature('RobotCollisions', dfPractice, ['PracticeStatisticsId', 'StudentId'])
#No of Times collided with box
robotCollisionsBoxCount = dfRobotCollisions[dfRobotCollisions['RobotCollisionsObstacle'] == "Box"].PracticeStatisticsId.value_counts()
#No of Times collected Coins
coinCollectedCount = dfRobotCollisions[dfRobotCollisions['RobotCollisionsObstacle'] == "Coin"].PracticeStatisticsId.value_counts()


#----------------
# ----- Keyboard -----------
#---------------
dfKeyboard = main.getDfFromJsonFeature('Keyboard', dfPractice, ['PracticeStatisticsId', 'StudentId'])
#No of Times Key pressed
keyboardKeyPressedCount = dfKeyboard.PracticeStatisticsId.value_counts()




#The new Dataframe - to be used for Clustering algorithms !!! Yaay
dfPlayerStrategyPractice = dfPractice

#---Code -----------
countDict = runsCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsErrorCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsErrorCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsSuccessCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsSuccessCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsErrorSyntaxCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsErrorSyntaxCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsErrorNameCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsErrorNameCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsErrorTypeCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsErrorTypeCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsErrorAttribiteCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsErrorAttribiteCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

#countDict = runsConceptPointsCount.to_dict() #converts to dictionary
#dfPlayerStrategyPractice['runsConceptPointsCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 


countDict = runsHasLoopCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasLoopCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsHasNestedLoopCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasNestedLoopCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsHasConditionCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasConditionCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsHasVariableCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasVariableCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 


countDict = runsHasExpressionsCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasExpressionsCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsHasAsyncOrAwaitCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasAsyncOrAwaitCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsHasFunctionClassCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasFunctionClassCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsHasControlFlowCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasControlFlowCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsHasImportsCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasImportsCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsHasStatementsCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasStatementsCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsHasComprehensionsCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasComprehensionsCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = runsHasSubscriptingCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsHasSubscriptingCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 



countDict = runsLineOfCodeCountAvg.to_dict() #converts to dictionary
dfPlayerStrategyPractice['runsLineOfCodeCountAvg'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 





#--- dragged -----------
countDict = draggedCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['draggedCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = tabsSwitchedCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['tabsSwitchedCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = tabsSwitchedDescriptionCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['tabsSwitchedDescriptionCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = tabsSwitchedCodeCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['tabsSwitchedCodeCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = tabsSwitchedOutputCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['tabsSwitchedOutputCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = deletedCodesCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['deletedCodesCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = robotCollisionsBoxCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['robotCollisionsBoxCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = coinCollectedCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['coinCollectedCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 

countDict = keyboardKeyPressedCount.to_dict() #converts to dictionary
dfPlayerStrategyPractice['keyboardKeyPressedCount'] = dfPlayerStrategyPractice['PracticeStatisticsId'].map(countDict) 







#---------------------------add the count of tasks performed ---------------------
studentTaskCount = dfPractice.groupby([ 'StudentId'], as_index=False).count()[['StudentId', 'PracticeTaskId']]
studentTaskCount.rename(columns = {'PracticeTaskId':'studentTaskCount'}, inplace = True) 
dfPlayerStrategyPractice = dfPlayerStrategyPractice.merge(studentTaskCount, how='left')





#---------------------------student average attempts performed ---------------------
studentAttemptsTotal = dfPractice.groupby([ 'StudentId'], as_index=False).mean()[['StudentId', 'Attempts']]
studentAttemptsTotal.rename(columns = {'Attempts':'studentAttemptsTotal'}, inplace = True) 
dfPlayerStrategyPractice = dfPlayerStrategyPractice.merge(studentAttemptsTotal, how='left')





#drop Practice Statistics Id - not needed !
#dfPlayerStrategyPractice = dfPlayerStrategyPractice.drop('PracticeStatisticsId', 1)







#Player strategy - for Practical results

dfPlayerStrategyPractice = dfPlayerStrategyPractice.loc[:,~dfPlayerStrategyPractice.columns.duplicated()]

dfPlayerStrategyPractice.fillna(0, inplace=True)





dfPlayerStrategyPractice[featuresToInt] = dfPlayerStrategyPractice[featuresToInt].astype(int)





#*****************************************************************************
#STEP 0 : group data . by date or courseId, group of students of same school
#*****************************************************************************

MIN_STUDENT_COUNT = 5

dfPlayerStrategyPracticeOriginal = dfPlayerStrategyPractice

#Student Wise
dfPlayerStrategyPractice = dfPlayerStrategyPractice.groupby(['GroupId','StudentId'], as_index=False).sum()

#drop courseId and get from main dataframe (since it Sum added the courseIds)
dfPlayerStrategyPractice = dfPlayerStrategyPractice.drop('CourseId', 1)
#get the Code column
dfPlayerStrategyPracticeCode = dfPlayerStrategyPractice.merge(
        dfPractice[['StudentId', 'Code', 'Name', 'CreatedAt', 'CourseId', 'Title', 'Description']]
        , how='inner', on=['StudentId'], left_index=False, right_index=False)
#Drop duplicates keeping only the first row for Student and Task
dfPlayerStrategyPractice = dfPlayerStrategyPracticeCode.drop_duplicates(subset=['StudentId'], keep='first')
                                                
#Concepts used in the Code - using ast parser
dfPlayerStrategyPractice['ConceptsUsed']    = dfPlayerStrategyPractice['Code'].apply(main.getAllNodeTypesUsefull)
#dfPlayerStrategyPractice["ConceptsUsed"] = dfPlayerStrategyPractice["ConceptsUsed"].astype(str)
dfPlayerStrategyPractice["ConceptsUsed"] = dfPlayerStrategyPractice["ConceptsUsed"]
dfPlayerStrategyPractice["ConceptsUsedDetails"] = dfPlayerStrategyPractice['ConceptsUsed'].replace(
        main.ProgramConceptsUsefull2UserNames, regex=True)




for feature in hasFeatures:    
    dfPlayerStrategyPractice[feature] = (dfPlayerStrategyPractice[feature] >= 1 ).astype(int)


dfPlayerStrategyPractice = dfPlayerStrategyPractice.loc[:,~dfPlayerStrategyPractice.columns.duplicated()]




#Task Wise
dfPlayerStrategyPracticeTask = dfPlayerStrategyPracticeOriginal.groupby([ 'PracticeTaskId' , 'StudentId'], as_index=False).sum()

#drop courseId and get from main dataframe (since it Sum added the courseIds)
dfPlayerStrategyPracticeTask = dfPlayerStrategyPracticeTask.drop('CourseId', 1)
#get the Code column
dfPlayerStrategyPracticeTask = dfPlayerStrategyPracticeTask.merge(
        dfPractice[['StudentId', 'PracticeTaskId' ,'Code', 'Name', 'CreatedAt', 'CourseId', 'Title', 'Description']]
        , how='inner', on=['PracticeTaskId' , 'StudentId'], left_index=False, right_index=False)
#Drop duplicates keeping only the first row for Student and Task
dfPlayerStrategyPracticeTask = dfPlayerStrategyPracticeTask.drop_duplicates(subset=['PracticeTaskId', 'StudentId'], keep='first')
                                                
#Concepts used in the Code - using ast parser
dfPlayerStrategyPracticeTask['ConceptsUsed']    = dfPlayerStrategyPracticeTask['Code'].apply(main.getAllNodeTypesUsefull)
#dfPlayerStrategyPracticeTask["ConceptsUsed"] = dfPlayerStrategyPracticeTask["ConceptsUsed"].astype(str)
dfPlayerStrategyPracticeTask["ConceptsUsed"] = dfPlayerStrategyPracticeTask["ConceptsUsed"]
dfPlayerStrategyPracticeTask["ConceptsUsedDetails"] = dfPlayerStrategyPracticeTask['ConceptsUsed'].replace(
        main.ProgramConceptsUsefull2UserNames, regex=True)

for feature in hasFeatures:    
    dfPlayerStrategyPracticeTask[feature] = (dfPlayerStrategyPracticeTask[feature] >= 1 ).astype(int)

dfPlayerStrategyPracticeTask = dfPlayerStrategyPracticeTask.loc[:,~dfPlayerStrategyPracticeTask.columns.duplicated()]


#---------------------------------------------------------------------------------------------
                          

def getGroupedData(df):
    #plot for these - grouped with Year, Month !!!
    #return df.groupby(  [df['CreatedAt'].dt.year, df['CreatedAt'].dt.month]  )
    #other option - grouped by date
    return df.groupby(  [df[constants.GROUPBY_FEATURE]] )
#    return df.groupby(  [ df['CreatedAt'].dt.date ] )


dfGrouped = getGroupedData(dfPlayerStrategyPractice)

dfGroupedPracticeTaskWise = getGroupedData(dfPlayerStrategyPracticeTask)



#---------------------------------------------------------------
#How many students used loops/certain concept in a certain task?
#---------------------------------------------------------------
def getGroupedDataSchoolTask(df):
    return df.groupby(  [df[ constants.GROUPBY_FEATURE ], df['PracticeTaskId']] )
#    return df.groupby(  [df['CreatedAt'].dt.date, df['PracticeTaskId']] )


dfGroupedBySchoolTask = getGroupedDataSchoolTask(dfPractice)
        
        
        
#--------------------------------------------------------------------
# Task information for Overview - admin
#How many lines students wrote
#How many variables used in a task
#How many conditions used in a task
#--------------------------------------------------------------------
def getGroupedDataTask(df):
    return df.groupby(  [df['PracticeTaskId']] )


dfGroupedByTask = getGroupedDataTask(dfPractice)


#----------------------------------------------------------------------
#---------------------- creteing student gantt chart data

dfGroupedOriginal = main.getGroupedDataStudent(dfPlayerStrategyPracticeOriginal)