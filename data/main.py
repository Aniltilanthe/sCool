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


#https://datatofish.com/how-to-connect-python-to-sql-server-using-pyodbc/

#imputer = Imputer(missing_values = "NaN", strategy = "mean", axis = 0)
imputer = impu.SimpleImputer(missing_values = "NaN", strategy = "mean")


DatabaseName = 'sCool-2020-05-28'

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost\SQLEXPRESS;'
                      'Database='+ DatabaseName +';'
                      'Trusted_Connection=yes;')





#------------------------------------Library functions Start----------------------------

positionFeature     = 'Position'
positionFeatureX    = 'PositionX'
positionFeatureY    = 'PositionY'
positionFeatureZ    = 'PositionZ'
booleanDict         = {'true': True, 'True': True, 'TRUE': True,'false': False, 'False': False, 'FALSE': False}
PlayerShootEndEnemyTypeDict = {'Bear': True, 'bear': True, 'BEAR': True,'Ground': False, 'ground': False, 'GROUND': False}




def executeSQL(sqlQuery):    
    df = pd.read_sql_query(sqlQuery, conn)
    return df


def read_json(json_data): 
    if (type(json_data) == str):  # For strings 
        return json.loads(json_data) 
    elif (str(type(json_data)) == "<class '_io.TextIOWrapper'>"): #For files 
        return json.load(json_data) 
    elif (type(json_data) == dict): # For dictionaries 
        return json.loads(json.dumps(json_data))





#Clean a Dataframe - removing null columns, rows, formatting etc...
def cleanDfForClustering(df):
    
#    clustering algo only accepts numerical, boolean features !
#    df = df.select_dtypes([np.number, np.bool])
    df = df.select_dtypes([np.number])
    
#    drop columns with all null values
    df = df.dropna(axis=1, how='all')
    
#    drop rows with null values
    df = df.dropna()
    
    
#    df = normalizeData(df)
    
    return df


def normalizeData(df):
#    normalize only numerical features
    num_cols = df.columns[df.dtypes.apply(lambda c: np.issubdtype(c, np.number))]
    return   ( df[num_cols] - df[num_cols].min() )  /  (df[num_cols].max() - df[num_cols].min())



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
            codeString = PythonParser( j[featureCode] )
        
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
                codeString = PythonParser( j[featureCode] )

                
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
            print('toFormatDatetime 1 ')
            print(e)


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




def removeCorrelatedFeatures(data):
    corr = data.corr()
    columns = np.full((corr.shape[0],), True, dtype=bool)
    for i in range(corr.shape[0]):
        for j in range(i+1, corr.shape[0]):
            if corr.iloc[i,j] >= 0.9:
                if columns[j]:
                    columns[j] = False
    selected_columns = data.columns[columns]
#    data = data[selected_columns]
    return selected_columns


def backwardElimination(x, Y, sl, columns):
    numVars = len(x[0])
    for i in range(0, numVars):
        regressor_OLS = sm.OLS(Y, x).fit()
        maxVar = max(regressor_OLS.pvalues).astype(float)
        if maxVar > sl:
            for j in range(0, numVars - i):
                if (regressor_OLS.pvalues[j].astype(float) == maxVar):
                    x = np.delete(x, j, 1)
                    columns = np.delete(columns, j)
                    
    regressor_OLS.summary()
    return x, columns


def calculateConceptComplexityPoints(df, featureCode, featureError, featureOutput):
    pointsLoop = 2
    pointsLogic = 1
    
    df[featureOutput] = 0
    df[featureOutput] = df[df[featureCode].str.contains("for ") & (df[featureError] == False ) ][featureOutput] + pointsLoop
    df[featureOutput].fillna(0, inplace=True)
    df[featureOutput] = df[df[featureCode].str.contains("if ") & (df[featureError] == False ) ][featureOutput] + pointsLogic
    df[featureOutput].fillna(0, inplace=True)
    
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


#------------------------------------Library functions End------------------------



#----------------------------------Theroy Part Start-----------------------------------
    
    
#------------------------------------ DB Queries -------------------------------------


