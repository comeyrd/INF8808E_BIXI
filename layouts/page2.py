from dash import html, dcc, Input, Output
from components.radar_chart_district_comparison import generate_radar_chart
import data_store


def layout():
    return html.Div([
        html.H2("Comparaison des arrondissements de Montréal",
                className="section-title"),
        dcc.Dropdown(
            options=[{"label": arr, "value": arr}
                     for arr in data_store.df_page2_data["arrondissement"]],
            value=data_store.df_page2_data["arrondissement"].iloc[0],
            id="quartier-dropdown"
        ),
        dcc.Loading(
            id="loading-viz-display",
            type="circle",
            color="#b71c1c",
            children=[
                dcc.Graph(id='radar-chart')
            ]
        ),
    ], className='page-content')


def register_callbacks(app):
    @app.callback(
        Output("radar-chart", "figure"),
        Input("quartier-dropdown", "value")
    )
    def update_radar(quartier_nom):
        return generate_radar_chart(data_store.df_page2_data, quartier_nom)
