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


from app import app
import constants


# the style arguments for the sidebar. We use position:fixed and a fixed width


#-------------------------------------------------------------------------

keyLabel    = 'label'
keyHref     = 'href'
keySubmenu  = 'submenu'
keyValue    = 'value'
keyScrollTo  = 'scrollTo'
keyClassName  = 'className'

menuLink = {
     "menu-link-0" : { keyLabel : 'Home', keyHref : '/Home',
                  keySubmenu : [ 
                          ],  keyClassName : 'fas fa-home m-right-small' }
    ,   "menu-link-1" : { keyLabel : 'Groups', keyHref : '/Groups',
                  keySubmenu : [
                          "menu-sub-link-0", "menu-sub-link-1", "menu-sub-link-2"
                          ],  keyClassName : 'fas fa-list m-right-small'   }
    ,   "menu-link-2" : { keyLabel : 'Details', keyHref : '/Details' ,
                  keySubmenu : [
                          "menu-sub-link-3", "menu-sub-link-7", "menu-sub-link-4"
                          ],  keyClassName : 'fas fa-clipboard m-right-small'   }
    ,   "menu-link-3" : { keyLabel : 'Students', keyHref : '/Students' ,
                  keySubmenu : [ "menu-sub-link-5"  
                          ],  keyClassName : 'fas fa-user-graduate m-right-small'   }
    ,   "menu-link-4" : { keyLabel : 'Custom', 'href' : '/Custom' ,
                  keySubmenu : [
                          "menu-sub-link-6"
                          ],  keyClassName : 'fas fa-wrench m-right-small'   }
}
menuSubLink2Scroll = {
		"menu-sub-link-0"  :  {keyLabel : "Overview", keyScrollTo: ''}
		,"menu-sub-link-1" :  {keyLabel : "Compare Groups", keyScrollTo: 'row-control-main-overview'}
		,"menu-sub-link-2" :  {keyLabel : "Distribution", keyScrollTo: "Group-Distribution-Information"}
		,"menu-sub-link-3" :  {keyLabel : "Tasks Info", keyScrollTo: 'Task-Information'}
		,"menu-sub-link-4" :  {keyLabel : "General Info", keyScrollTo: 'General-Information'}
		,"menu-sub-link-7" :  {keyLabel : "Concept Info", keyScrollTo: 'Concept-Information'}
		,"menu-sub-link-5" :  {keyLabel : "Student Info", keyScrollTo: 'Student-Information'}
		,"menu-sub-link-6" :  {keyLabel : "Custom", keyScrollTo: ''}
	}


br = [html.Br()]

def getSubmenuButtons(menuKey):
    currentMenu = menuLink.get(menuKey)
    result = []
    countMenuSubLink = 0
    
    for submenuKey in currentMenu.get(keySubmenu):
        result.append(
                dbc.Button(menuSubLink2Scroll.get(submenuKey).get('label'), 
                                   id="menu-sub-link-" + str(countMenuSubLink), 
                                   outline=True, color="primary", 
                                   className="mr-2 w-100", 
                                   block=True),
        )

def getMenu():
    menus = []
    
    countMenuLink = 0
    countMenuSubLink = 0
    
    for menuKey in menuLink.keys():
        currentMenu = menuLink.get(menuKey)
        
        menuOpener = [html.I(className="fas fa-chevron-right mr-3", style= {'float': 'right'})] 
        if len(currentMenu.get(keySubmenu)) == 0  :
            menuOpener = []
        
        menus.append( 
            html.Li(
                # use Row and Col components to position the chevrons
                dbc.Row(
                    [
                        dbc.Col([
                                
                                dbc.Button(html.Span([html.I(className=  currentMenu.get(keyClassName)),
                                                      currentMenu.get(keyLabel) ]
                                                       +
                                                       menuOpener ), 
                                           href= currentMenu.get(keyHref) , 
                                           size="lg", 
                                           className="mr-1", 
                                           outline=True, color="primary", 
                                           id= menuKey, 
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
                    dbc.Button(menuSubLink2Scroll.get(submenuKey).get('label'), 
                                       id=  submenuKey , 
                                       outline=True, color="primary", 
                                       className="mr-2 w-100", 
                                       block=True),
            )
            countMenuSubLink += 1
            
        
        menus.append( 
                dbc.Collapse(
                    subMenuButtons,
                    id= menuKey + "-collapse",
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
                value="Groups"
            ),
        html.Div(id='menu-sub-link-output-hidden', style={'display':'none'}),
        dcc.Input(
                id="menu-sub-link-input",
                type="text", 
                style={'display':'none'},
                value="Groups"
            )
    
    
    ],
    className = " page-sidebar ",
    id="sidebar",
)


menuLinksCount      =   len(menuLink.keys())  
@app.callback(
    [Output(f"{i}-collapse", "is_open") for i in menuLink],
    ([Input(f"{i}", "n_clicks") for i in menuLink ] + [ Input("url", "pathname")]),
    [State(f"{i}-collapse", "is_open") for i in menuLink],
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
        if args[menuLinksCount ] in ["/"]:
            newToggle[0] = True 
        else :
            for index, menuLinkKey in enumerate(list(menuLink.keys())):
                if args[ menuLinksCount ].lower()   in  menuLink.get(menuLinkKey).get(keyHref).lower():
                    newToggle[index] = True   
        
        return newToggle

    clickedButton_index = int(clickedButton_id.split('-')[2])
    
    if clickedButton_index >= 0  and  args[clickedButton_index] :
        newToggle[clickedButton_index] = not args[menuLinksCount + 1 + clickedButton_index ]   # add 1 for URL pathname param
        
    
    return newToggle





@app.callback(  [ Output(f"{i}", "className") for i in menuLink ], 
                 [Input(f"{i}-collapse", "is_open") for i in menuLink] )
def setMenuClassOnChangeOpen(*args):   
    return  np.where(args,"open highlight",'').tolist()

     



@app.callback ( Output("menu-sub-link-input", "value") , 
              [Input(f"{j}", "n_clicks")   for j in menuSubLink2Scroll ])
def changeMenuSetInput(*args):
    ctx = dash.callback_context
    newValue = ""

    
    if not ctx.triggered or not any(args):
        return newValue
    
    triggered_id = [p['prop_id'] for p in ctx.triggered][0]
    clickedButton_id = triggered_id.split('.')[0]

    print(clickedButton_id)
    
    if clickedButton_id     and   clickedButton_id in menuSubLink2Scroll :
         return menuSubLink2Scroll.get(clickedButton_id).get('scrollTo')
        
    return newValue    
    


app.clientside_callback(
        # specifiy the callback with ClientsideFunction(<namespace>, <function name>)
        ClientsideFunction('ui', 'jsFunction'),
        # the Output, Input and State are passed in as with a regular callback
         Output('menu-sub-link-output-hidden', 'children'),
        [Input("menu-sub-link-input", "value")]
    )