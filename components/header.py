"""
Composant d'en-tête de l'application
"""
import dash
from dash import html
import dash_bootstrap_components as dbc

def create_header():
    """
    Crée l'en-tête de l'application avec logo et titre
    
    Returns:
        dash.html.Div: Composant d'en-tête
    """
    header = html.Div([
        dbc.Row([
            # Logo
            dbc.Col(
                html.Div([
                    html.Img(
                        src='/assets/logo.png',  # Assurez-vous d'avoir ce fichier dans le dossier assets
                        height="50px",
                        alt="Logo"
                    ),
                    html.H3("Equity Portfolio Tracker", className="header-title")
                ], className="logo-container"),
                width=6
            ),
            
            # Espace vide ou autres éléments d'en-tête si nécessaire
            dbc.Col(width=6)
        ], className="header-row")
    ], className="header-container")
    
    return header
