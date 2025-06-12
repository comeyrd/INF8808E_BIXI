import plotly.express as px
import pandas as pd


def generate_montreal_interactive_map(map_df):
    center = {'lat': 45.5017, 'lon': -73.5673}
    fig = px.scatter_mapbox(
        map_df,
        lat='lat',
        lon='lon',
        hover_name='name',
        custom_data=['station_id_s'],
        zoom=11,
        center=center,
        height=600
    )
    fig.update_layout(
        mapbox_style='open-street-map',
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
    )
    return fig