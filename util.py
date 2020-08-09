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


featureDescription = constants.featureDescription


#-----------------------------------  DATA INFO  START ----------------------------

def plotGroupOverview(groupSelected, groupStudents, studentDataDf, classes = ""):
    plots = []
    
    
    if studentDataDf is None    or   studentDataDf.empty :
        plots.append(
                getNoDataMsg()
        )
        return plots
    
    
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



def getNoDataMsg():
    return html.Div(
                html.H2(  constants.labelNoData  )
        )

#----------------------------------- DATA INFO END -----------------------------------------


#---------------------------------- UI HTML START------------------------------------
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
                

#----------------------------- UI CONTROLS START ------------------------------
                
                

feature2Default            = "Name"
feature3SizeDefault        = "SessionDuration"
colorDefault                = "Name"
def generateControlCardCustomPlotForm(idApp                 = "", 
                                      feature1Options       = [], 
                                      feature2Options       = [], 
                                      feature3Options       = [], 
                                      feature1ValueDefault  = "",
                                      feature2ValueDefault  = feature2Default,
                                      feature3ValueDefault  = feature3SizeDefault,
                                      figureTypeDefault     = constants.FigureTypeBar,
                                      featureAxisDefault    = constants.AxisH,
                                      colorDefault          = colorDefault
                                      ):
    """
    :return: A Div containing controls for feature selection for plotting graphs.
    """
    return html.Div(
        id = idApp + "-control-card-custom-plot-form",
        children=[

            html.P("Select Features")
            
            , dbc.Row([
                    dbc.Col(
                      html.Div([
                                dcc.Dropdown(
                                    id              = idApp + "-form-feature-1",
                                    placeholder     = "Select feature X",
                                    options         = BuildOptionsFeatures( feature1Options ),
                                    value           = feature1ValueDefault
                                )
                            ],
                            className = "c-container"
                       )
                        , width=6
                    ),
                    dbc.Col(
                        html.Div([
                            dcc.Dropdown(
                                    id              = idApp + "-form-feature-2", 
                                    placeholder     = "Select feature Y",
                                    options         = BuildOptionsFeatures( feature2Options ),
                                    value           = feature2ValueDefault
                                )
                            ],
                            className = "c-container"
                        )
                        , width=3
                    ),
                    dbc.Col(
                        html.Div([
                            dcc.Dropdown(
                                    id              = idApp + "-form-feature-3", 
                                    placeholder     = "Select Size",
                                    options         = BuildOptionsFeatures( feature3Options ),
                                    value           = feature3ValueDefault
                                )
                            ],
                            className = "c-container"
                        )
                        , width=3
                    )
            ])
            
            , dbc.Row([
                    dbc.Col(
                      html.Div([ dcc.RadioItems(
                                id          = idApp + "-form-figure-type",
                                options     = constants.getFigureTypesOptions(),
                                value       = figureTypeDefault ,
                                className   = "radio-items-inline"
                             )
                            ],
                            className = "c-container"
                       ) , width=6
                ),
            ])
            
            , dbc.Row([
                    dbc.Col(
                      html.Div([
                                dcc.RadioItems(
                                    id      =   idApp + "-form-feature-axis",
                                    options = [
                                        {'label': 'Horizontal (x-axis)', 'value': constants.AxisH},
                                        {'label': 'Vertical (y-axis)', 'value': constants.AxisV},
                                    ],
                                    value       = featureAxisDefault ,
                                    className   = "radio-items-inline"
                                )
                            ],
                            className = "c-container"
                       )
                        , width=6
                    ),
                    dbc.Col(
                        html.Div([
                            dbc.FormGroup([
#                                    dbc.Label("Distribution"),
                                    dbc.Checklist(
                                        options=[
                                            {"label": constants.labelMean, "value": constants.PlotDistributionMean},
                                            {"label": constants.labelStd, "value": constants.PlotDistributionStd},
                                            {"label": constants.labelMedian, "value": constants.PlotDistributionMedian},
                                        ],
                                        value   = [],
                                        id      = idApp + "-form-feature-distribution",
                                        inline  = True,
                                        switch  = True,
                                    ),
                                ])
                            ],
                            className   = "c-container",
                            title       = "This can work only when both features are Numerical (default SessionDuration).",
                        )
                        , width=3
                    ),
                    dbc.Col(
                      html.Div([
                                dcc.RadioItems(
                                    id      =   idApp + "-form-feature-color-group",
                                    options = [
                                        {'label': 'Student', 'value': 'Name'  },
                                        {'label': 'Group', 'value': 'GroupId'  },
                                    ],
                                    value       = colorDefault ,
                                    className   = "radio-items-inline"
                                )
                            ],
                            className = "c-container"
                       )
                        , width=3
                    ),
            ])

            , html.Button(children=[
                    html.I(className="fas fa-plus font-size_medium p-right_xx-small"),
                    'Add Plot',  ], 
                        id  =   idApp + "-form-submit-btn", 
                        className="c-button btn btn-outline-primary", n_clicks=0),
            html.Br(),
        ],
        className = "form"
    )
                
                

