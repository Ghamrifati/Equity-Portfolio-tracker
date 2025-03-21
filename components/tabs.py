# Onglets pour la navigation
"""
Composant de navigation par onglets
"""
import dash
from dash import html
import dash_bootstrap_components as dbc

def create_tab_navigation():
    """
    Crée la navigation par onglets en bas de l'application
    
    Returns:
        dash.html.Div: Composant de navigation par onglets
    """
    tabs = html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    "Valeur du Portefeuille",
                    id="btn-portfolio-value",
                    color="secondary",
                    outline=True,
                    className="tab-button active"
                ),
                width="auto"
            ),
            dbc.Col(
                dbc.Button(
                    "Répartition du Portefeuille",
                    id="btn-portfolio-breakdown",
                    color="secondary",
                    outline=True,
                    className="tab-button"
                ),
                width="auto"
            ),
            dbc.Col(
                dbc.Button(
                    "Profits Manqués",
                    id="btn-missed-profit",
                    color="secondary",
                    outline=True,
                    className="tab-button"
                ),
                width="auto"
            ),
            dbc.Col(
                dbc.Button(
                    "Stratégie d'Achat/Vente",
                    id="btn-buy-high-sell-low",
                    color="secondary",
                    outline=True,
                    className="tab-button"
                ),
                width="auto"
            ),
            dbc.Col(width=4),  # Espacement
            dbc.Col(
                dbc.Button(
                    "MASI",
                    id="btn-masi",
                    color="secondary",
                    outline=True,
                    className="tab-button"
                ),
                width="auto"
            ),
            dbc.Col(
                dbc.Button(
                    "Actions",
                    id="btn-stocks",
                    color="secondary",
                    outline=True,
                    className="tab-button active"
                ),
                width="auto"
            ),
        ], className="tabs-row", justify="start")
    ], className="tabs-container")
    
    return tabs
