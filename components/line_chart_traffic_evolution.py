import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go

def generate_line_chart_traffic(station_id,line_chart_df,station_name):
    fig = go.Figure()
    df_station = line_chart_df[line_chart_df['station_id_s'] == station_id]

    fig.add_trace(go.Scatter(
        x=df_station['week_date'],
        y=df_station['nb_passages'],
        mode='lines+markers',
        name=f'Trafic station {station_id}'
    ))

    fig.update_layout(
    title=f'Évolution du trafic en 2024 sur la station {station_name}',
    xaxis_title='Semaine',
    yaxis_title='Nombre de passages',
    xaxis=dict(
        tickformat='%d %b',
        tickangle=45,
        range=['2024-01-01', '2024-12-31']  # Axe X fixe toute l'année
    ),
    yaxis=dict(
        range=[0, line_chart_df['nb_passages'].max() * 1.1]  # Limite y max = 10% au-dessus du max des données
    ),
    template='plotly_white'
)

    return fig

def update_line_chart_traffic(fig, param=None):
    return fig
