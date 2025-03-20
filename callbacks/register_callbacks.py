"""
Enregistrement de tous les callbacks de l'application
"""
from callbacks.date_callbacks import register_date_callbacks
from callbacks.portfolio_callbacks import register_portfolio_callbacks
from callbacks.tab_callbacks import register_tab_callbacks

def register_all_callbacks(app, historical_data, transactions_data):
    """
    Enregistre tous les callbacks de l'application
    
    Args:
        app (dash.Dash): Application Dash
        historical_data (pd.DataFrame): Données historiques des prix
        transactions_data (pd.DataFrame): Données des transactions
    """
    # Enregistrer les callbacks pour les sélecteurs de date
    register_date_callbacks(app)
    
    # Enregistrer les callbacks pour le portefeuille
    register_portfolio_callbacks(app)
    
    # Enregistrer les callbacks pour la navigation par onglets
    register_tab_callbacks(app)