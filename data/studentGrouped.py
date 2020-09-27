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
getUserDetails                                          = main.getUserDetails


dfUser                                                  = main.getUsers()


dfLearningActivityDetails                               = main.getLearningActivityDetails()
dfLearningActivityDetails[constants.featureGroup]       = constants.TypeGroup + '-' + dfLearningActivityDetails[constants.GROUPBY_FEATURE].astype(str) 

dfEnrolledDetails                                       = main.getEnrolledDetails()
dfEnrolledDetails[constants.featureGroup]               = constants.TypeGroup + '-' + dfEnrolledDetails[constants.GROUPBY_FEATURE].astype(str) 
dfEnrolledDetails[constants.featureStudent]             = constants.TypeStudent + '-' + dfEnrolledDetails['StudentId'].astype(str) 

dfStudentDetails                                        = main.getStudentDetails()
dfStudentDetails[constants.featureStudent]              = constants.TypeStudent + '-' + dfStudentDetails['StudentId'].astype(str) 

dfCourseDetails                                         = main.getCourseDetails()
dfCourseDetails[constants.featureCourse]                = constants.TypeCourse + '-' + dfCourseDetails['CourseId'].astype(str) 
dfSkillDetails                                          = main.getSkillDetails()
dfSkillDetails[constants.featureSkill]                  = constants.TypeSkill + '-' + dfSkillDetails['SkillId'].astype(str) 
dfPracticeTaskDetails                                   = main.getPracticeTaskDetails()
dfPracticeTaskDetails[constants.featureTaskType]        = constants.TaskTypePractice
dfPracticeTaskDetails[constants.featureTask]            = constants.TaskTypePractice + '-' + dfPracticeTaskDetails['PracticeTaskId'].astype(str) 
dfPracticeTaskDetails[constants.featureSkill]           = constants.TypeSkill + '-' + dfPracticeTaskDetails['SkillId'].astype(str) 
dfPracticeTaskDetails[constants.featureCourse]          = constants.TypeCourse + '-' + dfPracticeTaskDetails['CourseId'].astype(str) 
dfPracticeTaskDetails                                   = dfPracticeTaskDetails.merge(
               dfSkillDetails
               , how='inner', on=['SkillId'], left_index=False, right_index=False, suffixes = ['', 'Skill'])
dfPracticeTaskDetails                                   = dfPracticeTaskDetails.merge(
               dfCourseDetails
               , how='inner', on=['CourseId'], left_index=False, right_index=False, suffixes = ['', 'Course'])
dfTheoryTaskDetails                                     = main.getTheoryTaskDetails()
dfTheoryTaskDetails[constants.featureTaskType]          = constants.TaskTypeTheory
dfTheoryTaskDetails[constants.featureTask]              = constants.TaskTypeTheory + '-' + dfTheoryTaskDetails['TheoryTaskId'].astype(str)
dfTheoryTaskDetails[constants.featureSkill]             = constants.TypeSkill + '-' + dfTheoryTaskDetails['SkillId'].astype(str) 
dfTheoryTaskDetails[constants.featureCourse]            = constants.TypeCourse + '-' + dfTheoryTaskDetails['CourseId'].astype(str) 
dfTheoryTaskDetails                                     = dfTheoryTaskDetails.merge(
               dfSkillDetails
               , how='inner', on=['SkillId'], left_index=False, right_index=False, suffixes = ['', 'Skill'])
dfTheoryTaskDetails                                   = dfTheoryTaskDetails.merge(
               dfCourseDetails
               , how='inner', on=['CourseId'], left_index=False, right_index=False, suffixes = ['', 'Course'])
dfTaskDetails                   =   pd.concat([dfPracticeTaskDetails, dfTheoryTaskDetails], ignore_index=True)
        


