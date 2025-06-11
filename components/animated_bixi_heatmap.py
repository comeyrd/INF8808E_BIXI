import plotly.express as px
import pandas as pd
import numpy as np

def generate_animated_bixi_heatmap(data=None):
    df = pd.DataFrame({
        'Semaine': pd.date_range(start='2025-01-01', periods=10, freq='W'),
        'Passages': np.random.randint(100, 500, 10)
    })
    fig = px.line(df, x='Semaine', y='Passages', title='Carte animée BIXI (démo)')
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def update_animated_bixi_heatmap(fig, param=None):
    return fig
