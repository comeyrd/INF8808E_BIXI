import plotly.express as px
import pandas as pd
import numpy as np

def generate_animated_bixi_heatmap(gdf):
    fig = px.density_mapbox(
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
        hover_data=['name', 'nb_passages'],
        mapbox_style="open-street-map",
        title="Nombre de passages par station Bixi - Animation hebdomadaire",
    )
    
    fig.update_traces(
        hovertemplate="<b>Station :</b> %{customdata[0]}<br><b>Passages:</b> %{z:.0f}<extra></extra>",
        customdata=gdf[['name']].values
    )

    # Animation speed
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 0
    fig.layout.sliders[0]['transition']['duration'] = 0

    fig.update_layout(
        title="Nombre de passages par station Bixi - Animation hebdomadaire",
        title_font_size=20,
        title_x=0.5,
        height=700,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    # Corriger le hovertemplate pour chaque frame
    for frame in fig.frames:
        week = int(frame.name)
        frame_df = gdf[gdf['week'] == week]
        for i, trace in enumerate(frame.data):
            trace.hovertemplate = "<b>Station :</b> %{customdata[0]}<br><b>Passages:</b> %{z:.0f}<extra></extra>"
            trace.customdata = frame_df[['name']].values


    return fig


def update_animated_bixi_heatmap(fig, param=None):
    return fig
