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
import dash_table
import flask
import math


FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
MATERIAL_CSS = "https://fonts.googleapis.com/icon?family=Material+Icons"
BOOTSTRAP_CSS = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"

external_stylesheets = [
                        dbc.themes.BOOTSTRAP,
                        dbc.themes.MATERIA,
                        FA,
                        MATERIAL_CSS,
                        BOOTSTRAP_CSS
                        ]



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True






#returns top indicator div
def indicator(color, text, id_value):
    return html.Div(
        [
            
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
        
)
        
        
        

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
