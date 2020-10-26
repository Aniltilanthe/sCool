# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 22:42:22 2020

@author: tilan
"""


DatabaseName = 'sCool-2020-05-28'






keyLabel                    = 'label'
keyHref                     = 'href'
keySubmenu                  = 'submenu'
keyValue                    = 'value'
keyScrollTo                 = 'scrollTo'
keyClassName                = 'className'
keyHasMeanStd               = 'hasMeanStd'
keyIsAxisEnabled            = 'isAxisEnabled'
keyIsFeature3Enabled        = 'isFeature3Enabled'
keyIsDistributionEnabled    = 'isDistributionEnabled'
keyIsMultiFeatureEnabled    = 'isMultiFeatureEnabled'
keyIsDccGraph               = 'isDccGraph'
keyColor                    = 'color'
keyBackgroundColor          = 'backgroundColor'
keyExpress                  = 'express'
keyLight                    = 'light'
keyIsDefault                = 'isDefault'
keyOnlyForAdmin             = 'onlyForAdmin'







loginRedirect               = "/Details"



languageLocal               = "en"


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

GROUPBY_FEATURE         =  'LearningActivityId'
COUNT_STUDENT_FEATURE   =  'CountOfStudents'
STUDENT_ID_FEATURE      =  'StudentId'
TASK_TYPE_FEATURE       =  'TaskType'



featureAdderGroup = "LAId-"
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
featureTaskType                     = TASK_TYPE_FEATURE
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
TypeCourse                          = "Course"
featureCourse                       = "Course"
TypeTask                            = "Task"
featureTask                         = "Task"
featureTaskId                       = "TaskId"
TypeSkill                           = "Skill"
featureSkill                        = "Skill"
TypeStudent                         = "Student"
featureStudent                      = "Student"
TypeGroup                           = "LA"
featureGroup                        = "LA"






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
        ,"tabsSwitchedOutputCount" : "Switched Tabs to Output (No. of times)"
		,"tabsSwitchedCodeCount" : "Switched Tabs to Code (No. of times)"
		,"tabsSwitchedDescriptionCount" : "Switched to read Description (No. of times)"
		,"tabsSwitchedCount" : "Switched tabs (No. of times)"
		,"draggedCount" : "Dragged (No. of times)"
		
        ,"NumberOfBoxes" : "No. of Boxes"
		,"NumberOfCoins" : "No. of Coins"
		,"NumberOfHidden" : "No. of Hidden items"
		,featureLineOfCodeCount : "Count of Lines of Code" 
        ,featureConceptsUsedDetailsStr : "Concepts used details"
        ,"StudentId" : "StudentId"
        , "Result" : "Result"
        
		,"runsErrorAttribiteCount" : "Attribute Errors in runs (No. of times)"
		,"runsErrorTypeCount" : "Type Errors in runs (No. of times)"
		,"runsErrorNameCount" : "Name Errors in runs (No. of times)"
		,"runsErrorSyntaxCount" : "Syntax Errors in runs (No. of times)"
        
		,"runsSuccessCount" : "Successful code (No. of times in all code runs)"
		,"runsErrorCount" : "Errors in Code (No. of times in all code runs)"
		,"runsCount" : "Code executed (No. of times in all code runs)"
        
		,"runsLineOfCodeCountAvg" : "Avg. Count of Lines of Code (No. of times in all code runs)"  
		,"runsHasVariableCount" : "Used Variables (No. of times in all code runs)"
		,"runsHasConditionCount" : "Used Conditions (No. of times in all code runs)"
		,"runsHasNestedLoopCount" : "Used Nested Loop (No. of times in all code runs)"
		,"runsHasLoopCount" : "Used Loop (No. of times in all code runs)"
		,"runsHasExpressionsCount" : "Used Expressions (no. of time in all code runs)"
		,"runsHasAsyncOrAwaitCount" : "Used Async (no. of time in all code runs)"
		,"runsHasFunctionClassCount" : "Used Function or Class (no. of time in all code runs)"
		,"runsHasControlFlowCount" : "Used Control Flows (no. of time in all code runs)"
		,"runsHasImportsCount" : "Used Imports (no. of time in all code runs)"
		,"runsHasStatementsCount" : "Used Statements  (e.g. Assignment, Assert, Delete) (no. of time in all code runs)"
		,"runsHasComprehensionsCount" : "Used Comprehensions (ListComp, SetComp, GeneratorExp, DictComp, comprehension)(no. of time in all code runs)"
		,"runsHasSubscriptingCount" : "Used Subscription (no. of time in all code runs)"
		,"runsHasExpressionsArithematicCount" : "Used Arithematic Operators (no. of time in all code runs)"
		,"runsHasExpressionsBoolCount" : "Used Boolean (no. of time in all code runs)"
		,"runsHasExpressionsLogicalCount" : "Used Logical Operators (no. of time in all code runs)"
		,"runsHasExpressionsUnaryCount" : "Used Unary Operators(no. of time in all code runs)"
		,"runsHasExpressionsBitwiseCount" : "Used Bitwise Operators(no. of time in all code runs)"
		,"runsHasExpressionsDictCount" : "Used Dictionary Or Map (no. of time in all code runs)"
		,"runsHasExpressionsDataStructureCount" : "Used Data Structure (no. of time in all code runs)"
		,"runsHasControlFlowConditionalCount" : "Used Conditional Flows (no. of time in all code runs)"
		,"runsHasExpressionsKeywordCount" : "Used Keywords (no. of time in all code runs)"
		,"runsHasControlFlowTryExceptionCount" : "Used Try exception (no. of time in all code runs)"        
		,"runsHasVariablesNamedCount" : "Used Variables (no. of time in all code runs)"
		,"runsHasConstantsUsefulCount" : "Used Constants (e.g. 3 or 'a') (no. of time in all code runs)"
		,"runsHasConstantsCount" : "Used Constants (no. of time in all code runs)"
		,"runsHasVariablesCount" : "Used Variables (Load, Store, Del, Name, Starred) (no. of time in all code runs)"

		,"hasLoop" : "Used Loop"
		,"hasNestedLoop" : "Used Nested Loop"
		,"hasCondition" : "Used Condition"
		,"hasVariable" : "Used Variable"
		,"hasExpressions" : "Used Expressions"
		,"hasAsyncOrAwait" : "Used Async"
		,"hasFunctionClass" : "Used Function or Class"
		,"hasControlFlow" : "Used Control Flows"
		,"hasImports" : "Used Imports"
		,"hasStatements" : "Used Statements (e.g. Assignment, Assert, Delete)"
		,"hasComprehensions" : "Used Comprehensions (ListComp, SetComp, GeneratorExp, DictComp, comprehension)"
		,"hasSubscripting" : "Used Subscription (Subscript, Slice)"
		,"hasExpressionsArithematic" : "Used Arithematic Operators (e.g. Add, Div, Mult)"
		,"hasExpressionsBool" : "Used Boolean (And, Or)"
		,"hasExpressionsLogical" : "Used Logical Operators (e.g. Eq, Lt, Gt)"
		,"hasExpressionsUnary" : "Used Unary Operators"
		,"hasExpressionsBitwise" : "Used Bitwise Operators"
		,"hasExpressionsDict" : "Used Dictionary Or Map (Dict)"
		,"hasExpressionsDataStructure" : "Used Data Structure (e.g. Dict, List, Set)"
        ,"hasExpressionsFunctionCall" : "Used function call (e.g. call('friend') )"
		,"hasControlFlowConditional" : "Used Conditional Flows (e.g. If, continue, Break)"
		,"hasControlFlowTryException" : "Used Try exception"
		,"hasVariablesNamed" : "Used Variables"
		,"hasConstantsUseful" : "Used Constants (e.g. 3 or 'a' or None)"
		,"hasExpressionsKeyword" : "Used Keyword (e.g. and, while, None)"
		,"hasConstants" : "Used Constants (e.g. 3 or 'a' or JoinedStr or List)"
		,"hasVariables" : "Used Variables (Load, Store, Del, Name, Starred)"
        
        
        
		, "PracticeSessionDuration" : "Session D. Practice(s)"
		, "TheorySessionDuration" : "Session D. Theory(s)"
        , featureSessionDuration : "Session Duration(s)"
        , COUNT_STUDENT_FEATURE : "No. of Students"
        
        
        , featurePlayerShootEndEnemyHitCount : "Player Shoot Enemy Hit Count"
        , "enemiesCount" : "Count of Enemies"
        , "playerShootCount" : "Player Shoot Count"
        , "playerShootEndCount" : "Player Shoot End Count"
        , "playerShootEndEnemyMissedHitCount" : "Player Shoot Enemy Missed Count"
        , "enemysShootEndPlayerHitCount" : "Enemies Shoot Player Hit Count"
        , "enemysShootEndPlayerNotHitCount" : "Enemies Shoot Player Missed Count"
	}


feature2UserNamesDict[featurePracticeTaskDesc] = "Practice Task"
feature2UserNamesDict[featureTheoryTaskDesc] = "Theory Task"
feature2UserNamesDict[featureTaskDesc] = "Task"
feature2UserNamesDict[featureTaskType] = "Task Type"
feature2UserNamesDict[featureItemsCollectedCount] = "No. Items Collected"
feature2UserNamesDict[featureRobotCollisionsBoxCount] = "Robot box collision Count"
feature2UserNamesDict[featureConceptsUsedDetailsStr] = "Concepts used details"











#https://docs.python.org/dev/library/ast.html
ProgramConceptsUsefull2UserNames =  {
		"Name" : "Variable",
		"Starred" : "Variable",
        "Store" : "Variable",
        
        "BinOp" : "Binary operation (Syntax: left operator right ; e.g. a + b ) ",
		
        "Expr" : "Expression (e.g. function call or Add or BitOr etc.)",
		"Add" : "Addition ",
		"Sub" : "Subtraction ",
		"Mult" : "Multiplication",
		"Div" : "Division",
		"BoolOp" : "Boolean operation",
		"And" : "Boolean And",
		"Or" : "Boolean Or",
		"Eq" : "Equal",
		"NotEq" : "Not Equal",
		"Lt" : "Less Than",
		"Is" : "Is",
		"In" : "In",
        
		"Num" : "Number",
		"Str" : "String",
		
        "Assign" : "Assignment (e.g. a = 2)",
		"For" : "For loop",
		"While" : "While loop",
		"If" : "If",
		"Break" : "Break",
		"Continue" : "Continue",
        
		"Try" : "Try",
        "ExceptHandler" : "Exception handler",
		
        "Call" : "Function call",
        "FunctionDef" : "Function definition",
		"arguments" : "Arguments for a function",
		"arg" : "Argument for a Function",
		"Return" : "Return",
		
        "ClassDef" : "Class definition",
        
        "Dict" : "Dictionary (key value)",
		
        "Import" : "Import",
		
        "ListComp" : "List comprehension (Comprehensions)",
		"SetComp" : "Set comprehension (Comprehensions)",
		"DictComp" : "Dict comprehension (Comprehensions)",
	}




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
colorPracticeError = 'rgb(204, 204, 255)'
colorTheory = 'rgb(214,12,140)'
colorTheoryError = 'rgb(255,127,80)'


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
labelDistAll                = 'All details'
labelTotal                  = 'total'
labelSuccess                = "Success"
labelFail                   = "Fail"

labelStudentTimeline        = "Student Timeline"


FigureTypeScatter           = 'Scatter'
FigureTypePie               = 'Pie.'
FigureTypeBar               = 'Bar'
FigureTypeLine              = 'Line'
FigureTypeBubble            = 'Bubble'
FigureTypeTable             = 'Table'
     
AxisV                       = 'v'
AxisH                       = 'h'
MarginalPlotDefault         = 'box'

PlotDistributionMedian      = "median"
PlotDistributionMean        = "mean"
PlotDistributionStd         = "std"
PlotDistributionAll         = "all"


FigureTypes                 = {
     FigureTypeBar      : { keyLabel        : FigureTypeBar, 
                   keyValue                 : FigureTypeBar,
                  keyIsAxisEnabled          : True,
                  keyIsFeature3Enabled      : False,
                  keyIsDistributionEnabled  : False  ,
                  keyIsMultiFeatureEnabled  : False ,
                  keyIsDccGraph             : True,       }
    ,   
     FigureTypeScatter : { keyLabel             : FigureTypeScatter, 
                  keyValue                      : FigureTypeScatter,
                  keyIsAxisEnabled              : True,
                  keyIsFeature3Enabled          : False,
                  keyIsDistributionEnabled      : True  ,
                  keyIsMultiFeatureEnabled      : False  ,
                  keyIsDccGraph                 : True,       }
#    ,   
#     FigureTypePie      : { keyLabel      : FigureTypePie, 
#                   keyValue     : FigureTypePie,
#                  keyIsAxisEnabled : False,
#                  keyIsFeature3Enabled : False  }
    ,   
     FigureTypeBubble     : { keyLabel      : FigureTypeBubble, 
                   keyValue                 : FigureTypeBubble,
                  keyIsAxisEnabled          : True,
                  keyIsFeature3Enabled      : True,
                  keyIsDistributionEnabled  : False ,
                  keyIsMultiFeatureEnabled  : False   }
    ,   
     FigureTypeLine     : { keyLabel        : FigureTypeLine, 
                   keyValue                 : FigureTypeLine,
                  keyIsAxisEnabled          : True,
                  keyIsFeature3Enabled      : False ,
                  keyIsDistributionEnabled  : False ,
                  keyIsMultiFeatureEnabled  : False,
                  keyIsDccGraph             : True,      }
    ,   
     FigureTypeTable     : { keyLabel       : FigureTypeTable, 
                   keyValue                 : FigureTypeTable,
                  keyIsAxisEnabled          : False,
                  keyIsFeature3Enabled      : False ,
                  keyIsDistributionEnabled  : False ,
                  keyIsMultiFeatureEnabled  : True,
                  keyIsDccGraph             : False, 
                  keyClassName              : " col-sm-12 " }
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








colors = ['skyblue', 'palegreen', 'mistyrose', 'cadetblue', 'pink', 'lightcoral'
         ,'violet' , 'lime', 'tomato', 'lightgrey', 'darkslategray']
markers = ['.', 'o', 'v', '^', '<', '>', '*', 's', '+', 'x', 'D', 'H', '|', '-']
markerfacecolors = ['navy', 'seagreen', 'red', 'cyan', 'magenta', 'maroon'
                   ,'darkviolet' , 'green', 'tomato', 'grey', 'mediumturqoise']









#------------------------------------
#-- Label
#------------------------------------
labelSelectLA = 'Select Learning Activity'



