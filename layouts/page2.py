from dash import html, dcc, Input, Output
from components.radar_chart_district_comparison import generate_radar_chart
from components.bar_chart_district import generate_bar_chart_district
import data_store
import plotly.graph_objects as go

# Noms des variables (colonnes)
features = [
    "densite_piste_km_par_km2",
    "densite_piste_protegee_km_par_km2",
    "densite_station_par_km2",
    "nb_passages",
    "volume_par_km"
]

labels_pretties = [
    "Densité de pistes (km/km²)",
    "Densité pistes protégées (km/km²)",
    "Densité stations Bixi (/km²)",
    "Nombre de passages",
    "Nombre de passages par km de pistes (/km)"
]

def layout():
    return html.Div([
        html.H2("Comparaison des arrondissements de Montréal",
                className="section-title"),
        
        # Premier menu : choix de l'arrondissement
        dcc.Dropdown(
            options=[{"label": arr, "value": arr}
                     for arr in data_store.df_page2_data["arrondissement"]],
            value=data_store.df_page2_data["arrondissement"].iloc[0],
            id="quartier-dropdown",
            placeholder="Sélectionner un arrondissement"
        ),

        # Chargement radar chart
        dcc.Loading(
            id="loading-viz-display",
            type="circle",
            color="#b71c1c",
            children=[
                html.Br(),
                dcc.Graph(id='radar-chart')
            ]
        ),

        # Deuxième menu : choix de la feature (sous le radar chart)
        html.Br(),
        dcc.Dropdown(
            options=[{"label": label, "value": var}
                     for var, label in zip(features, labels_pretties)],
            id="feature-dropdown",
            placeholder="Sélectionner une variable pour un bar chart (optionnel)"
        ),

        html.Br(),
        dcc.Graph(id='bar-chart')
        
    ], className='page-content')



def register_callbacks(app):
    @app.callback(
        Output("radar-chart", "figure"),
        Output("bar-chart", "figure"),
        Input("quartier-dropdown", "value"),
        Input("feature-dropdown", "value")
    )
    def update_charts(quartier_nom, feature):
        radar_fig = generate_radar_chart(data_store.df_page2_data, quartier_nom)

        if feature:
            bar_fig = generate_bar_chart_district(feature, data_store.df_page2_data, quartier_highlight=quartier_nom)
        else:
            bar_fig = go.Figure(layout={
                "template": "plotly_white",
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "annotations": [{
                    "text": "Sélectionnez une variable pour afficher un bar chart",
                    "xref": "paper", "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 16, "color": "gray"},
                    "x": 0.5, "y": 0.5, "xanchor": "center", "yanchor": "middle"
                }],
                "height": 300,
                "margin": dict(t=20, b=20, l=20, r=20)
            })

        return radar_fig, bar_fig
