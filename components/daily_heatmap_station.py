import plotly.express as px
import pandas as pd
import numpy as np

def generate_daily_heatmap_station(data=None):
    df = pd.DataFrame({
        'Date': pd.date_range(start='2025-01-01', periods=30),
        'Valeur': np.random.randint(100, 700, 30)
    })
    fig = px.line(df, x='Date', y='Valeur', title='Heatmap journalière station (démo)')
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def update_daily_heatmap_station(fig, param=None):
    return fig
