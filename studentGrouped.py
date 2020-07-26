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
    if constants.featureConceptsUsedDetailsStr in dfPractice.columns:
        dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featureConceptsUsedDetailsStr)) + '</b>: ' + dfPractice[constants.featureConceptsUsedDetailsStr].astype(str)
    if constants.featureLineOfCodeCount in dfPractice.columns:    
        dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featureLineOfCodeCount)) + '</b>: ' + dfPractice[constants.featureLineOfCodeCount].astype(str)
    if constants.featureRobotCollisionsBoxCount in dfPractice.columns:
        dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featureRobotCollisionsBoxCount)) + '</b>: ' + dfPractice[constants.featureRobotCollisionsBoxCount].astype(str)
    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('StudentId')) + '</b>: ' + dfPractice['StudentId'].astype(str)
    return dfPractice[featureDescription]


def getTheoryDescription(dfTheory) :    
    dfTheory[featureDescription] = '<b>' + dfTheory['Name'].astype(str) + '</b>' + '<br>'
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('SessionDuration')) + '</b>: ' + dfTheory['SessionDuration'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Points')) + '</b>: ' + dfTheory['Points'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Result')) + '</b>: ' + dfTheory['Result'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Attempts')) + '</b>: ' + dfTheory['Attempts'].astype(str)
    if constants.featureItemsCollectedCount in dfTheory.columns:
        dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featureItemsCollectedCount)) + '</b>: ' + dfTheory[constants.featureItemsCollectedCount].astype(str)
    
    if constants.featurePlayerShootEndEnemyHitCount in dfTheory.columns:
        dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featurePlayerShootEndEnemyHitCount)) + '</b>: ' + dfTheory[constants.featurePlayerShootEndEnemyHitCount].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('StudentId')) + '</b>: ' + dfTheory['StudentId'].astype(str)
    return dfTheory[featureDescription]



def getDescription(df) :    
    df[featureDescription] = '<b>' + df['Name'].astype(str) + '</b>' + '<br>'
    df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('SessionDuration')) + '</b>: ' + df['SessionDuration'].astype(str)
    df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Points')) + '</b>: ' + df['Points'].astype(str)
    df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Result')) + '</b>: ' + df['Result'].astype(str)
    df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Attempts')) + '</b>: ' + df['Attempts'].astype(str)
    
    if df[constants.TASK_TYPE_FEATURE] == 'Theory':
        if constants.featureItemsCollectedCount in df.columns:
            df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featureItemsCollectedCount)) + '</b>: ' + df[constants.featureItemsCollectedCount].astype(str)
        
        if constants.featurePlayerShootEndEnemyHitCount in df.columns:
            df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featurePlayerShootEndEnemyHitCount)) + '</b>: ' + df[constants.featurePlayerShootEndEnemyHitCount].astype(str)
    
    if df[constants.TASK_TYPE_FEATURE] == 'Practice':
        if constants.featureConceptsUsedDetailsStr in df.columns:
            df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featureConceptsUsedDetailsStr)) + '</b>: ' + df[constants.featureConceptsUsedDetailsStr].astype(str)
        if constants.featureLineOfCodeCount in df.columns:    
            df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featureLineOfCodeCount)) + '</b>: ' + df[constants.featureLineOfCodeCount].astype(str)
        if constants.featureRobotCollisionsBoxCount in df.columns:
            df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featureRobotCollisionsBoxCount)) + '</b>: ' + df[constants.featureRobotCollisionsBoxCount].astype(str)
           
    
    df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('StudentId')) + '</b>: ' + df['StudentId'].astype(str)
    return df[featureDescription]


def getPracticeConceptsUsedDetailsStr(dfPractice):    
    if constants.featureConceptsUsedDetails in dfPractice.columns:
        return dfPractice['ConceptsUsedDetails'].apply(lambda x: x[1:-1])

def getStudentWiseData(df):
    if "Name" in df.columns:
        return df.groupby([constants.STUDENT_ID_FEATURE, "Name"], as_index=False).sum()    
    else :
        return df.groupby([constants.STUDENT_ID_FEATURE], as_index=False).sum()

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
def getStudentsOfSchoolDF(groupSelected, isOriginal = False):
    
    if not(isOriginal) and groupSelected in dfGroupedPractice.groups.keys():
        schoolPractice = dfGroupedPractice.get_group(groupSelected)
        schoolPractice['TaskId']        = 'Practice' + schoolPractice['PracticeTaskId'].astype(str)
        schoolPractice[constants.TASK_TYPE_FEATURE]      = 'Practice'
    
        schoolPractice = schoolPractice.loc[:,~schoolPractice.columns.duplicated()]     

        studentDF = schoolPractice
        
        studentDF['ConceptsUsedGroup'] =  [ studentDF.ConceptsUsed.agg(get_merge_list) ] * studentDF.shape[0]
        studentDF['ConceptsUsedDetailsGroup'] = [  studentDF.ConceptsUsedDetails.agg(get_merge_list) ] * studentDF.shape[0]
        
        studentDF[featureDescription] = getPracticeDescription(studentDF)    

    
    if groupSelected in dfGroupedPlayerStrategyTheory.groups.keys():
        schoolTheory = dfGroupedPlayerStrategyTheory.get_group(groupSelected)
        schoolTheory['TaskId']      = 'Theory' + schoolTheory['TheoryTaskId'].astype(str)
        schoolTheory[constants.TASK_TYPE_FEATURE]    = 'Theory' 
        print('2 schoolTheory in studentGrouped')  
        print(schoolTheory)   
        schoolTheory = schoolTheory.loc[:,~schoolTheory.columns.duplicated()]  
        studentDF[featureDescription] = getTheoryDescription(studentDF)    
        
#        if defined, else
        try:
            studentDF = pd.concat([studentDF, schoolTheory], ignore_index=True, sort=False)
        
            print(studentDF)
            print('in try part concated both')
        except NameError:
            print("studentDF WASN'T defined after all!")
            studentDF = schoolTheory
    
    
    groupStudents = getStudentsOfSchool(groupSelected)
    
    
    if 'studentDF' in locals()     and    studentDF is not None :
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
    
