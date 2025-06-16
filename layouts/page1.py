from dash import html, dcc, Input, Output, State
import components.montreal_interactive_map as mip
from components.line_chart_traffic_evolution import generate_line_chart_traffic
from components.bar_chart_nearby_stations import generate_bar_chart_nearby_stations
from components.bar_chart_daily_traffic import generate_bar_chart_daily_traffic
import pandas as pd
import data_store
DEFAULT_STATION_ID = "1"
DEFAULT_STATION_NAME = "10e avenue / Masson"

def layout():
    fig = mip.generate_montreal_interactive_map(data_store.page1_map_df)
    return html.Div([


        html.Div([
            dcc.Graph(
                id='montreal-map',
                figure=fig,
                style={'height': '80vh'}
            )
        ], style={'flex': '1'}),

        html.Div([
            html.Div(
                id='selected-station-output',
                style={'padding': '1rem', 'fontSize': '18px'}
            ),
            dcc.Dropdown(
                id='viz-selector',
                options=[
                    {'label': "Évolution du trafic (1.1)", 'value': 'line'},
                    {'label': "Stations proches (1.2)", 'value': 'bar'},
                    {'label': "Fréquentation journalière (1.3)", 'value': 'heatmap'}
                ],
                value='line',
                clearable=False
            ),
            dcc.Graph(
                id='right-side-viz',
                style={'height': '75vh', 'marginTop': '20px'}
            )
        ], style={'flex': '1', 'marginLeft': '20px'})
    ], style={'display': 'flex', 'height': '85vh', 'padding': '10px'})


def register_callbacks(app):
    @app.callback(
        Output('selected-station-output', 'children'),
        Input('montreal-map', 'clickData')
    )
    def handle_station_click(clickData):
        if clickData:
            point = clickData['points'][0]
            name = point['hovertext']
            station_id = point['customdata']
            return f"📍 Station sélectionnée : {name} (ID: {station_id})"
        return "🧭 Cliquez sur un point pour voir les données d’une station."

    @app.callback(
        Output('right-side-viz', 'figure'),
        Input('viz-selector', 'value'),
        Input('montreal-map', 'clickData'),
    )
    def update_right_plot(viz_type, clickData):
        station_id = DEFAULT_STATION_ID
        name = DEFAULT_STATION_NAME

        if clickData:
            station_id = clickData['points'][0]['customdata']
            name = clickData['points'][0]['hovertext']

        if viz_type == 'bar':
            return generate_bar_chart_nearby_stations(station_id)
        elif viz_type == 'heatmap':
            day_df = data_store.page1_day_df
            return generate_bar_chart_daily_traffic(station_id, day_df, name)
        else:  # 'line'
            line_df = data_store.page1_line_df
            return generate_line_chart_traffic(station_id, line_df, name)

    @app.callback(
        Output('montreal-map', 'figure'),
        Input('montreal-map', 'clickData'),
        State('montreal-map', 'relayoutData')
    )
    def update_map_on_click(clickData, relayoutData):
        selected_station_id = DEFAULT_STATION_ID
        center = None
        zoom = None
        df = data_store.page1_map_df

        if clickData:
            selected_station_id = clickData['points'][0]['customdata']
        if relayoutData:
            if 'mapbox.center' in relayoutData:
                center = relayoutData['mapbox.center']
            if 'mapbox.zoom' in relayoutData:
                zoom = relayoutData['mapbox.zoom']

        return mip.generate_montreal_interactive_map(df, selected_station_id, center, zoom)
