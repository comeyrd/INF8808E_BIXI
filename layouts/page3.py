from dash import html, dcc, Input, Output, State
from components.weekly_heatmap_network import generate_weekly_network_heatmap
from dash import html, dcc, Input, Output, State, no_update
import plotly.express as px
from components.weekly_heatmap_network import generate_weekly_network_heatmap, generate_bar_chart
from components.animated_bixi_heatmap import generate_animated_bixi_heatmap
import geopandas as gpd
import data_store

def layout():
    return html.Div([
        html.H2("Fréquentation du réseau cyclable et BIXI toute l'année 2024", className="section-title"),
        dcc.Dropdown(
            id='page3-viz-selector',
            options=[
                {'label': "Affluence journalier (3.1)", 'value': 'heatmap'},
                {'label': "Carte animée BIXI (3.2)", 'value': 'bixi'}
            ],
            value='heatmap',
            clearable=False
        ),

        dcc.Store(id='page3-selected-week', storage_type='memory'),

        dcc.Graph(id='page3-viz-display'),
        dcc.Graph(id='page3-bar-chart', style={'display': 'none'}, config={'staticPlot': True}),
    ], className='page-content')


def register_callbacks(app):
    @app.callback(
        Output('page3-viz-display', 'figure'),
        Input('page3-viz-selector', 'value'),
        Input('page3-selected-week', 'data'),
    )
    def update_page3_viz_main(selected_viz, selected_week):
        if selected_viz == 'bixi':
            gdf = data_store.page3_viz2_gdf
            return generate_animated_bixi_heatmap(gdf)

        df_day = data_store.page3_df_day
        heatmap_data = data_store.page3_heatmap_data
        mois_ticks = data_store.mois_ticks
        mois_labels = data_store.mois_labels
        return generate_weekly_network_heatmap(df_day, heatmap_data, mois_ticks, mois_labels, selected_week)

        
    @app.callback(
        Output('page3-selected-week', 'data'),
        Input('page3-viz-display', 'clickData'),
        State('page3-viz-selector', 'value')
    )
    def store_selected_week(clickData, selected_viz):
        if selected_viz != 'heatmap' or clickData is None:
            return None
        return int(clickData['points'][0]['x'])

    @app.callback(
        Output('page3-bar-chart', 'figure'),
        Output('page3-bar-chart', 'style'),
        Input('page3-selected-week', 'data'),
        State('page3-viz-selector', 'value')
    )
    def update_bar_chart(week, selected_viz):
        df_day = data_store.page3_df_day

        if selected_viz != 'heatmap' or week is None:
            return {}, {'display': 'none'}
        
        fig = generate_bar_chart(df_day, week)
        return fig, {'display': 'block'}