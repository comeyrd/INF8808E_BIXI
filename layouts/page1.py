from dash import html, dcc, Input, Output, State
import components.montreal_interactive_map as mip
from components.line_chart_traffic_evolution import generate_line_chart_traffic
from components.bar_chart_nearby_stations import generate_bar_chart_nearby_stations
from components.daily_heatmap_station import generate_daily_heatmap_station
import plotly.graph_objects as go
import pandas as pd

def layout(page1_map_df):
    fig = mip.generate_montreal_interactive_map(page1_map_df)
    return html.Div([
        dcc.Store(id='map-data', data=page1_map_df.to_dict('records')),
        html.Div([
            dcc.Graph(
                id='montreal-map',
                figure=fig,
                style={'height': '80vh'}
            ),
            html.Div(id='selected-station-output',
                     style={'padding': '1rem', 'fontSize': '18px'})
        ], style={'flex': '1'}),

        html.Div([
            dcc.Dropdown(
                id='viz-selector',
                options=[
                    {'label': "Évolution du trafic (1.1)", 'value': 'line'},
                    {'label': "Stations proches (1.2)", 'value': 'bar'},
                    {'label': "Fréquentation journalière (1.3)",
                     'value': 'heatmap'}
                ],
                value='line',
                clearable=False
            ),
            dcc.Graph(id='right-side-viz',
                      style={'height': '75vh', 'marginTop': '20px'})
        ], style={'flex': '1', 'marginLeft': '20px'})
    ], style={'display': 'flex', 'height': '85vh', 'padding': '10px'})


def register_callbacks(app):
    @app.callback(
        Output('right-side-viz', 'figure'),
        Input('viz-selector', 'value')
    )
    def update_right_plot(viz_type):
        if viz_type == 'bar':
            return generate_bar_chart_nearby_stations()
        elif viz_type == 'heatmap':
            return generate_daily_heatmap_station()
        return generate_line_chart_traffic()

    @app.callback(
        Output('selected-station-output', 'children'),
        Input('montreal-map', 'clickData')
    )
    def handle_station_click(clickData):
        if clickData:
            print(clickData)
            point = clickData['points'][0]
            name = point['hovertext']
            station_id = point['customdata'][0]
            return f"📍 Selected Station: {name} (ID: {station_id})"
        return "🧭 Click on a station marker to see details."