def getTheoryData():
    

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

    
     + '  FROM [' + DatabaseName +'].[dbo].[Students] s ' 
     
     
     + '  JOIN [' + DatabaseName +'].[dbo].[TheoryStatistics] tstat ON tstat.Student_StudentId = s.studentId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[TheoryTasks] ttask ON ttask.TheoryTaskId = tstat.TheoryTask_TheoryTaskId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[Skills] skill ON skill.SkillId = ttask.Skill_SkillId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[Courses] c ON c.CourseId = skill.Course_CourseId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[Enrolleds] en ON en.Course_CourseId = c.CourseId AND en.Student_StudentId = s.StudentId'  
    
     + '  WHERE s.IsConsentGiven = 1 '
     , conn)
    
    
    dfDB[constants.GROUPBY_FEATURE]                     = dfDB['LearningActivity_LearningActivityId']
    dfDB[constants.GROUPBY_FEATURE].fillna(0, inplace=True)
    dfDB[constants.GROUPBY_FEATURE]    = dfDB[constants.GROUPBY_FEATURE].astype(int)
    dfDB[constants.featureGroup]       = constants.TypeGroup + '-' + dfDB[constants.GROUPBY_FEATURE].astype(str) 
    
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
    
    dfTheoryTaskDetails = pd.read_sql_query('SELECT  '
             
     + ' ttask.TheoryTaskId, ttask.Title, ttask.Description, ttask.Difficulty, ttask.Solution, ttask.Hint '
     + ' , ttask.Answer1, ttask.Answer2, ttask.ShortDescription '

     + ' , skill.SkillId '
     + ' , c.CourseId , c.isVisible '
    
     + '  FROM [' + DatabaseName +'].[dbo].[TheoryTasks] ttask  ' 
     
     + '  JOIN [' + DatabaseName +'].[dbo].[Skills] skill ON skill.SkillId = ttask.Skill_SkillId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[Courses] c ON c.CourseId = skill.Course_CourseId ' 
     , conn)
                    
    return dfTheoryTaskDetails


#----------------------------------Practice Part Start-----------------------------------
    
    
#------------------------------------ DB Queries -------------------------------------
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
    
     + '  FROM [' + DatabaseName +'].[dbo].[Students] s ' 
     
     
     + '  JOIN [' + DatabaseName +'].[dbo].[PracticeStatistics] pstat ON pstat.Student_StudentId = s.studentId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[PracticeTasks] ptask ON ptask.PracticeTaskId = pstat.PracticeTask_PracticeTaskId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[Skills] skill ON skill.SkillId = ptask.Skill_SkillId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[Courses] c ON c.CourseId = skill.Course_CourseId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[Enrolleds] en ON en.Course_CourseId = c.CourseId AND en.Student_StudentId = s.StudentId'  
    
     + '  WHERE s.IsConsentGiven = 1 '
     , conn)
    
    dfPractice[constants.GROUPBY_FEATURE]                     = dfPractice['LearningActivity_LearningActivityId']
    dfPractice[constants.GROUPBY_FEATURE].fillna(0, inplace=True)
    dfPractice[constants.GROUPBY_FEATURE]    = dfPractice[constants.GROUPBY_FEATURE].astype(int)
    dfPractice[constants.featureGroup]       = constants.TypeGroup + '-' + dfPractice[constants.GROUPBY_FEATURE].astype(str) 

    
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
     
     + '  FROM [' + DatabaseName +'].[dbo].[PracticeTasks] ptask ' 
     
     + '  JOIN [' + DatabaseName +'].[dbo].[Skills] skill ON skill.SkillId = ptask.Skill_SkillId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[Courses] c ON c.CourseId = skill.Course_CourseId ' 

     , conn)
                    
    return dfPracticeTaskDetails



def getSkillDetails():
    
    dfSkillDetails = pd.read_sql_query('SELECT  '
                               
     + ' skill.SkillId, skill.Title, skill.Description, skill.CreatedAt , skill.UpdatedAt '
 
     + ', course.CourseId, course.User_Id , course.isVisible '

     + '  FROM [' + DatabaseName +'].[dbo].[Skills] skill ' 
 
     + '  JOIN [' + DatabaseName +'].[dbo].[Courses] course ON course.CourseId = skill.Course_CourseId ' 
     , conn)
                
    return dfSkillDetails

def getCourseDetails():
    
    dfCourseDetails = pd.read_sql_query('SELECT  '

     + ' course.CourseId, course.Title, course.Description, course.User_Id , course.isVisible, course.CreatedAt , course.UpdatedAt  '
    
     + '  FROM [' + DatabaseName +'].[dbo].[Courses] course ' 
     , conn)
                    
    return dfCourseDetails

