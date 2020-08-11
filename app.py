# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 19:06:08 2020

@author: tilan
"""

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from dash.dependencies import Input, Output, State


import numpy as np
import pandas as pd


FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
MATERIAL_CSS = "https://fonts.googleapis.com/icon?family=Material+Icons"

external_stylesheets = [
                        dbc.themes.BOOTSTRAP,
                        dbc.themes.MATERIA,
                        FA,
#                        MATERIAL_CSS
                        ]



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True



#app.scripts.append_script({"external_url": ['https://code.jquery.com/jquery-3.2.1.min.js']})
#app.layout += gdc.Import(src="https://code.jquery.com/jquery-3.3.1.min.js")