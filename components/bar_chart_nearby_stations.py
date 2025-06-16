import pandas as pd
import numpy as np
import plotly.graph_objs as go
from geopy.distance import great_circle

def generate_bar_chart_nearby_stations(station_id, map_df, annual_df):
    station_id = int(station_id)

    def get_nearby_stations(map_df, station_id, radius_km=0.5):
        station = map_df[map_df['station_id'] == station_id].iloc[0]
        ref_coords = (station['lat'], station['lon'])

        def compute_distance(row):
            return great_circle(ref_coords, (row['lat'], row['lon'])).km

        df = map_df.copy()
        df['distance_km'] = df.apply(compute_distance, axis=1)
        nearby = df[(df['station_id'] != station_id) & (df['distance_km'] <= radius_km)]
        return nearby.sort_values('distance_km').head(5), station

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

def update_bar_chart_nearby_stations(fig, param=None):
    # Pas de mise à jour nécessaire pour le graphique
    return fig
