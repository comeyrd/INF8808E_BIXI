import pandas as pd
import plotly.graph_objects as go

# Noms des variables (colonnes)
features = [
    "densite_piste_km_par_km2",
    "densite_piste_protegee_km_par_km2",
    "densite_station_par_km2",
    "nb_passages",
    "volume_par_km"
]

# Labels plus lisibles pour l'affichage
labels_pretties = [
    "Densité de pistes (km/km²)",
    "Densité pistes protégées (km/km²)",
    "Densité stations Bixi (/km²)",
    "Nombre de passages",
    "Nombre de passages par km de pistes (/km)"
]


def generate_bar_chart_district(feature, data, quartier_highlight=None):
    # Vérification que la feature est valide
    if feature not in features:
        raise ValueError(f"'{feature}' n'est pas une feature valide.")

    # Tri décroissant
    sorted_data = data.sort_values(by=feature, ascending=False)

    # Extraction
    values = sorted_data[feature]
    labels = sorted_data["arrondissement"]

    # Détection de l'arrondissement à mettre en valeur
    colors = ['black' if arr == quartier_highlight else 'indianred' for arr in labels]
    text_style = ['<b>' + f"{v:.2f}" + '</b>' if arr == quartier_highlight else f"{v:.2f}"
                  for arr, v in zip(labels, values)]
    hover_style = ['<b>%{x}</b><br>' if arr == quartier_highlight else '%{x}<br>'
                   for arr in labels]

    # Titre lisible
    index_feature = features.index(feature)
    titre = labels_pretties[index_feature]

    # Bar chart avec couleur personnalisée
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            text=text_style,
            textposition='outside',
            marker_color=colors,
            hovertemplate=[
    f"{hover}{titre} : " + "%{y:.2f}<extra></extra>" for hover in hover_style
]
        )
    ])

    fig.update_layout(
        title=f"{titre} par arrondissement (ordre décroissant)",
        xaxis_title="Arrondissement",
        yaxis_title=titre,
        xaxis_tickangle=-45,
        margin=dict(t=60, b=120, l=60, r=40),
        height=700,
        template='plotly_white'
    )

    return fig
