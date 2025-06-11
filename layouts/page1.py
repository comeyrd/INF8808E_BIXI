from dash import html, dcc, Input, Output
from components.montreal_interactive_map import generate_montreal_interactive_map
from components.line_chart_traffic_evolution import generate_line_chart_traffic
from components.bar_chart_nearby_stations import generate_bar_chart_nearby_stations
from components.daily_heatmap_station import generate_daily_heatmap_station
def layout(data):
    return html.Div([
        html.Div([
            dcc.Graph(
                id='montreal-map',
                figure=generate_montreal_interactive_map(data),
                style={'height': '80vh'}  # hauteur pour que la carte s’affiche
            )
        ], style={'flex': '1'}),

        html.Div([
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
            dcc.Graph(id='right-side-viz', style={'height': '75vh', 'marginTop': '20px'})
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