def getCustomPlot( df, 
                  featureX              = "", 
                  featureY              = "", 
                  feature3              = "", 
                  selectedFigureType    = constants.FigureTypeBar, 
                  selectedAxis          = constants.AxisH, 
                  plotTitle             = '',
                  hoverName             = "Name",
                  marginalX             = '',
                  marginalY             = '',
                  hoverData             = [],
                  color                 = colorDefault,
                  selectedDistribution  = [],
                  isThemeSizePlot       = False
    ):
    
    rows = []
    
    
    print('getCustomPlot')
    
    if df is None  or df.empty   or    featureX == None :
        return rows
    
    if ( '' == featureY     and    not selectedFigureType == constants.FigureTypePie ):
        return rows
    
    
    if not featureX in df.columns  :
        return rows.append(html.H3('Feature not in data ' + str(featureX ) + '  . Select another! ' ))

    if not featureY in df.columns     and    not selectedFigureType == constants.FigureTypePie  :
        return rows.append(html.H3('Feature not in data ' + str(featureY ) + '  . Select another! ' ))
    
    
    featureX2Plot = featureX
    featureY2Plot = featureY

    orientation = constants.AxisH

    if not None == selectedAxis and selectedAxis == constants.AxisV:
        featureX2Plot   = featureY
        featureY2Plot   = featureX
        orientation     = constants.AxisV

    
    plotTitle = ' Details of ' 
    plotTitle = plotTitle + str( constants.feature2UserNamesDict.get(featureX2Plot) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot )
    plotTitle = plotTitle + ' vs ' + str( constants.feature2UserNamesDict.get(featureY2Plot) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot )
    
    
    try:
        
        studentDataDfSumMean        = df.mean().round(decimals=2)
        studentDataDfSumStd         = df.std().round(decimals=2)
        studentDataDfSumMedian      = df.median().round(decimals=2)

        df[featureDescription]      = getDataFeatureDescription(df, hoverData, featureTitle = color)


        if selectedFigureType == constants.FigureTypeScatter:

            if checkIsFeatureNumeric(df, featureX2Plot):
                 marginalX = constants.MarginalPlotDefault
     
            if checkIsFeatureNumeric(df, featureY2Plot):
                 marginalY = constants.MarginalPlotDefault


            if not selectedDistribution is None  and len(selectedDistribution) > 0:
    
                if featureY == 'Name' :
                    featureY2Plot   = constants.featureSessionDuration
    
                featureX2Plot = featureX
    
                plotTitle = ' Details of ' 
                plotTitle = plotTitle + str( constants.feature2UserNamesDict.get(featureX2Plot) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot )
                plotTitle = plotTitle + ' vs ' + str( constants.feature2UserNamesDict.get(featureY2Plot) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot )


                mean_featureX = studentDataDfSumMean[featureX2Plot]
                std_featureX = studentDataDfSumStd[featureX2Plot]
                med_featureX = studentDataDfSumMedian[featureX2Plot]

                figStudents = getCustomPlotScatter(df, featureX2Plot, featureY2Plot, 
                                 selectedDistribution = selectedDistribution,
                                 mean_featureX      = mean_featureX,
                                 std_featureX       = std_featureX,
                                 med_featureX       = med_featureX,
                                 mean_featureY      = 0,
                                 std_featureY       = 0,
                                 med_featureY       = 0,
                                 textFeature        = featureDescription,
                                 plotTitle          = plotTitle
                         )

            else :