dfPlayerStrategyPracticeOriginal        = studentGroupedPerformance.dfPlayerStrategyPracticeOriginal
dfPlayerStrategyPracticeOriginal[constants.featureTaskType] = constants.TaskTypePractice
dfPlayerStrategyPracticeOriginal[constants.featureTaskId] = constants.TaskTypePractice + '-' + dfPlayerStrategyPracticeOriginal['PracticeTaskId'].astype(str)


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
dfPlayerStrategyTheory[constants.featureTaskId] = constants.TaskTypeTheory + '-' + dfPlayerStrategyTheory['TheoryTaskId'].astype(str)
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
        
def getGroups():
    return [constants.TypeGroup + '-' + str(0)] + [constants.TypeGroup + '-' + str(learningActivityId) for learningActivityId in dfLearningActivityDetails[constants.GROUPBY_FEATURE].unique()]
 


def BuildOptions(options):  
    return [{'label': i, 'value': i} for i in options]


def getUserLA():

    return dfLearningActivityDetails[constants.GROUPBY_FEATURE].unique()


def getUserLAOptions():
    userLA = [0] + getUserLA()
    
    print(getUserLA())
    print(userLA)
    
    return BuildOptions( [ int(groupId) for groupId in [0] + userLA ]  )

GroupSelector_options = getUserLAOptions()



def getUserFromUserId(usernameOrId):
    
    userDB = dfUser[ (dfUser['Id'] == usernameOrId ) |  (dfUser['UserName'] == usernameOrId) ]
        
    if len(userDB) > 0:            
        return userDB.iloc[0]   
    else:
        return None


#--------------------------------------------------------------------------------------------
#--------------------- get students of School  START ---------------------------------------

def get_merge_list(values):
    return list(set([a for b in values.tolist() for a in b]))

#get List of Students for a group
def getStudentsOfSchool(groupSelected):
        
#    students = list(dfStudentDetails[dfStudentDetails[constants.GROUPBY_FEATURE] == groupSelected][constants.STUDENT_ID_FEATURE].unique())
    
    students = list(dfEnrolledDetails[dfEnrolledDetails[constants.GROUPBY_FEATURE] == groupSelected][constants.STUDENT_ID_FEATURE].unique())
    
    return students

#get students DataFrame a group
def getStudentsOfSchoolDF(groupSelected, isOriginal = False):
    
    if not(isOriginal) and groupSelected in dfGroupedPractice.groups.keys():
        schoolPractice = dfGroupedPractice.get_group(groupSelected)
        schoolPractice[constants.featureTaskId]        = constants.TaskTypePractice + '-' + schoolPractice['PracticeTaskId'].astype(str)
        schoolPractice[constants.TASK_TYPE_FEATURE]      = constants.TaskTypePractice
    
        schoolPractice = schoolPractice.loc[:,~schoolPractice.columns.duplicated()]     

        studentDF = schoolPractice
        
        studentDF['ConceptsUsedGroup'] =  [ studentDF.ConceptsUsed.agg(get_merge_list) ] * studentDF.shape[0]
        studentDF['ConceptsUsedDetailsGroup'] = [  studentDF.ConceptsUsedDetails.agg(get_merge_list) ] * studentDF.shape[0]
        studentDF[constants.featureConceptsUsedDetailsStr]     = studentDF['ConceptsUsedDetailsGroup']
        
        studentDF[featureDescription] = getPracticeDescription(studentDF)  
    
    elif isOriginal and groupSelected in dfGroupedOriginal.groups.keys():
        schoolPractice = dfGroupedOriginal.get_group(groupSelected)
        schoolPractice[constants.featureTaskId]        = constants.TaskTypePractice + '-' + schoolPractice['PracticeTaskId'].astype(str)
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
        schoolTheory[constants.featureTaskId]      =  constants.TaskTypeTheory + schoolTheory['TheoryTaskId'].astype(str)
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
    
    
    print('first isOriginal')
    print(isOriginal)
    
    groupStudents = getStudentsOfSchool(groupSelected)
    print('first groupStudents')
    print(groupStudents)
    print(len(groupStudents))
    
    groupStudents = studentDF['StudentId'].unique()
    print('second groupStudents')
    print(groupStudents)
    print(len(groupStudents))
    
    
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
    
