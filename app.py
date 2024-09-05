from dash import Dash, html, dcc 
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from sqlalchemy import create_engine
from credentials import sql_engine_string_generator
import os
from dotenv import load_dotenv 

# initialize the dash app as 'app'
app = Dash(__name__,external_stylesheets=[dbc.themes.SLATE])

# conect to swapit and dcp databases
sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_SWAPIT_DBNAME','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD')
swapit_sql_engine=create_engine(sql_engine_string)

sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_DCP_DBNAME','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD')
dcp_sql_engine=create_engine(sql_engine_string)


# set up the app layout
## MOBILE
app.layout = html.Div(
    children=[
        
        #title + instructions
        html.H1('SWAPIT CRUISER Field Log'),
        html.Div([
            html.Span('Required fields indicated by '),
            html.Span('*',style={"color": "red","font-weight": "bold"})
        ]),
        html.Br(),
        
        # Name
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2([
                    "Name",
                    html.Span('*',style={"color": "red","font-weight": "bold"})
                ])),
                dbc.Input(placeholder="...", type="text"),
                html.Br()],
                width = 6
            )],
            justify = "center"
        ),
        
        # Site
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2([
                    "Site",
                    html.Span('*',style={"color": "red","font-weight": "bold"})
                ])),
                dbc.Input(placeholder="...", type="text"),
                html.Br()],
                width = 6
            )],
            justify = "center"
        ),
        
        # Instrument
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2([
                    "Instrument",
                    html.Span('*',style={"color": "red","font-weight": "bold"})
                ])),
                dbc.Input(placeholder="...", type="text"),
                html.Br()],
                width = 6
            )],
            justify = "center"
        ),
        
        # Flag Category
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2("Flag Category")),
                dbc.Input(placeholder="...", type="text"),
                html.Br()],
                width = 6
            )],
            justify = "center"
        ),
        
        # Flag
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2("Flag")),
                dbc.Input(placeholder="...", type="text"),
                html.Br()],
                width = 6
            )],
            justify = "center"
        ),
        
        # Note
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2("Note")),
                dbc.Input(placeholder="...", type="text"),
                html.Br()],
                width = 6
            )],
            justify = "center"
        ),
        
        # Date and time
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2([
                    "Datetime",
                    html.Span('*',style={"color": "red","font-weight": "bold"})
                ])),
                dbc.Input(placeholder="...", type="datetime-local",step="1")],
                width = 8
            )],
            justify = "center"
        ),
        
        dbc.Row([
            dbc.Col([
                dbc.Input(placeholder="Timezone", type="text"),
                
                html.Br()],
                width = 4
            )],
            justify = "center"
        )
        
    
    ],
    style={'textAlign': 'center'}
)



@app.callback(
    Output('', ''))

def update_output(start_date, end_date):
    pass
 
server = app.server 
#if __name__=='__main__':
#    app.run_server(debug=True, use_reloader=False,port=8080)