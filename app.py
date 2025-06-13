from dash import Dash, html, dcc 
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from sqlalchemy import create_engine,text
from credentials import sql_engine_string_generator
from flask import request
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv 
import logging

# Version number to display
version = "1.3"

# Setup logger
if not os.path.exists('logs'):
    os.mkdir('logs')
    
logging.basicConfig(
    format = '%(message)s',
    filename='logs/log.log', 
    filemode='w+',
    level = 20)

logging.getLogger("azure").setLevel(logging.ERROR)

#initialize the dash app as 'app'
app = Dash(__name__,
            external_stylesheets=[dbc.themes.SLATE],
            requests_pathname_prefix="/app/AQPDDEV/",
            routes_pathname_prefix="/app/AQPDDEV/")
# app = Dash(__name__,
#             external_stylesheets=[dbc.themes.SLATE])

# Global variable to store headers
request_headers = {}

print ( 'DATAHUB_PSQL_SERVER' )

# # Get connection string
# sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_SWAPIT_DBNAME','DATAHUB_PSQL_EDITUSER','DATAHUB_PSQL_EDITPASSWORD')
# swapit_sql_engine=create_engine(sql_engine_string)

sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','dcp','DATAHUB_PSQL_EDITUSER','DATAHUB_PSQL_EDITPASSWORD')
# dcp_sql_engine=create_engine(sql_engine_string)

print ( sql_engine_string )

app.layout = [html.Div(children='SQL: ' + sql_engine_string)]

server = app.server 
# if __name__=='__main__':
#     app.run_server(debug=True,port=8080)
