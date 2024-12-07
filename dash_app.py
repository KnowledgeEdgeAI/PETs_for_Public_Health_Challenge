import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime
import pandas as pd
import numpy as np
import sys
import os
import random
from src.DP_epidemiology.utilities import *
from src.DP_epidemiology.hotspot_analyzer import hotspot_analyzer 
from src.DP_epidemiology.mobility_analyzer import mobility_analyzer
from src.DP_epidemiology.pandemic_adherence_analyzer import pandemic_adherence_analyzer
from src.DP_epidemiology.contact_matrix import get_age_group_count_map, get_contact_matrix_country

import plotly.express as px
import plotly.graph_objects as go
import opendp.prelude as dp

dp.enable_features("contrib", "floating-point", "honest-but-curious")


def create_dash_app(df: pd.DataFrame, df_google_mobility_data: pd.DataFrame = None):
    cities = {
        "Medellin": (6.2476, -75.5658),
        "Bogota": (4.7110, -74.0721),
        "Brasilia": (-15.7975, -47.8919),
        "Santiago": (-33.4489, -70.6693)
    }
    category_list = ['grocery_and_pharmacy', 'transit_stations', 'retail_and_recreation', "other"]
    entry_types = ["luxury", "essential", "other"]
    age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75+']
    scaling_factor = pd.read_csv('fractions_offline.csv')['0'].values
    P = np.array([4136344, 4100716, 3991988, 3934088, 4090149, 4141051, 3895117, 3439202,
                  3075077, 3025100, 3031855, 2683253, 2187561, 1612948, 1088448, 1394217])
    consumption_distribution_raw = pd.read_csv(r"consumption_distribution.csv")
    categories = consumption_distribution_raw['categories'].values
    consumption_distribution = {}
    for category in categories:
        consumption_distribution[category] = consumption_distribution_raw[consumption_distribution_raw['categories'] == category].values[0][:-1]

    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Tabs([
            dcc.Tab(label='Hotspot Analysis', children=[
                dcc.DatePickerSingle(id='hotspot-start-date-picker', date='2019-01-01'),
                dcc.DatePickerSingle(id='hotspot-end-date-picker', date='2019-12-31'),
                dcc.Slider(id='hotspot-epsilon-slider', min=0, max=10, step=0.1, value=1, marks={i: str(i) for i in range(11)}),
                dcc.Dropdown(id='hotspot-city-dropdown', options=[{'label': city, 'value': city} for city in cities.keys()], value='Medellin'),
                dcc.Graph(id='hotspot-geo-plot')
            ]),
            dcc.Tab(label='Mobility Analysis', children=[
                dcc.DatePickerSingle(id='mobility-start-date-picker', date='2019-01-01'),
                dcc.DatePickerSingle(id='mobility-end-date-picker', date='2019-12-31'),
                dcc.Slider(id='mobility-epsilon-slider', min=0, max=10, step=0.1, value=1, marks={i: str(i) for i in range(11)}),
                dcc.Dropdown(id='mobility-city-dropdown', options=[{'label': city, 'value': city} for city in cities.keys()], value='Medellin'),
                dcc.Dropdown(id='mobility-category-list-dropdown', options=[{'label': category, 'value': category} for category in category_list], value='transit_stations'),
                dcc.Graph(id='mobility-graph')
            ]),
            dcc.Tab(label='Pandemic Adherence Analysis', children=[
                dcc.DatePickerSingle(id='adherence-start-date-picker', date='2019-01-01'),
                dcc.DatePickerSingle(id='adherence-end-date-picker', date='2019-12-31'),
                dcc.Slider(id='adherence-epsilon-slider', min=0, max=10, step=0.1, value=1, marks={i: str(i) for i in range(11)}),
                dcc.Dropdown(id='adherence-city-dropdown', options=[{'label': city, 'value': city} for city in cities.keys()], value='Medellin'),
                dcc.Dropdown(id='adherence-entry-type-dropdown', options=[{'label': entry_type, 'value': entry_type} for entry_type in entry_types], value='luxury'),
                dcc.Graph(id='adherence-graph')
            ]),
            dcc.Tab(label='Contact Matrix Analysis', children=[
                dcc.DatePickerSingle(id='matrix-start-date-picker', date='2019-01-01'),
                dcc.DatePickerSingle(id='matrix-end-date-picker', date='2019-12-31'),
                dcc.Slider(id='matrix-epsilon-slider', min=0, max=10, step=0.1, value=1, marks={i: str(i) for i in range(11)}),
                dcc.Dropdown(id='matrix-city-dropdown', options=[{'label': city, 'value': city} for city in cities.keys()], value='Medellin'),
                dcc.Graph(id='matrix-heatmap'),
                html.Div(id='matrix-output', style={'whiteSpace': 'pre-line'})
            ]),
            dcc.Tab(label='Mobility Validation', children=[
                dcc.DatePickerSingle(id='validation-start-date-picker', date='2020-02-15'),
                dcc.DatePickerSingle(id='validation-end-date-picker', date='2020-12-31'),
                dcc.Slider(id='validation-epsilon-slider', min=0, max=10, step=0.1, value=1, marks={i: str(i) for i in range(11)}),
                dcc.Dropdown(id='validation-city-dropdown', options=[{'label': city, 'value': city} for city in cities.keys()], value='Medellin'),
                dcc.Dropdown(id='validation-category-list-dropdown', options=[{'label': category, 'value': category} for category in category_list], value='transit_stations'),
                dcc.Graph(id='validation-mobility-graph')
            ])
        ])
    ])

    @app.callback(
        Output('hotspot-geo-plot', 'figure'),
        [Input('hotspot-start-date-picker', 'date'),
         Input('hotspot-end-date-picker', 'date'),
         Input('hotspot-epsilon-slider', 'value'),
         Input('hotspot-city-dropdown', 'value')]
    )
    def update_hotspot_graph(start_date, end_date, epsilon, city):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        output = hotspot_analyzer(df, start_date, end_date, city, epsilon)
        filtered_df = get_coordinates(output)
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
        fig.update_geos(center=dict(lat=cities[city][0], lon=cities[city][1]), projection_scale=2.5)
        return fig

    @app.callback(
        Output('mobility-graph', 'figure'),
        [Input('mobility-start-date-picker', 'date'),
         Input('mobility-end-date-picker', 'date'),
         Input('mobility-city-dropdown', 'value'),
         Input('mobility-category-list-dropdown', 'value'),
         Input('mobility-epsilon-slider', 'value')]
    )
    def update_mobility_graph(start_date, end_date, city_filter, category, epsilon):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_df = mobility_analyzer(df, start_date, end_date, city_filter, category, epsilon)
        fig = px.line(
            filtered_df,
            x='date',
            y='nb_transactions',
            title=f"Mobility Analysis for {city_filter} and category {category} from {start_date.date()} to {end_date.date()} with epsilon={epsilon}",
            labels={'nb_transactions': 'Number of Transactions', 'date': 'Date'}
        )
        if city_filter == "Bogota":
            events = [
                ("Isolation Start Drill", "2020-03-20"),
                ("National Quarantine", "2020-03-26"),
                ("Gender Restriction", "2020-04-16"),
                ("Day Without VAT (IVA)", "2020-06-19"),
                ("Lockdown 1", "2020-07-15"),
                ("Lockdown 2", "2020-07-30"),
                ("Lockdown 3", "2020-08-13"),
                ("Lockdown 4", "2020-08-20"),
                ("End of National Quarantine", "2020-09-04"),
                ("Day Without VAT", "2020-11-19"),
                ("Candle Day", "2020-12-07"),
                ("Start of Novenas", "2020-12-16"),
                ("Lockdown 1 (2021)", "2021-01-05"),
                ("Lockdown 2 (2021)", "2021-01-12"),
                ("Lockdown 3 (2021)", "2021-01-18"),
                ("Lockdown 4 (2021)", "2021-01-28"),
                ("Holy Week", "2021-03-28"),
                ("Model 4x3", "2021-04-06"),
                ("Model 4x3 (Extension)", "2021-04-06"),
                ("Vaccination Stage 1", "2021-02-18"),
                ("Vaccination Stage 2", "2021-03-08"),
                ("Vaccination Stage 3", "2021-05-22"),
                ("Vaccination Stage 4", "2021-06-17"),
                ("Vaccination Stage 5", "2021-07-17"),
                ("Riots and Social Unrest", "2021-05-01")
            ]
            for event, date in events:
                fig.add_shape(type="line", x0=date, y0=0, x1=date, y1=1, xref='x', yref='paper', line=dict(color="Red", width=2, dash="dash"))
                fig.add_annotation(x=date, y=1, xref='x', yref='paper', text=event, showarrow=True, arrowhead=1, ax=-10, ay=-40, font=dict(color="Red"))
        return fig

    @app.callback(
        Output('adherence-graph', 'figure'),
        [Input('adherence-start-date-picker', 'date'),
         Input('adherence-end-date-picker', 'date'),
         Input('adherence-city-dropdown', 'value'),
         Input('adherence-entry-type-dropdown', 'value'),
         Input('adherence-epsilon-slider', 'value')]
    )
    def update_adherence_graph(start_date, end_date, city_filter, essential_or_luxury, epsilon):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_df = pandemic_adherence_analyzer(df, start_date, end_date, city_filter, essential_or_luxury, epsilon)
        fig = px.line(
            filtered_df,
            x='date',
            y='nb_transactions',
            title=f"Pandemic adherence Analysis for {city_filter} from {start_date.date()} to {end_date.date()} with epsilon={epsilon}",
            labels={'nb_transactions': 'Number of Transactions', 'date': 'Date'}
        )
        if city_filter == "Bogota":
            events = [
                ("Isolation Start Drill", "2020-03-20"),
                ("National Quarantine", "2020-03-26"),
                ("Gender Restriction", "2020-04-16"),
                ("Day Without VAT (IVA)", "2020-06-19"),
                ("Lockdown 1", "2020-07-15"),
                ("Lockdown 2", "2020-07-30"),
                ("Lockdown 3", "2020-08-13"),
                ("Lockdown 4", "2020-08-20"),
                ("End of National Quarantine", "2020-09-04"),
                ("Day Without VAT", "2020-11-19"),
                ("Candle Day", "2020-12-07"),
                ("Start of Novenas", "2020-12-16"),
                ("Lockdown 1 (2021)", "2021-01-05"),
                ("Lockdown 2 (2021)", "2021-01-12"),
                ("Lockdown 3 (2021)", "2021-01-18"),
                ("Lockdown 4 (2021)", "2021-01-28"),
                ("Holy Week", "2021-03-28"),
                ("Model 4x3", "2021-04-06"),
                ("Model 4x3 (Extension)", "2021-04-06"),
                ("Vaccination Stage 1", "2021-02-18"),
                ("Vaccination Stage 2", "2021-03-08"),
                ("Vaccination Stage 3", "2021-05-22"),
                ("Vaccination Stage 4", "2021-06-17"),
                ("Vaccination Stage 5", "2021-07-17"),
                ("Riots and Social Unrest", "2021-05-01")
            ]
            for event, date in events:
                fig.add_shape(type="line", x0=date, y0=0, x1=date, y1=1, xref='x', yref='paper', line=dict(color="Red", width=2, dash="dash"))
                fig.add_annotation(x=date, y=1, xref='x', yref='paper', text=event, showarrow=True, arrowhead=1, ax=-10, ay=-40, font=dict(color="Red"))
        return fig

    @app.callback(
        [Output('matrix-heatmap', 'figure'),
         Output('matrix-output', 'children')],
        [Input('matrix-start-date-picker', 'date'),
         Input('matrix-end-date-picker', 'date'),
         Input('matrix-city-dropdown', 'value'),
         Input('matrix-epsilon-slider', 'value')]
    )
    def update_contact_matrix(start_date, end_date, city, epsilon):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        counts_per_city = []
        for city in cities:
            counts = get_age_group_count_map(df, age_groups, consumption_distribution, start_date, end_date, city)
            counts_per_city.append(list(counts.values()))
        contact_matrix = get_contact_matrix_country(counts_per_city, P, scaling_factor)
        fig = px.imshow(contact_matrix, labels=dict(x="Age Group", y="Age Group", color="Contact Rate"), x=age_groups, y=age_groups, color_continuous_scale='viridis')
        matrix_output = f"Contact Matrix:\n{np.array_str(contact_matrix, precision=2, suppress_small=True)}"
        return fig, matrix_output

    @app.callback(
        Output('validation-mobility-graph', 'figure'),
        [Input('validation-start-date-picker', 'date'),
         Input('validation-end-date-picker', 'date'),
         Input('validation-city-dropdown', 'value'),
         Input('validation-category-list-dropdown', 'value'),
         Input('validation-epsilon-slider', 'value')]
    )
    def update_validation_graph(start_date, end_date, city_filter, category, epsilon):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_df_transactional = mobility_analyzer(df, start_date, end_date, city_filter, category, epsilon)
        offset = filtered_df_transactional["date"].iloc[0]
        filtered_df_google = preprocess_google_mobility(df_google_mobility_data, start_date, end_date, city_filter, category, offset)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df_transactional['date'], y=filtered_df_transactional['nb_transactions'], mode='lines', name='Transactional Mobility', yaxis='y1'))
        fig.add_trace(go.Scatter(x=filtered_df_google['date'], y=filtered_df_google[category], mode='lines', name='Google Mobility', yaxis='y2'))
        fig.update_layout(
            title=f"Mobility Analysis for {city_filter} and category {category} from {start_date.date()} to {end_date.date()} with epsilon={epsilon}",
            xaxis_title='Date',
            yaxis=dict(title='Transactional Mobility', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
            yaxis2=dict(title='Google Mobility', titlefont=dict(color='red'), tickfont=dict(color='red'), overlaying='y', side='right'),
            legend_title='Data Source'
        )
        return fig

    return app

# Example usage:
df = pd.read_csv(r'D:\workspace\pet_local\technical_phase_data.csv')
df_google_mobility_data = pd.read_csv('D:\workspace\PETs_challenge_data.csv')
app = create_dash_app(df, df_google_mobility_data)
app.run_server(debug=True)