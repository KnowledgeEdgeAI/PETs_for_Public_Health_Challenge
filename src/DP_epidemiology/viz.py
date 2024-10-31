import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime
import plotly.express as px
import pandas as pd
import numpy as np
import sys
import os
import random
from datetime import datetime
import opendp.prelude as dp

dp.enable_features("contrib", "floating-point", "honest-but-curious")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DP_epidemiology.utilities import *

from DP_epidemiology.hotspot_analyzer import hotspot_analyzer 
from DP_epidemiology.mobility_analyzer import mobility_analyzer
from DP_epidemiology.pandemic_adherence_analyzer import pandemic_adherence_analyzer
from DP_epidemiology.contact_matrix import get_age_group_count_map, get_contact_matrix, get_pearson_similarity


def create_hotspot_dash_app(df:pd.DataFrame):
    cities = {
    "Medellin": (6.2476, -75.5658),
    "Bogota": (4.7110, -74.0721),
    "Brasilia": (-15.7975, -47.8919),
    "Santiago": (-33.4489, -70.6693)
    }
    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.DatePickerSingle(
            id='start-date-picker',
            date='2019-01-01'
        ),
        dcc.DatePickerSingle(
            id='end-date-picker',
            date='2019-12-31'
        ),
        dcc.Slider(
            id='epsilon-slider',
            min=0,
            max=10,
            step=0.1,
            value=1,
            marks={i: str(i) for i in range(11)}
        ),
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': city, 'value': city} for city in cities.keys()],
            value='Medellin'
        ),
        dcc.Graph(id='geo-plot')
    ])

    @app.callback(
        Output('geo-plot', 'figure'),
        [Input('start-date-picker', 'date'),
         Input('end-date-picker', 'date'),
         Input('epsilon-slider', 'value'),
         Input('city-dropdown', 'value')]
    )
    def update_graph(start_date, end_date, epsilon, city):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Filter data using hotspot_analyser
        output = hotspot_analyzer(df, start_date, end_date, city, epsilon)
        filtered_df = get_coordinates(output)

        # Plot using Plotly Express
        fig = px.scatter_geo(
            filtered_df,
            lat='Latitude',
            lon='Longitude',
            color='nb_transactions',
            size='nb_transactions',
            hover_name='merch_postal_code',
            hover_data={'merch_postal_code': True, 'nb_transactions': True, 'Latitude': False, 'Longitude': False},
            projection='mercator',
            title=f"Transaction Locations in {city} from {start_date.date()} to {end_date.date()} with epsilon={epsilon}",
            color_continuous_scale=px.colors.sequential.Plasma
        )

        # Center the map around the selected city
        fig.update_geos(
            center=dict(lat=cities[city][0], lon=cities[city][1]),
            projection_scale=2.5  # Zoom level
        )

        return fig

    return app

def create_mobility_dash_app(df:pd.DataFrame):
    cities = {
        "Medellin": (6.2476, -75.5658),
        "Bogota": (4.7110, -74.0721),
        "Brasilia": (-15.7975, -47.8919),
        "Santiago": (-33.4489, -70.6693)
        }
    app = dash.Dash(__name__)

    app.layout = html.Div([
            dcc.DatePickerSingle(
                id='start-date-picker',
                date='2019-01-01'
            ),
            dcc.DatePickerSingle(
                id='end-date-picker',
                date='2019-12-31'
            ),
            dcc.Slider(
                id='epsilon-slider',
                min=0,
                max=10,
                step=0.1,
                value=1,
                marks={i: str(i) for i in range(11)}
            ),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': city, 'value': city} for city in cities.keys()],
                value='Medellin'
            ),
            dcc.Graph(id='mobility-graph')
        ])

    # Callback to update the graph based on input values
    @app.callback(
        Output('mobility-graph', 'figure'),
        [Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('city-dropdown', 'value'),
        Input('epsilon-slider', 'value')]
    )
    def update_graph(start_date, end_date, city_filter, epsilon):
        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Call the mobility_analyser function
        filtered_df = mobility_analyzer(df, start_date, end_date, city_filter, epsilon)

        # Plot using Plotly Express
        fig = px.line(
            filtered_df,
            x='date',
            y='nb_transactions',
            title=f"Mobility Analysis for {city_filter} from {start_date.date()} to {end_date.date()} with epsilon={epsilon}",
            labels={'nb_transactions': 'Number of Transactions', 'date': 'Date'}
        )

        return fig
    return app

