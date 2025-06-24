from dash import Dash, html, dcc , dash_table
# from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
# import numpy as np
from sqlalchemy import create_engine,text
from sqlalchemy.exc import OperationalError
# from credentials import sql_engine_string_generator
from flask import request
# from datetime import datetime
# from azure.identity import DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv 
import logging
import socket

# Local dev boolean
computer = socket.gethostname()
if computer == 'WONTN74906':
    local = True
else:
    local = False

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
# request_headers = {}

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

    MSG += "<BR>DB_HOST: "
    MSG += DB_HOST
    MSG += " :: "

except Exception as e:
    # declare FSDH keys exception
    error_occur = True
    print(f"An error occurred trying to get ENV VARS: {e}")
    MSG += f"<BR> :: An error occurred trying to get ENV VARS: {e}"

print ( 'python print: after credentials' )

## db_url = "postgresql://dcpweb:clean@fsdh-aqpd-psql-prd.postgres.database.azure.com:5432/borden?sslmode=require"

db_url = "postgresql://" + DB_USER + ":" + DB_PASS + "@" + DB_HOST + ":5432/borden?sslmode=require"

MSG += f"<BR> :: connecting to db: " + db_url
 
# Create engine
engine = create_engine(db_url, pool_pre_ping=True)  # pool_pre_ping helps detect dead connections

# sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='data';"
  
def fetch_table_list():
    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='data' ORDER BY table_name;"
    df = pd.read_sql(sql, engine)
    return df

try:
    with engine.connect() as connection:
        print("Connection successful!")
        MSG += "<BR>Connection successful!"
        # result = connection.execute(text( sql ))
        # for row in result:
        #     print(row)

except OperationalError as e:
    print(f"Connection failed: {e}")
    MSG += f"<BR> :: An error occurred: {e}"

# app.layout = [ html.div( children = MSG ) ]

# print ( fetch_table_list() )

#app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in fetch_table_list().columns])
app.layout = html.Div([
    html.H1("SQL Database Test :: " + DB_HOST ),
    dash_table.DataTable(
        id='sql-data-table',
        columns=[{"name": i, "id": i} for i in fetch_table_list().columns],
        data=fetch_table_list().to_dict('records'),
        editable=False,  # Set to True if you want to allow editing in the table
        filter_action="native",
        sort_action="native",
        page_action="native",
        page_size=100,
            style_cell_conditional=[
        {'if': {'column_id': 'table_name'},
         'width': '30%',
         'textAlign': 'left'
         },
        ]
    )
])

print ( 'python print: after app layout' )

# server = app.server 

if not local:
    server = app.server
else:
    if __name__=='__main__':
        app.run(debug=True,port=8080)

print ( 'python print: after app loaded' )
