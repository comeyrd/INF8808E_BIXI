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

def generate_radar_chart(data, quartier_nom):
    # Min/max pour normalisation
    max_values = data[features].max()
    min_values = data[features].min()

    # Données du quartier sélectionné
    quartier = data[data["arrondissement"] == quartier_nom].iloc[0]
    superficie = quartier["superficie"] 
    quartier_label = f"{quartier_nom} ({superficie:.1f} km²)"

    quartier_normalized = (quartier[features] - min_values) / (max_values - min_values)
    quartier_valeurs_reelles = quartier[features].astype(float).values

    # Données moyennes (normalisées aussi)
    moyenne = data[features].mean()
    moyenne_normalized = (moyenne - min_values) / (max_values - min_values)

    # Fermer les polygones
    theta = labels_pretties + [labels_pretties[0]]
    r_quartier = list(quartier_normalized.values) + [quartier_normalized.values[0]]
    r_moyenne = list(moyenne_normalized.values) + [moyenne_normalized.values[0]]
    customdata_quartier = list(quartier_valeurs_reelles) + [quartier_valeurs_reelles[0]]
    customdata_moyenne = list(moyenne.values) + [moyenne.values[0]]

    # Figure radar
    fig = go.Figure()

    # Trace de la moyenne (gris)
    fig.add_trace(go.Scatterpolar(
        r=r_moyenne,
        theta=theta,
        fill='toself',
        name="Moyenne",
        line_color='gray',
        customdata=[[val] for val in customdata_moyenne],
        hovertemplate="%{theta}<br>Moyenne : %{customdata[0]:.2f}",
        mode='lines+markers'
    ))

    # Trace du quartier sélectionné (rouge)
    fig.add_trace(go.Scatterpolar(
        r=r_quartier,
        theta=theta,
        fill='toself',
        name=quartier_nom,
        line_color='red',
        customdata=[[val] for val in customdata_quartier],
        hovertemplate="%{theta}<br>Valeur réelle : %{customdata[0]:.2f}",
        mode='lines+markers'
    ))

    fig.update_layout(
    title=f"Profil normalisé de {quartier_label}",
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=True,
    legend=dict(
        orientation="h",          # horizontal
        yanchor="bottom",         # ancrage vertical en bas
        y=-0.3,                   # position en dessous du graphe
        xanchor="center",         # centré horizontalement
        x=0.5                     # position horizontale (0 = gauche, 1 = droite)
    ),
    margin={"r": 20, "t": 40, "l": 20, "b": 80}  # on agrandit un peu la marge en bas
)


    return fig
