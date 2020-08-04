# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 23:15:55 2020

@author: tilan
"""
import numpy as np
import pandas as pd
from dateutil.parser import parse
from six.moves.urllib.parse import quote


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash_table
import math
import constants





#-----------------------------------

def plotGroupOverview(groupSelected, groupStudents, studentDataDf, classes = ""):
    plots = []
    
    plotRow = []
    
    plotRow.append( html.Div([],
                            className="col-sm-3",
                    ))
    plotRow.append( html.Div([
                                generateCardBase([html.I(className="fas fa-users m-right-small"),   'No of Students'], len(groupStudents),
                                        classes = classes)
                            ],
                            className="col-sm-6",
                    ))
    plots.append(
            html.Div(children  = plotRow,                
                     className = "row")
    )

    plotRow = []    
    plotRow.append(
            html.Div([
                   generateCardDetail([html.I(className="fas fa-clock m-right-small"),   'Game Time'], 
                                        '' + seconds_2_dhms(studentDataDf[constants.featureSessionDuration].sum().round(decimals=2)), 
                                        '' + str(studentDataDf[constants.featureSessionDuration].mean().round(decimals=2)) + 's', 
                                        '' + str(studentDataDf[constants.featureSessionDuration].std().round(decimals=2)) + 's', 
                                        'total',
                                        'mean',
                                        'std',
                                        classes = classes
                                        )
                ],
                className="col-sm-4",
            ))
    plotRow.append(
            html.Div([
                   generateCardDetail2([html.I(className="fas fa-clock m-right-small"),   'Game Time - Practice vs Theory'], 
                                        '' + seconds_2_dhms(studentDataDf[studentDataDf[constants.TASK_TYPE_FEATURE] ==  constants.TaskTypePractice  ][
                                                constants.featureSessionDuration ].sum().round(decimals=2)), 
                                        '' + seconds_2_dhms(studentDataDf[studentDataDf[constants.TASK_TYPE_FEATURE] ==  constants.TaskTypeTheory ][
                                                constants.featureSessionDuration ].sum().round(decimals=2)), 
                                        constants.TaskTypePractice,
                                        constants.TaskTypeTheory,
                                        classes = classes
                                        )
                ],
                className="col-sm-4",
            ))
    plotRow.append(
            html.Div([
                   generateCardDetail('Points', 
                                        '' + millify(studentDataDf['Points'].sum().round(decimals=2)), 
                                        '' + str(studentDataDf['Points'].mean().round(decimals=2)), 
                                        '' + str(studentDataDf['Points'].std().round(decimals=2)), 
                                        'total',
                                        'mean',
                                        'std',
                                        classes = classes
                                        )
                ],            
                className="col-sm-4",
            ))
            
    plots.append(
            html.Div(children  = plotRow,                
                     className = "row")
    )
    
    return plots





studentOverviewFeaturesDefault = [ constants.featureSessionDuration, constants.featurePoints ]

def plotStudentOverview(studentDataDf, classes = ""):
    plots = []
    
    print(studentDataDf)
    print(studentDataDf[constants.featureSessionDuration])
    print(studentDataDf['Points'])
    print(studentDataDf.std())
    print(studentDataDf.std()[constants.featureSessionDuration])
    print(studentDataDf.std().round(decimals=2)[constants.featureSessionDuration])
    print(studentDataDf[constants.featureSessionDuration].std())
    
    if studentDataDf is None or studentDataDf.empty :
        return plots
    
    
    try:
        studentDataDfMean    = studentDataDf.mean().round(decimals=2)
        studentDataDfStd    = studentDataDf.std().round(decimals=2)
        
        studentDataDfMean.fillna(0, inplace=True)
        studentDataDfStd.fillna(0, inplace=True)
    except Exception as e: 
        print(e)
    
    
    plotRow = []    

    try:
        plotRow.append(
                html.Div([
                       generateCardDetail([html.I(className="fas fa-clock m-right-small"),   'Game Time'], 
                                            '' + seconds_2_dhms(studentDataDf[constants.featureSessionDuration].sum().round(decimals=2)), 
                                            '' + str(studentDataDfMean[constants.featureSessionDuration]) + 's', 
                                            '' + str( studentDataDfStd[constants.featureSessionDuration] ) + 's', 
                                            'total',
                                            'mean',
                                            'std',
                                            classes = classes
                                            )
                    ],
                    className="col-sm-4",
                ))
    except Exception as e: 
        print(e)
    try:
        plotRow.append(
                html.Div([
                       generateCardDetail2([html.I(className="fas fa-clock m-right-small"),   'Game Time - Practice vs Theory'], 
                                            '' + seconds_2_dhms(studentDataDf[studentDataDf[constants.TASK_TYPE_FEATURE] ==  constants.TaskTypePractice  ][
                                                    constants.featureSessionDuration].sum().round(decimals=2)), 
                                            '' + seconds_2_dhms(studentDataDf[studentDataDf[constants.TASK_TYPE_FEATURE] ==  constants.TaskTypeTheory ][
                                                    constants.featureSessionDuration].sum().round(decimals=2)), 
                                            constants.TaskTypePractice,
                                            constants.TaskTypeTheory,
                                            classes = classes
                                            )
                    ],
                    className="col-sm-4",
                ))
    except Exception as e: 
        print(e)
    try:
        plotRow.append(
                html.Div([
                       generateCardDetail( 
                               ((constants.feature2UserNamesDict.get(constants.featurePoints)) if constants.featurePoints in constants.feature2UserNamesDict.keys() else constants.featurePoints ) 
                                , 
                                            '' + millify(studentDataDf[ constants.featurePoints ].sum().round(decimals=2)), 
                                            '' + str(studentDataDfMean[ constants.featurePoints ]), 
                                            '' + str( studentDataDfStd[ constants.featurePoints ] ), 
                                            'total',
                                            'mean',
                                            'std',
                                            classes = classes
                                            )
                    ],            
                    className="col-sm-4",
                ))
    except Exception as e: 
        print(e)
            
    plots.append(
            html.Div(children  = plotRow,                
                     className = "row")
    )
    
    return plots


#---------------------------------- UI ------------------------------------
def generateCardBase(label, value, classes = ""):
    return html.Div(
        [
            html.Span(
                children = [ value ],
                className="card_value"
            ),
            html.P(
                label,
                className="card_label"
            ),
        ],
        className="c-card card-base " + classes,
    )
        
  
def generateCardDetail(label, valueMain = '', value1 = '', value2 = '', 
                       valueMainLabel = '', value1Label = '', value2Label = '',
                       description = '',
                       classes = '' ):
    return html.Div(
        [
            html.Div(
                children = [html.Div(
                                    children = [ value1Label ],
                                    className="card_value_label"
                                ), value1 ],
                className="card_value1"
            ),
            html.Div(
                children = [html.Div(
                                    children = [ value2Label ],
                                    className="card_value_label"
                                ),   value2 ],
                className="card_value2"
            ),
            html.Div(
                children =[html.Div(
                                    children = [ valueMainLabel ],
                                    className="card_value_label"
                                ),  valueMain],
                className="card_value"
            ),
            html.Span(
                label,
                className="card_label"
            ),
            html.Span(
                description,
                className="card_description"
            ),
        ],
        className="c-card card-detail " + classes,
    )
              

def generateCardDetail2(label, value1 = '', value2 = '',
                        value1Label = '', value2Label = '',
                        description = '', classes = ''):
    return html.Div(
        [
            html.Div(
                children = [html.Div(
                                    children = [ value1Label ],
                                    className="card_value_label"
                                ),  value1 ],
                className="card_value1"
            ),
            html.Div(
                children = [html.Div(
                                    children = [ value2Label ],
                                    className="card_value_label"
                                ),  value2 ],
                className="card_value2"
            ),
            html.Span(
                label,
                className="card_label"
            ),
            html.Span(
                description,
                className="card_description"
            ),
        ],
        className="c-card card-detail-2 " + classes,
    )
                
                
#----------------------------- UI END ----------------------------------------
                

#------------------------------GENERIC START-------------------------------------------
                      

millnames = ["", " K", " M", " B", " T"] # used to convert numbers

#returns most significant part of a number
def millify(n):
    n = float(n)
    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )

    return "{:.0f}{}".format(n / 10 ** (3 * millidx), millnames[millidx])


#converts seconds to Day, Hour, Minutes, Seconds
def seconds_2_dhms(time, isLong = False):
    seconds_to_minute   = 60
    seconds_to_hour     = 60 * seconds_to_minute
    seconds_to_day      = 24 * seconds_to_hour

    days    =   time // seconds_to_day
    time    %=  seconds_to_day

    hours   =   time // seconds_to_hour
    time    %=  seconds_to_hour

    minutes =   time // seconds_to_minute
    time    %=  seconds_to_minute

    seconds = time
    
    result = ''
    
    dayLabel = 'days' if days > 1 else 'day'
    hoursLabel = 'hours' if hours > 1 else 'hour'
    minutesLabel = 'minutes' if minutes > 1 else 'minute'
    secondsLabel = 'seconds' if seconds > 1 else 'second'
    
    if days > 0:
            result = "%d %s, %02d:%02d:%02d" % (days, dayLabel, hours, minutes, seconds)
            if isLong :
                result = "%d %s, %d %s, %d %s, %d %s" % (days, dayLabel, hours, hoursLabel, minutes, minutesLabel, seconds, secondsLabel)
    else :
        if isLong :
            if hours > 0 :
                result = "%d %s, %d %s, %d %s" % (hours, hoursLabel, minutes, minutesLabel, seconds, secondsLabel)
            else :
                result = "%d %s, %d %s" % (minutes, minutesLabel, seconds, secondsLabel)
        else :
            result = "%02d:%02d:%02d" % (hours, minutes, seconds)
            
    return result



def get_download_link_data_uri(df):
    if df is None:
        return ''
    
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return csv_string


def is_valid_date(dateStr):
    try:
        parse(dateStr)
        return True
    except ValueError:
        return False
    
    

def get_unique_list_items(dfFeature):
    return set(dfFeature.sum())
    
    

def checkIsFeatureNumeric(df, feature):
    return pd.to_numeric(df[feature], errors='coerce').notnull().all()



def getNumericFeatures(df):
    return df.select_dtypes(include=np.number).columns.tolist()


#------------------------------ GENERIC END --------------------------------------------
    


#---------------------------- App Specific ---------------------------------------------
    
    
def BuildOptionsFeatures(options):  
    return [{ constants.keyLabel : constants.feature2UserNamesDict.get(i) if i in constants.feature2UserNamesDict.keys() else i , 
             constants.keyValue : i} for i in options]




def get_unique_list_feature_items(dfData, feature =    constants.featureConceptsUsed  ):
    return set(dfData[ dfData[feature].notnull() & (dfData[feature]  !=  u'')  ][feature].sum())
    

