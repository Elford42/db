from dash import Dash, html, dcc 
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# import pandas as pd
# import numpy as np
from sqlalchemy import create_engine,text
from sqlalchemy.exc import OperationalError
# from credentials import sql_engine_string_generator
from flask import request
from datetime import datetime
# from azure.identity import DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient
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

#logging.getLogger("azure").setLevel(logging.ERROR)
logging.getLogger("azure").setLevel(logging.DEBUG)

#initialize the dash app as 'app'
app = Dash(__name__,
            external_stylesheets=[dbc.themes.SLATE],
            requests_pathname_prefix="/app/AQPDDEV/",
            routes_pathname_prefix="/app/AQPDDEV/")
# app = Dash(__name__,
#             external_stylesheets=[dbc.themes.SLATE])

# Global variable to store headers
request_headers = {}

print ( 'python print: DATAHUB_PSQL_SERVER' )

# # Get connection string
# sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_SWAPIT_DBNAME','DATAHUB_PSQL_EDITUSER','DATAHUB_PSQL_EDITPASSWORD')
# swapit_sql_engine=create_engine(sql_engine_string)

#sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','dcp','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD')
# dcp_sql_engine=create_engine(sql_engine_string)

MSG = " PYTHON START :: "

try:
    DB_HOST = os.getenv('DATAHUB_PSQL_SERVER')
    DB_USER = os.getenv('DATAHUB_PSQL_USER')
    DB_PASS = os.getenv('DATAHUB_PSQL_PASSWORD')

    print(DB_HOST)
    print ('\n')

    MSG += "DB_HOST: "
    MSG += DB_HOST
    MSG += " :: "

except Exception as e:
    # declare FSDH keys exception
    error_occur = True
    print(f"An error occurred: {e}")
    MSG += f" :: An error occurred: {e}"

print ( 'python print: after credentials' )

db_url = "postgresql://dcpweb:clean@fsdh-aqpd-psql-prd.postgres.database.azure.com:5432/borden?sslmode=require"

db_url = "postgresql://" + DB_USER + ":" + DB_PASS + "@" + DB_HOST + ":5432/borden?sslmode=require"
MSG += f" :: connecting to db: " + db_url
 
# Create engine
engine = create_engine(db_url, pool_pre_ping=True)  # pool_pre_ping helps detect dead connections
  
try:
    with engine.connect() as connection:
        print("Connection successful!")
except OperationalError as e:
    print(f"Connection failed: {e}")
    MSG += f" :: An error occurred: {e}"

app.layout = [ html.Div(children= MSG ) ]

print ( 'python print: after app layout' )

server = app.server 

print ( 'python print: after app loaded' )
