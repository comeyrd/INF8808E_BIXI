import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

import data_preprocessing as data_preprocessing

import layouts.page1 as page1_layout
import layouts.page2 as page2_layout
import layouts.page3 as page3_layout

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = 'Projet INF8808 - Réseau Cyclable Montréal'
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Header(children=[
        html.H1("Utilisation du Réseau Cyclable à Montréal"),
        html.Nav(children=[
            dcc.Link('Accueil (Carte & Trafic)',
                     href='/', className='nav-link'),
            dcc.Link('Comparaison des Quartiers',
                     href='/page2', className='nav-link'),
            dcc.Link('Fréquentation Réseau & BIXI',
                     href='/page3', className='nav-link'),
        ])
    ], className='app-header'),

    html.Div(id='page-content', className='page-container'),

    html.Footer(children=[
        html.P("INF8808 - Visualisation de données | Été 2025 | Équipe 1 - Plotly")
    ], className='app-footer')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page2':
        return page2_layout.layout()
    elif pathname == '/page3':
        return page3_layout.layout(
        )
    else:
        return page1_layout.layout()



page1_layout.register_callbacks(app)
page2_layout.register_callbacks(app)
page3_layout.register_callbacks(app)
