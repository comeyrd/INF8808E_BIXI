import plotly.express as px
import pandas as pd
import numpy as np


def generate_animated_bixi_heatmap(gdf):
    fig = px.density_map(
        gdf,
        lat='lat',
        lon='lon',
        z='nb_passages',
        animation_frame='week',
        radius=15,
        center=dict(lat=gdf['lat'].mean(), lon=gdf['lon'].mean()),
        zoom=10,
        range_color=[0, gdf['nb_passages'].max()],
        color_continuous_scale=px.colors.sequential.Turbo,
        hover_data=['station_id', 'nb_passages'],
        title="Nombre de passages par station Bixi - Animation hebdomadaire"
    )

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
    # Optional: no delay between
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 0
    fig.layout.sliders[0]['transition']['duration'] = 0

    fig.update_layout(
        title="Nombre de passages par station Bixi - Animation hebdomadaire",
        title_font_size=20,
        title_x=0.5,
        height=700 
    )
    return fig

def update_animated_bixi_heatmap(fig, param=None):
    return fig
