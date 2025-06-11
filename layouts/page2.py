from dash import html, dcc
from components.radar_chart_district_comparison import generate_radar_chart

def layout(data):
    return html.Div([
        html.H2("Comparaison des Quartiers de Montréal", className="section-title"),

        dcc.Graph(
            id='radar-chart',
            figure=generate_radar_chart(data)
        )
    ], className='page-content')
