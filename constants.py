# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 22:42:22 2020

@author: tilan
"""


#--------------------------------------------------------------------------------
#-------------------------------- STYLES START -----------------------------------
# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
}

THEME = "theme-cyan"

THEME_COLOR_MAP = {
        "theme-cyan": '#3aaab2'
}
THEME_CYAN_COLOR = ''
if THEME in THEME_COLOR_MAP.keys():    
    THEME_CYAN_COLOR = THEME_COLOR_MAP.get(THEME)
else :
    THEME_CYAN_COLOR = "white"


ERROR_COLOR = "#FF4136"
#-------------------------------- STYLES END -----------------------------------
THEME_CYAN_EXPRESS_LAYOUT = {
    "plot_bgcolor"      : 'rgb(243, 243, 243)',
    "paper_bgcolor"     : 'rgb(243, 243, 243)',
}
THEME_TABLE_HEADER_STYLE = {
    'backgroundColor'   : 'rgb(230, 230, 230)',
    'fontWeight'        : 'bold'
}

#---------------------------------------------------------------------------------
#--------------------------------------------------------------------------------


GROUPBY_FEATURE         =  'GroupId'
COUNT_STUDENT_FEATURE   =  'CountOfStudents'
STUDENT_ID_FEATURE      =  'StudentId'
TASK_TYPE_FEATURE       =  'TaskType'


#------------------- feature related START -----------------------------------------------
countStudentCompletingTaskFeature   = "No. of Students Completing Task"
countTaskCompletedByStudentFeature  = "No. of Tasks Completed"
featurePracticeTaskDesc             = "PracticeTaskDesc"
featureTheoryTaskDesc               = "TheoryTaskDesc"
featureTaskDesc                     = "TaskDesc"
featureTaskType                     = "TaskType"
featureDescription                  = "Description"
featureConceptsUsedDetails          = "ConceptsUsedDetails"
featureConceptsUsedDetailsStr       = "ConceptsUsedDetailsStr"
featureItemsCollectedCount          = "itemsCollectedCount"
featurePlayerShootEndEnemyHitCount  = "playerShootEndEnemyHitCount"
featureRobotCollisionsBoxCount      = "robotCollisionsBoxCount"
featureLineOfCodeCount              = "lineOfCodeCount"

TaskTypePractice                    = "Practice"
TaskTypeTheory                      = "Theory "






#User understandable Column names
feature2UserNamesDict = {
		"Attempts" : "Attempts (total)"
		,"PracticeTaskId" : "Practice Task Id"
		,"Points" : "Points"
		,"ConceptsUsed" : 'Concept Used'
		,"studentTaskCount" : "No. of Tasks performed"
		,"studentAttemptsTotal" : "Attempts (total)"
		,featureRobotCollisionsBoxCount : "Robot Collision Box (No. of times)"
		,"CollectedCoins" :  "Coins Collected"
		,"coinCollectedCount" : "Coins Collected"
		,"keyboardKeyPressedCount" : "Keyboard Key Pressed (No. of times)"
		,"deletedCodesCount" : "Deleted Codes (No. of times)"
		,"tabsSwitchedCodeCount" : "Switched Tabs (No. of times)"
		,"tabsSwitchedDescriptionCount" : "Switched to read Description (No. of times)"
		,"tabsSwitchedCount" : "Switched tabs (No. of times)"
		,"draggedCount" : "Dragged (No. of times)"
		,"NumberOfBoxes" : "No. of Boxes"
		,"NumberOfCoins" : "No. of Coins"
		,"NumberOfHidden" : "No. of Hidden items"
		,featureLineOfCodeCount : "Count of Lines of Code"
		,"runsLineOfCodeCountAvg" : "Avg. Count of Lines of Code"   
        ,featureConceptsUsedDetailsStr : "Concepts used details"
        ,"StudentId" : "StudentId"
        
		,"runsErrorAttribiteCount" : "Attribute Errors in Code (No. of times)"
		,"runsErrorTypeCount" : "Type Errors in Code (No. of times)"
		,"runsErrorNameCount" : "Name Errors in Code (No. of times)"
		,"runsErrorSyntaxCount" : "Syntax Errors in Code (No. of times)"
		,"runsSuccessCount" : "Successful code (No. of times)"
		,"runsErrorCount" : "Errors in Code (No. of times)"
		,"runsCount" : "Code executed (No. of times)"
		,"runsHasVariableCount" : "Used Variables in Code"
		,"runsHasConditionCount" : "Used Conditions in Code"
		,"runsHasNestedLoopCount" : "Used Nested Loop in Code"
		,"runsHasLoopCount" : "Used Loop in Code"
		,"runsHasExpressionsCount" : "Used Expressions in Code (no. of time in all code runs)"
		,"runsHasAsyncOrAwaitCount" : "Used Async in Code (no. of time in all code runs)"
		,"runsHasFunctionClassCount" : "Used Function or Class in Code (no. of time in all code runs)"
		,"runsHasControlFlowCount" : "Used Control Flows in Code (no. of time in all code runs)"
		,"runsHasImportsCount" : "Used Imports in Code (no. of time in all code runs)"
		,"runsHasStatementsCount" : "Used Statements in Code (no. of time in all code runs)"
		,"runsHasComprehensionsCount" : "Used Comprehensions in Code (no. of time in all code runs)"
		,"runsHasSubscriptingCount" : "Used Subscription in Code (no. of time in all code runs)"

		,"hasLoop" : "Used Loop in Code"
		,"hasNestedLoop" : "Used Nested Loop in Code"
		,"hasCondition" : "Used Condition in Code"
		,"hasVariable" : "Used Variable in Code"
		,"hasExpressions" : "Used Expressions in Code"
		,"hasAsyncOrAwait" : "Used Async in Code"
		,"hasFunctionClass" : "Used Function or Class in Code"
		,"hasControlFlow" : "Used Control Flows in Code"
		,"hasImports" : "Used Imports in Code"
		,"hasStatements" : "Used Statements in Code"
		,"hasComprehensions" : "Used Comprehensions in Code"
		,"hasSubscripting" : "Used Subscription in Code"
	}

feature2UserNamesDict[featurePracticeTaskDesc] = "Practice Task"
feature2UserNamesDict[featureTheoryTaskDesc] = "Theory Task"
feature2UserNamesDict[featureTaskDesc] = "Task"
feature2UserNamesDict[featureTaskType] = "Task Type"
feature2UserNamesDict["SessionDuration"] = "Session Duration"
feature2UserNamesDict["playerShootEndEnemyHitCount"] = "Player Shoot Enemy Hit Count"
feature2UserNamesDict[featureItemsCollectedCount] = "Items Collected Count"
feature2UserNamesDict[featureRobotCollisionsBoxCount] = "Robot box collision Count"
feature2UserNamesDict["Result"] = "Result"
feature2UserNamesDict[featureConceptsUsedDetailsStr] = "Concepts used details"


#------------------- feature related END -----------------------------------------------



#------------------- GRAPHS START -----------------------------------------------
graphHeight = 800
graphWidth =  1300

graphTemplete = 'seaborn'

successPieFigClassSuccess = "Successfully completed a task"
successPieFigClassOthers = "Others"

StudentResultExplanation = '        (*has student completed this task in any runs)'

colorError = 'rgb(255,127,80)'
colorSuccess = 'rgb(0,128,0)'
#------------------- GRAPHS END ----------------------------------------------