def create_pandemic_adherence_dash_app(df:pd.DataFrame):
    cities = {
        "Medellin": (6.2476, -75.5658),
        "Bogota": (4.7110, -74.0721),
        "Brasilia": (-15.7975, -47.8919),
        "Santiago": (-33.4489, -70.6693)
        }
    entry_types=["luxury","essential","other"]
    app = dash.Dash(__name__)

    app.layout = html.Div([
            dcc.DatePickerSingle(
                id='start-date-picker',
                date='2019-01-01'
            ),
            dcc.DatePickerSingle(
                id='end-date-picker',
                date='2019-12-31'
            ),
            dcc.Slider(
                id='epsilon-slider',
                min=0,
                max=10,
                step=0.1,
                value=1,
                marks={i: str(i) for i in range(11)}
            ),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': city, 'value': city} for city in cities.keys()],
                value='Medellin'
            ),
            dcc.Dropdown(
                id='entry-type-dropdown',
                options=[{'label': entry_type, 'value': entry_type} for entry_type in entry_types],
                value='luxury'
            ),
            dcc.Graph(id='pandemic-stage-graph')
        ])

    # Callback to update the graph based on input values
    @app.callback(
        Output('pandemic-stage-graph', 'figure'),
        [Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('city-dropdown', 'value'),
        Input('entry-type-dropdown', 'value'),
        Input('epsilon-slider', 'value')]
    )
    def update_graph(start_date, end_date, city_filter,essential_or_luxury, epsilon):
        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Call the mobility_analyser function
        filtered_df = pandemic_adherence_analyzer(df, start_date, end_date, city_filter,essential_or_luxury, epsilon)

        # Plot using Plotly Express
        fig = px.line(
            filtered_df,
            x='date',
            y='nb_transactions',
            title=f"Pandemic Stage Analysis for {city_filter} from {start_date.date()} to {end_date.date()} with epsilon={epsilon}",
            labels={'nb_transactions': 'Number of Transactions', 'date': 'Date'}
        )

        return fig
    return app

def create_contact_matrix_dash_app(df:pd.DataFrame):
    cities = {
        "Medellin": (6.2476, -75.5658),
        "Bogota": (4.7110, -74.0721),
        "Brasilia": (-15.7975, -47.8919),
        "Santiago": (-33.4489, -70.6693)
    }
    # Initialize the Dash app
    app = dash.Dash(__name__)

    app.layout = html.Div([
            dcc.DatePickerSingle(
                id='start-date-picker',
                date='2019-01-01'
            ),
            dcc.DatePickerSingle(
                id='end-date-picker',
                date='2019-12-31'
            ),
            dcc.Slider(
                id='epsilon-slider',
                min=0,
                max=10,
                step=0.1,
                value=1,
                marks={i: str(i) for i in range(11)}
            ),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': city, 'value': city} for city in cities.keys()],
                value='Medellin'
            ),
            dcc.Graph(id='matrix-heatmap'),

        # Output table to display contact matrix values
        html.Div(id='matrix-output', style={'whiteSpace': 'pre-line'})
    ])

    # Callback to update the graph and output based on inputs
    @app.callback(
        [Output('matrix-heatmap', 'figure'),
        Output('matrix-output', 'children')],
        [Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'),
        Input('city-dropdown', 'value'),
        Input('epsilon-slider', 'value')]
    )
    def update_contact_matrix(start_date, end_date, city, epsilon):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Get age group count map
        age_group_count_map = get_age_group_count_map(df, start_date, end_date, city, epsilon)
        age_group_sample_size = list(age_group_count_map.values())
        
        # Hardcoded population distribution for the example
        age_group_population_distribution = [8231200, 7334319, 6100177]

        # Generate contact matrix
        contact_matrix = get_contact_matrix(age_group_sample_size, age_group_population_distribution)

        # Generate a heatmap for the contact matrix
        fig = px.imshow(contact_matrix,
                        labels=dict(x="Age Group", y="Age Group", color="Contact Rate"),
                        x=['20-30', '30-40', '50-60'],
                        y=['20-30', '30-40', '50-60'],
                        title=f"contact matrix for {city} from {start_date.date()} to {end_date.date()} with epsilon={epsilon} and pearson similarity={get_pearson_similarity(contact_matrix)}",
                        zmin=2.5, zmax=3.5,
                        color_continuous_scale='Blues')

        # Convert the matrix to a readable format
        matrix_output = f"Contact Matrix:\n{np.array_str(contact_matrix, precision=2, suppress_small=True)}"
        
        return fig, matrix_output
    
    return app