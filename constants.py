# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 22:42:22 2020

@author: tilan
"""




keyLabel                    = 'label'
keyHref                     = 'href'
keySubmenu                  = 'submenu'
keyValue                    = 'value'
keyScrollTo                 = 'scrollTo'
keyClassName                = 'className'
keyHasMeanStd               = 'hasMeanStd'
keyIsAxisEnabled            = 'isAxisEnabled'
keyIsFeature3Enabled        = 'isFeature3Enabled'
keyIsDistributionEnabled        = 'isDistributionEnabled'
keyColor                    = 'color'
keyBackgroundColor          = 'backgroundColor'
keyExpress                  = 'express'
keyLight                    = 'light'
keyIsDefault                = 'isDefault'






#--------------------------------------------------------------------------------
#-------------------------------- STYLES START -----------------------------------
# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
}

THEME           = "theme-app"

THEME_COLOR_MAP = {
	"theme-app": {
        keyLabel : 'app', 
        keyBackgroundColor  : '#3aaab2',
		keyColor : 'white',
		keyLight 	: "rgb(232 252 253)",
        keyClassName : 'theme-color-app',
		keyExpress	: {
			"plot_bgcolor"      : 'rgb(243, 243, 243)',
			"paper_bgcolor"     : 'rgb(243, 243, 243)',
		},
        keyIsDefault : True
	},
	"theme-teal": {
        keyLabel : 'teal', 
        keyBackgroundColor  : '#009688',
		keyColor : 'white',
		keyLight 	: "#e9fffd",
        keyClassName : 'theme-color-teal',
		keyExpress	: {
			"plot_bgcolor"      : '#e9fffd',
			"paper_bgcolor"     : '#e9fffd',
		},
        keyIsDefault : False
	},
	"theme-pink": {
        keyLabel : 'pink', 
        keyBackgroundColor  : '#e91e63',
		keyColor : 'white',
		keyLight 	: "#fbd2e0",
        keyClassName : 'theme-color-pink',
		keyExpress	: {
			"plot_bgcolor"      : '#fef2f6',
			"paper_bgcolor"     : '#fef2f6',
		},
        keyIsDefault : False
	},
	"theme-dark": {
        keyLabel : 'dark', 
        keyBackgroundColor  : 'black',
		keyColor : 'white',
		keyLight 	: "grey",
        keyClassName : 'theme-color-dark',
		keyExpress	: {
			"plot_bgcolor"      : 'rgb(243, 243, 243)',
			"paper_bgcolor"     : 'rgb(243, 243, 243)',
		},
        keyIsDefault : False
	}
}  

THEME_COLOR = 'black'
THEME_BACKGROUND_COLOR = 'white'
THEME_COLOR_LIGHT  = 'white'
THEME_EXPRESS_LAYOUT = THEME_COLOR_MAP.get(THEME).get(keyExpress)


def refreshThemeColor():
    if THEME in THEME_COLOR_MAP.keys():    
        THEME_COLOR                     = THEME_COLOR_MAP.get(THEME).get(keyColor)
        THEME_BACKGROUND_COLOR          = THEME_COLOR_MAP.get(THEME).get(keyBackgroundColor)
        THEME_COLOR_LIGHT               = THEME_COLOR_MAP.get(THEME).get(keyLight)
        THEME_EXPRESS_LAYOUT            = THEME_COLOR_MAP.get(THEME).get(keyExpress)
    return THEME_COLOR, THEME_BACKGROUND_COLOR, THEME_COLOR_LIGHT, THEME_EXPRESS_LAYOUT

THEME_COLOR, THEME_BACKGROUND_COLOR, THEME_COLOR_LIGHT, THEME_EXPRESS_LAYOUT = refreshThemeColor()


ERROR_COLOR = "#FF4136"
SUCCESS_COLOR = "#4caf50"

THEME_MARKER = dict(size = 16
                                            , showscale    = False
                                            ,  line = dict(width=1,
                                                        color='DarkSlateGrey'))


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#f8f9fa",
}


MENU_BUTTON_STYLE = {
    'width': '100%'
}


THEME_TABLE_HEADER_STYLE = {
    'backgroundColor'   : 'rgb(230, 230, 230)',
    'fontWeight'        : 'bold'
}
THEME_TABLE_ODDROW_COLOR_STYLE = 'rgb(248, 248, 248)'

#-------------------------------- STYLES END -----------------------------------

#---------------------------------------------------------------------------------
#--------------------------------------------------------------------------------



#------------------- feature related START -----------------------------------------------

GROUPBY_FEATURE         =  'GroupId'
COUNT_STUDENT_FEATURE   =  'CountOfStudents'
STUDENT_ID_FEATURE      =  'StudentId'
TASK_TYPE_FEATURE       =  'TaskType'



featureAdderGroup = "GroupId-"
featureAdderAvg = ' Avg.'

featuresCombined = [GROUPBY_FEATURE,'SessionDuration', 'Points', 'Attempts' ]
featuresOverview = featuresCombined + ['itemsCollectedCount' ]
featuresOverviewAvg = [GROUPBY_FEATURE, 'SessionDuration'+ featureAdderAvg, 'Points'+ featureAdderAvg
                       , 'Attempts'+ featureAdderAvg, 'itemsCollectedCount'+ featureAdderAvg ]

featuresOverviewAvgNames = {
        'SessionDuration': 'SessionDuration'+ featureAdderAvg,
                                      'Points': 'Points' + featureAdderAvg,
                                      'Attempts' : 'Attempts' + featureAdderAvg,
                                      'itemsCollectedCount' : 'itemsCollectedCount' + featureAdderAvg
  }




countStudentCompletingTaskFeature   = "No. of Students Completing Task"
countTaskCompletedByStudentFeature  = "No. of Tasks Completed"
featureSessionDuration              = "SessionDuration"
featurePracticeTaskDesc             = "PracticeTaskDesc"
featureTheoryTaskDesc               = "TheoryTaskDesc"
featureTaskDesc                     = "TaskDesc"
featureTaskType                     = "TaskType"
featureDescription                  = "Description"
featureConceptsUsed                 = "Concept Used"
featureConceptsUsedDetails          = "ConceptsUsedDetails"
featureConceptsUsedDetailsStr       = "ConceptsUsedDetailsStr"
featureItemsCollectedCount          = "itemsCollectedCount"
featureSolution                     = "Solution"
featurePlayerShootEndEnemyHitCount  = "playerShootEndEnemyHitCount"
featureRobotCollisionsBoxCount      = "robotCollisionsBoxCount"
featureLineOfCodeCount              = "lineOfCodeCount"
featurePoints                       = "Points"
featureCollectedCoins               = "CollectedCoins"

TaskTypePractice                    = "Practice"
TaskTypeTheory                      = "Theory"






#User understandable Column names
feature2UserNamesDict = {
		"Attempts" : "Attempts"
		,"PracticeTaskId" : "Practice Task Id"
		,featurePoints : "Points"
		,featureConceptsUsed : 'Concept Used'
		,"studentTaskCount" : "No. of Tasks performed"
		,"studentAttemptsTotal" : "Attempts (total)"
		,featureRobotCollisionsBoxCount : "Robot Collision Box (No. of times)"
		,featureCollectedCoins :  "Coins Collected"
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
        , "Result" : "Result"
        
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
        
		,"PracticeSessionDuration" : "Session D. Practice(s)"
		,"TheorySessionDuration" : "Session D. Theory(s)"
        ,featureSessionDuration : "Session Duration(s)"
        ,COUNT_STUDENT_FEATURE : "No. of Students"
        
        ,featurePlayerShootEndEnemyHitCount : "Player Shoot Enemy Hit Count"
	}


feature2UserNamesDict[featurePracticeTaskDesc] = "Practice Task"
feature2UserNamesDict[featureTheoryTaskDesc] = "Theory Task"
feature2UserNamesDict[featureTaskDesc] = "Task"
feature2UserNamesDict[featureTaskType] = "Task Type"
feature2UserNamesDict[featureItemsCollectedCount] = "No. Items Collected"
feature2UserNamesDict[featureRobotCollisionsBoxCount] = "Robot box collision Count"
feature2UserNamesDict[featureConceptsUsedDetailsStr] = "Concepts used details"


#------------------- feature related END -----------------------------------------------



#------------------- GRAPHS START -----------------------------------------------
graphHeight     = 800
graphWidth      =  1300
graphHeightMin  = 400

graphTemplete = 'seaborn'

successPieFigClassSuccess = "Successfully completed a task"
successPieFigClassOthers = "Fail"

StudentResultExplanation = '        (*has student completed this task in any runs)'

colorError = 'rgb(255,127,80)'
colorSuccess = 'rgb(0,128,0)'
colorPractice = 'rgb(76, 114, 176)'
colorTheory = 'rgb(214,12,140)'


sortOrderDescending = 'Desc'
sortOrderAscending = 'Asc'
sortOrder = {
        'Desc' : 'Desc',
        'Asc' : 'Asc'
}


#------------------- GRAPHS END ----------------------------------------------



#--------------------------------- General ---------------------------------------
labelNoData                 = "Has no game interactions"

iconNameHome                = "fa-home"
iconNameGroups              = "fa-list"
iconNameDetails             = "fa-clipboard"
iconNameStudents            = "fa-user-graduate"
iconNameCustom              = "fa-wrench"



labelMedian                 = 'median'
labelMean                   = 'mean'
labelStd                    = 'std'
labelTotal                  = 'total'
labelSuccess                = "Success"
labelFail                   = "Fail"


FigureTypeScatter           = 'Scatter'
FigureTypePie               = 'Pie.'
FigureTypeBar               = 'Bar'
FigureTypeLine              = 'Line'
FigureTypeBubble            = 'Bubble'
FigureTypeScatterMedian            = 'ScatterMedian'
     
AxisV                       = 'v'
AxisH                       = 'h'
MarginalPlotDefault         = 'box'

PlotDistributionMedian      = "median"
PlotDistributionMean        = "mean"
PlotDistributionStd         = "std"

FigureTypes                 = {
     FigureTypeBar      : { keyLabel      : FigureTypeBar, 
                   keyValue     : FigureTypeBar,
                  keyIsAxisEnabled : True,
                  keyIsFeature3Enabled : False,
                  keyIsDistributionEnabled : False  }
    ,   
     FigureTypeScatter : { keyLabel           : FigureTypeScatter, 
                  keyValue      : FigureTypeScatter,
                  keyIsAxisEnabled : True,
                  keyIsFeature3Enabled : False,
                  keyIsDistributionEnabled : True   }
#    ,   
#     FigureTypePie      : { keyLabel      : FigureTypePie, 
#                   keyValue     : FigureTypePie,
#                  keyIsAxisEnabled : False,
#                  keyIsFeature3Enabled : False  }
    ,   
     FigureTypeBubble     : { keyLabel       : FigureTypeBubble, 
                   keyValue     : FigureTypeBubble,
                  keyIsAxisEnabled : True,
                  keyIsFeature3Enabled : True,
                  keyIsDistributionEnabled : False  }
    ,   
     FigureTypeLine     : { keyLabel       : FigureTypeLine, 
                   keyValue     : FigureTypeLine,
                  keyIsAxisEnabled : True,
                  keyIsFeature3Enabled : False ,
                  keyIsDistributionEnabled : False }
}
     
     
     
def getFigureTypesOptions():
    return [{keyLabel: FigureTypes.get(i).get(keyLabel) , keyValue: FigureTypes.get(i).get(keyValue)} for i in FigureTypes]





FeaturesCustom          = ['SessionDuration', 'Points', 'Attempts', 'CollectedCoins', 'Difficulty']

FeaturesCustomPractice  = ['NumberOfCoins', 'runsCount', 'runsErrorCount', 'runsSuccessCount', 'runsErrorSyntaxCount',
                                           'runsErrorNameCount', 'runsErrorTypeCount', 'runsLineOfCodeCountAvg',
                                           'tabsSwitchedCount', 'tabsSwitchedDescriptionCount', 'deletedCodesCount', 'robotCollisionsBoxCount']
FeaturesCustomTheory    = ['playerShootCount', 'playerShootEndCount', 'playerShootEndEnemyHitCount',
                                         'playerShootEndEnemyMissedHitCount', 'enemysShootEndPlayerHitCount']
hoverData               = ["CollectedCoins", "Result", "SessionDuration", "Attempts", "robotCollisionsBoxCount", "Points", "lineOfCodeCount", 'StudentId']