#                if not color == 'Name' :
#                    figStudents = px.scatter(df, x = featureX2Plot, y = featureY2Plot
#                         , title        =   plotTitle
#                         , labels       =   constants.feature2UserNamesDict # customize axis label
#                         , hover_name   =   hoverName
#                         , color        =   color
#                         , hover_data   =   hoverData
#                         , marginal_x   =   marginalX
#                         , marginal_y   =   marginalY
#        #                     , height       =   constants.graphHeight
#                         , template     =   constants.graphTemplete
#                        )
#                else :
#                    figStudents = px.scatter(df, x = featureX2Plot, y = featureY2Plot
#                         , title        =   plotTitle
#                         , labels       =   constants.feature2UserNamesDict # customize axis label
#                         , hover_name   =   hoverName
#                         , hover_data   =   hoverData
#                         , marginal_x   =   marginalX
#                         , marginal_y   =   marginalY
#        #                     , height       =   constants.graphHeight
#                         , template     =   constants.graphTemplete
#                        )
                figStudents = px.scatter(df, x = featureX2Plot, y = featureY2Plot
                     , title        =   plotTitle
                     , labels       =   constants.feature2UserNamesDict # customize axis label
                     , hover_name   =   hoverName
                     , hover_data   =   hoverData
                     , marginal_x   =   marginalX
                     , marginal_y   =   marginalY
    #                     , height       =   constants.graphHeight
                     , template     =   constants.graphTemplete
                    )

                figStudents.update_traces(marker    =  constants.THEME_MARKER,
                                  selector          = dict(mode='markers') )
                figStudents.update_layout(constants.THEME_EXPRESS_LAYOUT)
                print('Scatter Chart figure   Made Success ! ' )
       
    
    
#            Error when plotting pie charts !!!
        elif selectedFigureType == constants.FigureTypePie:
            
            plotTitle = ' Details of ' 
            plotTitle = plotTitle + str( constants.feature2UserNamesDict.get(featureX) if featureX in constants.feature2UserNamesDict.keys() else featureX )


    
    
            figStudents = go.Figure(data =  [go.Pie(
                                         labels         =   df[color],
                                         values         =   df[featureX]  ,
#                                         hovertext      =   df[featureDescription],
                                    )])
            figStudents.update_traces(
                                hoverinfo       =  'label+percent', 
                              textinfo          ='percent+label+value'     
                        )
            figStudents.update_layout(title_text    = plotTitle)
            figStudents.update_layout(constants.THEME_EXPRESS_LAYOUT)
            
            if isThemeSizePlot:
                figStudents.update_layout(autosize  =  False,
                                          height    =   constants.graphHeight,
                                          width     =   constants.graphWidth)
                

