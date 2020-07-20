# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 15:48:22 2020

@author: tilan
"""


import numpy as np
import pandas as pd

import main
import studentGroupedPerformance
import studentGroupedPerformanceTheory
import constants



# Fixing random state for reproducibility
np.random.seed(19680801)


#----------------------- groupby feature --------------------------------------

#------------------------------------------------------------------------------

#------------------ Database interactions START --------------------------------------------

dfStudentDetails = main.getStudentDetails()



dfPracticeTaskDetails = studentGroupedPerformance.dfPracticeTaskDetails
dfTheoryTaskDetails   = studentGroupedPerformanceTheory.dfTheoryTaskDetails


dfGroupedPractice                       = studentGroupedPerformance.dfGrouped
dfGroupedOriginal                       = studentGroupedPerformance.dfGroupedOriginal
dfPlayerStrategyPractice                = studentGroupedPerformance.dfPlayerStrategyPractice  
dfGroupedPracticeTaskWise               = studentGroupedPerformance.dfGroupedPracticeTaskWise
#dfGroupedPracticeDB  = studentGroupedPerformance.dfPractice.groupby(  [studentGroupedPerformance.dfPractice['CreatedAt'].dt.date] )
dfGroupedPracticeDB         = studentGroupedPerformance.dfPractice.groupby(  [studentGroupedPerformance.dfPractice[constants.GROUPBY_FEATURE]] )


dfRuns                      = studentGroupedPerformance.dfRuns
        

dfPlayerStrategyTheory = pd.concat([studentGroupedPerformanceTheory.dfPlayerStrategyNN, studentGroupedPerformanceTheory.dfPlayerStrategyN], ignore_index=True, sort =False)
#dfGroupedPlayerStrategyTheory = dfPlayerStrategyTheory.groupby(  [dfPlayerStrategyTheory['CreatedAt'].dt.date] )
dfGroupedPlayerStrategyTheory = dfPlayerStrategyTheory.groupby(  [dfPlayerStrategyTheory[constants.GROUPBY_FEATURE]] )


#------------------ Database interactions END --------------------------------------------


#----------------------------------

featureDescription = constants.featureDescription
feature2UserNamesDict = constants.feature2UserNamesDict

hasFeatures =  studentGroupedPerformance.hasFeatures

#-------------------------------------------------------------------


#--------------------------- helper functions START -----------------------
getGroupedData = main.getGroupedData


def getTaskWiseSuccessFail(groupData, taskId, dfTaskDetails, featureTaskId, typeOfTask):
    
    groupData = groupData.sort_values(['StudentId','Result'], ascending=False)
    
    taskTitle = ' missing '
    
    try :
        taskTitle = dfTaskDetails[ dfTaskDetails[featureTaskId] == int(taskId) ]['Title'].values[0]
    except Exception as e: 
        print(e)   
        
    return  [str(taskTitle)] + [groupData[groupData['Result'] == 1].count()[0], 
                                  groupData[groupData['Result'] == 0].count()[0]] + [  str(typeOfTask) ] + [ taskId ]




def getPracticeDescription(dfPractice) :
    dfPractice[featureDescription] = '<b>' + dfPractice['Name'].astype(str) + '</b>' + '<br>'
    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('SessionDuration')) + '</b>: ' + dfPractice['SessionDuration'].astype(str)
    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Points')) + '</b>:' + dfPractice['Points'].astype(str)
    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('CollectedCoins')) + '</b>: ' + dfPractice['CollectedCoins'].astype(str)
    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Result')) + '</b>: ' + dfPractice['Result'].astype(str)
    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Attempts')) + '</b>: ' + dfPractice['Attempts'].astype(str)
    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('ConceptsUsedDetailsStr')) + '</b>: ' + dfPractice['ConceptsUsedDetailsStr'].astype(str)
    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('lineOfCodeCount')) + '</b>: ' + dfPractice['lineOfCodeCount'].astype(str)
    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('robotCollisionsBoxCount')) + '</b>: ' + dfPractice['robotCollisionsBoxCount'].astype(str)
    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('StudentId')) + '</b>: ' + dfPractice['StudentId'].astype(str)
    return dfPractice[featureDescription]

def getTheoryDescription(dfTheory) :    
    dfTheory[featureDescription] = '<b>' + dfTheory['Name'].astype(str) + '</b>' + '<br>'
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('SessionDuration')) + '</b>: ' + dfTheory['SessionDuration'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Points')) + '</b>: ' + dfTheory['Points'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Result')) + '</b>: ' + dfTheory['Result'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Attempts')) + '</b>: ' + dfTheory['Attempts'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('itemsCollectedCount')) + '</b>: ' + dfTheory['itemsCollectedCount'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('playerShootEndEnemyHitCount')) + '</b>: ' + dfTheory['playerShootEndEnemyHitCount'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('StudentId')) + '</b>: ' + dfTheory['StudentId'].astype(str)
    return dfTheory[featureDescription]
#-------------------------- helper functions END -----------------------


#---------------------------------
# school selection
def BuildOptions(options):  
    return [{'label': i, 'value': i} for i in options]


GroupSelector_options = BuildOptions(dfStudentDetails[constants.GROUPBY_FEATURE].unique())




#--------------------------------------------------------------------------------------------
#--------------------- get students of School  START ---------------------------------------

def get_merge_list(values):
    return list(set([a for b in values.tolist() for a in b]))

#get List of Students for a group
def getStudentsOfSchool(groupSelected):
    
    print(groupSelected)
    
    students = list()

    try :
        studentWiseData = dfGroupedOriginal.get_group(groupSelected)
        students = studentWiseData['StudentId'].unique()
        students = list(students)   
    except Exception as e: 
        print(e)
    
    try :
        groupOriginalTheory = dfGroupedPlayerStrategyTheory.get_group(groupSelected)
        studentsTheory = groupOriginalTheory['StudentId'].unique()
        studentsTheory = list(studentsTheory)
        
        students = students + studentsTheory        
    except Exception as e: 
        print(e)
        
    students = list(set(students))
    
    return students

#get students DataFrame a group
def getStudentsOfSchoolDF(groupSelected):
    
    if groupSelected in dfGroupedPractice.groups.keys():
        schoolPractice = dfGroupedPractice.get_group(groupSelected)
        schoolPractice['TaskId']        = 'Practice' + schoolPractice['PracticeTaskId'].astype(str)
        schoolPractice['TaskType']      = 'Practice'
        
    
        schoolPractice = schoolPractice.loc[:,~schoolPractice.columns.duplicated()]     
                
        studentDF = schoolPractice
        print('1 studentDF in studentGrouped')  
        print(studentDF)  
        print(studentDF.ConceptsUsed.agg(get_merge_list))  
        print(studentDF.ConceptsUsedDetails.agg(get_merge_list))  
        
        studentDF['ConceptsUsedGroup'] =  [ studentDF.ConceptsUsed.agg(get_merge_list) ] * studentDF.shape[0]
        studentDF['ConceptsUsedDetailsGroup'] = [  studentDF.ConceptsUsedDetails.agg(get_merge_list) ] * studentDF.shape[0]


    
    if groupSelected in dfGroupedPlayerStrategyTheory.groups.keys():
        schoolTheory = dfGroupedPlayerStrategyTheory.get_group(groupSelected)
        schoolTheory['TaskId']      = 'Theory' + schoolTheory['TheoryTaskId'].astype(str)
        schoolTheory['TaskType']    = 'Theory' 
        print('2 schoolTheory in studentGrouped')  
        print(schoolTheory)   
        schoolTheory = schoolTheory.loc[:,~schoolTheory.columns.duplicated()]  
        
#        if defined, else
        try:
            studentDF = pd.concat([studentDF, schoolTheory], ignore_index=True, sort=False)
            print(studentDF)
            print('in try part concated both')
        except NameError:
            print("studentDF WASN'T defined after all!")
            studentDF = schoolTheory
    
    
    groupStudents = getStudentsOfSchool(groupSelected)
    
    
    if 'studentDF' in locals():
        print('Students of group')
        print(groupStudents)
        print('studentDF.columns')
        print(studentDF.columns)
        
        if len(groupStudents) > 0:
            studentDF[constants.GROUPBY_FEATURE]    =     groupSelected 
            studentDF[constants.COUNT_STUDENT_FEATURE]      =     len(groupStudents) 
            
            if 'ConceptsUsedGroup' in studentDF.columns :
                studentDF['ConceptsUsed'] =  [ studentDF['ConceptsUsedGroup'][0] ] * studentDF.shape[0]
                studentDF['ConceptsUsedDetails'] =  [ studentDF['ConceptsUsedDetailsGroup'][0] ] * studentDF.shape[0]
            
            return studentDF
#--------------------- get students of School  END ---------------------------------------
#--------------------------------------------------------------------------------------------
    
