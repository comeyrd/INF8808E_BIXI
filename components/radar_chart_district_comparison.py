import plotly.express as px
import pandas as pd
import numpy as np

def generate_radar_chart(data=None):
    categories = ['Quartier A', 'Quartier B', 'Quartier C', 'Quartier D', 'Quartier E']
    values = np.random.randint(10, 100, len(categories))

    df = pd.DataFrame({
        'district': categories,
        'value': values
    })

    fig = px.line_polar(df, r='value', theta='district', line_close=True,
                        title='Comparaison des quartiers (démo)')
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

def update_radar_chart(fig, param=None):
    return fig
