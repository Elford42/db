from dash import Dash, html, dcc 
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from credentials import sql_engine_string_generator
import os
from dotenv import load_dotenv 
from copy import copy


# initialize the dash app as 'app'
app = Dash(__name__,
           external_stylesheets=[dbc.themes.SLATE],
           requests_pathname_prefix="/app/QPW/",
           routes_pathname_prefix="/app/QPW/")

# conect to swapit and dcp databases
sql_engine_string,user=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_SWAPIT_DBNAME','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD')
swapit_sql_engine=create_engine(sql_engine_string)

sql_engine_string,user=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_DCP_DBNAME','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD')
dcp_sql_engine=create_engine(sql_engine_string)


# pull required data from tables
users = pd.read_sql_table("users", dcp_sql_engine)
sites = pd.read_sql_query(
    "select * from stations", 
    dcp_sql_engine)
instruments = pd.read_sql_query(
    "select * from instrument_history where active = 'True'", 
    dcp_sql_engine)
projects = np.sort(instruments['projectid'].dropna().unique())
flag_table = pd.read_sql_query(
    "select * from flags", 
    dcp_sql_engine)


# set up the app layout
## MOBILE
app.layout = html.Div(
    children=[
        
        #title + instructions
        html.H1('QP Field Log'),
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
                dcc.Dropdown(
                    sorted(users['fullname'].values, key=lambda x: x.split(" ")[-1]),
                    id = "name",
                    placeholder="..."
                ),
                html.Br()],
                width = 8
            )],
            id = "name_row",
            justify = "center"
        ),
        
        # Project
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2([
                    "Project",
                    html.Span('*',style={"color": "red","font-weight": "bold"})
                ])),
                dcc.Dropdown(
                    projects.tolist(),
                    id = "project",
                    placeholder="..."
                ),
                html.Br()],
                width = 8
            )],
            id = "project_row",
            justify = "center"
        ),
        
        # Site
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2([
                    "Site",
                    html.Span('*',style={"color": "red","font-weight": "bold"})
                ])),
                dcc.Dropdown(
                    id = "site",
                    placeholder="...",
                    optionHeight=50
                ),
                html.Br()],
                width = 8
            )],
            id = "site_row",
            justify = "center",
            style={'display':'none'}
        ),
        
        # Instrument
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2([
                    "Instrument",
                    html.Span('*',style={"color": "red","font-weight": "bold"})
                ])),
                dcc.Dropdown(
                    id = "instrument",
                    placeholder="...",
                    optionHeight=50
                ),
                html.Br()],
                width = 8
            )],
            id = "instrument_row",
            justify = "center",
            style={'display':'none'}
        ),
        
        # Flag Category
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2("Flag Category")),
                dcc.Dropdown(
                    options=list(set(flag_table['category'].tolist())),
                    id = "flag_cat",
                    placeholder="...",
                    optionHeight=50
                ),
                html.Br()],
                width = 8
            )],
            id = "flagcat_row",
            justify = "center",
            style={'display':'none'}
        ),
        
        # Flag
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2("Flag")),
                dcc.Dropdown(
                    id = "flag",
                    placeholder="...",
                    optionHeight=50
                ),
                html.Br()],
                width = 8
            )],
            id = "flag_row",
            justify = "center",
            style={'display':'none'}
        ),
        
        # Note
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2("Note")),
                dbc.Input(placeholder="...", type="text"),
                html.Br()],
                width = 8
            )],
            id = "note_row",
            justify = "center",
            style={'display':'none'}
        ),
        
        # Date and time
        dbc.Row([
            dbc.Col(
                [dbc.Label(html.H2([
                    "Datetime",
                    html.Span('*',style={"color": "red","font-weight": "bold"})
                ])),
                dbc.Input(
                    placeholder="...",
                    id = "datetime",
                    type="datetime-local",
                    step="1"
                )],
                width = 8
            )],
            id = "date_row",
            justify = "center",
            style={'display':'none'}
        ),
        
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    options = ["UTC","EST","EDT"],
                    id = "timezone",
                    placeholder="Timezone",
                    optionHeight=50
                ),
                html.Br()],
                width = 4
            )],
            id = "tz_row",
            justify = "center",
            style={'display':'none'}
        ),
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    "Submit",
                    id = "submit_button",
                    color="info", 
                    disabled=True),
                html.Br()],
                width = 4
            )],
            id = "buttons_row",
            justify = "center",
            className="d-grid gap-2"
        ),
        dbc.Tooltip(
            "Required input missing",
            id="submit_tooltip",
            target="buttons_row",
            placement="bottom"
        )
    
    ],
    style={'textAlign': 'center'}
)


# Select project callback
@app.callback(
    Output('site_row', 'style'),
    Output('site','options'),
    Input('project','value'))
def project_update(project):
    
    # sites for selected project
    sites_filtered = np.sort(sites.loc[sites["projectid"]==project]['short_description']).tolist()
    
    # show row and update
    if project == "" or project is None:
        return [{'display':'none'},sites_filtered]
    else:
        return [{'display':'flex'},sites_filtered]


# Site selection callback
@app.callback(
    Output('instrument_row', 'style'),
    Output('flagcat_row', 'style'),
    Output('flag_row', 'style'),
    Output('note_row', 'style'),
    Output('date_row', 'style'),
    Output('tz_row', 'style'),
    Output('instrument','options'),
    Input('site','value'),
    State('project','value'))
def site_update(site,project):
    
    # show all remaining rows
    if site == "" or site is None:
        d = {'display':'none'}
        return_list = [d]*6
        return_list.append([''])
    else:
        d ={'display':'flex'}
        return_list = [d]*6
        
        # instruments for selected site
        siteid = sites[(sites['short_description']==site) &
                               (sites['projectid']==project)]['siteid'].tolist()[0]
        
        instruments_filtered = np.sort(instruments.loc[
                (instruments["projectid"]==project) &
                (instruments["currentlocation"] == siteid)]['instrumentnamelabel']).tolist()
        
        return_list.append(instruments_filtered)
        
    return return_list
        

# Flag category selection callback
@app.callback(
    Output('flag','options'),
    Input('flag_cat','value'))
def flag_update(flag_cat):
    
    # flags for selected category
    if flag_cat == "" or flag_cat is None:
        flags = [""]
    else:
        flags = np.sort(flag_table.loc[flag_table["category"]==flag_cat]['description']).tolist()
    return flags

# Activate submit button callback
@app.callback(
    Output('submit_button','disabled'),
    Output('submit_tooltip','children'),
    Input('name','value'),
    Input('project','value'),
    Input('site','value'),
    Input('instrument','value'),
    Input('datetime','value'),
    Input('timezone','value'))
    
def button_update(name,project,site,instrument,datetime,timezone):
    
    if any([name is None, 
            project is None,
            site is None,
            instrument is None,
            datetime is None,
            timezone is None]):
        return [True,"Required input missing"]
    else:
        return [False,"Ready to submit"]


server = app.server 
# if __name__=='__main__':
#     app.run_server(debug=True, use_reloader=False,port=8080)