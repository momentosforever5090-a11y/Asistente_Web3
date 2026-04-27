# dashboard.py
from auth import app  # reutiliza la misma app Flask
import dash
from dash import html, dcc
from flask_login import current_user

# Integrar Dash usando el servidor Flask
dash_app = dash.Dash(__name__,
                     server=app,
                     url_base_pathname='/dashboard/',
                     assets_folder='assets')  # opcional: carpeta para CSS propio

dash_app.layout = html.Div([
    html.Div([
        html.H1('Dashboard Protegido', style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.Hr(),
        html.Div(id='user-greeting', style={'fontSize': '18px', 'marginBottom': '20px'}),
        dcc.Graph(
    figure={
        'data': [
            {'x': ['Enero', 'Febrero', 'Marzo', 'Abril'], 
             'y': [10, 20, 15, 25], 
             'type': 'bar', 
             'name': 'Ventas 2024',
             'marker': {'color': '#e74c3c', 'line': {'width': 1, 'color': 'black'}}},
            {'x': ['Enero', 'Febrero', 'Marzo', 'Abril'], 
             'y': [5, 12, 8, 18], 
             'type': 'line', 
             'name': 'Objetivo',
             'line': {'color': '#2ecc71', 'width': 3, 'dash': 'dash'}}
        ],
        'layout': {
            'title': {'text': '📊 Comparativa Ventas vs Objetivo', 'font': {'size': 24}},
            'xaxis': {'title': 'Mes', 'tickangle': -45},
            'yaxis': {'title': 'Miles de €', 'gridcolor': '#ddd'},
            'plot_bgcolor': '#f9f9f9',
            'paper_bgcolor': '#ffffff',
            'font': {'family': 'Arial', 'size': 12, 'color': '#2c3e50'},
            'legend': {'x': 0, 'y': 1, 'bgcolor': 'rgba(255,255,255,0.8)'},
            'hovermode': 'closest'
        }
    }
),
        html.Br(),
        html.Div([
            html.A('Cerrar sesión', href='/logout', 
                   style={'backgroundColor': '#e74c3c', 'color': 'white', 
                          'padding': '10px 20px', 'textDecoration': 'none', 
                          'borderRadius': '5px'})
        ], style={'textAlign': 'center'})
    ], style={'padding': '30px', 'maxWidth': '800px', 'margin': 'auto'})
])

@dash_app.callback(
    dash.dependencies.Output('user-greeting', 'children'),
    dash.dependencies.Input('user-greeting', 'id')
)
def update_greeting(_):
    if current_user.is_authenticated:
        return html.Div([
            html.Span(f'👋 Bienvenido, {current_user.username}!', 
                      style={'fontWeight': 'bold', 'fontSize': '20px'}),
            html.Br(),
            html.Small('Este es tu panel de control personalizado')
        ])
    return html.Div('⚠️ No autenticado', style={'color': 'red'})
