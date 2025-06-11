import plotly.express as px
import pandas as pd
import numpy as np

def generate_weekly_network_heatmap(data=None):
    df = pd.DataFrame({
        'Semaine': pd.date_range(start='2025-01-01', periods=30, freq='W'),
        'Trafic': np.random.randint(300, 1000, 30)
    })
    fig = px.line(df, x='Semaine', y='Trafic', title='Heatmap hebdomadaire réseau (démo)')
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def update_weekly_network_heatmap(fig, param=None):
    return fig
