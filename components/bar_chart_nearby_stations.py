import pandas as pd
import numpy as np
import plotly.graph_objs as go
from geopy.distance import great_circle
import calendar

def get_nearby_stations(map_df, station_id, radius_km=0.5):
    station = map_df[map_df['station_id'] == station_id].iloc[0]
    ref_coords = (station['lat'], station['lon'])

    def compute_distance(row):
        return great_circle(ref_coords, (row['lat'], row['lon'])).km

    df_copy = map_df.copy()
    df_copy['distance_km'] = df_copy.apply(compute_distance, axis=1)
    nearby = df_copy[(df_copy['station_id'] != station_id) & (df_copy['distance_km'] <= radius_km)]
    nearby = nearby.sort_values('distance_km').head(5)
    return nearby, station

def generate_bar_chart_nearby_stations(station_id, map_df, annual_df):
    station_id = int(station_id)

    nearby_stations, selected_station = get_nearby_stations(map_df, station_id)
    selected_name = selected_station['name']

    # Extraire les données de la station sélectionnée et des voisines
    df_combined = pd.concat([
        annual_df[annual_df['station_id'] == station_id],
        annual_df[annual_df['station_id'].isin(nearby_stations['station_id'])]
    ])
    
    # Ajouter les infos station
    map_subset = pd.concat([nearby_stations, selected_station.to_frame().T], ignore_index=True)
    df_combined = df_combined.merge(map_subset[['station_id', 'name', 'distance_km']], on='station_id', how='left')

    # Préparer les étiquettes, couleurs, ordre
    df_combined['x_label'] = df_combined.apply(
        lambda row: f"{row['name']}<br>({row['distance_km']*1000:.0f} m)" if row['station_id'] != station_id else row['name'],
        axis=1
    )
    df_combined['color'] = df_combined['station_id'].apply(lambda x: 'black' if x == station_id else 'red')

    # 👉 Mettre la station sélectionnée en premier
    df_combined['is_selected'] = df_combined['station_id'] == station_id
    df_combined = df_combined.sort_values(by=['is_selected', 'distance_km'], ascending=[False, True])

    # Créer le graphique avec 1 trace par barre
    fig = go.Figure()
    for _, row in df_combined.iterrows():
        fig.add_trace(go.Bar(
            x=[row['x_label']],
            y=[row['nb_passages']],
            marker_color=row['color'],
            hovertemplate=(
                f"<b>Station :</b> {row['name']}<br>" +
                (f"<b>Distance :</b> {row['distance_km']*1000:.0f} m<br>" if row['station_id'] != station_id else "") +
                f"<b>Passages annuels :</b> {row['nb_passages']:,} passages<extra></extra>"
            )
        ))

    fig.update_layout(
        title=f'Passage annuel à {selected_name} et stations proches',
        yaxis_title='Nombre de passages',
        xaxis_title='',
        template='plotly_white',
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        showlegend=False
    )

    return fig

def generate_stacked_bar_chart_nearby_stations(station_id, map_df, monthly_df):
    station_id = int(station_id)

    nearby_stations, selected_station = get_nearby_stations(map_df, station_id)
    selected_name = selected_station['name']
    selected_coords = (selected_station['lat'], selected_station['lon'])

    # Station sélectionnée + voisines
    selected_df = pd.DataFrame([{
        'station_id': station_id,
        'name': selected_name,
        'lat': selected_coords[0],
        'lon': selected_coords[1],
        'distance_km': 0
    }])
    stations_info = pd.concat([selected_df, nearby_stations], ignore_index=True)

    station_ids = stations_info['station_id'].tolist()
    df_filtered = monthly_df[monthly_df['station_id'].isin(station_ids)].copy()
    df_filtered = df_filtered.merge(stations_info[['station_id', 'name', 'distance_km']], on='station_id', how='left')

    # Ajoute labels et structure
    df_filtered['x_label'] = df_filtered.apply(
        lambda row: row['name'] if row['distance_km'] == 0
        else f"{row['name']}<br>({row['distance_km']*1000:.0f} m)",
        axis=1
    )
    df_filtered['is_selected'] = df_filtered['distance_km'] == 0

    # Ordre des stations : sélectionnée d'abord
    station_order = (
        df_filtered.drop_duplicates('station_id')
        .sort_values(by=['is_selected', 'distance_km'], ascending=[False, True])
        ['x_label'].tolist()
    )
    
    # Obtenir tous les mois présents
    all_months = sorted(df_filtered['month'].unique())

    # Obtenir toutes les stations considérées
    stations = df_filtered[['station_id', 'x_label']].drop_duplicates()

    # Produit cartésien station × mois
    full_index = pd.MultiIndex.from_product(
        [stations['station_id'], all_months], names=['station_id', 'month']
    ).to_frame(index=False)

    # Rejoindre pour inclure les distances et noms
    full_df = full_index.merge(stations, on='station_id', how='left')
    full_df = full_df.merge(
        stations_info[['station_id', 'distance_km']], on='station_id', how='left'
    )

    # Fusionner avec les données existantes
    df_filtered = full_df.merge(
        df_filtered[['station_id', 'month', 'nb_passages']], 
        on=['station_id', 'month'], how='left'
    )

    # Remplir les valeurs manquantes avec 0
    df_filtered['nb_passages'] = df_filtered['nb_passages'].fillna(0)

    df_filtered['x_label'] = pd.Categorical(df_filtered['x_label'], categories=station_order, ordered=True)
    df_filtered = df_filtered.sort_values(['x_label', 'month'])

    # Créer le graphe avec une couleur par mois
    fig = go.Figure()
    for month in sorted(df_filtered['month'].unique()):
        df_month = df_filtered[df_filtered['month'] == month]
        month_name = calendar.month_name[month]  # ex : "Février"
        fig.add_trace(go.Bar(
            x=df_month['x_label'],
            y=df_month['nb_passages'],
            name=month_name,
            hovertemplate=(
                "<b>Station :</b> %{x}<br>"
                f"<b>Mois :</b> {month_name}<br>"
                "<b>Passages :</b> %{y}<extra></extra>"
            )
        ))

    fig.update_layout(
        barmode='stack',
        title=f'Trafic mensuel empilé à {selected_name} et stations proches',
        yaxis_title='Nombre de passages',
        xaxis_title='',
        template='plotly_white',
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        showlegend=True
    )

    return fig

def update_bar_chart_nearby_stations(fig, param=None):
    # Pas de mise à jour nécessaire pour le graphique
    return fig