def getEnrolledDetails():
    
    dfEnrolledDetails = pd.read_sql_query('SELECT  '

     + ' enrol.EnrolledId, enrol.Activated, enrol.Points, enrol.CreatedAt, enrol.UpdatedAt '
 
     + ', course.CourseId, course.User_Id , course.isVisible '
 
     + ', s.StudentId, s.Name '
     
     + ', la.LearningActivityId, la.Title, la.Description, la.BeginDate, la.EndDate, la.GroupType, la.SchoolName  '
     + ', la.Grade, la.NrOfParticipants, la.JoinCode, la.Notes, la.User_Id  '
    
     + '  FROM [' + DatabaseName +'].[dbo].[Enrolleds] enrol ' 
 
     + '  JOIN [' + DatabaseName +'].[dbo].[Courses] course  ON course.CourseId = enrol.Course_CourseId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[Students] s   ON s.StudentId = enrol.Student_StudentId ' 
     + '  JOIN [' + DatabaseName +'].[dbo].[LearningActivity] la  ON la.LearningActivityId = enrol.LearningActivity_LearningActivityId ' 
     
     + '  WHERE s.IsConsentGiven = 1 '
     , conn)
                    
    return dfEnrolledDetails


def getStudentDetails():
    
    dfStudentDetails = pd.read_sql_query('SELECT  '
                                   
     + ' s.StudentId, s.Name, s.Email, s.IsConsentGiven, s.CreatedAt, s.UpdatedAt  ' 
    
     + ' , en.EnrolledId, en.LearningActivity_LearningActivityId, en.Course_CourseId '
     
     
     + '  FROM [' + DatabaseName +'].[dbo].[Students] s ' 
     
     + '  JOIN [' + DatabaseName +'].[dbo].[Enrolleds] en ON  en.Student_StudentId = s.StudentId'  
     
     + '  WHERE s.IsConsentGiven = 1 '
     , conn)
    
    dfStudentDetails[constants.GROUPBY_FEATURE]                     = dfStudentDetails['LearningActivity_LearningActivityId']
    dfStudentDetails[constants.GROUPBY_FEATURE].fillna(0, inplace=True)
    dfStudentDetails[constants.GROUPBY_FEATURE]    = dfStudentDetails[constants.GROUPBY_FEATURE].astype(int)
    dfStudentDetails[constants.featureGroup]       = constants.TypeGroup + '-' + dfStudentDetails[constants.GROUPBY_FEATURE].astype(str) 
                    
    return dfStudentDetails




def getUsers():
    
    dfUserDetails = pd.read_sql_query('SELECT  '
                                   
     + ' u.Id, u.IsAdmin, u.Email, u.PasswordHash, u.UserName ' 
    
     + '  FROM [' + DatabaseName +'].[dbo].[AspNetUsers] u ' 
     , conn)
                    
    return dfUserDetails

def getUserDetails(usernameOrId):
    
    dfUserDetails = pd.read_sql_query('SELECT  '
                                   
     + ' u.Id, u.IsAdmin, u.Email, u.PasswordHash, u.UserName ' 
    
     + '  FROM [' + DatabaseName +'].[dbo].[AspNetUsers] u ' 
     
     + '  WHERE u.Email = \'' + usernameOrId + '\'   OR   u.UserName = \'' + usernameOrId + '\'  OR   u.Id = \'' + usernameOrId + '\''
     , conn)
                    
    return dfUserDetails


def getLearningActivityDetails():
    
    dfLearningActivityDetails = pd.read_sql_query('SELECT  '
                                   
     + ' la.LearningActivityId, la.Title, la.Description, la.BeginDate, la.EndDate, la.GroupType, la.SchoolName  '
     + ', la.Grade, la.NrOfParticipants, la.JoinCode, la.Notes, la.User_Id  '
 
     + ', u.Id, u.IsAdmin , u.Email '
     + ', u.UserName , u.PasswordHash '
    
     + '  FROM [' + DatabaseName +'].[dbo].[LearningActivity] la ' 
 
     + '  JOIN [' + DatabaseName +'].[dbo].[AspNetUsers] u ON u.Id = la.User_Id ' 
     , conn)
                    
    return dfLearningActivityDetails

#------------------------------------ General Dataframe functions ----------------------------

GROUPBY_FEATURE     = constants.GROUPBY_FEATURE

def getGroupedDataStudent(df):
    #plot for these - grouped with Year, Month !!!
    #return df.groupby(  [df['CreatedAt'].dt.year, df['CreatedAt'].dt.month]  )
    #other option - grouped by date
#    return df.groupby(  [ df['CreatedAt'].dt.date ] )
    return df.groupby(  [df[GROUPBY_FEATURE]] )