#            figStudents = px.pie(df
#                                 , values       = featureX
#                                 , names        =  'Name'
#                                 , title        =   plotTitle
#                                 , labels       =   constants.feature2UserNamesDict # customize axis label
#                                 , hover_name   =   hoverName
#                                 , hover_data   =   hoverData
##                                 , height       =   constants.graphHeight
#                                 , template     =   constants.graphTemplete
#                                 )
#            figStudents.update_traces(textposition='inside', textinfo='percent+label+value')
#            figStudents.update_layout(constants.THEME_EXPRESS_LAYOUT)
                
            print('Pie Chart figure   Made Success ' )
            
            
        elif selectedFigureType == constants.FigureTypeBar :
            
            figStudents = px.bar( df
                , x             =   featureX2Plot
                , y             =   featureY2Plot
                , title         =   plotTitle
                , labels        =   constants.feature2UserNamesDict # customize axis label
                , template      =   constants.graphTemplete                              
                , orientation   =   orientation
                , hover_name    =   hoverName
                , hover_data    =   hoverData
#                    , height        =   constants.graphHeight
            )
            
            figStudents.update_layout(constants.THEME_EXPRESS_LAYOUT)
            print('Baar Chart figure   Made Success ! ' )
        
        
        elif selectedFigureType == constants.FigureTypeBubble :
            df.loc[df[feature3] < 0, feature3] = 0
            
            figStudents = px.scatter(df
                 , x            =   featureX2Plot
                 , y            =   featureY2Plot
                 , title        =   plotTitle
                 , labels       =   constants.feature2UserNamesDict # customize axis label
                 , hover_name   =   hoverName
                 , hover_data   =   hoverData
                 , size         =   feature3
                 , color        =   color
                 , size_max     =   60
#                     , height       =   constants.graphHeight
                 , template     =   constants.graphTemplete
                )
            figStudents.update_layout(constants.THEME_EXPRESS_LAYOUT)
            
            rows.append( html.Div(children=[
                            html.P('Size is based on ' + ((constants.feature2UserNamesDict.get(feature3)) if feature3 in constants.feature2UserNamesDict.keys() else feature3 ) ),
                            ]) )
            
            
        elif selectedFigureType == constants.FigureTypeLine :

            if not None == selectedAxis and selectedAxis == constants.AxisV:
                featureX2Plot   = featureY
                featureY2Plot   = featureX
            
            figStudents = px.line(df
                , x             =   featureX2Plot
                , y             =   featureY2Plot
                , color         =   color
                , hover_name    =   hoverName
                , hover_data    =   hoverData
#                    , height        =   constants.graphHeight
                , template      =   constants.graphTemplete                              
            )
            figStudents.update_layout(constants.THEME_EXPRESS_LAYOUT)
        
        
        
        
        
        
        rows.append( html.Div( dcc.Graph(
                figure = figStudents
        ) ) )
        
        print('Before Mean and Std calculation ! ' )
        
        print('After Mean and Std calculation ! ' )
        
        try :
            if   featureX2Plot is not None   and     not featureX2Plot == ''   and   not 'Name' == featureX2Plot    and      featureX2Plot in studentDataDfSumMean:
                rows.append( html.Div(children=[
                        html.P(constants.labelMean + ' ' + ((constants.feature2UserNamesDict.get(featureX2Plot)) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot )  + ' = ' + str(studentDataDfSumMean[featureX2Plot]) ),
                        html.P(constants.labelStd + ' ' + ((constants.feature2UserNamesDict.get(featureX2Plot)) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot ) + ' = ' + str(studentDataDfSumStd[featureX2Plot]) ),
                        html.P(constants.labelMedian + ' ' + ((constants.feature2UserNamesDict.get(featureX2Plot)) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot ) + ' = ' + str(studentDataDfSumMedian[featureX2Plot]) ),
                    ]) )
        except Exception as e: 
            print('Exception Mean and Std calculation for feature1 ! ' )
            print(e)
        try :
            if  featureY2Plot is not None   and   not featureY2Plot == ''  and    not 'Name' == featureY2Plot   and     featureY2Plot in studentDataDfSumMean:
                rows.append( html.Div(children=[
                        html.P(constants.labelMean + ' ' + ((constants.feature2UserNamesDict.get(featureY2Plot)) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot )  + ' = ' + str(studentDataDfSumMean[featureY2Plot]) ),
                        html.P(constants.labelStd + ' ' + ((constants.feature2UserNamesDict.get(featureY2Plot)) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot ) + ' = ' + str(studentDataDfSumStd[featureY2Plot]) ),
                        html.P(constants.labelMedian + ' ' + ((constants.feature2UserNamesDict.get(featureY2Plot)) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot ) + ' = ' + str(studentDataDfSumMedian[featureY2Plot]) ),
                    ]) )
        except Exception as e: 
            print('Exception Mean and Std calculation for feature2 ! ' )
            print(e)
    
    except Exception as e: 
        print('Add Graph exception ! ' )
        print(e)
        
                
    return rows         
                

