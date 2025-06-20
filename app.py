import dash
from dash import html, dcc, Input, Output, State

import data_preprocessing as data_preprocessing
import layouts.page1 as page1_layout
import layouts.page2 as page2_layout
import layouts.page3 as page3_layout

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = 'Projet INF8808 - Réseau cyclable Montréal'
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Header(children=[
        html.H1("Utilisation du réseau cyclable à Montréal"),
        html.P("Analyse des données de trafic et de BIXI durant l'année 2024"),
        html.Div(id='nav-buttons', style={'display': 'flex',
                                          'gap': '10px',
                                          'marginBottom': '10px',
                                          'justifyContent': 'center'}),
    ], className='app-header'),

    html.Div(id='page-content', className='page-container'),

    html.Footer(children=[
        html.P("INF8808 - Visualisation de données | Été 2025 | Équipe 1 - Plotly")
    ], className='app-footer')
])

# Callback pour mettre à jour l’URL selon le bouton cliqué
@app.callback(
    Output('url', 'pathname'),
    Input('btn-page1', 'n_clicks'),
    Input('btn-page2', 'n_clicks'),
    Input('btn-page3', 'n_clicks'),
    prevent_initial_call=True
)
def navigate(btn1, btn2, btn3):
    ctx = dash.callback_context
    if not ctx.triggered:
        return '/'
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'btn-page1':
        return '/'
    elif button_id == 'btn-page2':
        return '/page2'
    elif button_id == 'btn-page3':
        return '/page3'
    return '/'

# Callback pour afficher les bons boutons avec le bon style
@app.callback(
    Output('nav-buttons', 'children'),
    Input('url', 'pathname')
)
def style_nav_buttons(pathname):
    def button(label, page_href, btn_id):
        is_active = pathname == page_href
        return html.Button(label, id=btn_id, n_clicks=0, style={
            'backgroundColor': '#b71c1c' if is_active else '#f0f0f0',
            'color': 'white' if is_active else '#b71c1c',
            'border': '2px solid #b71c1c',
            'padding': '10px 20px',
            'cursor': 'pointer',
            'fontWeight': 'bold',
            'borderRadius': '30px',
            'transition': 'all 0.3s ease'
        })

    return [
        button("Accueil (carte et trafic)", "/", "btn-page1"),
        button("Comparaison des quartiers", "/page2", "btn-page2"),
        button("Fréquentation réseau et BIXI", "/page3", "btn-page3"),
    ]

# Affichage de la page en fonction de l’URL
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page2':
        return page2_layout.layout()
    elif pathname == '/page3':
        return page3_layout.layout()
    else:
        return page1_layout.layout()

# Enregistrement des callbacks
page1_layout.register_callbacks(app)
page2_layout.register_callbacks(app)
page3_layout.register_callbacks(app)