def getGroupedData(df):
#    return df.groupby(  [df['CreatedAt'].dt.date] )
    return df.groupby(  [df[GROUPBY_FEATURE]] )
  
#---------------------------------- Code Parser ----------------------------------------------

def hasRecursion(expr):
    tree = ast.parse(expr, mode="exec")

    tree = resolve_negative_literals(tree)

    for node in [n for n in ast.walk(tree)]:
            if isinstance(node, (ast.For, ast.While)):
                for nodeChild in ast.iter_child_nodes(node):
                    if isinstance(nodeChild, (ast.For, ast.While)):
                        return True
    return False


def hasLoop(expr):
    tree = ast.parse(expr, mode="exec")

    tree = resolve_negative_literals(tree)

    for node in [n for n in ast.walk(tree)]:
            if isinstance(node, (ast.For, ast.While)):
                return True
    return False


def hasConditions(expr):
    tree = ast.parse(expr, mode="exec")

    tree = resolve_negative_literals(tree)

    for node in [n for n in ast.walk(tree)]:
            if isinstance(node, (ast.If)):
                return True
    return False


def resolve_negative_literals(_ast):

    class RewriteUnaryOp(ast.NodeTransformer):
        def visit_UnaryOp(self, node):
            if isinstance(node.op, ast.USub) and isinstance(node.operand, ast.Num):
                node.operand.n = 0 - node.operand.n
                return node.operand
            else:
                return node

    return RewriteUnaryOp().visit(_ast)


def countOfLines(stringExpr):
    return stringExpr.count('\n')



def getAllNodeTypes(expr):    
    try:
      parser = PythonParser(expr)
      return parser.nodeTypes
    except:
      return ''

def getAllNodeTypesUsefull(expr):    
    try:
      parser = PythonParser(expr)
      return parser.nodeTypesUsefull
    except:
      return ''



ProgramConceptsExpressions = [
#        'Expr'
#        
#        , 
 
            'UnaryOp', 'UAdd', 'USub' ,
         'Not', 'Invert', 'BinOp' ,
         'Add' , 'Sub', 'Mult' , 'Div', 'FloorDiv'  ,
         'Mod' , 'Pow'  ,
         'LShift' , 'RShift' ,
         'BitOr' , 'BitXor' , 'BitAnd' ,
         'MatMult' , 'BoolOp' ,
        
         'And' , 'Or' , 'Compare'  , 'Eq' ,
         'NotEq' , 'Lt'  , 'LtE' , 'Gt' , 'GtE' ,
         'Is' , 'IsNot'  ,
         'In' , 'NotIn' ,
        
         'Call' , 'keyword' , 'IfExp',        
        ]


ProgramConceptsSubscripting = [
        'Subscript' ,
        'Slice' ,
        ]

ProgramConceptsComprehensions = [
        'ListComp' ,
        'SetComp' , 'GeneratorExp', 'DictComp', 'comprehension'      ,   
        ]

ProgramConceptsStatements = [
        'Assign' ,
        'AnnAssign' , 'AugAssign', 'Raise', 'Assert', 'Delete', 'Pass' ,
        ]

ProgramConceptsImports = [
        'Import' ,
        'ImportFrom' , 'alias' ,
        ]
ProgramConceptsControlFlow = [
        'If' ,
        'For' , 'While', 'Break', 'Continue', 'Try', 'ExceptHandler'  ,      
        'With' , 'withitem' ,
        ]
ProgramConceptsFunctionClass  = [
        'FunctionDef'  ,
        'Lambda' , 'arguments', 'arg', 'Return', 'Yield', 'YieldFrom'   ,      
        'Global' , 'Nonlocal',
        
        'ClassDef'
        ]

ProgramConceptsAsync   = [
        'AsyncFunctionDef'    ,     
        'Await' , 'AsyncFor', 'AsyncWith'
        ]

ProgramConceptsVariables   = [
#        'Name' ,
#        , 'Load' 
        'Store', 'Del' , 'Starred' ,
        ]
    
ProgramConstants   = [
        'Constant'
        , 'FormattedValue' , 'JoinedStr', 'Str' , 'List' , 'Tuple' , 'Set' , 'Dict'
        ]



