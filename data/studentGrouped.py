# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 15:48:22 2020

@author: tilan
"""


import numpy as np
import pandas as pd

from data import main
from data import studentGroupedPerformance
from data import studentGroupedPerformanceTheory

import constants



# Fixing random state for reproducibility
np.random.seed(19680801)


#----------------------- groupby feature --------------------------------------

#------------------------------------------------------------------------------

#------------------ Database interactions START --------------------------------------------

dfStudentDetails        = main.getStudentDetails()

dfSkillDetails          = main.getSkillDetails()
dfPracticeTaskDetailsExtra          = main.getPracticeTaskDetailsExtra()




dfPracticeTaskDetails = studentGroupedPerformance.dfPracticeTaskDetails
dfTheoryTaskDetails   = studentGroupedPerformanceTheory.dfTheoryTaskDetails

dfPlayerStrategyPracticeOriginal        = studentGroupedPerformance.dfPlayerStrategyPracticeOriginal
dfPlayerStrategyPracticeOriginal[constants.featureTaskType] = constants.TaskTypePractice
dfPlayerStrategyPracticeOriginal['TaskId'] = constants.TaskTypePractice + '-' + dfPlayerStrategyPracticeOriginal['PracticeTaskId'].astype(str)


dfPracticeDB                            = studentGroupedPerformance.dfPractice
dfGroupedPractice                       = studentGroupedPerformance.dfGrouped
dfGroupedOriginal                       = studentGroupedPerformance.dfGroupedOriginal
dfPlayerStrategyPractice                = studentGroupedPerformance.dfPlayerStrategyPractice  
dfGroupedPracticeTaskWise               = studentGroupedPerformance.dfGroupedPracticeTaskWise
#dfGroupedPracticeDB  = studentGroupedPerformance.dfPractice.groupby(  [studentGroupedPerformance.dfPractice['CreatedAt'].dt.date] )
dfGroupedPracticeDB                     = studentGroupedPerformance.dfPractice.groupby(  [studentGroupedPerformance.dfPractice[constants.GROUPBY_FEATURE]] )


dfRuns                                  = studentGroupedPerformance.dfRuns
dfRuns[constants.featureTaskType]       = constants.TaskTypePractice
        

dfPlayerStrategyTheory = pd.concat([studentGroupedPerformanceTheory.dfPlayerStrategyNN, studentGroupedPerformanceTheory.dfPlayerStrategyN], ignore_index=True, sort =False)
dfPlayerStrategyTheory[constants.featureTaskType]   = constants.TaskTypeTheory
dfPlayerStrategyTheory['TaskId'] = constants.TaskTypeTheory + '-' + dfPlayerStrategyTheory['TheoryTaskId'].astype(str)
#dfGroupedPlayerStrategyTheory = dfPlayerStrategyTheory.groupby(  [dfPlayerStrategyTheory['CreatedAt'].dt.date] )
dfGroupedPlayerStrategyTheory = dfPlayerStrategyTheory.groupby(  [dfPlayerStrategyTheory[constants.GROUPBY_FEATURE]] )


#------------------ Database interactions END --------------------------------------------


#-----------------------functions from Main -------------------------------------------------

getAllNodeTypesUsefull                  = main.getAllNodeTypesUsefull
            
#----------------------------functions from Main  END ---------------------------------------


#----------------------------------

ProgramConceptsUsefull2UserNames        = constants.ProgramConceptsUsefull2UserNames


featureDescription      = constants.featureDescription
feature2UserNamesDict   = constants.feature2UserNamesDict
featureSessionDuration  = constants.featureSessionDuration

hasFeatures =  studentGroupedPerformance.hasFeatures

#-------------------------------------------------------------------


#--------------------------- helper functions START -----------------------
getGroupedData = main.getGroupedData


def getTaskWiseSuccessFail(groupData, taskId, dfTaskDetails, featureTaskId, typeOfTask):
    
    groupData = groupData.sort_values(['StudentId','Result'], ascending=False)
    
    taskTitle = ' missing '
    taskDescription = ''
    skill = ''
    
    print('getTaskWiseSuccessFail')
    try :
        currentTask     = dfTaskDetails[ dfTaskDetails[featureTaskId] == int(taskId) ]
        taskTitle       = currentTask['Title'].values[0] 
        taskDescription = dfTaskDetails[ dfTaskDetails[featureTaskId] == int(taskId) ][constants.featureDescription].values[0]
        
        str(groupData['SkillId'].values[0])
    except Exception as e: 
        print(e)
        
    return  [str(taskTitle)] + [str(taskDescription)] + [groupData[groupData['Result'] == 1].count()[0], 
                                  groupData[groupData['Result'] == 0].count()[0]] +   [  groupData['SessionDuration'].sum() ] + [  str(typeOfTask) ] + [ taskId ]




def getPracticeDescription(dfPractice, hasNameTitle = True) :
    dfPractice[featureDescription] = ''
    
    if hasNameTitle:
        dfPractice[featureDescription] = '<b>' + dfPractice['Name'].astype(str) + '</b>' + '<br>'

    dfPractice[featureDescription] = dfPractice[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(featureSessionDuration)) + '</b>: ' + dfPractice[featureSessionDuration].astype(str)
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


def getTheoryDescription(dfTheory, hasNameTitle = True) :
    dfTheory[featureDescription] = ''
    
    if hasNameTitle:
        dfTheory[featureDescription] = '<b>' + dfTheory['Name'].astype(str) + '</b>' + '<br>'
    
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(featureSessionDuration)) + '</b>: ' + dfTheory[featureSessionDuration].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Points')) + '</b>: ' + dfTheory['Points'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Result')) + '</b>: ' + dfTheory['Result'].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Attempts')) + '</b>: ' + dfTheory['Attempts'].astype(str)
    
    if constants.featureSolution in dfTheory.columns:
        dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>Solution</b>: ' +  dfTheory[constants.featureSolution].astype(str)
    if constants.featureItemsCollectedCount in dfTheory.columns:
        dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featureItemsCollectedCount)) + '</b>: ' + dfTheory[constants.featureItemsCollectedCount].astype(str)
    if constants.featurePlayerShootEndEnemyHitCount in dfTheory.columns:
        dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featurePlayerShootEndEnemyHitCount)) + '</b>: ' + dfTheory[constants.featurePlayerShootEndEnemyHitCount].astype(str)
    dfTheory[featureDescription] = dfTheory[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('StudentId')) + '</b>: ' + dfTheory['StudentId'].astype(str)

    return dfTheory[featureDescription]



def getDescription(df) :    
    df[featureDescription] = '<b>' + df['Name'].astype(str) + '</b>' + '<br>'
    df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(featureSessionDuration)) + '</b>: ' + df[featureSessionDuration].astype(str)
    df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Points')) + '</b>: ' + df['Points'].astype(str)
    df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Result')) + '</b>: ' + df['Result'].astype(str)
    df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get('Attempts')) + '</b>: ' + df['Attempts'].astype(str)
    
    if df[constants.TASK_TYPE_FEATURE] == constants.TaskTypeTheory :
        if constants.featureItemsCollectedCount in df.columns:
            df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featureItemsCollectedCount)) + '</b>: ' + df[constants.featureItemsCollectedCount].astype(str)
        
        if constants.featurePlayerShootEndEnemyHitCount in df.columns:
            df[featureDescription] = df[featureDescription] + '<br><b>' + str(feature2UserNamesDict.get(constants.featurePlayerShootEndEnemyHitCount)) + '</b>: ' + df[constants.featurePlayerShootEndEnemyHitCount].astype(str)
    
    if df[constants.TASK_TYPE_FEATURE] == constants.TaskTypePractice :
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
        
    students = list(dfStudentDetails[dfStudentDetails['GroupId'] == groupSelected]['StudentId'].unique())
    
    return students

#get students DataFrame a group
def getStudentsOfSchoolDF(groupSelected, isOriginal = False):
    
    if not(isOriginal) and groupSelected in dfGroupedPractice.groups.keys():
        schoolPractice = dfGroupedPractice.get_group(groupSelected)
        schoolPractice['TaskId']        = constants.TaskTypePractice + schoolPractice['PracticeTaskId'].astype(str)
        schoolPractice[constants.TASK_TYPE_FEATURE]      = constants.TaskTypePractice
    
        schoolPractice = schoolPractice.loc[:,~schoolPractice.columns.duplicated()]     

        studentDF = schoolPractice
        
        studentDF['ConceptsUsedGroup'] =  [ studentDF.ConceptsUsed.agg(get_merge_list) ] * studentDF.shape[0]
        studentDF['ConceptsUsedDetailsGroup'] = [  studentDF.ConceptsUsedDetails.agg(get_merge_list) ] * studentDF.shape[0]
        studentDF[constants.featureConceptsUsedDetailsStr]     = studentDF['ConceptsUsedDetailsGroup']
        
        studentDF[featureDescription] = getPracticeDescription(studentDF)  
    
    elif isOriginal and groupSelected in dfGroupedOriginal.groups.keys():
        schoolPractice = dfGroupedOriginal.get_group(groupSelected)
        schoolPractice['TaskId']        = constants.TaskTypePractice + schoolPractice['PracticeTaskId'].astype(str)
        schoolPractice[constants.TASK_TYPE_FEATURE]      = constants.TaskTypePractice
    
        schoolPractice = schoolPractice.loc[:,~schoolPractice.columns.duplicated()]     

        studentDF = schoolPractice
        
        studentDF['ConceptsUsed']    = studentDF['Code'].apply(main.getAllNodeTypesUsefull)
        studentDF["ConceptsUsedDetails"] = studentDF['ConceptsUsed'].replace(
                constants.ProgramConceptsUsefull2UserNames, regex=True)
        
        studentDF['ConceptsUsedGroup'] =  [ studentDF.ConceptsUsed.agg(get_merge_list) ] * studentDF.shape[0]
        studentDF['ConceptsUsedDetailsGroup'] = [  studentDF.ConceptsUsedDetails.agg(get_merge_list) ] * studentDF.shape[0]
        studentDF[constants.featureConceptsUsedDetailsStr]     = studentDF['ConceptsUsedDetailsGroup']
        
        studentDF[featureDescription] = getPracticeDescription(studentDF)  
        

    
    if groupSelected in dfGroupedPlayerStrategyTheory.groups.keys():
        schoolTheory = dfGroupedPlayerStrategyTheory.get_group(groupSelected)
        schoolTheory['TaskId']      =  constants.TaskTypeTheory + schoolTheory['TheoryTaskId'].astype(str)
        schoolTheory[constants.TASK_TYPE_FEATURE]    =  constants.TaskTypeTheory 
        
        schoolTheory = schoolTheory.loc[:,~schoolTheory.columns.duplicated()]          
        schoolTheory[featureDescription] = getTheoryDescription(schoolTheory)    
        
#        if defined, else
        try:
            studentDF = pd.concat([studentDF, schoolTheory], ignore_index=True, sort=False)
            print('in try part concated both')
        except NameError:
            print("studentDF WASN'T defined after all!")
            studentDF = schoolTheory
    
    
    groupStudents = getStudentsOfSchool(groupSelected)
    
    
    if 'studentDF' in locals()     and    studentDF is not None :
        
        if len(groupStudents) > 0:
            studentDF[constants.GROUPBY_FEATURE]            =     groupSelected 
            studentDF[constants.COUNT_STUDENT_FEATURE]      =     len(groupStudents) 
            
            if 'ConceptsUsedGroup' in studentDF.columns :
                studentDF['ConceptsUsed'] =  [ studentDF['ConceptsUsedGroup'][0] ] * studentDF.shape[0]
                studentDF['ConceptsUsedDetails'] =  [ studentDF['ConceptsUsedDetailsGroup'][0] ] * studentDF.shape[0]
            
            return studentDF
#--------------------- get students of School  END ---------------------------------------
#--------------------------------------------------------------------------------------------
    
