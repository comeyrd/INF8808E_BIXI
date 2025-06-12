import plotly.express as px
import pandas as pd


def generate_montreal_interactive_map(map_df, selected_station_id=""):
    map_df = map_df.copy()
    map_df['color'] = map_df['station_id_s'].apply(
        lambda x: 'red' if x == selected_station_id else 'blue'
    )
    zoom = 11

    if selected_station_id and selected_station_id in map_df['station_id_s'].values:
        selected_row = map_df[map_df['station_id_s']
                              == selected_station_id].iloc[0]
        center = {'lat': selected_row['lat'], 'lon': selected_row['lon']}
    else:
        center = {'lat': 45.5017, 'lon': -73.5673}

    fig = px.scatter_mapbox(
        map_df,
        lat='lat',
        lon='lon',
        hover_name='name',
        custom_data=['station_id_s'],
        color='color',
        color_discrete_map={'red': 'red', 'blue': 'blue'},
        zoom=zoom,
        center=center,
        height=600,
    )

    fig.update_layout(
        mapbox_style='open-street-map',
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
        showlegend=False
    )
    return fig
