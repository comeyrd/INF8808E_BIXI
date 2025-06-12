import plotly.graph_objects as go
import pandas as pd

def generate_montreal_interactive_map(map_df, selected_station_id=None,center=None,zoom=11):
    map_df = map_df.copy()

    latitudes = map_df['lat']
    longitudes = map_df['lon']
    names = map_df['name']
    ids = map_df['station_id_s']
    if center is None : 
        center = {'lat': 45.5017, 'lon': -73.5673}
    if zoom is None : 
        zoom = 11
    colors = ['red' if sid == selected_station_id else 'blue' for sid in ids]
    sizes = [12 if sid == selected_station_id else 5 for sid in ids]

    fig = go.Figure(go.Scattermapbox(
        lat=latitudes,
        lon=longitudes,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=sizes,
            color=colors
        ),
        customdata=ids,
        hovertext=names,
        hoverinfo='text'
    ))

    fig.update_layout(
        mapbox_style='open-street-map',
        mapbox_center=center,
        mapbox_zoom=zoom,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )

    return fig
