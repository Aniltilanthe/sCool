# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 21:01:42 2020

@author: tilan
"""

import numpy as np
import plotly.express as px
import io
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import chart_studio.plotly as py
from plotly import graph_objs as go

from app import app


from data import studentGrouped
import constants
import util

#--------------------- school selection START ----------------------
GroupSelector_options = studentGrouped.GroupSelector_options 
#--------------------- school selection END ----------------------



#--------------------------------- DataBase get data START ---------------------------
dfStudentDetails                        = studentGrouped.dfStudentDetails


dfPracticeTaskDetails                   = studentGrouped.dfPracticeTaskDetails
dfTheoryTaskDetails                     = studentGrouped.dfTheoryTaskDetails


dfGroupedPractice                       = studentGrouped.dfGroupedPractice
dfGroupedOriginal                       = studentGrouped.dfGroupedOriginal
dfPlayerStrategyPractice                = studentGrouped.dfPlayerStrategyPractice  
dfGroupedPracticeTaskWise               = studentGrouped.dfGroupedPracticeTaskWise
dfGroupedPracticeDB                     = studentGrouped.dfGroupedPracticeDB
dfRuns                                  = studentGrouped.dfRuns
dfPracticeDB                            = studentGrouped.dfPracticeDB


dfPlayerStrategyTheory                  = studentGrouped.dfPlayerStrategyTheory
dfGroupedPlayerStrategyTheory           = studentGrouped.dfGroupedPlayerStrategyTheory

#--------------------------------- DataBase get data END ---------------------------

#--------------------------- helper functions START -----------------------    
getTaskWiseSuccessFail                  =  studentGrouped.getTaskWiseSuccessFail
getStudentsOfSchool                     =  studentGrouped.getStudentsOfSchool
getPracticeConceptsUsedDetailsStr          =  studentGrouped.getPracticeConceptsUsedDetailsStr
getStudentWiseData                      =  studentGrouped.getStudentWiseData

#--------------------------- helper functions END -----------------------  



#-----------------------------------Functions START ----------------------------------------
featureAdderGroup       =   constants.featureAdderGroup
featureAdderAvg         =   constants.featureAdderAvg
featuresOverview        =   constants.featuresOverview
featuresOverviewAvg     =   constants.featuresOverviewAvg

featuresOverviewAvgNames =  constants.featuresOverviewAvgNames

featuresOverviewGeneralNames = {constants.COUNT_STUDENT_FEATURE: 'No. of Students'}

def get_merge_list(values):
    return list(set([a for b in values.tolist() for a in b]))


def getTable(df, groupKey, isMinNotHighlight, isMean, featureAdder):
    
    return dash_table.DataTable(
            columns=[
                {"name": (constants.feature2UserNamesDict.get(i) + featureAdder) if i in constants.feature2UserNamesDict.keys() else i , "id": i, "selectable": True} for i in df.columns
            ],
            data            = df.to_dict('records'),
            filter_action       = "native",
            sort_action             = "native",
            sort_mode           = "multi",
            style_data_conditional=(
            [
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': constants.THEME_TABLE_ODDROW_COLOR_STYLE
                        },
            ] +
                    
            ( []  if ( isMinNotHighlight ) else   [
                {
                    'if': {
                        'filter_query'  : '{SessionDuration}' + ' = {}'.format(i) ,
                        'column_id'     : 'SessionDuration',
                    },
                    'color': constants.ERROR_COLOR,
                }
                for i in  df['SessionDuration'].nsmallest(1)
            ] ) +   ( []  if ( isMinNotHighlight ) else   [
                {
                    'if': {
                        'filter_query'  : '{SessionDuration}' + ' = {}'.format(i) ,
                        'column_id'     : 'SessionDuration',
                    },
                    'color': constants.SUCCESS_COLOR,
                }
                for i in  df['SessionDuration'].nlargest(1)
            ] ) +
            ( []  if ( isMinNotHighlight ) else   [
                {
                    'if': {
                        'filter_query'  : '{PracticeSessionDuration}' + ' = {}'.format(i) ,
                        'column_id'     : 'PracticeSessionDuration',
                    },
                    'color': constants.ERROR_COLOR,
                }
                for i in  df['PracticeSessionDuration'].nsmallest(1)
            ] ) + 
            ( []  if ( isMinNotHighlight ) else   [
                {
                    'if': {
                        'filter_query'  : '{PracticeSessionDuration}' + ' = {}'.format(i) ,
                        'column_id'     : 'PracticeSessionDuration',
                    },
                    'color': constants.SUCCESS_COLOR,
                }
                for i in  df['PracticeSessionDuration'].nlargest(1)
            ] ) +
            ( []  if ( isMinNotHighlight ) else   [
                {
                    'if': {
                        'filter_query'  : '{TheorySessionDuration}' + ' = {}'.format(i) ,
                        'column_id'     : 'TheorySessionDuration',
                    },
                    'color': constants.ERROR_COLOR,
                }
                for i in  df['TheorySessionDuration'].nsmallest(1)
            ] ) +  
            ( []  if ( isMinNotHighlight ) else   [
                {
                    'if': {
                        'filter_query'  : '{TheorySessionDuration}' + ' = {}'.format(i) ,
                        'column_id'     : 'TheorySessionDuration',
                    },
                    'color': constants.SUCCESS_COLOR,
                }
                for i in  df['TheorySessionDuration'].nlargest(1)
            ] ) +
            ( []  if ( isMinNotHighlight ) else   [
                {
                    'if': {
                        'filter_query'  : '{Points}' + ' = {}'.format(i) ,
                        'column_id'     : 'Points',
                    },
                    'color': constants.ERROR_COLOR,
                }
                for i in  df['Points'].nsmallest(1)     
            ] ) + 
            ( []  if ( isMinNotHighlight ) else   [
                {
                    'if': {
                        'filter_query'  : '{Points}' + ' = {}'.format(i) ,
                        'column_id'     : 'Points',
                    },
                    'color': constants.SUCCESS_COLOR,
                }
                for i in  df['Points'].nlargest(1)     
            ] ) + 
            ( []  if ( isMinNotHighlight )  else   [
                {
                    'if': {
                        'filter_query'  : '{Attempts}' + (' = {}'.format(i)),
                        'column_id'     : 'Attempts',
                    },
                    'color': constants.ERROR_COLOR,
                }
                for i in     df['Attempts'].nsmallest(1)   
            ] ) + 
            ( []  if ( isMinNotHighlight )  else   [
                {
                    'if': {
                        'filter_query'  : '{Attempts}' + (' = {}'.format(i)),
                        'column_id'     : 'Attempts',
                    },
                    'color': constants.SUCCESS_COLOR,
                }
                for i in     df['Attempts'].nlargest(1)   
            ] ) + 
            ( []  if ( isMinNotHighlight )  else   [
                {
                    'if': {
                        'filter_query'  : '{itemsCollectedCount}' + ' = {}'.format(i),
                        'column_id'     : 'itemsCollectedCount',
                    },
                    'color': constants.ERROR_COLOR,
                }
                for i in   df['itemsCollectedCount'].nsmallest(1)
            ] ) +  
            ( []  if ( isMinNotHighlight )  else   [
                {
                    'if': {
                        'filter_query'  : '{itemsCollectedCount}' + ' = {}'.format(i),
                        'column_id'     : 'itemsCollectedCount',
                    },
                    'color': constants.SUCCESS_COLOR,
                }
                for i in   df['itemsCollectedCount'].nlargest(1)
            ] ) + 
             ( [
                {
                    'if': {
                        'filter_query': '{{GroupId}} = {}'.format(i),
                    },
                    'color': constants.THEME_BACKGROUND_COLOR,
                    'backgroundColor': constants.THEME_COLOR_LIGHT,
                }
                for i in [ featureAdderGroup + str(groupKey) ]
            ] )
            ),
            style_header = constants.THEME_TABLE_HEADER_STYLE
        )



def plotGroupOverview(groupSelected):
    
    groupStudents     =  getStudentsOfSchool(groupSelected)
    studentDataDf     =  studentGrouped.getStudentsOfSchoolDF(groupSelected)
    
    plots = util.plotGroupOverview(groupSelected, groupStudents, studentDataDf)
    
    return plots



def getGroupData(schoolKey, schoolKeys2Compare):
    
    studentDataDf = pd.DataFrame()
    
    if (None == schoolKey) :
        return studentDataDf
    
    if (None == schoolKeys2Compare) :
        schoolKeys2Compare = []
    
    studentDataDf = studentGrouped.getStudentsOfSchoolDF(schoolKey, isOriginal = True)
    
    for sckoolKey2Com in schoolKeys2Compare:
        studentDataDf2Com = studentGrouped.getStudentsOfSchoolDF(sckoolKey2Com, isOriginal = True)
        
        if 'studentDataDf2Com' in locals()    and    studentDataDf2Com is not None :
            studentDataDf = pd.concat([studentDataDf, studentDataDf2Com], ignore_index=True, sort=False)
    

    if 'studentDataDf' in locals()     and    studentDataDf is not None  :
        
        studentDataDf[constants.GROUPBY_FEATURE]    = studentDataDf[constants.GROUPBY_FEATURE].apply(str)
        studentDataDf[constants.GROUPBY_FEATURE]    = featureAdderGroup + studentDataDf[constants.GROUPBY_FEATURE]
#        studentDataDf[constants.featureConceptsUsedDetailsStr]     = getPracticeConceptsUsedDetailsStr(studentDataDf)
        
    return studentDataDf
    

#Student Interaction with Game - TIMELINE
def plotClassOverview(schoolKey, schoolKeys2Compare):

    graphs = []
    rows = []
    
    if (None == schoolKey) :
        return html.Div()
    
    if (None == schoolKeys2Compare) :
        schoolKeys2Compare = []
    
    studentDataDf = getGroupData(schoolKey, schoolKeys2Compare)
    
    if 'studentDataDf' in locals()     and    studentDataDf is not None  :
                
        studentDataDfGrouped = studentDataDf.groupby([constants.GROUPBY_FEATURE], as_index = False)

        
    #   Sum of features
        studentDataDfStudentSum = studentDataDf.groupby([constants.GROUPBY_FEATURE, constants.COUNT_STUDENT_FEATURE, 
                                                  constants.STUDENT_ID_FEATURE], as_index=False).sum()
        studentDataDfStudentSumGrouped = studentDataDfStudentSum.groupby([constants.GROUPBY_FEATURE], as_index = False)
        studentDataDfStudentSumGrouped.fillna(0, inplace=True)  
        
        studentDataDfStudentTaskWiseSum = studentDataDf.groupby([constants.GROUPBY_FEATURE, constants.STUDENT_ID_FEATURE, 
                                                              constants.TASK_TYPE_FEATURE], as_index=False).sum()   
        studentDataDfStudentTaskWiseSum.fillna(0, inplace=True)  
        
    
#--------------------------------Total of each Features ----------------------------------             
        graphs.append(html.Div(id='Group-Overview-Information', children = []))   
        
        studentDataDfSum = studentDataDf.groupby([constants.GROUPBY_FEATURE, constants.COUNT_STUDENT_FEATURE], as_index=False).sum()
#        studentDataDfSumGrouped = studentDataDfSum.groupby([constants.GROUPBY_FEATURE], as_index = False)
        
        studentDataDfFeaturesInterpreted = pd.DataFrame(columns = [constants.GROUPBY_FEATURE, 'PracticeSessionDuration', 'TheorySessionDuration']) 
        for groupKey, group in studentDataDfGrouped :     
            practiceSessionDuration = group[group[constants.TASK_TYPE_FEATURE] ==  constants.TaskTypePractice ]['SessionDuration'].sum()
            theorySessionDuration =  group[group[constants.TASK_TYPE_FEATURE] == constants.TaskTypeTheory ]['SessionDuration'].sum()
            studentDataDfFeaturesInterpreted = studentDataDfFeaturesInterpreted.append({constants.GROUPBY_FEATURE : groupKey, 
                                                                                        'PracticeSessionDuration' : practiceSessionDuration, 
                                                                                        'TheorySessionDuration' : theorySessionDuration, },  
                                                                                ignore_index = True)
        studentDataDfFeaturesInterpreted = studentDataDfFeaturesInterpreted.groupby([constants.GROUPBY_FEATURE],  as_index=False).sum()

        studentDataDfSum = studentDataDfSum.merge(right= studentDataDfFeaturesInterpreted
                                          , left_on = constants.GROUPBY_FEATURE, right_on = constants.GROUPBY_FEATURE
                                            , left_index=False, right_index=False
                                            , how='inner')
        
        studentDataDfFeaturesInterpreted2 = pd.DataFrame(columns = [constants.GROUPBY_FEATURE, 'ConceptsUsed'])
        for groupKey, group in studentDataDfGrouped :    
            conceptsUsedStr = ' '
            if 'ConceptsUsed' in group.columns and  group[ group['ConceptsUsed'].notnull() & (group['ConceptsUsed']  !=  u'') ].shape[0] > 0 :
                conceptsUsedStr = ', '.join(  util.get_unique_list_feature_items(group, 'ConceptsUsed' )  )
                
                
                
            studentDataDfFeaturesInterpreted2 = studentDataDfFeaturesInterpreted2.append({constants.GROUPBY_FEATURE : groupKey,
                                                                                        'ConceptsUsed' : conceptsUsedStr },  
                                                                                ignore_index = True)
            
        
        studentDataDfSum = studentDataDfSum.merge(right= studentDataDfFeaturesInterpreted2
                                          , left_on = constants.GROUPBY_FEATURE, right_on = constants.GROUPBY_FEATURE
                                            , left_index=False, right_index=False
                                            , how='inner')
        
        featuresOverviewNew = featuresOverview.copy()
        for i in range(len(featuresOverviewNew)):
            if featuresOverviewNew[i] == 'SessionDuration':
                featuresOverviewNew.insert(i + 1, 'PracticeSessionDuration')
                featuresOverviewNew.insert(i + 2, 'TheorySessionDuration')
        
        studentDataDfSumToPlot = studentDataDfSum[featuresOverviewNew  + [ constants.COUNT_STUDENT_FEATURE ] + ['ConceptsUsed'
                                                                        ]].round(decimals=2)
#        studentDataDfSumToPlot.rename(columns = featuresOverviewGeneralNames, inplace=True)

        tableMean = getTable(studentDataDfSumToPlot, schoolKey, False, False, '')
        
        columns2 = []
        columns2.append(dbc.Col(tableMean , align="center"))
    

        rows.append( dbc.Row( html.Div([
                    html.H3('Overview', id='group-overview-title'), 
                ]) ) )
        
        rows.append( html.Br() )
        rows.append( dbc.Row( html.Div([
                    html.H4('Overall Sum'), 
                ]) ) )
        rows.append( dbc.Row( columns2 ) )
        rows.append( dbc.Row( html.Div([html.A(children=[html.I(className="fas fa-download font-size_medium p_small"),
                       "download data", ],id = "groups_download_overview_link", 
                                               href="", target="_blank",
                                               download='groups-overview.csv' )]) ) )

#-------------------------------------------------------------------------------------
    #   Mean of comparision features    
        studentDataDfMean = studentDataDfStudentSum.groupby([constants.GROUPBY_FEATURE], as_index = False).mean()
        
        studentDataDfMeanToPlot = studentDataDfMean[ featuresOverview ].round(decimals=2)
        
        studentDataDfMeanTaskWise = studentDataDfStudentTaskWiseSum.groupby([constants.GROUPBY_FEATURE, constants.TASK_TYPE_FEATURE], 
                                        as_index=False).mean()[[constants.GROUPBY_FEATURE, constants.TASK_TYPE_FEATURE,
                                        'SessionDuration']].round(decimals=2)        
        
        
        
        studentDataDfFeaturesInterpreted = pd.DataFrame(columns = [constants.GROUPBY_FEATURE, 'PracticeSessionDuration', 'TheorySessionDuration']) 
        for groupKey, group in studentDataDfGrouped :     
            practiceSessionDuration = studentDataDfMeanTaskWise[ (studentDataDfMeanTaskWise[constants.GROUPBY_FEATURE ] == groupKey )   &
                        (studentDataDfMeanTaskWise[constants.TASK_TYPE_FEATURE] ==  constants.TaskTypePractice )  ]['SessionDuration'].sum()
            theorySessionDuration =  studentDataDfMeanTaskWise[ (studentDataDfMeanTaskWise[constants.GROUPBY_FEATURE ] == groupKey )   &
                        (studentDataDfMeanTaskWise[constants.TASK_TYPE_FEATURE] ==  constants.TaskTypeTheory )  ]['SessionDuration'].sum()
            studentDataDfFeaturesInterpreted = studentDataDfFeaturesInterpreted.append({constants.GROUPBY_FEATURE : groupKey, 
                                                                                        'PracticeSessionDuration' : practiceSessionDuration, 
                                                                                        'TheorySessionDuration' : theorySessionDuration, },  
                                                                                ignore_index = True)
        studentDataDfFeaturesInterpreted = studentDataDfFeaturesInterpreted.groupby([constants.GROUPBY_FEATURE],  as_index=False).sum()

        studentDataDfMeanToPlot = studentDataDfMeanToPlot.merge(right= studentDataDfFeaturesInterpreted
                                          , left_on = constants.GROUPBY_FEATURE, right_on = constants.GROUPBY_FEATURE
                                            , left_index=False, right_index=False
                                            , how='inner')
        
#        studentDataDfMeanToPlot[featuresOverviewNew].rename(columns = featuresOverviewAvgNames, inplace=True)
        
#        currentColumns = studentDataDfMeanToPlot.columns
#        for i in range(len(currentColumns)):
#            if 'SessionDuration' in currentColumns[i] :
#                currentColumns.insert(i + 1, 'PracticeSessionDuration')
#                currentColumns.insert(i + 2, 'TheorySessionDuration')
        
        
        tableMean = getTable(studentDataDfMeanToPlot[featuresOverviewNew], schoolKey, False, True, featureAdderAvg)

        columns2 = []
        columns2.append(dbc.Col(tableMean , align="center"))
        rows.append( html.Br() )
        rows.append( dbc.Row( html.Div([
                    html.H4('Mean'), 
                ]) ) )
        rows.append( dbc.Row( columns2 ) )
        
        
#-------------------------------------------------------------------------------------
#    Standard Deviation of comparision features    
        
        studentDataDfStd = studentDataDfStudentSum[featuresOverview].groupby(
                    [constants.GROUPBY_FEATURE], as_index = False).agg([np.std])
        studentDataDfStd.reset_index(level=0, inplace=True)
        studentDataDfStd = studentDataDfStd.round(decimals=2)
        
        studentDataDfMeanTaskWise = studentDataDfStudentTaskWiseSum.groupby([constants.GROUPBY_FEATURE, constants.TASK_TYPE_FEATURE], 
                                        as_index=False).agg([np.std])      
        studentDataDfMeanTaskWise.fillna(0, inplace=True)  
        studentDataDfMeanTaskWise.reset_index(level=[0,1], inplace=True)
        studentDataDfMeanTaskWise = studentDataDfMeanTaskWise[[constants.GROUPBY_FEATURE, constants.TASK_TYPE_FEATURE,
                                        'SessionDuration']].round(decimals=2) 
        studentDataDfMeanTaskWise.columns = studentDataDfMeanTaskWise.columns.droplevel(1)
        
        
        studentDataDfFeaturesInterpreted = pd.DataFrame(columns = [constants.GROUPBY_FEATURE, 'PracticeSessionDuration', 'TheorySessionDuration']) 
        for groupKey, group in studentDataDfGrouped :     
            practiceSessionDuration = studentDataDfMeanTaskWise[ (studentDataDfMeanTaskWise[constants.GROUPBY_FEATURE ] == groupKey )   &
                        (studentDataDfMeanTaskWise[constants.TASK_TYPE_FEATURE] ==  constants.TaskTypePractice )  ]['SessionDuration'].sum()
            theorySessionDuration =  studentDataDfMeanTaskWise[ (studentDataDfMeanTaskWise[constants.GROUPBY_FEATURE ] == groupKey )   &
                        (studentDataDfMeanTaskWise[constants.TASK_TYPE_FEATURE] ==  constants.TaskTypeTheory )  ]['SessionDuration'].sum()
            studentDataDfFeaturesInterpreted = studentDataDfFeaturesInterpreted.append({constants.GROUPBY_FEATURE : groupKey, 
                                                                                        'PracticeSessionDuration' : practiceSessionDuration, 
                                                                                        'TheorySessionDuration' : theorySessionDuration, },  
                                                                                ignore_index = True)
        studentDataDfFeaturesInterpreted.columns = pd.MultiIndex.from_product([studentDataDfFeaturesInterpreted.columns, ['']])
        studentDataDfFeaturesInterpreted = studentDataDfFeaturesInterpreted.groupby([constants.GROUPBY_FEATURE],  as_index=False).sum()

        studentDataDfStd = studentDataDfStd.merge(right= studentDataDfFeaturesInterpreted
                                          , left_on = constants.GROUPBY_FEATURE, right_on = constants.GROUPBY_FEATURE
                                            , left_index=False, right_index=False
                                            , how='inner')
        
        studentDataDfStd = studentDataDfStd.droplevel(level=1, axis=1)
        
        
        tableStd = getTable(studentDataDfStd[featuresOverviewNew], schoolKey, False, False, ' std')

        columns2 = []
        columns2.append(dbc.Col(tableStd , align="center"))
        rows.append( html.Br() )
        rows.append( dbc.Row( html.Div([
                    html.H4('Standard Deviation'), 
                ]) ) )
        rows.append( dbc.Row( columns2 ) )


        
#        --------------------------------------------------------------------------
        
#        -------------------
#        the Quantile Plots - distribution for each feature
        rows.append(html.Div(id='Group-Distribution-Information', children = []))   
        rows.append( dbc.Row( html.Div([
                    html.H3('Distributions', id='group-distribution-title'), 
                ]) ) )
        rows.append( html.Br() )


        studentDataDfStudentSum = studentDataDf.groupby([constants.GROUPBY_FEATURE, constants.COUNT_STUDENT_FEATURE, 
                                                         constants.STUDENT_ID_FEATURE, "Name" ], as_index=False).sum()
        

#Session duration
        figQuantile = px.box(studentDataDfStudentSum, x="GroupId", y="SessionDuration", points="all",
                             title="Distribution of Session Duration",
                             hover_data=[constants.STUDENT_ID_FEATURE, "Name", "SessionDuration", "Attempts", "Points"]
#                             , marker_color = 'rgb(214,12,140)'
                             )   
        figQuantile.update_layout(constants.THEME_EXPRESS_LAYOUT)         
        columns3 = []
        columns3.append(dbc.Col(
                dcc.Graph(
                        figure= figQuantile
                    ) , align="center"))    
        rows.append( dbc.Row( columns3 ) ) 
        rows.append( html.Br() )       

#Attempts
        figQuantile = px.box(studentDataDfStudentSum, x="GroupId", y="Attempts", points="all",
                             title="Distribution of Attempts",
                             hover_data=["StudentId", "Name", "SessionDuration", "Attempts", "Points"]
                             )       
        figQuantile.update_layout(constants.THEME_EXPRESS_LAYOUT)            
        columns3 = []
        columns3.append(dbc.Col(
                dcc.Graph(
                        figure= figQuantile
                    ) , align="center"))    
        rows.append( dbc.Row( columns3 ) )      
        rows.append( html.Br() )         
        
#Points
        figQuantile = px.box(studentDataDfStudentSum, x="GroupId", y="Points", points="all",
                             title="Distribution of Points",
                             hover_data=["StudentId", "Name", "SessionDuration", "Attempts", "Points"]
                             )     
        figQuantile.update_layout(constants.THEME_EXPRESS_LAYOUT)                      
        columns3 = []
        columns3.append(dbc.Col(
                dcc.Graph(
                        figure= figQuantile
                    ) , align="center"))    
        rows.append( dbc.Row( columns3 ) )       
        rows.append( html.Br() )           

#Items Collected
        figQuantile = px.box(studentDataDfStudentSum, x="GroupId", y="itemsCollectedCount", points="all",
                             title="Distribution of Items Collected",
                             hover_data=["StudentId", "Name", "SessionDuration", "Attempts", "Points"]
                             )    
        figQuantile.update_layout(constants.THEME_EXPRESS_LAYOUT)                           
        columns3 = []
        columns3.append(dbc.Col(
                dcc.Graph(
                        figure= figQuantile
                    ) , align="center"))    
        rows.append( dbc.Row( columns3 ) )      
        rows.append( html.Br() )             


#        fig = go.Figure()        
#        for groupId, group in studentDataDfStudentSum.groupby([constants.GROUPBY_FEATURE], as_index=False):
#            groupDataStudent = getStudentWiseData(group)
#            fig.add_trace(go.Box(
#                y               = groupDataStudent['itemsCollectedCount'],                    
#                marker_color    = 'rgb(214,12,140)',
#                name            = groupId,
#                boxpoints       = 'all',
#                text            = groupDataStudent['Name'],
#            ))
#        
#        fig.update_layout(
#            title           ='Distribution of Items Collected',
#            paper_bgcolor   = 'rgb(243, 243, 243)',
#            plot_bgcolor    = 'rgb(243, 243, 243)',
#            yaxis_title     ='Item Collected Count', 
#            xaxis_title     = 'Group',
#        )
#        columns3 = []
#        columns3.append(dbc.Col(
#                                dcc.Graph(
#                                        figure = fig
#                                )  , align="center"))    
#        rows.append( dbc.Row( columns3 ) )          

        
        graphs.append(html.Div(  rows,
                     className = "width-100"  ))
        
    return graphs




def generateControlCard():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="Control-Card-Overview",
        children=[

            html.P("Select Group for Comparision"),
            dcc.Dropdown(
                id      ="group-selector-comparision-overview",
                options = GroupSelector_options,
                multi   = True,
            ),
            html.Div(
                id="reset-btn-outer",
                children =  
                        dbc.Button( "Reset", id="reset-btn", 
                           outline=True, color="primary", className="mr-1", n_clicks=0
                        ),
            ),
            html.Br(),
        ],
    )


#----------------------------------Functions END --------------------------------------------






layout = [
            
    dbc.Row([
            dbc.Col(
                html.Div(
                    id="group-main-overview",
                    className="",
                    children=  [html.H1("Group")]  ,
                ),
        ),
    ]),
    dbc.Row([
            dbc.Col(
                html.Div(
                    id="group-main-overview-content",
                    className="overview m-bottom_medium ",
                    children= []  ,
                ),
        ),
    ]),
                
    dbc.Row([
            dbc.Col(
                # Left column
                html.Div(
                    id="row-control-main-overview",
                    className="p-top_x-large m-bottom_medium",
                    children=
                    [html.H1("Group Comparision")] +
                    [ generateControlCard() ]
                    + [
                        html.Div(
                            ["initial child"], id="row-control-main-output-clientside-overview", className="hidden"
                        )
                    ],
                ),
        ),
    ]),
        
                    

    html.Div(id='group-comparision-container', className = "row group-comparision-container c-table" )
    
    
]
                
                
                                
@app.callback(
    [ 
         Output("group-selector-comparision-overview", "value"), 
    ],
    [
        Input("reset-btn", "n_clicks")
    ],
)
def on_reset(reset_click):
    # Find which one has been triggered
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "reset-btn" and reset_click:
            return [""]
            
#    return [GroupSelector_options[0]['value']]
    return [""]



# Update bar plot
@app.callback(
    Output("group-comparision-container", "children"),
    [
        Input("group-selector-main", "value"),
        Input("group-selector-comparision-overview", "value"),
    ],
)
def update_bar(groupMain, groupComparision ):    
    graphs = []

    if groupMain is None or not int(groupMain) >= 0:
        return html.Div(graphs)
 
    graphs = plotClassOverview( int(groupMain), groupComparision )    
    
    return  html.Div(graphs,
                     className = "col")
    

# Update bar plot
@app.callback(
    Output("group-main-overview-content", "children"),
    [
        Input("group-selector-main", "value"),
    ],
)
def update_main_overview(groupMain):    
    graphs = []

    if groupMain is None or not int(groupMain) >= 0:
        return html.Div(graphs)
 
    graphs = plotGroupOverview(groupMain)  

    return  html.Div(graphs,
#                     className = "width-100"
                     )


@app.callback(
    Output('groups_download_overview_link', 'href'),
    [ Input("group-selector-main", "value"),
        Input("group-selector-comparision-overview", "value"), ])
def update_download_link(groupMain, groupComparision):
    if groupMain is None or not int(groupMain) >= 0:
        return ""
    
    csv_string = util.get_download_link_data_uri(getGroupData( int(groupMain), groupComparision))
    return csv_string