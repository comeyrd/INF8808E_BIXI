from dash import html, dcc, Input, Output, State, no_update
import plotly.express as px
from components.weekly_heatmap_network import generate_weekly_network_heatmap, generate_bar_chart
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

        dcc.Graph(id='page3-viz-display'),
        dcc.Graph(id='page3-bar-chart', style={'display': 'none'})
    ], className='page-content')

def register_callbacks(app):
    @app.callback(
        Output('page3-viz-display', 'figure'),
        Output('page3-bar-chart', 'figure'),
        Output('page3-bar-chart', 'style'),
        Input('page3-viz-selector', 'value'),
        Input('page3-viz-display', 'clickData'),
        State('viz2-data','data')
    )
    def update_page3_viz(selected_viz,clickData, viz2_data):
        gdf = gpd.GeoDataFrame.from_features(viz2_data["features"])
        if selected_viz == 'bixi':
            return generate_animated_bixi_heatmap(gdf), {}, {'display': 'none'}
        # Extraire semaine cliquée (sinon 0)
        week = int(clickData['points'][0]['x']) if clickData else None
        fig_heatmap = generate_weekly_network_heatmap(selected_week=week)
        
        if week is not None:
            fig_bar = generate_bar_chart(week)
            return fig_heatmap, fig_bar, {'display': 'block'}
        else:
            return fig_heatmap, no_update, {'display': 'none'}
        #return generate_weekly_network_heatmap(), {'display': 'block'}

    
    
    def update_bar_chart(clickData, selected_viz):
        if selected_viz != 'heatmap' or not clickData:
            return generate_bar_chart(0)  # par défaut, ou vide
        week = int(clickData['points'][0]['x'])  # 'x' = WeekIndex
        return generate_bar_chart(week)
    
    
