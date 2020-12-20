# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 23:15:55 2020

@author: tilan
"""
import numpy as np
import pandas as pd
from dateutil.parser import parse
from six.moves.urllib.parse import quote


import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

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
                                generateCardBase([html.I(className="fas fa-users m-right-small"),   'No of Students'], len(studentDataDf[constants.STUDENT_ID_FEATURE].unique()),
                                        classes = classes
                                        )
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
                    
                    generateCardBase([html.I(className="fas fa-clock m-right-small"),   'Game Time'], 
                                        '' + seconds_2_dhms(studentDataDf[constants.featureSessionDuration].sum().round(decimals=2)), 
                                        classes = classes)
                    
#                   generateCardDetail([html.I(className="fas fa-clock m-right-small"),   'Game Time'], 
#                                        '' + seconds_2_dhms(studentDataDf[constants.featureSessionDuration].sum().round(decimals=2)), 
#                                        '' + str(studentDataDf[constants.featureSessionDuration].mean().round(decimals=2)) + 's', 
#                                        '' + str(studentDataDf[constants.featureSessionDuration].std().round(decimals=2)) + 's', 
#                                        'total',
#                                        'mean',
#                                        'std',
#                                        classes = classes
#                                        )
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
                    generateCardBase(
                            [html.I(className="far fa-star m-right-small"),    
                            'Points' ]
                               ,
                                        '' + millify(studentDataDf['Points'].sum().round(decimals=2)), 
                                        classes = classes)
#                   generateCardDetail('Points', 
#                                        '' + millify(studentDataDf['Points'].sum().round(decimals=2)), 
#                                        '' + str(studentDataDf['Points'].mean().round(decimals=2)), 
#                                        '' + str(studentDataDf['Points'].std().round(decimals=2)), 
#                                        'total',
#                                        'mean',
#                                        'std',
#                                        classes = classes
#                                        )
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
                        
                        generateCardBase([html.I(className="fas fa-clock m-right-small"),   'Game Time'], 
                                            '' + seconds_2_dhms(studentDataDf[constants.featureSessionDuration].sum().round(decimals=2)),
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
                        
                        generateCardBase([html.I(className="far fa-star m-right-small"),    
                                 ((constants.feature2UserNamesDict.get(constants.featurePoints)) if constants.featurePoints in constants.feature2UserNamesDict.keys() else constants.featurePoints ) ]
                               , 
                                            '' + millify(studentDataDf[ constants.featurePoints ].sum().round(decimals=2)), 
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
featureGroupByDefault      = "Name"
def generateControlCardCustomPlotForm(idApp                 = "", 
                                      feature1Options       = [], 
                                      feature2Options       = [], 
                                      feature3Options       = [], 
                                      featureMultiOptions   = [], 
                                      feature1ValueDefault  = "",
                                      feature2ValueDefault  = feature2Default,
                                      feature3ValueDefault  = feature3SizeDefault,
                                      figureTypeDefault     = constants.FigureTypeBar,
                                      featureAxisDefault    = constants.AxisH,
                                      featureGroupByDefault = featureGroupByDefault,
                                      colorGroupIsDisabled  = False,
                                      featureGroupByOptions = [],
                                      featureGroupByFilterOptionsDefault  = [] ,
                                      ):
    """
    :return: A Div containing controls for feature selection for plotting graphs.
    """
    
    layout = [                   
            dbc.Row([
                    dbc.Col(
                      html.Div([
                              
                                html.Span("Select Group By ")  ,
                                dcc.RadioItems(
                                    id          =   idApp + "-form-feature-color-group",
                                    options     =   BuildOptionsFeatures( featureGroupByOptions ),                                    
                                    value       =   featureGroupByDefault ,
                                    className   =   "radio-items-inline " + ( ' disabled ' if colorGroupIsDisabled else ' ')
                                )
                            ],
                            className = "c-container"
                       )
                        , width=6
                    ),
                    dbc.Col(
                      html.Div([
                              
                                html.Span("Select Sub Group By ")  ,
                                dcc.Dropdown(
                                    id              = idApp + "-form-feature-color-group-sub",
                                    placeholder     = "Select features",
                                    options         = BuildOptionsFeatures( featureGroupByOptions ), 
                                    multi           = True ,
                                    className   =   " " + ( ' disabled ' if colorGroupIsDisabled else ' ')
                                ),
                            ],
                            className = "c-container"
                       )
                        , width=4
                    ),
            ])  ,
        ]
    
    if featureGroupByFilterOptionsDefault and len(featureGroupByFilterOptionsDefault) > 0:
        layout = layout + [
                 dbc.Row([
                        dbc.Col(
                          html.Div([
                                  
                                    html.Span("Select Filter By ")  ,
                                    dcc.Dropdown(
                                        id          =   idApp + "-form-feature-color-group-filter",
                                        placeholder     = "Select group by filter by",
                                        options     =   BuildOptionsFeatures( featureGroupByFilterOptionsDefault ), 
                                        multi       = True ,
                                        className   =   " "
                                    )
                                ],
                                className = "c-container"
                           )
                            , width=6
                        ),
                ])  ,  
            ]
                    
    layout = layout + [             
            html.P("Select Features")  ,   
            
            dbc.Row([
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
                        , width=5
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
                        , width=4
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
            ])  ,
            
            dbc.Row([
                    dbc.Col(
                      html.Div([
                              html.Span("Type")  ,
                                
                                dcc.RadioItems(
                                    id          = idApp + "-form-figure-type",
                                    options     = constants.getFigureTypesOptions(),
                                    value       = figureTypeDefault ,
                                    className   = "radio-items-inline"
                                 )
                            ],
                            className = "c-container"
                       ) , width=6
                ),
            ])  ,
            
            dbc.Row([
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
                                    dbc.Label("Distribution"),
                                    dbc.Checklist(
                                        options=[
                                            {"label": constants.labelMean, "value": constants.PlotDistributionMean},
                                            {"label": constants.labelStd, "value": constants.PlotDistributionStd},
                                            {"label": constants.labelMedian, "value": constants.PlotDistributionMedian},
                                            {"label": constants.labelDistAll, "value": constants.PlotDistributionAll},
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
                        , width = 6
                    ),
            ])  ,
                                
            dbc.Row([
                    dbc.Col(
                      html.Div([
                                dcc.Dropdown(
                                    id              = idApp + "-form-feature-multi",
                                    placeholder     = "Select features",
                                    options         = BuildOptionsFeatures( featureMultiOptions ),
                                    multi           = True
                                )
                            ],
                            className = "c-container"
                       )
                        , width=12
                    ),
            ])  ,
            
            dbc.Row([
                    dbc.Col(
                        html.Button(children=[
                                    html.I(className="fas fa-plus font-size_medium p-right_xx-small"),
                                    'Add Plot',  ], 
                                id  =   idApp + "-form-submit-btn", 
                                className="c-button btn btn-outline-primary", n_clicks=0)
                        
                        , width=8
                    ),
            ], className = "m-top_small" )  ,
            
            html.Br()  ,
        ]
    
    
    return html.Div(
        id = idApp + "-control-card-custom-plot-form",
        children =  layout,
        className = "form"
    )
                
                

def getCustomPlot( df, dfOriginal, dfOriginalMean = None, dfOriginalMedian = None, dfOriginalStd = None,
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
                  groupBy               = featureGroupByDefault,
                  selectedDistribution  = [],
                  isThemeSizePlot       = False,
                  selectedFeatureMulti  = [],
    ):
    
    rows = []
    selectedFeatures = []
    
    
    
    if df is None  or df.empty :
        return rows
    
    
    
    if (selectedFigureType in constants.FigureTypes  and 
            constants.keyIsMultiFeatureEnabled in constants.FigureTypes.get(selectedFigureType) and 
            constants.FigureTypes.get(selectedFigureType).get(constants.keyIsMultiFeatureEnabled) ):
        
        if ( (featureX is None    or   '' == featureX ) and  (featureY is None    or   '' == featureY ) and
            (feature3 is None    or   '' == feature3 ) and
            len(selectedFeatureMulti) == 0 ):
            return rows.append( getMsgSelectFeature() )
        
    else:
        if featureX is None    or   '' == featureX :
            return rows.append( getMsgSelectFeature() )
    
        if ( '' == featureY     and    not selectedFigureType == constants.FigureTypePie ):
            return rows.append( getMsgSelectFeature() )
    
        if not featureX in df.columns  :
            return rows.append( getMsgFeatureNotInDF(featureY) )
    
        if not featureY in df.columns     and    not selectedFigureType == constants.FigureTypePie  :
            return rows.append( getMsgFeatureNotInDF(featureY) )
    
    
    if ( '' == feature3     and   constants.FigureTypes.get(selectedFigureType).get(constants.keyIsFeature3Enabled) ):
        return rows
    
    
    
    if selectedFeatureMulti is not None :
        selectedFeatures = list(set(selectedFeatures + selectedFeatureMulti))
    if  feature3 :
        selectedFeatures.insert(0, feature3)
    if  featureY :
        selectedFeatures.insert(0, featureY)
    if  featureX :
        selectedFeatures.insert(0, featureX)
    selectedFeatures = list(set(selectedFeatures))
    
    
    featureX2Plot = featureX
    featureY2Plot = featureY

    orientation = constants.AxisH

    if    selectedAxis == constants.AxisV  :
        featureX2Plot   = featureY
        featureY2Plot   = featureX
        orientation     = constants.AxisV


    
    plotTitle = ' Details of ' 
    plotTitle = plotTitle + str( constants.feature2UserNamesDict.get(featureX2Plot) if featureX2Plot in constants.feature2UserNamesDict.keys() else featureX2Plot )
    plotTitle = plotTitle + ' vs ' + str( constants.feature2UserNamesDict.get(featureY2Plot) if featureY2Plot in constants.feature2UserNamesDict.keys() else featureY2Plot )
    

    numericFeatures = getNumericFeatures(df)
        
    try:
        
        studentDataDfSumMean        = df.mean().round(decimals=2)
        studentDataDfSumStd         = df.std().round(decimals=2)
        studentDataDfSumMedian      = df.median().round(decimals=2)

        df[featureDescription]      = getDataFeatureDescription(df, hoverData, featureTitle = groupBy)
        

        if selectedFigureType == constants.FigureTypeScatter:

            if checkIsFeatureNumeric(df, featureX2Plot):
                 marginalX = constants.MarginalPlotDefault
     
            if checkIsFeatureNumeric(df, featureY2Plot):
                 marginalY = constants.MarginalPlotDefault


            if    selectedDistribution    and   len(selectedDistribution) > 0     and     featureY in numericFeatures :
                
                if   not  featureX in numericFeatures    and    not  featureY in numericFeatures:
                    rows.append(html.Div('Features must be Numerical for Distribution Mean, Std, Median Plot'))
                    return rows
    
    
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
                                 plotTitle          = plotTitle,
                                 isThemeSizePlot    = isThemeSizePlot
                         )

            else :
                if isThemeSizePlot : 
                    figStudents = px.scatter(df, x = featureX2Plot, y = featureY2Plot
                         , title        =   plotTitle
                         , labels       =   constants.feature2UserNamesDict # customize axis label
                         , hover_name   =   hoverName
                         , color        =   groupBy
                         , hover_data   =   hoverData
                         , marginal_x   =   marginalX
                         , marginal_y   =   marginalY
                         , height       =   constants.graphHeight
                         , template     =   constants.graphTemplete
                        )
                    
                else:
                    figStudents = px.scatter(df, x = featureX2Plot, y = featureY2Plot
                         , title        =   plotTitle
                         , labels       =   constants.feature2UserNamesDict # customize axis label
                         , hover_name   =   hoverName
                         , hover_data   =   hoverData
                         , marginal_x   =   marginalX
                         , marginal_y   =   marginalY
                         , template     =   constants.graphTemplete
                    )
                    
                    
    
                figStudents.update_traces(marker    =  constants.THEME_MARKER,
                                  selector          = dict(mode='markers') )
                figStudents.update_layout(constants.THEME_EXPRESS_LAYOUT)
       
    
    
#            Error when plotting pie charts !!!
        elif selectedFigureType == constants.FigureTypePie:       
            plotTitle = ' Details of ' 
            plotTitle = plotTitle + str( constants.feature2UserNamesDict.get(featureX) if featureX in constants.feature2UserNamesDict.keys() else featureX )
    
            figStudents = go.Figure(data =  [go.Pie(
                                         labels         =   df[groupBy],
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
            
            
        elif selectedFigureType == constants.FigureTypeBar :
            
            df = df.sort_values(by=[ featureX2Plot ], ascending=False)
            
            if isThemeSizePlot : 
                figStudents = px.bar( df
                    , x             =   featureX2Plot
                    , y             =   featureY2Plot
                    , title         =   plotTitle
                    , labels        =   constants.feature2UserNamesDict # customize axis label
                    , template      =   constants.graphTemplete                              
                    , orientation   =   orientation
                    , hover_name    =   hoverName
                    , hover_data    =   hoverData
                    , color         =   groupBy
                    , height        =   constants.graphHeight
                )
                
            else:
                figStudents = px.bar( df
                    , x             =   featureX2Plot
                    , y             =   featureY2Plot
                    , title         =   plotTitle
                    , labels        =   constants.feature2UserNamesDict # customize axis label
                    , template      =   constants.graphTemplete                              
                    , orientation   =   orientation
                    , hover_name    =   hoverName
                    , hover_data    =   hoverData
                )
            
            figStudents.update_layout(constants.THEME_EXPRESS_LAYOUT)
        
        
        elif selectedFigureType == constants.FigureTypeBubble :
            df.loc[df[feature3] < 0, feature3] = 0
            
            if not feature3:
                if featureX2Plot in numericFeatures:
                    feature3 = featureX2Plot
                else:
                    feature3 = featureY2Plot
                    

            
            if isThemeSizePlot : 
                figStudents = px.scatter(df
                     , x            =   featureX2Plot
                     , y            =   featureY2Plot
                     , title        =   plotTitle
                     , labels       =   constants.feature2UserNamesDict # customize axis label
                     , hover_name   =   hoverName
                     , hover_data   =   hoverData
                     , size         =   feature3
                     , color        =   groupBy
                     , size_max     =   60
                     , height       =   constants.graphHeight
                     , template     =   constants.graphTemplete
                )
                
            else:
                figStudents = px.scatter(df
                     , x            =   featureX2Plot
                     , y            =   featureY2Plot
                     , title        =   plotTitle
                     , labels       =   constants.feature2UserNamesDict # customize axis label
                     , hover_name   =   hoverName
                     , hover_data   =   hoverData
                     , size         =   feature3
                     , color        =   groupBy
                     , size_max     =   60
                     , template     =   constants.graphTemplete
                    )
            figStudents.update_layout(constants.THEME_EXPRESS_LAYOUT)
            
            rows.append( html.Div(children=[
                            html.P('Size is based on ' + ((constants.feature2UserNamesDict.get(feature3)) if feature3 in constants.feature2UserNamesDict.keys() else feature3 ) ),
                            ]) )
            
            
        elif selectedFigureType == constants.FigureTypeLine :

            if    selectedAxis == constants.AxisV:
                featureX2Plot   = featureY
                featureY2Plot   = featureX
            
            if    isThemeSizePlot : 
                figStudents = px.line(df
                    , x             =   featureX2Plot
                    , y             =   featureY2Plot
                    , color         =   groupBy
                    , hover_name    =   hoverName
                    , hover_data    =   hoverData
                    , height        =   constants.graphHeight
                    , template      =   constants.graphTemplete
                )
                
            else:
                figStudents = px.line(df
                    , x             =   featureX2Plot
                    , y             =   featureY2Plot
                    , color         =   groupBy
                    , hover_name    =   hoverName
                    , hover_data    =   hoverData
                    , template      =   constants.graphTemplete
                )
            figStudents.update_layout(constants.THEME_EXPRESS_LAYOUT)
        
        
        
        
            
        elif     selectedFigureType == constants.FigureTypeTable :
            print('Inside Table Figure')
            plotTitle = ' Details '             
            
            if    groupBy  and    groupBy  in selectedFeatures  :
                selectedFeatures.remove(groupBy)
            
            if    groupBy  and    groupBy not in selectedFeatures :
                selectedFeatures.insert(0, groupBy)
                
            figStudents =  dash_table.DataTable(
                    columns=[
                        {"name": ((constants.feature2UserNamesDict.get(i)) if i in constants.feature2UserNamesDict.keys() else i ), "id": i, "deletable": True, "selectable": True} for i in df[selectedFeatures].columns
                    ],
                    data            =   df[selectedFeatures].to_dict('records'),
                    row_deletable   =   True,
                    filter_action   =   "native",
                    sort_action     =   "native",
                    sort_mode       =   "multi",
                    style_data_conditional = ([
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': constants.THEME_TABLE_ODDROW_COLOR_STYLE
                                },
                     ])
                )
        
        
#default is Dcc Graph        
        if (selectedFigureType in constants.FigureTypes  and 
            constants.keyIsDccGraph in constants.FigureTypes.get(selectedFigureType) and 
            not constants.FigureTypes.get(selectedFigureType).get(constants.keyIsDccGraph) ):
             
            rows.append(
                    html.Span('Data ' + plotTitle), 
                )
            rows.append(
                    html.Div([ figStudents ],
                             className = "c-table ")
            )
        else :
            rows.append( html.Div( dcc.Graph(
                    figure = figStudents
            ) ) )
        


        if 'dfOriginalMean' in locals()   and   dfOriginalMean is not None   and   not dfOriginalMean.empty :
            rows.append(
                    html.Span('Mean'),
                )
            rows.append(
                    html.Div([ getTable(dfOriginalMean[selectedFeatures]) ],
                             className = "c-table ")
            )
        if 'dfOriginalMedian' in locals()   and   dfOriginalMedian is not None   and   not dfOriginalMedian.empty :
            rows.append(
                    html.Span('Median'), 
                )
            rows.append(
                    html.Div([ getTable(dfOriginalMedian[selectedFeatures]) ],
                             className = "c-table ")
            )
        if 'dfOriginalStd' in locals()   and   dfOriginalStd is not None   and   not dfOriginalStd.empty :
            try:
                rows.append(
                    html.Div('Std')
                )
                rows.append(
                        html.Div([ getTable(dfOriginalStd[selectedFeatures]) ],
                                 className = "c-table ")
                )
            except Exception as e: 
                print('std error ' )
                print(e)
        
        
        rows.append(
            html.Span('Distribution')
        )
        
        for featureDist in selectedFeatures:
            try :
                if  (  selectedDistribution  and len(selectedDistribution) > 0 and constants.PlotDistributionAll in selectedDistribution 
                     and  
                     'dfOriginal' in locals()    and dfOriginal is not None and not dfOriginal.empty   
                     and featureDist in dfOriginal.columns  and groupBy in  dfOriginal.columns ) :
                    
                    if  featureDist   in     numericFeatures :
                        figQuantile = px.box(dfOriginal, x = groupBy, y = featureDist, points="all",
                                             title="Distribution of " + str(featureDist),
                                             hover_data=[groupBy, constants.featureStudent , featureDist, "SessionDuration", "Attempts", "Points"]
                                )
                        figQuantile.update_layout(constants.THEME_EXPRESS_LAYOUT)
                        rows.append( html.Div(
                                            dcc.Graph(
                                                    figure = figQuantile
                                )))
                        rows.append( html.Br() )
                
                else:
                    if  featureDist   in     numericFeatures :
                        rows.append( getDistributionForFeature(dfMean = studentDataDfSumMean, 
                                                               dfStd = studentDataDfSumStd,
                                                               dfMedian = studentDataDfSumMedian,
                                                               featureDist = featureDist)  )
            except Exception as e: 
                print('Exception Mean and Std calculation for feature =  ' + featureDist )
                print(e)
                
    except Exception as e: 
        print('Add Graph exception ! ' )
        print(e)
        
                
    return rows         
                

def getTable(df):
    return  dash_table.DataTable(
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
                    ],
                    data            =   df.to_dict('records'),
                    row_deletable   =   True,
                    filter_action   =   "native",
                    sort_action     =   "native",
                    sort_mode       =   "multi",
                    style_data_conditional = ([
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': constants.THEME_TABLE_ODDROW_COLOR_STYLE
                                },
                     ])
            ) 


def getMsgSelectFeature():
    return html.H4('Select Features' )

def getMsgFeatureNotInDF(feature):
    return html.H4('Feature not in data ' + str(feature) + '  . Select another! ' )

def getDistributionForFeature(dfMean, dfStd, dfMedian, featureDist):
    return html.P( children= [
                                    html.Span(((constants.feature2UserNamesDict.get(featureDist)) if featureDist in constants.feature2UserNamesDict.keys() else featureDist ),
                                              className = "p-right_medium" ),
                                    html.Span(constants.labelMean + ' '  + ' = ' + str(dfMean[featureDist]),
                                              className = "p-right_medium" ),
                                    html.Span(constants.labelStd + ' ' + ' = ' + str(dfStd[featureDist]),
                                              className = "p-right_medium"  ),
                                    html.Span(constants.labelMedian + ' ' + ' = ' + str(dfMedian[featureDist]),
                                              className = "p-right_medium"  ),
                            ])
                                    
def updateSelectorDisabled(selectedFigureType, initialClass, isEnabledKey):   
    if None is selectedFigureType or '' == selectedFigureType:
        return initialClass
 
    initialClassS = set()
    
    if not None is initialClass:
        initialClassS = set(initialClass.split(' '))  
    
    if selectedFigureType in constants.FigureTypes   and   not  constants.FigureTypes.get(selectedFigureType).get(isEnabledKey):
        initialClassS.add('disabled')
    else:
        initialClassS.discard('disabled')

    return  ' '.join(initialClassS)


def getCustomPlotScatter(df, featureX2Plot, featureY2Plot, 
                         selectedDistribution = [],
                         mean_featureX      = 0,
                         std_featureX       = 0,
                         med_featureX       = 0,
                         mean_featureY      = 0,
                         std_featureY       = 0,
                         med_featureY       = 0,
                         textFeature        = featureDescription,
                         plotTitle          = '',
                         isThemeSizePlot    = False) :
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
                                    name            = "Mean ",
                                    )
        data_comp.append(trace_median0)
        
    
    if constants.PlotDistributionStd in  selectedDistribution:
        trace_median0 =  go.Scatter(x           = [std_featureX, std_featureX ],
                                    y           = [0, df[featureY2Plot].max() ],
                                    mode        = "lines",
                                    legendgroup = "a",
                                    showlegend  = False,
                                    name        = "Std",
                                    )
        data_comp.append(trace_median0)
        
     
    if constants.PlotDistributionMedian in  selectedDistribution:
        trace_median0 =  go.Scatter(x           = [med_featureX, med_featureX ],
                                    y           = [0, df[featureY2Plot].max() ],
                                    mode        = "lines",
                                    legendgroup = "a",
                                    showlegend  = False,
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
    
    if isThemeSizePlot:
        fig.update_layout(
                autosize    =   False ,
                height      =   constants.graphHeight ,
        )
    
    fig.update_layout(constants.THEME_EXPRESS_LAYOUT)
    
    return fig



def groupedBySelectedFeaturesDf(df, groupBy = '', groupBySub = [], groupByAll = [], hoverData = []):
    
    if not groupBy in groupByAll:
        groupByAll.append( groupBy )

    groupByAll = list(set(groupByAll))

    if groupBySub is not None  and  not groupBySub == [] :
        if groupBy in groupBySub:
            groupBySub.remove(groupBy)
    
        groupByAll = groupByAll + groupBySub
    
    
    groupByAll = list(set(groupByAll))
        
    resultDfSum = df.groupby(groupByAll ,
                                                as_index=False).sum()
    
    for hoverFeature in groupByAll:
        if not hoverFeature in hoverData:
            hoverData.insert(0, hoverFeature)
            
    return resultDfSum, hoverData, groupByAll
                
#---------------------------- UI CONTROLS END ---------------------------------

def getDataFeatureDescription(df, hoverData, featureTitle = "Name"):
    df[featureDescription] = ''
    
    
    if featureTitle in df.columns:
        df[featureDescription] = '<b>' + df[featureTitle].astype(str) + '</b>' + '<br>'
        
    for feature in hoverData:
        if feature in df.columns:
            df[featureDescription] = df[featureDescription] + '<br><b>' + str(constants.feature2UserNamesDict.get(feature) if feature in constants.feature2UserNamesDict.keys() else feature  ) + '</b>: ' + df[feature].astype(str)
    
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
    
def BuildOptions(options):  
    return [{ constants.keyLabel : i , 
             constants.keyValue : i} for i in options]

def BuildOptionsFeatures(options):  
    return [{ constants.keyLabel : constants.feature2UserNamesDict.get(i) if i in constants.feature2UserNamesDict.keys() else i , 
             constants.keyValue : i} for i in options]




def get_unique_list_feature_items(dfData, feature =    constants.featureConceptsUsed  ):
    return set(dfData[ dfData[feature].notnull() & (dfData[feature]  !=  u'')  ][feature].sum())
    




def isValidValueId(valueId):
    if valueId is not None and not (valueId == '') and (type(valueId) == int or type(valueId) == float) and  int(valueId) >= 0 :
        return True
 
    return False