ProgramConceptsUsefull = [

                   'BitAnd', 'BitOr', 'BitXor', 'BoolOp', 'LShift', 'BoolOp', 'UAdd', 'USub', 'UnaryOp',
                   'Add', 'Div', 'Gt',  'GtE', 'Is',  'IsNot','Lt',  'LtE', 'MatMult',  'Mult',   'NotEq',  'NotIn', 'Sub', 
                   'And', 'Or', 'Not',
                   'Assert', 'Break', 'Compare', 'Constant', 'Del', 'Delete', 'If', 'IfExp',  'In',  'While',  
                   'ClassDef', 'Dict', 'FunctionDef', 'Global', 'List', 'ListComp', 'Mod', 
#                   'Module',  
                   'Param',  'Return', 'Set', 
                   'Continue', 'For', 
                   'ExceptHandler',  'Import', 'Invert', 'JoinedStr', 'NameConstant',  'Try',
                   'Num', 'Str', 'Expression', 'Import', 'Invert', 'JoinedStr',
                   
                   'Assign' , 'AugAssign' , 'AnnAssign'    ,
                   ]


ProgramConceptsUsefull = ( ProgramConceptsUsefull + ProgramConceptsExpressions + ProgramConceptsAsync
                          + ProgramConceptsFunctionClass + ProgramConceptsControlFlow + ProgramConceptsImports + ProgramConceptsStatements
                          + ProgramConceptsComprehensions + ProgramConceptsSubscripting 
                          + ProgramConceptsVariables + ProgramConstants)

ProgramConceptsUsefull = set(ProgramConceptsUsefull)
ProgramConceptsUsefull = list(ProgramConceptsUsefull)



#-----------------------------------------------------------------------------------------
# PYTHON CODE PARSER
#----------------------------------------------------------------------------------------
class PythonParser:
    def __init__(self, expr):
        self.expr = expr
        self.tree = ast.parse(self.expr, mode="exec")
        self.tree = resolve_negative_literals(self.tree)
        
#        count lines of code
        self.countLineOfCode = 0
        
#        node types  - create an empty set and fill it
        self.nodeTypes = {''}
        self.nodeTypes = self.getAllNodeTypes()
        self.nodeTypesUsefull = list(self.nodeTypes.intersection(ProgramConceptsUsefull))
        
    
# 1 :   Common programming concepts
    def hasLoop(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.For, ast.While)):
                    return True
        return False
    
    def hasNestedLoop(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.For, ast.While)):
                    for nodeChild in ast.iter_child_nodes(node):
                        if isinstance(nodeChild, (ast.For, ast.While)):
                            return True
        return False

    def hasCondition(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.If)):
                    return True
        return False

    def hasVariable(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Store, ast.NameConstant,   ast.Starred  )):
                    return True
        return False
    
    
    def hasRecursion(self):
        
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.For, ast.While)):
                    for nodeChild in ast.iter_child_nodes(node):
                        if isinstance(nodeChild, (ast.For, ast.While)):
                            return True
        return False
    
    
    def resolve_negative_literals(_ast):
    
        class RewriteUnaryOp(ast.NodeTransformer):
            def visit_UnaryOp(self, node):
                if isinstance(node.op, ast.USub) and isinstance(node.operand, ast.Num):
                    node.operand.n = 0 - node.operand.n
                    return node.operand
                else:
                    return node
    
        return RewriteUnaryOp().visit(_ast)
    
    
# 2 :   Lines of Code
    
    def countLinesOfCode(self):
        self.countLineOfCode  = countOfLines(self.expr)
        return self.countLineOfCode

    def visit(self):
        self.node_count += 1
        try:
            
            self.line_numbers2 = self.tree.lineno
            self.line_numbers.add(self.tree.lineno)
        except AttributeError:
            pass
        self.visit(self.tree)

    @property
    def density(self):
        """The density of code (nodes per line) in the visited AST."""
        return self.node_count / len(self.line_numbers)
    
    
# 3 :   All Node types - all concepts used
    
    def getAllNodeTypes(self):    
        for node in [n for n in ast.walk(self.tree)]:
            self.nodeTypes.add( node.__class__.__name__ )
            
        return self.nodeTypes


