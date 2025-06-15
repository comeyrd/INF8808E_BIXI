from dash import html, dcc, Input, Output
from components.radar_chart_district_comparison import generate_radar_chart

def layout(data):
    return html.Div([
        html.H2("Comparaison des Arrondissements de Montréal", className="section-title"),
        dcc.Dropdown(
            options=[{"label": arr, "value": arr} for arr in data["arrondissement"]],
            value=data["arrondissement"].iloc[0],
            id="quartier-dropdown"
        ),
        dcc.Graph(id='radar-chart')
    ], className='page-content')

def register_callbacks(app, data):
    @app.callback(
        Output("radar-chart", "figure"),
        Input("quartier-dropdown", "value")
    )
    def update_radar(quartier_nom):
        return generate_radar_chart(data, quartier_nom)
