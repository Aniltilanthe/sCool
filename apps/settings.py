# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 21:24:40 2020

@author: tilan
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ClientsideFunction


from app import app
import constants

THEME_COLOR_MAP     = constants.THEME_COLOR_MAP

keyLabel            = constants.keyLabel
keyHref             = constants.keyHref
keySubmenu          = constants.keySubmenu
keyValue            = constants.keyValue
keyScrollTo         = constants.keyScrollTo
keyClassName        = constants.keyClassName
keyColor            = constants.keyColor
keyBackgroundColor  = constants.keyBackgroundColor
keyIsDefault        = constants.keyIsDefault

iconNameHome        = constants.iconNameHome
iconNameGroups      = constants.iconNameGroups
iconNameDetails     = constants.iconNameDetails
iconNameStudents    = constants.iconNameStudents
iconNameCustom      = constants.iconNameCustom




themeOptionsButtonPre = "setting-customize-"

layoutModalBodyCustomize =[
    html.H5( children = [ html.I(className="fas fas fa-palette p-right_xx-small"),   "Customize theme"  ] ),
    html.P("Customize application theme"),
    
    html.Br()
    
    , dcc.Input(
                id              = "setting-customize-theme-color-input",
                type            = "text", 
                className       = "hidden",
                value           = "cyan"
            )
    , dcc.Input(
                id              = "setting-customize-theme-background-color-input",
                type            = "text", 
                className       = "hidden",
                value           = "cyan"
            )
    , html.Div(id='setting-customize-theme-color-output', className = "hidden"  )
]
layoutModalBodyCustomize = layoutModalBodyCustomize + [ html.Button(children=[
                                                            html.Span(  THEME_COLOR_MAP.get(i).get(keyLabel)  ) ],
                                                            id          = themeOptionsButtonPre + i, 
                                                            className   = "c-button button w3-btn w3-xlarge btn c-button-tile " + THEME_COLOR_MAP.get(i).get(keyClassName), 
                                                            n_clicks    = 0 )   for i in THEME_COLOR_MAP ]


layoutModalBodyHelp = [
    html.H5( children = [ html.I(className="fas " + iconNameHome + " p-right_xx-small"),   "Home"  ] ),
    html.P("Information about the game data"),
    
    html.Br(),
    
    html.H5( children = [ html.I(className="fas " + iconNameGroups + " p-right_xx-small"),   "Groups"  ] ),
    html.P("Compare groups for quick informations"),
    html.P("Main group is highlighted with application theme"),
    html.P("The minimum values of other groups are highlighted"),
    html.P("Distribution : distribution of various features"),
    
    html.Br(),
    
    
    html.H5( children = [ html.I(className="fas " + iconNameDetails + " p-right_xx-small"),   "Details"  ] ),
    html.P("Group details"),
    
    html.Br(),
    
    html.H5( children = [ html.I(className="fas " + iconNameStudents + " p-right_xx-small"),   "Students"  ] ),
    html.P("Group Student details"),
    
    html.Br(),
    
    html.H5( children = [ html.I(className="fas " + iconNameCustom + " p-right_xx-small"),   "Custom"  ] ),
    html.P("Create custom figures specifying various parameters"),
    html.P( children = [ html.I(className="fas fa-chart-bar font-size_medium p-right_xx-small"),   "Bar"  ]),
    html.P( children = [ html.I(className="fas fa-circle font-size_medium p-right_xx-small"),   "Scatter"  ] ),
    html.P( children = [ html.I(className="fas fa-chart-pie font-size_medium p-right_xx-small"),   "Pie"  ] ),
    html.P( children = [ html.I(className="fas fa-ellipsis-h font-size_medium p-right_xx-small"),   "Bubble" ] ),
    html.P( children = [ html.I(className="fas fa-chart-line font-size_medium p-right_xx-small"),   "Line" ] ),
    
       
    html.Br(),
        
    
    html.H5("Programming concepts"),
      
    dcc.Link(children       = ['Python programming concepts']
             , href         = "https://docs.python.org/dev/library/ast.html"
             , className    = "c-link"
    ),
    
    html.P("The ast module helps Python applications to process trees of the Python abstract syntax grammar. The abstract syntax itself might change with each Python release; this module helps to find out programmatically what the current grammar looks like."),
    html.P("expr   =   BoolOp , NamedExpr, BinOp, UnaryOp"),
    html.P("operator    =   Add , Sub , Mult , MatMult , Div , Mod , Pow , LShift , RShift , BitOr , BitXor , BitAnd , FloorDiv"),
       
    html.Br(),
]



settingsLayout = [
        
    dbc.Tabs(
        [
            dbc.Tab( layoutModalBodyCustomize , label="Customize"),
            dbc.Tab( layoutModalBodyHelp , label="Help"),
        ]
    )
        
]





#------------------------------Customize Application ------------------------------

def setAppTheme(newTheme):
    
    constants.THEME = newTheme
    constants.THEME_COLOR, constants.THEME_BACKGROUND_COLOR, constants.THEME_COLOR_LIGHT, constants.THEME_EXPRESS_LAYOUT = constants.refreshThemeColor()


@app.callback ( [ Output("setting-customize-theme-background-color-input", "value") ,
                    Output("setting-customize-theme-color-input", "value"), 
                 ], 
              [Input( themeOptionsButtonPre + f"{j}", "n_clicks")   for j in THEME_COLOR_MAP ])
def onChangeCustomizeAppTheme(*args):
    ctx = dash.callback_context
    newValue = "", ""

    if not ctx.triggered or not any(args):
        return newValue
    
    triggered_id = [p['prop_id'] for p in ctx.triggered][0]
    clickedButton_id = triggered_id.split('.')[0]
    
    if not clickedButton_id == ''  and clickedButton_id.split(themeOptionsButtonPre)[1] in THEME_COLOR_MAP :
        setAppTheme( clickedButton_id.split(themeOptionsButtonPre)[1] )
        
        return [
                THEME_COLOR_MAP.get( clickedButton_id.split(themeOptionsButtonPre)[1] ).get(keyBackgroundColor),
                THEME_COLOR_MAP.get( clickedButton_id.split(themeOptionsButtonPre)[1] ).get(keyColor),  ]
        
    return newValue  




app.clientside_callback(
        # specifiy the callback with ClientsideFunction(<namespace>, <function name>)
        ClientsideFunction('ui', 'updateThemeColor'),
        # the Output, Input and State are passed in as with a regular callback
         Output('setting-customize-theme-color-output', 'children'),
        [ Input("setting-customize-theme-background-color-input", "value"),
            Input("setting-customize-theme-color-input", "value"),
            ]
    )