# 4.1 Subset programming concepts Classes
    def hasExpressionsArithematic(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Add,  ast.Sub,  ast.Mult,  ast.Div,  ast.FloorDiv,  ast.Mod,  ast.Pow )):
                    return True
        return False

    def hasExpressionsBool(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (  ast.And,  ast.Or )):
                    return True
        return False

    def hasExpressionsLogical(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Compare,  ast.Eq,  ast.NotEq,  ast.Lt
                                     ,  ast.LtE,  ast.Gt,  ast.GtE,  ast.Is,  ast.IsNot,  ast.In,  ast.NotIn )):
                    return True
        return False
   
    def hasExpressionsUnary(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.UnaryOp, ast.Not,  ast.Invert
                                     ,  ast.UAdd ,  ast.USub  )):
                    return True
        return False
    
    def hasExpressionsBitwise(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (  ast.LShift,  ast.RShift,  ast.BitOr,  ast.BitXor,  ast.BitAnd,  ast.MatMult
                                     ,  ast.BoolOp )):
                    return True
        return False

    def hasExpressionsDict(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Dict )):
                    return True
        return False

    def hasExpressionsDataStructure(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Dict, ast.List, ast.Set )):
                    return True
        return False

    def hasExpressionsKeyword(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.keyword )):
                    return True
        return False

    def hasExpressionsFunctionCall(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Call )):
                    return True
        return False
    
    def hasControlFlowConditional(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.If,  ast.Break,  ast.Continue
                                     , ast.With,  ast.withitem )):
                    return True
        return False

    def hasControlFlowTryException(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Try,  ast.ExceptHandler )):
                    return True
        return False

    def hasVariablesNamed(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Name,   ast.NameConstant,  ast.Starred ,  )):
                    return True
        return False

    def hasConstantsUseful(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Constant, ast.FormattedValue, ast.JoinedStr, ast.Str,
                                     ast.NameConstant, ast.Num )):
                    return True
        return False


# 4 :   Generic programming concepts Classes
    def hasExpressions(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.Expr,  ast.UnaryOp,  ast.UAdd,  ast.USub,  ast.Not,  ast.Invert
                                     ,  ast.BinOp,  ast.Add,  ast.Sub,  ast.Mult,  ast.Div,  ast.FloorDiv,  ast.Mod,  ast.Pow
                                     ,  ast.LShift,  ast.RShift,  ast.BitOr,  ast.BitXor,  ast.BitAnd,  ast.MatMult
                                     ,  ast.BoolOp,  ast.And,  ast.Or,  ast.Compare,  ast.Eq,  ast.NotEq,  ast.Lt
                                     ,  ast.LtE,  ast.Gt,  ast.GtE,  ast.Is,  ast.IsNot,  ast.In,  ast.NotIn,  ast.Call
                                     ,  ast.keyword,  ast.IfExp,  ast.Attribute)):
                    return True
        return False

    def hasAsyncOrAwait(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.AsyncFunctionDef,  ast.Await,  ast.AsyncFor,  ast.AsyncWith)):
                    return True
        return False
    

    def hasFunctionClass(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (ast.FunctionDef,  ast.Lambda,  ast.arguments,  ast.arg,  ast.Return,  ast.Yield,  ast.YieldFrom,  ast.Global,  ast.Nonlocal,  ast.ClassDef)):
                    return True
        return False

    def hasControlFlow(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.If,  ast.For,  ast.While,  ast.Break,  ast.Continue
                                     ,  ast.Try,  ast.ExceptHandler,  ast.With,  ast.withitem )):
                    return True
        return False
    
    
    def hasImports(self):
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Import,  ast.ImportFrom,  ast.alias )):
                    return True
        return False

    def hasStatements(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Assign,  ast.AnnAssign,  ast.AugAssign,  ast.Raise
                                     ,  ast.Assert,  ast.Delete,  ast.Pass )):
                    return True
        return False
    
    def hasComprehensions(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (  ast.ListComp,  ast.SetComp,  ast.GeneratorExp,  ast.DictComp,  ast.comprehension )):
                    return True
        return False
    
    def hasSubscripting(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, (  ast.Subscript,  ast.Slice )):
                    return True
        return False

    
    def hasConstants(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Constant, ast.FormattedValue, ast.JoinedStr, ast.Str, ast.NameConstant, ast.Num
                                     , ast.List  ,   ast.Tuple ,  ast.Set, ast.Dict  )):
                    return True
        return False

    def hasVariables(self):    
        for node in [n for n in ast.walk(self.tree)]:
                if isinstance(node, ( ast.Name, ast.Load, ast.Store
                                     , ast.Del  ,   ast.Starred  )):
                    return True
        return False
    
    
#e.g.
#expr="""
#for i in 3:
#   print (i)
#   for j in i:
#        print(j)
#        for k in i:
#            print(k)
#"""
#stf = PythonParser(dfRuns[dfRuns['RunsCode'].str.contains("for") & (dfRuns.RunsError == False ) ]['RunsCode'].iloc[1])
#
#print(stf.hasRecursion())
