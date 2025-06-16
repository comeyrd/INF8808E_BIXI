from dash import html, dcc, Input, Output, State
import components.montreal_interactive_map as mip
from components.line_chart_traffic_evolution import generate_line_chart_traffic
from components.bar_chart_nearby_stations import generate_bar_chart_nearby_stations
from components.bar_chart_daily_traffic import generate_bar_chart_daily_traffic
import pandas as pd

DEFAULT_STATION_ID = "1"
DEFAULT_STATION_NAME = "10e avenue / Masson"

def layout(page1_map_df, page1_line_df, page1_day_df):
    fig = mip.generate_montreal_interactive_map(page1_map_df)
    return html.Div([
        dcc.Store(id='map-data', data=page1_map_df.to_dict('records')),
        dcc.Store(id='line-data', data=page1_line_df.to_dict('records')),
        dcc.Store(id='day-data', data=page1_day_df.to_dict('records')),

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
        State('line-data', 'data'),
        State('day-data', 'data')
    )
    def update_right_plot(viz_type, clickData, linedata, daydata):
        station_id = DEFAULT_STATION_ID
        name = DEFAULT_STATION_NAME

        if clickData:
            station_id = clickData['points'][0]['customdata']
            name = clickData['points'][0]['hovertext']

        if viz_type == 'bar':
            return generate_bar_chart_nearby_stations(station_id)
        elif viz_type == 'heatmap':
            day_df = pd.DataFrame(daydata)
            return generate_bar_chart_daily_traffic(station_id, day_df, name)
        else:  # 'line'
            line_df = pd.DataFrame(linedata)
            return generate_line_chart_traffic(station_id, line_df, name)

    @app.callback(
        Output('montreal-map', 'figure'),
        Input('montreal-map', 'clickData'),
        State('map-data', 'data'),
        State('montreal-map', 'relayoutData')
    )
    def update_map_on_click(clickData, data, relayoutData):
        selected_station_id = DEFAULT_STATION_ID
        center = None
        zoom = None
        df = pd.DataFrame(data)

        if clickData:
            selected_station_id = clickData['points'][0]['customdata']
        if relayoutData:
            if 'mapbox.center' in relayoutData:
                center = relayoutData['mapbox.center']
            if 'mapbox.zoom' in relayoutData:
                zoom = relayoutData['mapbox.zoom']

        return mip.generate_montreal_interactive_map(df, selected_station_id, center, zoom)
