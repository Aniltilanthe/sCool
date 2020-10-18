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


from flask_login import current_user

from app import app
import constants
from data import studentGrouped

from apps import settings


# the style arguments for the sidebar. We use position:fixed and a fixed width


#-------------------------------------------------------------------------

keyLabel            = constants.keyLabel
keyHref             = constants.keyHref
keySubmenu          = constants.keySubmenu
keyValue            = constants.keyValue
keyScrollTo         = constants.keyScrollTo
keyClassName        = constants.keyClassName
keyOnlyForAdmin     = constants.keyOnlyForAdmin

iconNameHome        = constants.iconNameHome
iconNameGroups      = constants.iconNameGroups
iconNameDetails     = constants.iconNameDetails
iconNameStudents    = constants.iconNameStudents
iconNameCustom      = constants.iconNameCustom



menuLink = {
     "menu-link-0" : { keyLabel : 'Game Data', keyHref : '/Home',
                  keySubmenu : [ 
                          ],  keyClassName : 'fas ' + iconNameHome + ' m-right-small',
                          keyOnlyForAdmin : True }
    ,   "menu-link-1" : { keyLabel : 'Groups', keyHref : '/Groups',
                  keySubmenu : [
                          "menu-sub-link-0", "menu-sub-link-1", "menu-sub-link-2"
                          ],  keyClassName : 'fas ' + iconNameGroups + ' m-right-small',
                          keyOnlyForAdmin : True    }
    ,   "menu-link-2" : { keyLabel : 'Details', keyHref : '/Details' ,
                  keySubmenu : [
                          "menu-sub-link-3", "menu-sub-link-7", "menu-sub-link-4"
                          ],  keyClassName : 'fas ' + iconNameDetails + ' m-right-small',
                          keyOnlyForAdmin : False    }
    ,   "menu-link-3" : { keyLabel : 'Students', keyHref : '/Students' ,
                  keySubmenu : [ "menu-sub-link-5"  
                          ],  keyClassName : 'fas ' + iconNameStudents + ' m-right-small',
                          keyOnlyForAdmin : False    }
    ,   "menu-link-4" : { keyLabel : 'Custom', keyHref : '/Custom' ,
                  keySubmenu : [
                          "menu-sub-link-6"
                          ],  keyClassName : 'fas ' + iconNameCustom + ' m-right-small',
                          keyOnlyForAdmin : False    }
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


spacer = [html.Div(className = "  m-bottom_x-small ")]

def getSubmenuButtons(menuKey):
    currentMenu = menuLink.get(menuKey)
    result = []
    countMenuSubLink = 0
    
    for submenuKey in currentMenu.get(keySubmenu):
        result.append(
                dbc.Button(menuSubLink2Scroll.get(submenuKey).get('label'), 
                                   id="menu-sub-link-" + str(countMenuSubLink), 
                                   outline=True, color="primary", 
                                   className="", 
                                   block=True),
        )

def getMenu():
    menus = []
    
    print('getMenu ')
    
    countMenuLink = 0
    countMenuSubLink = 0
    
    isUserAdmin = False    
    
    print(current_user)
    
    if current_user and current_user is not None   and   not isinstance(current_user, type(None))  and    current_user.is_authenticated:
        userDB = studentGrouped.getUserFromUserId(current_user.id)
        
        print(userDB)
        if  userDB is not None:        
            if userDB['IsAdmin']:
                isUserAdmin = True

    
    print('getMenu check isUserAdmin')
    print(isUserAdmin)

    for menuKey in menuLink.keys():
        currentMenu = menuLink.get(menuKey)
        
#        menuOpener = [html.I(className="fas fa-chevron-right mr-3 c-button-nav-icon-right float-r")] 
        contentClass = ""
        if len(currentMenu.get(keySubmenu)) > 0  :
            contentClass = " c-button-nav-content-hover-items "
        
        menus.append(
            html.Li(
                # use Row and Col components to position the chevrons
                        dbc.Button(html.Span([
                                                html.Span(children = [
                                                            html.I(className=  currentMenu.get(keyClassName)),
                                                            html.Span(currentMenu.get(keyLabel), className = "c-button-nav-text")
                                                    ], 
                                                    className = contentClass)
                                                ]
                                        ,
                                        className = " c-button-nav-content " ), 
                                    href= currentMenu.get(keyHref) , 
                                    size="lg", 
                                    className=" c-button-nav ", 
                                    outline=True, color="primary", 
                                    id= menuKey, 
                                    block=True),
                className = "hidden-v "  if    not isUserAdmin   and   currentMenu.get(keyOnlyForAdmin)   else   "m-top_x-small",
                id = menuKey + '-li-container' 
            )
        )
        # we use the Collapse component to hide and reveal the navigation links
        subMenuButtons = []
        
        for submenuKey in currentMenu.get(keySubmenu):
            subMenuButtons.append(
                    dbc.Button(menuSubLink2Scroll.get(submenuKey).get('label'), 
                                       id=  submenuKey , 
                                       outline=True, color="primary", 
                                       className="m_x-small", 
                                       block=True),
            )
            countMenuSubLink += 1
            
        
        menus.append( 
                dbc.Collapse(
                    subMenuButtons,
                    id= menuKey + "-collapse",
                    className=" p-left_small ",
                )
        )
                
        countMenuLink += 1
        menus = menus + spacer

    return menus



def getModalHelpBody():
    return settings.settingsLayout

sidebar = html.Div(
    [

        html.H2(
                html.Img(src=app.get_asset_url('sCool-Logo.png'), className="img-fit" ), className="display-4"),

        html.P(
            "Student perfomance in sCool", className="lead"
        ),

        html.Hr(),

        dbc.Nav( children = getMenu(), 
                id = "menu-main-nav",
                vertical=True),
                
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
        
        , html.Div(
            [
                html.Button(children=[
                        html.I(className="fas fa-cogs font-size_medium p-right_xx-small"),
#                        html.Span( 'Help', className = "menu-modal-help-button-text"  ) 
                        ],
                        id='menu-modal-setting-open', 
                        className="c-button button w3-btn w3-xlarge menu-modal-help-button btn btn-outline-info ", n_clicks=0),
                dbc.Modal(
                    [
                        dbc.ModalHeader("sCool Data Analysis Tool Information & Settings"),
                        dbc.ModalBody(  children = getModalHelpBody()  ),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="menu-modal-setting-close", className="ml-auto")
                        ),
                    ],
                    id="menu-modal-setting",
                    className = "c-modal-large"
                ),
            ],
            className = "menu-modal-help"
        ) 
        , 
    ],
    className = " page-sidebar p-bottom_x-large hidden",
    id="page-sidebar",
)


