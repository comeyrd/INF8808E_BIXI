import plotly.express as px
import pandas as pd
import numpy as np

def generate_bar_chart_nearby_stations(data=None):
    df = pd.DataFrame({
        'Station': [f'Station {i}' for i in range(5)],
        'Trafic': np.random.randint(100, 500, 5)
    })
    fig = px.bar(df, x='Station', y='Trafic', title='Trafic des stations proches (démo)')
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def update_bar_chart_nearby_stations(fig, param=None):
    return fig
