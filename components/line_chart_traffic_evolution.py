import plotly.express as px
import pandas as pd
import numpy as np

def generate_line_chart_traffic(data=None):
    df = pd.DataFrame({
        'x': pd.date_range(start='2025-01-01', periods=30),
        'y': np.random.randint(200, 900, 30)
    })
    fig = px.line(df, x='x', y='y', title='Évolution du trafic cyclable (démo)')
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def update_line_chart_traffic(fig, param=None):
    return fig