menuLinksCount      =   len(menuLink.keys())  
@app.callback(
    [Output(f"{i}-collapse", "is_open") for i in menuLink],
    ([Input(f"{i}", "n_clicks") for i in menuLink ] + [ Input("url", "pathname")]),
    [State(f"{i}-collapse", "is_open") for i in menuLink],
)
def toggle_accordion(*args):
    ctx = dash.callback_context

    print('sidebar  toggle_accordion ')
    
    newToggle = [False] * (menuLinksCount)
    print(newToggle)
    print(ctx.triggered)
    print(args)
    print(args[ menuLinksCount ])
    
    if not ctx.triggered:
        
        for index, menuLinkKey in enumerate(list(menuLink.keys())):
                if  (   ( args[ menuLinksCount ] is not None  ) 
                        and   args[ menuLinksCount ].lower()   in  menuLink.get(menuLinkKey).get(keyHref).lower()):
                    newToggle[index] = True
                    
        return newToggle

    triggered_id = [p['prop_id'] for p in ctx.triggered][0]
    clickedButton_id = triggered_id.split('.')[0]
            
    print('sidebar  clickedButton_id ')
    print(clickedButton_id)
    
#    on INIT url changes is the clickedButton_id
    if len(clickedButton_id.split('-')) == 1 :
        if args[menuLinksCount ] in ["/"]:
            newToggle[0] = True 
        else :
            for index, menuLinkKey in enumerate(list(menuLink.keys())):
                if (  ( args[ menuLinksCount ] is not None  ) 
                        and  args[ menuLinksCount ].lower()   in  menuLink.get(menuLinkKey).get(keyHref).lower()  ) :
                    newToggle[index] = True   
        
        print('on init url')
        print(args[menuLinksCount ])
        print(newToggle)
        return newToggle

    clickedButton_index = int(clickedButton_id.split('-')[2])
    print(clickedButton_index)
    
    if clickedButton_index >= 0  and  args[clickedButton_index] :
        newToggle[clickedButton_index] = not args[menuLinksCount + 1 + clickedButton_index ]   # add 1 for URL pathname param
        
    
    print(newToggle)
    
    return newToggle





@app.callback(  [  Output(f"{i}-li-container", "className") for i in menuLink   ], 
                [  Input("url", "pathname")   ],
)
def setMenuClassOnLogin(pathname):   
    
    newClasses =  ['m-top_x-small'] * menuLinksCount
    
    if   current_user and current_user is not None   and   not isinstance(current_user, type(None))  and    current_user.is_authenticated  :

        isUserAdmin = False    
        
        userDB = studentGrouped.getUserFromUserId(current_user.id)
        
        if  userDB is not None:        
            if userDB['IsAdmin']:
                isUserAdmin = True
        
        print('setMenuClassOnLogin   isUserAdmin')
        print(isUserAdmin)
        print(newClasses)
        
        for index, menuKey in enumerate(menuLink):
            currentMenu = menuLink.get(menuKey)
            newClasses[index] = "hidden-v "  if    not isUserAdmin   and   currentMenu.get(keyOnlyForAdmin)   else   "m-top_x-small"
            
        print(newClasses)
        
    
    return  newClasses




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
    

@app.callback(
    Output("menu-modal-setting", "is_open"),
    [Input("menu-modal-setting-open", "n_clicks"), Input("menu-modal-setting-close", "n_clicks")],
    [State("menu-modal-setting", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



app.clientside_callback(
        # specifiy the callback with ClientsideFunction(<namespace>, <function name>)
        ClientsideFunction('ui', 'jsFunction'),
        # the Output, Input and State are passed in as with a regular callback
         Output('menu-sub-link-output-hidden', 'children'),
        [Input("menu-sub-link-input", "value")]
    )