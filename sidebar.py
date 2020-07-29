# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:45:09 2020

@author: tilan
"""
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ClientsideFunction
import visdcc
import dash_dangerously_set_inner_html


from app import app
import constants


# the style arguments for the sidebar. We use position:fixed and a fixed width


#-------------------------------------------------------------------------

keyLabel    = 'label'
keyHref     = 'href'
keySubmenu  = 'submenu'
keyValue    = 'value'
keyScrollTo  = 'scrollTo'

menu = {
    "Overview" : { keyLabel : 'Overview', keyHref : '/Overview',
                  keySubmenu : [
                          "menu-sub-link-0", "menu-sub-link-1", "menu-sub-link-2"
                          ]  }
    ,   "Details" : { keyLabel : 'Details', keyHref : '/Details' ,
                  keySubmenu : [
                          "menu-sub-link-3", "menu-sub-link-4", "menu-sub-link-5"
                          ]  }
    ,   "Custom" : { keyLabel : 'Custom', 'href' : '/Custom' ,
                  keySubmenu : [
                          "menu-sub-link-6"
                          ]  }
}
menuLink2Scroll = {
		"menu-sub-link-0"  :  {keyLabel : "Overview", keyScrollTo: ''}
		,"menu-sub-link-1" :  {keyLabel : "Groups", keyScrollTo: 'row-control-main-overview'}
		,"menu-sub-link-2" :  {keyLabel : "Distribution", keyScrollTo: "Group-Distribution-Information"}
		,"menu-sub-link-3" :  {keyLabel : "Tasks Info", keyScrollTo: 'Task-Information'}
		,"menu-sub-link-4" :  {keyLabel : "General Info", keyScrollTo: 'General-Information'}
		,"menu-sub-link-5" :  {keyLabel : "Student Info", keyScrollTo: 'Student-Information'}
		,"menu-sub-link-6" :  {keyLabel : "Custom", keyScrollTo: ''}
	}


br = [html.Br()]

def getSubmenuButtons(menuKey):
    currentMenu = menu.get(menuKey)
    result = []
    countMenuSubLink = 0
    
    for submenuKey in currentMenu.get(keySubmenu):
        result.append(
                dbc.Button(menuLink2Scroll.get(submenuKey).get('label'), 
                                   id="menu-sub-link-" + str(countMenuSubLink), 
                                   outline=True, color="primary", 
                                   className="mr-2 w-100", 
                                   block=True),
        )

def getMenu():
    menus = []
    
    countMenuLink = 0
    countMenuSubLink = 0
    
    for menuKey in menu.keys():
        currentMenu = menu.get(menuKey)
        menus.append( 
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        dbc.Col([
                                
                                dbc.Button(html.Span([ currentMenu.get(keyLabel) , 
                                                      html.I(className="fas fa-chevron-right mr-3", 
                                                             style= {'float': 'right'})]), 
                                           href= currentMenu.get(keyHref) , 
                                           size="lg", 
                                           className="mr-1", 
                                           outline=True, color="primary", 
                                           id="menu-link-" + str(countMenuLink), 
                                           block=True),
                                ]),
                    ],
                    className="my-1",
                ),
            ) 
        )
        # we use the Collapse component to hide and reveal the navigation links
        subMenuButtons = []
        
        for submenuKey in currentMenu.get(keySubmenu):
            subMenuButtons.append(
                    dbc.Button(menuLink2Scroll.get(submenuKey).get('label'), 
                                       id="menu-sub-link-" + str(countMenuSubLink), 
                                       outline=True, color="primary", 
                                       className="mr-2 w-100", 
                                       block=True),
            )
            countMenuSubLink += 1
            
        
        menus.append( 
                dbc.Collapse(
                    subMenuButtons,
                    id="menu-link-" + str(countMenuLink) + "-collapse",
                    className="p-left_medium",
                )
        )
                
        countMenuLink += 1
        menus = menus + br

    return menus



sidebar = html.Div(
    [
        html.H2("sCool", className="display-4"),
        html.P(
            "Student perfomance in sCool", className="lead"
        ),
        html.Hr(),
#        dbc.Nav(submenu_1 + br + submenu_2 + br + submenu_3, vertical=True),
        dbc.Nav( getMenu(), vertical=True),
                
#        for menu link click output
        html.Div(id='menu-link-output-hidden', style={'display':'none'}),
        html.Div(id='menu-link-output-prevent-default', style={'display':'none'}),
        dcc.Input(
                id="menu-link-input",
                type="text", 
                style={'display':'none'},
                value="Overview"
            ),
        html.Div(id='menu-sub-link-output-hidden', style={'display':'none'}),
        dcc.Input(
                id="menu-sub-link-input",
                type="text", 
                style={'display':'none'},
                value="Overview"
            )
    
    
    ],
    style= constants.SIDEBAR_STYLE,
    id="sidebar",
)


#CHANGE THE MENU LINK COUNT WHEN ADDING A NEW MENU
menuLinksCount      =   3
menuSubLinksCount   =   len(menuLink2Scroll.keys())
initUrl0 = "/Overview"
initUrl1 = "/Details"
initUrl2 = "/Custom"
@app.callback(
    [Output(f"menu-link-{i}-collapse", "is_open") for i in range(menuLinksCount)],
    ([Input(f"menu-link-{i}", "n_clicks") for i in range(menuLinksCount) ] + [ Input("url", "pathname")]),
    [State(f"menu-link-{i}-collapse", "is_open") for i in range(menuLinksCount)],
)
def toggle_accordion(*args):
    ctx = dash.callback_context

    newToggle = [False] * (menuLinksCount)
    
    if not ctx.triggered:
        return newToggle

    triggered_id = [p['prop_id'] for p in ctx.triggered][0]
    clickedButton_id = triggered_id.split('.')[0]     
    
#    on INIT url changes is the clickedButton_id
    if len(clickedButton_id.split('-')) == 1 :
        if args[menuLinksCount ] in ["/", initUrl0]:
            newToggle[0] = True 
        elif args[menuLinksCount ] == initUrl1:
            newToggle[1] = True
        print(newToggle)
        return newToggle

    clickedButton_index = int(clickedButton_id.split('-')[2])
    
        
    if clickedButton_index >= 0  and  args[clickedButton_index] :
        newToggle[clickedButton_index] = not args[menuLinksCount + 1 + clickedButton_index ]   # add 1 for URL pathname param
        
    
    return newToggle





@app.callback(  [ Output(f"menu-link-{i}", "className") for i in range(menuLinksCount) ], 
                 [Input(f"menu-link-{i}-collapse", "is_open") for i in range(menuLinksCount)] )
def setMenuClassOnChangeOpen(*args):   
    return  np.where(args,"open highlight",'').tolist()

     



@app.callback ( Output("menu-sub-link-input", "value") , 
              [Input(f"menu-sub-link-{j}", "n_clicks")   for j in range(menuSubLinksCount) ])
def changeMenuSetInput(*args):
    ctx = dash.callback_context
    newValue = ""

    
    if not ctx.triggered or not any(args):
        return newValue
    
    triggered_id = [p['prop_id'] for p in ctx.triggered][0]
    clickedButton_id = triggered_id.split('.')[0]

    print(clickedButton_id)
    
    if clickedButton_id     and   clickedButton_id in menuLink2Scroll :
         return menuLink2Scroll.get(clickedButton_id).get('scrollTo')
        
    return newValue    
    


app.clientside_callback(
        # specifiy the callback with ClientsideFunction(<namespace>, <function name>)
        ClientsideFunction('ui', 'jsFunction'),
        # the Output, Input and State are passed in as with a regular callback
         Output('menu-sub-link-output-hidden', 'children'),
        [Input("menu-sub-link-input", "value")]
    )