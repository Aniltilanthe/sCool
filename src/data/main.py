# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 13:24:48 2020

@author: Anil


ONLY FOR DB INTERACTIONS & GENERAL FUNCTIONS 

"""

import pyodbc
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

#import streamlit as st
import json
import statsmodels.formula.api as sm

#python code parser
import ast

# Fixing random state for reproducibility
np.random.seed(19680801)


import sklearn.impute as impu
#from sklearn.impute import SimpleImputer 


import constants

from data.pythonCodeParser import PythonCodeParser, getAllNodeTypes, getAllNodeTypesUsefull



#https://datatofish.com/how-to-connect-python-to-sql-server-using-pyodbc/

#imputer = Imputer(missing_values = "NaN", strategy = "mean", axis = 0)
imputer = impu.SimpleImputer(missing_values = "NaN", strategy = "mean")


Driver          = constants.Driver
Server          = constants.Server
DatabaseName    = constants.DatabaseName
Uid             = constants.Uid
Pwd             = constants.Pwd
Port            = constants.Port

#print(pyodbc.drivers() )

conn = pyodbc.connect('Driver={' + Driver +'};'
                      'Server=' + Server + ';'
                      'Database=' + DatabaseName + ';'
                      'Uid=' + Uid + ';'
                      'Pwd=' + Pwd + ';'
                      'Port=' + Port + ';'
                      'Trusted_Connection=yes;')





#---------------------------------------------------------------------------------------------
#------------------------------------Library functions Start----------------------------
#---------------------------------------------------------------------------------------------

positionFeature     = 'Position'
positionFeatureX    = 'PositionX'
positionFeatureY    = 'PositionY'
positionFeatureZ    = 'PositionZ'
booleanDict         = {'true': True, 'True': True, 'TRUE': True,'false': False, 'False': False, 'FALSE': False}
PlayerShootEndEnemyTypeDict = {'Bear': True, 'bear': True, 'BEAR': True,'Ground': False, 'ground': False, 'GROUND': False}




def read_json(json_data): 
    if (type(json_data) == str):  # For strings 
        return json.loads(json_data) 
    elif (str(type(json_data)) == "<class '_io.TextIOWrapper'>"): #For files 
        return json.load(json_data) 
    elif (type(json_data) == dict): # For dictionaries 
        return json.loads(json.dumps(json_data))


def get_group(g, key):
     if key in g.groups: return g.get_group(key)
     return pd.DataFrame()



#****************************************************************
# Concept extraction !!!!!!!!!
#****************************************************************
conceptFeaturesMap = {
    'hasLoop' : 'hasLoop',
    'hasNestedLoop': 'hasNestedLoop',
    'hasCondition': 'hasCondition',
    'hasVariable': 'hasVariable',
    'lineOfCodeCount': 'countLinesOfCode',
                
    'hasExpressionsArithematic': 'hasExpressionsArithematic', 
    'hasExpressionsBool': 'hasExpressionsBool', 
    'hasExpressionsLogical': 'hasExpressionsLogical', 
    'hasExpressionsUnary': 'hasExpressionsUnary', 
    'hasExpressionsBitwise': 'hasExpressionsBitwise', 
    'hasExpressionsDict': 'hasExpressionsDict', 
    'hasExpressionsDataStructure': 'hasExpressionsDataStructure', 
    'hasControlFlowConditional': 'hasControlFlowConditional', 
    'hasControlFlowTryException': 'hasControlFlowTryException', 
    'hasVariablesNamed': 'hasVariablesNamed',
    'hasConstantsUseful': 'hasConstantsUseful', 
    'hasExpressionsKeyword' : 'hasExpressionsKeyword' ,
    'hasExpressionsFunctionCall' : 'hasExpressionsFunctionCall',
    
    'hasExpressions': 'hasExpressions',
    'hasAsyncOrAwait': 'hasAsyncOrAwait',
    'hasFunctionClass': 'hasFunctionClass',
    'hasControlFlow': 'hasControlFlow',
    'hasImports': 'hasImports',
    'hasStatements': 'hasStatements',
    'hasComprehensions': 'hasComprehensions',
    'hasSubscripting': 'hasSubscripting',
    'hasConstants': 'hasConstants',
    'hasVariables' : 'hasVariables'
}
def getConceptFeaturesFromCodeLines(df, featureCode):
    
    columnsFeatures = []
    dFeature  = []


    for i, j in df.iterrows():
        newFeaturesArrForThisRow = []
        columnsFeatures = []
            
        try:
            codeString = PythonCodeParser( j[featureCode] )
        
            newFeaturesArrForThisRow.append(j['PracticeStatisticsId'])
            columnsFeatures.append('PracticeStatisticsId')

            for featureName in conceptFeaturesMap:
                columnsFeatures.append(featureName)

                functionName = conceptFeaturesMap.get(featureName)

                if hasattr(codeString, functionName):
                    codeStringParsedFunction = getattr(codeString, functionName, None)
                    newFeaturesArrForThisRow.append(  codeStringParsedFunction()  )
                else:
                    newFeaturesArrForThisRow.append( 0 )

            dFeature.append(newFeaturesArrForThisRow)
            
        except SyntaxError:
            dFeature.append( (len(conceptFeaturesMap) + 1) * [0]    )


    dFeature = np.array(dFeature)
    dfFeature = pd.DataFrame(dFeature, columns=columnsFeatures)
    
    return dfFeature



def getConceptFeaturesFromCode(df, featureCode, featureError, featureOutput):
    
    columnsFeatures = []
    dFeature  = []
    newConceptFeatures = list(conceptFeaturesMap.keys())
    
#    add all column names to the list for new features
    columnsFeatures.extend(df.columns)
    columnsFeatures = columnsFeatures + newConceptFeatures



    for i, j in df.iterrows():
        newFeaturesArrForThisRow = []
        
        
        newFeaturesArrForThisRow.extend(j)
            
        if j[featureError] == False :
            
            try:
                codeString = PythonCodeParser( j[featureCode] )

                
                for featureName in conceptFeaturesMap:
                    functionName = conceptFeaturesMap.get(featureName)

                    if hasattr(codeString, functionName):
                        codeStringParsedFunction = getattr(codeString, functionName, None)
                        newFeaturesArrForThisRow.append(  int( codeStringParsedFunction()  )  )
                    else:
                        newFeaturesArrForThisRow.append( 0 )
                
                dFeature.append(newFeaturesArrForThisRow)
                
            except SyntaxError:
                dFeature.append( len(newConceptFeatures) * [0] )
                
        else:
            dFeature.append( len(newConceptFeatures) * [0] )    

    dfFeature = pd.DataFrame.from_records(dFeature,  columns = columnsFeatures )
    
    return dfFeature    


def getDfFromJsonFeature(jsonFeature, df, idFeatures):     

    dFeature  = []
    columnsRuns = []

    for i, j in df.iterrows(): 
        featureDataArr = read_json( j[jsonFeature] )
        for data in featureDataArr:
            
            columnsRuns = []
            runArr = []
            for key in data:
                runArr.append(data[key])
                columnsRuns.append(jsonFeature + '' + key)
            
            for idFeature in idFeatures:
                runArr.append( j[idFeature] )
                columnsRuns.append(idFeature)
            
            dFeature.append(runArr)
    
    
    dFeature = np.array(dFeature)
    dfFeature = pd.DataFrame(dFeature, columns=columnsRuns)
    
#    formatting 
    for idFeature in idFeatures:
        dfFeature.astype({idFeature: int})
        toFormatNumeric(dfFeature, idFeature)
    if 'TheoryStatisticsId' in dfFeature.columns:
        dfFeature.astype({"TheoryStatisticsId": int})
        toFormatNumeric(dfFeature, 'TheoryStatisticsId')
    if 'PracticeStatisticsId' in dfFeature.columns:
        dfFeature.astype({"PracticeStatisticsId": int})
        toFormatNumeric(dfFeature, 'PracticeStatisticsId')
    if 'StudentId' in dfFeature.columns:
        dfFeature.astype({"StudentId": int})
        toFormatNumeric(dfFeature, 'StudentId')

    if jsonFeature + '' + 'Time' in dfFeature.columns:
        toFormatDatetime(dfFeature, jsonFeature + '' + 'Time')
        
    if jsonFeature + '' + 'Damage' in dfFeature.columns:
        toFormatFloat(dfFeature, jsonFeature + '' + 'Damage')
    if jsonFeature + '' + 'Health' in dfFeature.columns:
        toFormatFloat(dfFeature, jsonFeature + '' + 'Health')
    if jsonFeature + '' + positionFeature  in dfFeature.columns:
        dfFeature = getPositionFeatures(dfFeature, jsonFeature)
        dfFeature.drop(jsonFeature + '' + positionFeature, inplace=True, axis=1)
    
    
        
#    drop columns with all null values
    dfFeature = dfFeature.dropna(axis=1, how='all')
        
    return dfFeature


def toFormatDatetime(df, feature):
    try :
         df[feature] = pd.to_datetime(df[feature])
    except Exception as e: 
        print('toFormatDatetime exception in Datetime - Erroneous Date !!! ')


def toFormatNumeric(df, feature):
#    if error, then add NaN for an erroneous value   -   https://stackoverflow.com/questions/15891038/change-data-type-of-columns-in-pandas
    df[feature] = pd.to_numeric(df[feature], errors='coerce')


def toFormatInt(df, feature):
#    if error, then add NaN for an erroneous value   -   https://stackoverflow.com/questions/15891038/change-data-type-of-columns-in-pandas
    df[feature] = df[feature].str.replace(',','.')
    toFormatNumeric(df, feature)
    df[feature] =  df[feature].astype(int)

def toFormatFloat(df, feature):
#    if error, then add NaN for an erroneous value   -   https://stackoverflow.com/questions/15891038/change-data-type-of-columns-in-pandas
    df[feature] = df[feature].str.replace(',','.')
    toFormatNumeric(df, feature)


def toFormatStringToBoolean(df, feature):
    df[feature] = df[feature].map(booleanDict)
    
    
def getPositionFeatures(df, featureName):     

    posX  = []
    posY  = []
    posZ  = []
    
#    since we combine different dataframes- so new features have names with the source featureName
    positionFeatureName = featureName + '' + positionFeature
    positionFeatureXName = featureName + '' + positionFeatureX
    positionFeatureYName = featureName + '' + positionFeatureY
    positionFeatureZName = featureName + '' + positionFeatureZ

    if positionFeatureName in df.columns:
        for i, j in df.iterrows(): 
            featureDataArr = j[positionFeatureName]
            positions = featureDataArr.strip('(').strip(')').split(',')
            
            if (len(positions) >= 0) :
                posX.append(positions[0])
            if (len(positions) > 0) :
                posY.append(positions[1])
            if (len(positions) > 1) :
                posZ.append(positions[2])
                
        df[positionFeatureXName] = posX
        df[positionFeatureYName] = posY
        df[positionFeatureZName] = posZ
        
        toFormatFloat(df, positionFeatureXName)
        toFormatFloat(df, positionFeatureYName)
        toFormatFloat(df, positionFeatureZName)
            
    return df





#-------------------------Panda s function
def convert_list_column_tostr(val):
    separator = ', '
    return separator.join(val)

#----Clustering


def getColorMarkers():
    
    markers = ['.', 'o', 'v', '^', '<', '>', '*', 's', '+', 'x', 'D', 'H', '|', '-']
    markerfacecolors = ['navy', 'seagreen', 'red', 'cyan', 'magenta', 'maroon'
                       ,'darkviolet' , 'green', 'tomato', 'grey', 'mediumturqoise']
    colors = ['skyblue', 'palegreen', 'mistyrose', 'cadetblue', 'pink', 'lightcoral'
             ,'violet' , 'lime', 'tomato', 'lightgrey', 'darkslategray']
    
    return colors, markers, markerfacecolors


#---------------------------------------------------------------------------------------------
#------------------------------------Library functions End------------------------
#---------------------------------------------------------------------------------------------





#-------------------------------------------------------------------------------------
#------------------------------------ DB Queries -------------------------------------
#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#----------------------------------Theroy Part Start-----------------------------------
#---------------------------------------------------------------------------------------------


#
def getTheoryData():
    '''
    Get Theory Students Data.

    Returns:
        Return Theory Students Data, numerical solution data, non numerical solution data.
    '''

    dfDB = pd.read_sql_query('SELECT  '
    
     + ' s.StudentId, s.Name, s.Email, s.IsConsentGiven '
     
     
     + ' , tstat.TheoryStatisticsId , tstat.CreatedAt , tstat.UpdatedAt, tstat.Result '
     + ' , tstat.SessionDuration, tstat.Points, tstat.Answer, tstat.Attempts, tstat.Health '
     + ' , tstat.TaskType, tstat.Map, tstat.Enemies '
     + ' , tstat.PlayerShoot, tstat.PlayerShootEnd, tstat.EnemysShootEnd, tstat.Items '
     
     + ' , ttask.TheoryTaskId, ttask.Title, ttask.Description, ttask.Difficulty, ttask.Solution, ttask.Hint '
     + ' , ttask.Answer1, ttask.Answer2, ttask.ShortDescription '

     + ' , skill.SkillId '
     + ' , c.CourseId, c.User_Id, c.isVisible '
     
     + ' , en.EnrolledId, en.LearningActivity_LearningActivityId '

    
     + '  FROM Students s ' 
     
     
     + '  JOIN TheoryStatistics tstat ON tstat.Student_StudentId = s.studentId ' 
     + '  JOIN TheoryTasks ttask ON ttask.TheoryTaskId = tstat.TheoryTask_TheoryTaskId ' 
     + '  JOIN Skills skill ON skill.SkillId = ttask.Skill_SkillId ' 
     + '  JOIN Courses c ON c.CourseId = skill.Course_CourseId ' 
     + '  JOIN Enrolleds en ON en.Course_CourseId = c.CourseId AND en.Student_StudentId = s.StudentId'  
    
     + '  WHERE s.IsConsentGiven = 1 '
     , conn)
    
    
    dfDB[constants.GROUPBY_FEATURE]                     = dfDB['LearningActivity_LearningActivityId']
    dfDB[constants.GROUPBY_FEATURE].fillna(0, inplace=True)
    dfDB[constants.GROUPBY_FEATURE]    = dfDB[constants.GROUPBY_FEATURE].astype(int)
    dfDB[constants.featureGroup]       = constants.TypeGroup + '-' +  dfDB[constants.GROUPBY_FEATURE].astype(str) 
    
    dfDB.sort_values(['Difficulty','StudentId', 'SkillId', 'TheoryStatisticsId'], 
                   axis=0, 
                   ascending=True, 
                   inplace=True, 
                   kind='quicksort', na_position='last')
    
    
    to_drop = ['Email',
               'Title',
               'Description',
               'Map',               
               'User_Id' ,
               'Hint', 
               'Health', 
               'Answer', 'ShortDescription',               
               'IsConsentGiven'
               ]
    dfDB.drop(to_drop, inplace=True, axis=1)
    
    
    df = dfDB[dfDB['Solution'].str.contains("1|2|3|4|5|6|7|8|9|0")==True]
    
    dfNummericNot = dfDB[~dfDB['Solution'].str.contains("1|2|3|4|5|6|7|8|9|0")==True]
    

    
    return dfDB, df, dfNummericNot


def getTheoryTaskDetails():
    '''
    Get Theory Task details Data.

    Returns:
        Return Theory Task details dataframe
    '''
    
    
    dfTheoryTaskDetails = pd.read_sql_query('SELECT  '
             
     + ' ttask.TheoryTaskId, ttask.Title, ttask.Description, ttask.Difficulty, ttask.Solution, ttask.Hint '
     + ' , ttask.Answer1, ttask.Answer2, ttask.ShortDescription '

     + ' , skill.SkillId '
     + ' , c.CourseId , c.isVisible '
    
     + '  FROM TheoryTasks ttask  ' 
     
     + '  JOIN Skills skill ON skill.SkillId = ttask.Skill_SkillId ' 
     + '  JOIN Courses c ON c.CourseId = skill.Course_CourseId ' 
     , conn)
                    
    return dfTheoryTaskDetails


#---------------------------------------------------------------------------------------------
#----------------------------------Practice Part Start-----------------------------------
#---------------------------------------------------------------------------------------------
def getPracticeData():
    
    dfPractice = pd.read_sql_query('SELECT  '
    
     + ' s.StudentId, s.Name, s.Email, s.IsConsentGiven  '
     + ' , pstat.PracticeStatisticsId , pstat.Result , pstat.Points, pstat.SessionDuration '
     + ' , pstat.Answer, pstat.Attempts, pstat.TaskType, pstat.CreatedAt, pstat.UpdatedAt '
     + ' , pstat.PracticeTask_PracticeTaskId, pstat.Student_StudentId, pstat.Code '
     + ' , pstat.DraggedOptions, pstat.Runs, pstat.Tabs, pstat.DeletedCodes, pstat.Obstacles '
     + ' , pstat.DiskPosition, pstat.RobotCollisions, pstat.Keyboard, pstat.InterfaceButton '
     + ' , pstat.CollectedCoins '
     
     + ' , ptask.PracticeTaskId, ptask.Title, ptask.Description, ptask.Difficulty, ptask.IfEnabled, ptask.VarEnabled '
     + ' , ptask.ForEnabled, ptask.LeftEnabled, ptask.RightEnabled, ptask.UpEnabled, ptask.DownEnabled, ptask.IfMin '
     + ' , ptask.IfMax, ptask.VarMin, ptask.VarMax, ptask.ForMin, ptask.ForMax, ptask.LeftMin, ptask.LeftMax, ptask.RightMin, ptask.RightMax '
     + ' , ptask.UpMin, ptask.UpMax, ptask.DownMin, ptask.DownMax '
     + ' , ptask.Skill_SkillId, ptask.Solution, ptask.PrintEnabled '
     + ' , ptask.ShortDescription, ptask.NumberOfBoxes, ptask.NumberOfCoins, ptask.RobotStorage, ptask.NumberOfHidden ' 
     
     + ' , skill.SkillId '
     + ' , skill.Course_CourseId '
     + ' , c.CourseId, c.User_Id, c.isVisible '
     
     + ' , en.EnrolledId, en.LearningActivity_LearningActivityId '
    
     + '  FROM Students s ' 
     
     
     + '  JOIN PracticeStatistics pstat ON pstat.Student_StudentId = s.studentId ' 
     + '  JOIN PracticeTasks ptask ON ptask.PracticeTaskId = pstat.PracticeTask_PracticeTaskId ' 
     + '  JOIN Skills skill ON skill.SkillId = ptask.Skill_SkillId ' 
     + '  JOIN Courses c ON c.CourseId = skill.Course_CourseId ' 
     + '  JOIN Enrolleds en ON en.Course_CourseId = c.CourseId AND en.Student_StudentId = s.StudentId'  
    
     + '  WHERE s.IsConsentGiven = 1 '
     , conn)
    
    dfPractice[constants.GROUPBY_FEATURE]                     = dfPractice['LearningActivity_LearningActivityId']
    dfPractice[constants.GROUPBY_FEATURE].fillna(0, inplace=True)
    dfPractice[constants.GROUPBY_FEATURE]    = dfPractice[constants.GROUPBY_FEATURE].astype(int)
    dfPractice[constants.featureGroup]       = constants.TypeGroup + '-' +  dfPractice[constants.GROUPBY_FEATURE].astype(str)

    
    dfPractice.sort_values(['Difficulty','StudentId', 'PracticeStatisticsId', 'SkillId'], 
                   axis=0, 
                   ascending=True, 
                   inplace=True, 
                   kind='quicksort', na_position='last')
        
    to_drop2 = [
    #        features with little or no information gain
            'Email'
               , 'IfMin','IfMax','VarMin'
               ,'VarMax','ForMin','ForMax','LeftMin'
               ,'LeftMax','RightMin','RightMax','UpMin'
               ,'UpMax','DownMin','DownMax'
               
               , 'IsConsentGiven'
               ]
    dfPractice.drop(to_drop2, inplace=True, axis=1)
    
    return dfPractice
        
def getPracticeTaskDetails():
    
    dfPracticeTaskDetails = pd.read_sql_query('SELECT  '
                                   
     + ' ptask.PracticeTaskId, ptask.Title, ptask.Description, ptask.Difficulty, ptask.IfEnabled, ptask.VarEnabled '
     + ' , ptask.ForEnabled, ptask.LeftEnabled, ptask.RightEnabled, ptask.UpEnabled, ptask.DownEnabled, ptask.IfMin '
     + ' , ptask.IfMax, ptask.VarMin, ptask.VarMax, ptask.ForMin, ptask.ForMax, ptask.LeftMin, ptask.LeftMax, ptask.RightMin, ptask.RightMax '
     + ' , ptask.UpMin, ptask.UpMax, ptask.DownMin, ptask.DownMax '
     + ' , ptask.Solution, ptask.PrintEnabled '
     + ' , ptask.ShortDescription, ptask.NumberOfBoxes, ptask.NumberOfCoins, ptask.RobotStorage, ptask.NumberOfHidden ' 
    
     + ' , skill.SkillId '
     + ' , c.CourseId, c.isVisible '
     
     + '  FROM PracticeTasks ptask ' 
     
     + '  JOIN Skills skill ON skill.SkillId = ptask.Skill_SkillId ' 
     + '  JOIN Courses c ON c.CourseId = skill.Course_CourseId ' 

     , conn)
                    
    return dfPracticeTaskDetails



def getSkillDetails():
    
    dfSkillDetails = pd.read_sql_query('SELECT  '
                               
     + ' skill.SkillId, skill.Title, skill.Description, skill.CreatedAt , skill.UpdatedAt '
 
     + ', course.CourseId, course.User_Id , course.isVisible '

     + '  FROM Skills skill ' 
 
     + '  JOIN Courses course ON course.CourseId = skill.Course_CourseId ' 
     , conn)
                
    return dfSkillDetails

def getCourseDetails():
    
    dfCourseDetails = pd.read_sql_query('SELECT  '

     + ' course.CourseId, course.Title, course.Description, course.User_Id , course.isVisible, course.CreatedAt , course.UpdatedAt  '
    
     + '  FROM Courses course ' 
     , conn)
                    
    return dfCourseDetails

def getEnrolledDetails():
    
    dfEnrolledDetails = pd.read_sql_query('SELECT  '

     + ' enrol.EnrolledId, enrol.Activated, enrol.Points, enrol.CreatedAt, enrol.UpdatedAt, enrol.LearningActivity_LearningActivityId '
 
     + ', course.CourseId, course.User_Id , course.isVisible '
 
     + ', s.StudentId, s.Name '
    
     + '  FROM Enrolleds enrol ' 
 
     + '  JOIN Courses course  ON course.CourseId = enrol.Course_CourseId ' 
     + '  JOIN Students s   ON s.StudentId = enrol.Student_StudentId ' 
     
     + '  WHERE s.IsConsentGiven = 1 '
     , conn)
    
    
    dfEnrolledDetails[constants.GROUPBY_FEATURE]                     = dfEnrolledDetails['LearningActivity_LearningActivityId']
    dfEnrolledDetails[constants.GROUPBY_FEATURE].fillna(0, inplace=True)
    dfEnrolledDetails[constants.GROUPBY_FEATURE]                     = dfEnrolledDetails[constants.GROUPBY_FEATURE].astype(int)
    
    return dfEnrolledDetails


def getStudentDetails():
    
    dfStudentDetails = pd.read_sql_query('SELECT  '
                                   
     + ' s.StudentId, s.Name, s.Email, s.IsConsentGiven, s.CreatedAt, s.UpdatedAt  ' 
    
     + ' , en.EnrolledId, en.LearningActivity_LearningActivityId, en.Course_CourseId '
     
     
     + '  FROM Students s ' 
     
     + '  JOIN Enrolleds en ON  en.Student_StudentId = s.StudentId'  
     
     + '  WHERE s.IsConsentGiven = 1 '
     , conn)
    
    dfStudentDetails[constants.GROUPBY_FEATURE]                     = dfStudentDetails['LearningActivity_LearningActivityId']
    dfStudentDetails[constants.GROUPBY_FEATURE].fillna(0, inplace=True)
    dfStudentDetails[constants.GROUPBY_FEATURE]                     = dfStudentDetails[constants.GROUPBY_FEATURE].astype(int)
    
    dfStudentDetails[constants.featureGroup]       = constants.TypeGroup + '-' + dfStudentDetails[constants.GROUPBY_FEATURE].astype(str)
                    
    return dfStudentDetails




def getUsers():
    
    dfUserDetails = pd.read_sql_query('SELECT  '
                                   
     + ' u.Id, u.IsAdmin, u.Email, u.PasswordHash, u.UserName, u.SecurityStamp  ' 
    
     + '  FROM AspNetUsers u ' 
     , conn)
                    
    return dfUserDetails

def getUserDetails(usernameOrId):
    
    dfUserDetails = pd.read_sql_query('SELECT  '
                                   
     + ' u.Id, u.IsAdmin, u.Email, u.PasswordHash, u.UserName, u.SecurityStamp  ' 
    
     + '  FROM AspNetUsers u ' 
     
     + '  WHERE u.Email = \'' + usernameOrId + '\'   OR   u.UserName = \'' + usernameOrId + '\'  OR   u.Id = \'' + usernameOrId + '\''
     , conn)
                    
    return dfUserDetails


def getLearningActivityDetails():
    
    dfLearningActivityDetails = pd.read_sql_query('SELECT  '
                                   
     + ' la.LearningActivityId, la.Title, la.Description, la.BeginDate, la.EndDate, la.GroupType, la.SchoolName  '
     + ', la.Grade, la.NrOfParticipants, la.JoinCode, la.Notes, la.User_Id  '
 
     + ', u.Id, u.IsAdmin , u.Email '
     + ', u.UserName , u.PasswordHash '
    
     + '  FROM LearningActivity la ' 
 
     + '  JOIN AspNetUsers u ON u.Id = la.User_Id ' 
     , conn)
                    
    return dfLearningActivityDetails


#---------------------------------------------------------------------------------------------
#------------------------------------ DB Queries END-------------------------------------
#---------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------
#------------------------------------ General Dataframe functions ----------------------------
#---------------------------------------------------------------------------------------------

GROUPBY_FEATURE     = constants.GROUPBY_FEATURE

def getGroupedDataStudent(df):
    return df.groupby(  [df[GROUPBY_FEATURE]] )


def getGroupedData(df):
    return df.groupby(  [df[GROUPBY_FEATURE]] )
  


#---------------------------------------------------------------------------------------------
#------------------------------------ General Dataframe functions END ----------------------------
#---------------------------------------------------------------------------------------------