# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 23:08:32 2020

@author: tilan
"""


#import pyodbc
import numpy as np
import pandas as pd
#import xlwt as xls_write
#import time

from plotly.offline import plot
import plotly.express as px


#main library
from data import main
#from main import PythonParser



# visual libraries
from matplotlib import pyplot as plt
#import seaborn as sns
#from mpl_toolkits.mplot3d import Axes3D 
plt.style.use('ggplot')
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Fixing random state for reproducibility
np.random.seed(19680801)




dfDB, df, dfNummericNot  = main.getTheoryData()



dfTheoryTaskDetails = main.getTheoryTaskDetails()
dfTheoryTaskDetails = dfTheoryTaskDetails.drop_duplicates(subset=['TheoryTaskId'], keep='first')


dfStudentDetails = main.getStudentDetails()
dfStudentDetails = dfStudentDetails.drop_duplicates(subset=['StudentId'], keep='first')



markers = ['.', 'o', 'v', '^', '<', '>', '*', 's', '+', 'x', 'D', 'H', '|', '-']
markerfacecolors = ['navy', 'seagreen', 'red', 'cyan', 'magenta', 'maroon'
                   ,'darkviolet' , 'green', 'tomato', 'grey', 'mediumturqoise']
colors = ['skyblue', 'palegreen', 'mistyrose', 'cadetblue', 'pink', 'lightcoral'
         ,'violet' , 'lime', 'tomato', 'lightgrey', 'darkslategray']

#User understandable Column names
feature2UserNamesDict = {
		"Attempts" : "Task Attempts (avg)"
		,"TheoryStatisticsId" : "Theory Task Id"
		,"Points" : "Points"
		,"SessionDuration" : 'Session Duration'
		,"TaskType" : "Task Type"
		,"enemiesCount" : "No. of Enemies"
		,"playerShootCount" : "No. of time Player shoot"
		,"playerShootEndCount" : "No. of time Player shoot bullet reached end"
		,"playerShootEndEnemyHitCount" : "No. of times Player shoot Enemy"
		,"enemysShootEndPlayerNotHitCount" : "No. of times Enemies shoot missed Player"
		,"enemysShootEndPlayerHitCount" : "No. of times Enemies shoot Player"
		,"itemsCollectedCount" : "No. of Items collected"
	}



groupedSkillStudents = df.groupby(['Difficulty', 'TheoryTaskId', 'SkillId', 'StudentId'])['Attempts'].agg('sum').reset_index()

uniqueTasks = np.array(df['TheoryTaskId'].unique())


#######
#######Data frames of JSON Features - NOT NUMERICAL SOLUTIONS
dfEnemiesNN = main.getDfFromJsonFeature('Enemies', dfNummericNot, ['TheoryStatisticsId', 'StudentId'])
#No of Enemies per session Id
enemiesCountNN = dfEnemiesNN.TheoryStatisticsId.value_counts()


dfPlayerShootNN = main.getDfFromJsonFeature('PlayerShoot', dfNummericNot, ['TheoryStatisticsId', 'StudentId'])
#No of time player shoots per session Id
playerShootCountNN = dfPlayerShootNN.TheoryStatisticsId.value_counts()


dfPlayerShootEndNN = main.getDfFromJsonFeature('PlayerShootEnd', dfNummericNot, ['TheoryStatisticsId', 'StudentId'])
main.toFormatStringToBoolean(dfPlayerShootEndNN, 'PlayerShootEnd'+ '' +'Status')
#No of time player shoot ends per session Id
playerShootEndCountNN = dfPlayerShootEndNN.TheoryStatisticsId.value_counts()
#No of time player shoot end hits Enemy per session Id
playerShootEndEnemyHitCountNN = dfPlayerShootEndNN[dfPlayerShootEndNN.PlayerShootEndEnemyType == 'Bear'].TheoryStatisticsId.value_counts()
#No of time player shoot end missed Enemy per session Id
playerShootEndEnemyMissedHitCountNN = dfPlayerShootEndNN[dfPlayerShootEndNN.PlayerShootEndEnemyType != 'Bear'].TheoryStatisticsId.value_counts()




dfEnemysShootEndNN = main.getDfFromJsonFeature('EnemysShootEnd', dfNummericNot, ['TheoryStatisticsId', 'StudentId'])
main.toFormatStringToBoolean(dfEnemysShootEndNN, 'EnemysShootEnd'+ '' +'Status')
#Helps us understand how well a player can escape enemies - about their controls
#No of time player hit by enemies
enemysShootEndPlayerHitCountNN = dfEnemysShootEndNN[dfEnemysShootEndNN.EnemysShootEndStatus == True].TheoryStatisticsId.value_counts()
#No of times player escaped enemies hit
enemysShootEndPlayerNotHitCountNN = dfEnemysShootEndNN[dfEnemysShootEndNN.EnemysShootEndStatus != True].TheoryStatisticsId.value_counts()



dfItemsNN = main.getDfFromJsonFeature('Items', dfNummericNot, ['TheoryStatisticsId', 'StudentId'])
#No of items collected by player
itemsCollectedCountNN = dfItemsNN.TheoryStatisticsId.value_counts()


#The new Dataframe - to be used for Clusterin algorithms !!! Yaay
dfPlayerStrategyNN = dfNummericNot


countNNDict = enemiesCountNN.to_dict() #converts to dictionary
dfPlayerStrategyNN['enemiesCount'] = dfPlayerStrategyNN['TheoryStatisticsId'].map(countNNDict) 
dfPlayerStrategyNN['enemiesCount'].fillna(0, inplace=True)


countNNDict = playerShootCountNN.to_dict() #converts to dictionary
dfPlayerStrategyNN['playerShootCount'] = dfPlayerStrategyNN['TheoryStatisticsId'].map(countNNDict) 
dfPlayerStrategyNN['playerShootCount'].fillna(0, inplace=True)


countNNDict = playerShootEndCountNN.to_dict() #converts to dictionary
dfPlayerStrategyNN['playerShootEndCount'] = dfPlayerStrategyNN['TheoryStatisticsId'].map(countNNDict) 
dfPlayerStrategyNN['playerShootEndCount'].fillna(0, inplace=True)


countNNDict = playerShootEndEnemyHitCountNN.to_dict() #converts to dictionary
dfPlayerStrategyNN['playerShootEndEnemyHitCount'] = dfPlayerStrategyNN['TheoryStatisticsId'].map(countNNDict) 
dfPlayerStrategyNN['playerShootEndEnemyHitCount'].fillna(0, inplace=True)


countNNDict = playerShootEndEnemyMissedHitCountNN.to_dict() #converts to dictionary
dfPlayerStrategyNN['playerShootEndEnemyMissedHitCount'] = dfPlayerStrategyNN['TheoryStatisticsId'].map(countNNDict) 
dfPlayerStrategyNN['playerShootEndEnemyMissedHitCount'].fillna(0, inplace=True)


countNNDict = enemysShootEndPlayerHitCountNN.to_dict() #converts to dictionary
dfPlayerStrategyNN['enemysShootEndPlayerHitCount'] = dfPlayerStrategyNN['TheoryStatisticsId'].map(countNNDict) 
dfPlayerStrategyNN['enemysShootEndPlayerHitCount'].fillna(0, inplace=True)


countNNDict = enemysShootEndPlayerNotHitCountNN.to_dict() #converts to dictionary
dfPlayerStrategyNN['enemysShootEndPlayerNotHitCount'] = dfPlayerStrategyNN['TheoryStatisticsId'].map(countNNDict) 
dfPlayerStrategyNN['enemysShootEndPlayerNotHitCount'].fillna(0, inplace=True)


countNNDict = itemsCollectedCountNN.to_dict() #converts to dictionary
dfPlayerStrategyNN['itemsCollectedCount'] = dfPlayerStrategyNN['TheoryStatisticsId'].map(countNNDict) 
dfPlayerStrategyNN['itemsCollectedCount'].fillna(0, inplace=True)






#######
#######Data frames of JSON Features  - ONLY NUMERICAL SOLUTIONS
dfEnemiesN = main.getDfFromJsonFeature('Enemies', df, ['TheoryStatisticsId', 'StudentId'])
#No of Enemies per session Id
enemiesCountN = dfEnemiesN.TheoryStatisticsId.value_counts()


dfPlayerShootN = main.getDfFromJsonFeature('PlayerShoot', df, ['TheoryStatisticsId', 'StudentId'])
#No of time player shoots per session Id
playerShootCountN = dfPlayerShootN.TheoryStatisticsId.value_counts()


#Use this - does player attack more enemies Or escapes them Or player strategy
dfPlayerShootEndN = main.getDfFromJsonFeature('PlayerShootEnd', df, ['TheoryStatisticsId', 'StudentId'])
main.toFormatStringToBoolean(dfPlayerShootEndN, 'PlayerShootEnd'+ '' +'Status')
#No of time player shoot ends per session Id
playerShootEndCountN = dfPlayerShootEndN.TheoryStatisticsId.value_counts()
#No of time player shoot end hits Enemy per session Id
playerShootEndEnemyHitCountN = dfPlayerShootEndN[dfPlayerShootEndN.PlayerShootEndEnemyType == 'Bear'].TheoryStatisticsId.value_counts()
#No of time player shoot end missed Enemy per session Id
playerShootEndEnemyMissedHitCountN = dfPlayerShootEndN[dfPlayerShootEndN.PlayerShootEndEnemyType != 'Bear'].TheoryStatisticsId.value_counts()



#Use this - does player escapes enermy attacks Or player strategy
dfEnemysShootEndN = main.getDfFromJsonFeature('EnemysShootEnd', df, ['TheoryStatisticsId', 'StudentId'])
main.toFormatStringToBoolean(dfEnemysShootEndN, 'EnemysShootEnd'+ '' +'Status')
#Helps us understand how well a player can escape enemies - about their controls
#No of time player hit by enemies
enemysShootEndPlayerHitCountN = dfEnemysShootEndN[dfEnemysShootEndN.EnemysShootEndStatus == True].TheoryStatisticsId.value_counts()
#No of times player escaped enemies hit
enemysShootEndPlayerNotHitCountN = dfEnemysShootEndN[dfEnemysShootEndN.EnemysShootEndStatus != True].TheoryStatisticsId.value_counts()




#Use this - does player collect items and explore the landscape OR just reaches goal point!
dfItemsN = main.getDfFromJsonFeature('Items', df, ['TheoryStatisticsId', 'StudentId'])
#No of items collected by player
itemsCollectedCountN = dfItemsN.TheoryStatisticsId.value_counts()




#The new Dataframe - to be used for Clusterin algorithms !!! Yaay
dfPlayerStrategyN = df


countNDict = enemiesCountN.to_dict() #converts to dictionary
dfPlayerStrategyN['enemiesCount'] = dfPlayerStrategyN['TheoryStatisticsId'].map(countNDict) 
dfPlayerStrategyN['enemiesCount'].fillna(0, inplace=True)
dfPlayerStrategyN['enemiesCount'] = dfPlayerStrategyN['enemiesCount'].astype(int)

countNDict = playerShootCountN.to_dict() #converts to dictionary
dfPlayerStrategyN['playerShootCount'] = dfPlayerStrategyN['TheoryStatisticsId'].map(countNDict) 
dfPlayerStrategyN['playerShootCount'].fillna(0, inplace=True)
dfPlayerStrategyN['playerShootCount'] = dfPlayerStrategyN['playerShootCount'].astype(int)

countNDict = playerShootEndCountN.to_dict() #converts to dictionary
dfPlayerStrategyN['playerShootEndCount'] = dfPlayerStrategyN['TheoryStatisticsId'].map(countNDict) 
dfPlayerStrategyN['playerShootEndCount'].fillna(0, inplace=True)
dfPlayerStrategyN['playerShootEndCount'] = dfPlayerStrategyN['playerShootEndCount'].astype(int)

countNDict = playerShootEndEnemyHitCountN.to_dict() #converts to dictionary
dfPlayerStrategyN['playerShootEndEnemyHitCount'] = dfPlayerStrategyN['TheoryStatisticsId'].map(countNDict) 
dfPlayerStrategyN['playerShootEndEnemyHitCount'].fillna(0, inplace=True)
dfPlayerStrategyN['playerShootEndEnemyHitCount'] = dfPlayerStrategyN['playerShootEndEnemyHitCount'].astype(int)

countNDict = playerShootEndEnemyMissedHitCountN.to_dict() #converts to dictionary
dfPlayerStrategyN['playerShootEndEnemyMissedHitCount'] = dfPlayerStrategyN['TheoryStatisticsId'].map(countNDict) 
dfPlayerStrategyN['playerShootEndEnemyMissedHitCount'].fillna(0, inplace=True)
dfPlayerStrategyN['playerShootEndEnemyMissedHitCount'] = dfPlayerStrategyN['playerShootEndEnemyMissedHitCount'].astype(int)

countNDict = enemysShootEndPlayerHitCountN.to_dict() #converts to dictionary
dfPlayerStrategyN['enemysShootEndPlayerHitCount'] = dfPlayerStrategyN['TheoryStatisticsId'].map(countNDict) 
dfPlayerStrategyN['enemysShootEndPlayerHitCount'].fillna(0, inplace=True)
dfPlayerStrategyN['enemysShootEndPlayerHitCount'] = dfPlayerStrategyN['enemysShootEndPlayerHitCount'].astype(int)

countNDict = enemysShootEndPlayerNotHitCountN.to_dict() #converts to dictionary
dfPlayerStrategyN['enemysShootEndPlayerNotHitCount'] = dfPlayerStrategyN['TheoryStatisticsId'].map(countNDict) 
dfPlayerStrategyN['enemysShootEndPlayerNotHitCount'].fillna(0, inplace=True)
dfPlayerStrategyN['enemysShootEndPlayerNotHitCount'] = dfPlayerStrategyN['enemysShootEndPlayerNotHitCount'].astype(int)

countNDict = itemsCollectedCountN.to_dict() #converts to dictionary
dfPlayerStrategyN['itemsCollectedCount'] = dfPlayerStrategyN['TheoryStatisticsId'].map(countNDict) 
dfPlayerStrategyN['itemsCollectedCount'].fillna(0, inplace=True)
dfPlayerStrategyN['itemsCollectedCount'] = dfPlayerStrategyN['itemsCollectedCount'].astype(int)







#drop all JSON features - to clear data / drop for clustering analysis
to_dropAfter = [           
#           JSON Features - extracted to new data frames           
          'Enemies', 'PlayerShoot', 'PlayerShootEnd', 'EnemysShootEnd' 
           ]


#Player strategy - drop unwanted features
dfPlayerStrategyNN.drop(to_dropAfter, inplace=True, axis=1)
dfPlayerStrategyN.drop(to_dropAfter, inplace=True, axis=1)



#convert not int to int 
featuresToInt = ['enemiesCount', 'playerShootCount', 'playerShootEndCount'
              , 'playerShootEndEnemyHitCount', 'playerShootEndEnemyMissedHitCount', 'enemysShootEndPlayerHitCount', 'enemysShootEndPlayerNotHitCount'
              , 'itemsCollectedCount']

dfPlayerStrategyNN[featuresToInt] = dfPlayerStrategyNN[featuresToInt].astype(int)
dfPlayerStrategyN[featuresToInt] = dfPlayerStrategyN[featuresToInt].astype(int)


#*****************************************************************************
#STEP 0 : group data . by date or courseId, group of students of same school
#*****************************************************************************
def getGroupedData(df):
    #plot for these - grouped with Year, Month !!!
    #return df.groupby(  [df['CreatedAt'].dt.year, df['CreatedAt'].dt.month]  )
    #other option - grouped by date
#    return df.groupby(  [df['CreatedAt'].dt.date] )
    return df.groupby(  [df['GroupId']] )
     


dfGroupedNN = getGroupedData(dfPlayerStrategyNN)
dfGroupedN = getGroupedData(dfPlayerStrategyN)



rowlength = dfGroupedNN.ngroups/2                         # fix up if odd number of groups

countSubPlots = 0

for groupKey, group in dfGroupedNN:
    entries = group.size
    columns = len(group.columns)
    groupSize = entries/columns

    if int(groupSize) > 10:    
        countSubPlots = countSubPlots + 1


#*************************************************************
#STEP 1 : Plot of varios features with information
#*************************************************************
featurePairsToPlot = [
        ['SessionDuration', 'StudentId']        
        ,['playerShootEndEnemyHitCount', 'StudentId']
        ]



#----------------------------------------
# class data

featurePairsToPlot = [
        ['SessionDuration', 'Name']        
        ,
        ['playerShootEndEnemyHitCount', 'Name']
        ]
