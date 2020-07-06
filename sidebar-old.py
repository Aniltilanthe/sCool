# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:45:09 2020

@author: tilan
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ClientsideFunction
import visdcc
import dash_dangerously_set_inner_html


from app import app



# the style arguments for the sidebar. We use position:fixed and a fixed width
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
    'borderColor': 'blanchedalmond',
    'borderWidth': '1px',
    'width': '100%'
}


submenu_1 = [
    html.Li(
        # use Row and Col components to position the chevrons
        dbc.Row(
            [
                dbc.Col([
                        dbc.NavLink("Overview", href="/Overview", className="menu-link", id="menu-link-0" )
                        ]),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3"), width="auto"
                ),
            ],
            className="my-1",
        ),
        id="menu-0",
    ),
    # we use the Collapse component to hide and reveal the navigation links
    dbc.Collapse(
        [
            dbc.NavLink("Groups", href="/Overview#Group-Information", className="menu-link", id="menu-link-1" ),
#            html.Button('Groups', className="menu-link", id="menu-link-1",
#                        style = MENU_BUTTON_STYLE),
            dbc.NavLink("Custom", href="/Overview#Custom-Information", className="menu-link", id="menu-link-2" ),
#            html.Button('Custom', className="menu-link", id="menu-link-2",
#                        style = MENU_BUTTON_STYLE),
            dbc.NavLink("Students", href="/Overview#Student-Information", className="menu-link", id="menu-link-3" ),
#            html.Button('Students', className="menu-link", id="menu-link-3",
#                        style = MENU_BUTTON_STYLE),
            
            dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
                <a href="/Details#Test-Information" class="nav-link" id="menu-link-227" onclick="pageMenuScroll(event, 'Student-Information')">Testing StudentInfo</a>
            '''),
        ],
        is_open = True,
        id="menu-0-collapse",
        className="p-left_medium",
    ),
]

submenu_2 = [
    html.Li(
        dbc.Row(
            [
                dbc.Col( [
                        dbc.NavLink("Details", href="/Details", className="menu-link", id="menu-link-4" ),            
                        ]),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3"), width="auto"
                ),
            ],
            className="my-1",
        ),
        id="menu-4",
    ),
    dbc.Collapse(
        [
            dbc.NavLink("Tasks Info", href="/Details#Task-Information", className="menu-link", id="menu-link-5" ),
#            html.Button('Tasks Info', className="menu-link", id="menu-link-5",
#                        style = MENU_BUTTON_STYLE),
            dbc.NavLink("General Info", href="/Details#General-Information", className="menu-link", id="menu-link-6" ),
#            html.Button('General Info', className="menu-link", id="menu-link-6",
#                        style = MENU_BUTTON_STYLE),
            dbc.NavLink("Student Info", href="/Details#Student-Information", className="Student-Information", id="menu-link-7" ),
#            html.Button('Student Info', className="menu-link", id="menu-link-7",
#                        style = MENU_BUTTON_STYLE),
            dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
                <a href="/Details#Test-Information" class="nav-link" id="menu-link-227" onclick="pageMenuScroll(event, 'Student-Information')">Testing StudentInfo</a>
            '''),
        ],
        is_open = True,
        id="menu-4-collapse",
        className="p-left_medium",
    ),
    html.Div(id='menu-link-output-hidden', style={'display':'none'}),
    html.Div(id='menu-link-output-prevent-default', style={'display':'none'}),
    dcc.Input(
            id="menu-link-input",
            type="text", 
            style={'display':'none'},
            value="Overview"
        )
]


sidebar = html.Div(
    [
        html.H2("sCool", className="display-4"),
        html.P(
            "Student perfomance in sCool", className="lead"
        ),
        html.Hr(),
        dbc.Nav(submenu_1 + submenu_2, vertical=True),
        
        
        visdcc.Run_js(id = 'javascript')
    
    
    ],
    style=SIDEBAR_STYLE,
    id="sidebar",
)



menuLinksCount = 8
@app.callback ( [ Output(f"menu-link-{i}", "className")  for i in range(menuLinksCount) ] , 
              [Input(f"menu-link-{j}", "n_clicks")   for j in range(menuLinksCount) ])
def changeMenuClass(*args):
    ctx = dash.callback_context
    newClasses = [""] * (menuLinksCount)

    print('change Menu Class')    
    print(args)
    print(ctx.triggered)
    
    if not ctx.triggered or not any(args):
        return newClasses
    
    triggered_id = [p['prop_id'] for p in ctx.triggered][0]
    clickedButton_id = triggered_id.split('.')[0]
    
    clickedButton_index = int(clickedButton_id.split('-')[2])
    
    
    if clickedButton_index >= 0:
        newClasses[clickedButton_index] = "open highlight"
        
    return newClasses    



       
                        
menuLink2Scroll = {
		"menu-link-1" : 'Group-Information'
		,"menu-link-2" : 'Custom-Information'
		,"menu-link-3" : "Student-Information"
		,"menu-link-5" : 'Task-Information'
		,"menu-link-6" : 'General-Information'
		,"menu-link-7" : 'Student-Information'
	}



@app.callback ( Output("menu-link-input", "value") , 
              [Input(f"menu-link-{j}", "n_clicks")   for j in range(menuLinksCount) ])
def changeMenuSetInput(*args):
    ctx = dash.callback_context
    newValue = ""

    
    if not ctx.triggered or not any(args):
        return newValue
    
    triggered_id = [p['prop_id'] for p in ctx.triggered][0]
    clickedButton_id = triggered_id.split('.')[0]

    print(clickedButton_id)
    
    if clickedButton_id     and   clickedButton_id in menuLink2Scroll :
         return menuLink2Scroll.get(clickedButton_id)
        
    return newValue    
    

#@app.callback ( Output('javascript', 'run'), 
#              [Input("menu-link-input", "value")   ])
#def onClickMenuNav(x): 
#    
#    execJs = "var elmnt = document.getElementById('Student-Information');"
#    execJs += "elmnt.scrollIntoView();"
#    
#    if x: 
#        return execJs
#    return ""


app.clientside_callback(
        # specifiy the callback with ClientsideFunction(<namespace>, <function name>)
        ClientsideFunction('ui', 'jsFunction'),
        # the Output, Input and State are passed in as with a regular callback
         Output('menu-link-output-hidden', 'children'),
        [Input("menu-link-input", "value")]
    )



#@app.callback ( Output("menu-link-output-prevent-default", "children") , 
#              [Input(f"menu-link-{j}", "n_clicks")   for j in range(menuLinksCount) ])
#def changeMenuPreventDefault(*args):
#    ctx = dash.callback_context
#    newClasses = [""] * (menuLinksCount)
#
#    print('change Menu Class')    
#    print(args)
#    print(ctx.triggered)
#    
#    if not ctx.triggered or not any(args):
#        return newClasses
#    
#    triggered_id = [p['prop_id'] for p in ctx.triggered][0]
#    clickedButton_id = triggered_id.split('.')[0]
#    
#    
#    if clickedButton_id   and   clickedButton_id in menuLink2Scroll :
#        raise dash.exceptions.PreventDefault
#        