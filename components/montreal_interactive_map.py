import plotly.express as px
import pandas as pd

def generate_montreal_interactive_map(data=None):
    center = {'lat': 45.5017, 'lon': -73.5673}
    fig = px.scatter_mapbox(
        pd.DataFrame({'lat': [], 'lon': []}),
        lat='lat',
        lon='lon',
        zoom=11,
        center=center,
        height=600
    )
    fig.update_layout(
        mapbox_style='open-street-map',
        margin={'l':0, 'r':0, 'b':0, 't':0},
        uirevision='constant'
    )
    return fig
