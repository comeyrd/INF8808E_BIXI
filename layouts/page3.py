from dash import html, dcc, Input, Output, State
from components.weekly_heatmap_network import generate_weekly_network_heatmap
from components.animated_bixi_heatmap import generate_animated_bixi_heatmap
import geopandas as gpd
import data_store
def layout():
    return html.Div([
        html.H2("Fréquentation du Réseau Cyclable & BIXI", className="section-title"),

        dcc.Dropdown(
            id='page3-viz-selector',
            options=[
                {'label': "Heatmap du réseau (3.1)", 'value': 'heatmap'},
                {'label': "Carte animée BIXI (3.2)", 'value': 'bixi'}
            ],
            value='heatmap',
            clearable=False
        ),

        dcc.Graph(id='page3-viz-display')
    ], className='page-content')

def register_callbacks(app):
    @app.callback(
        Output('page3-viz-display', 'figure'),
        Input('page3-viz-selector', 'value'),
    )
    def update_page3_viz(selected_viz):
        gdf = data_store.page3_viz2_gdf
        if selected_viz == 'bixi':
            return generate_animated_bixi_heatmap(gdf)
        return generate_weekly_network_heatmap()