def getCustomPlotScatter(df, featureX2Plot, featureY2Plot, 
                         selectedDistribution = [],
                         mean_featureX = 0,
                         std_featureX = 0,
                         med_featureX = 0,
                         mean_featureY = 0,
                         std_featureY = 0,
                         med_featureY = 0,
                         textFeature = featureDescription,
                         plotTitle = '') :
    data_comp = []
    trace_comp0 = go.Scatter(
            x               = df[featureX2Plot],
            y               = df[featureY2Plot],
            mode            = 'markers',
            marker          =  constants.THEME_MARKER,
    #                    name            = 'Name',
            text            = df[textFeature],
            legendgroup     = "a",
        )
    data_comp.append(trace_comp0)
    
    if constants.PlotDistributionMean in  selectedDistribution:
        trace_median0 =  go.Scatter(x               = [mean_featureX, mean_featureX],
                                    y               = [0, df[featureY2Plot].max() ],
                                    mode            = "lines",
                                    legendgroup     = "a",
                                    showlegend      = False,
    #                                                marker = dict(size  = 12,
    #                                                           line     = dict(width=0.8),
    #                                                           color    = "navy"
    #                                                           ),
                                    name            = "Mean ",
                                    )
        data_comp.append(trace_median0)
        
    
    if constants.PlotDistributionStd in  selectedDistribution:
        trace_median0 =  go.Scatter(x           = [std_featureX, std_featureX ],
                                    y           = [0, df[featureY2Plot].max() ],
                                    mode        = "lines",
                                    legendgroup = "a",
                                    showlegend  = False,
    #                                                marker = dict(size  = 12,
    #                                                           line     = dict(width=0.8),
    #                                                           color    = "navy"
    #                                                           ),
                                    name        = "Std",
                                    )
        data_comp.append(trace_median0)
        
     
    if constants.PlotDistributionMedian in  selectedDistribution:
        trace_median0 =  go.Scatter(x           = [med_featureX, med_featureX ],
                                    y           = [0, df[featureY2Plot].max() ],
                                    mode        = "lines",
                                    legendgroup = "a",
                                    showlegend  = False,
#                                    marker = dict(size  = 12,
#                                               line     = dict(width=0.8),
#    #                                                           color    = "navy"
#                                               ),
                                    name        = "Median",
                                    )
    data_comp.append(trace_median0)

    layout_comp = go.Layout(
        title       = plotTitle,
        hovermode   = 'closest',
        xaxis       = dict(
            title   = str( constants.feature2UserNamesDict.get(featureX2Plot) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot )
        ),
        yaxis       = dict(
            title   = str( constants.feature2UserNamesDict.get(featureY2Plot) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot )
        ),
        template    = constants.graphTemplete,
    )
    fig = go.Figure(data = data_comp, layout = layout_comp)
    fig.update_layout(constants.THEME_EXPRESS_LAYOUT)
    
    return fig


                
#---------------------------- UI CONTROLS END ---------------------------------

def getDataFeatureDescription(df, hoverData, featureTitle = "Name"):
    df[featureDescription] = ''
    
    
    if featureTitle in df.columns:
        df[featureDescription] = '<b>' + df[featureTitle].astype(str) + '</b>' + '<br>'
        
    for feature in hoverData:
        if feature in df.columns:
            df[featureDescription] = df[featureDescription] + '<br><b>' + str(constants.feature2UserNamesDict.get(feature)) + '</b>: ' + df[feature].astype(str)
    
    return df[featureDescription]



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
    

