"""
Layout principal de l'application
"""
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

from components.header import create_header
from components.date_selector import create_date_selector
from components.summary_cards import create_summary_cards
from components.portfolio_table import create_portfolio_table
from components.performance_chart import create_performance_chart
from components.tabs import create_tab_navigation

from modules.data_loader import calculate_portfolio_value, get_missed_profits
from modules.portfolio import calculate_portfolio_metrics, calculate_best_worst_performers, calculate_index_performance

def create_layout(historical_data, transactions_data):
    """
    Crée le layout principal de l'application
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
        transactions_data (pd.DataFrame): Données des transactions
    
    Returns:
        dash.html.Div: Layout principal
    """
    # Calcul des métriques du portefeuille
    portfolio_metrics = calculate_portfolio_metrics(transactions_data, historical_data)
    
    # Calcul des meilleures et pires performances
    best_performer, worst_performer = calculate_best_worst_performers(transactions_data, historical_data, '1Y')
    
    # Calcul de la performance de l'indice MASI
    masi_performance = calculate_index_performance(historical_data, '^MASI', '1Y')
    
    # Calcul des profits manqués
    missed_profits_data = get_missed_profits(historical_data, transactions_data)
    
    # Dates par défaut pour les sélecteurs
    start_date = datetime.now().replace(year=datetime.now().year - 1).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Création du layout
    layout = html.Div([
        # Header
        create_header(),
        
        # Sélecteur de dates
        create_date_selector(start_date, end_date),
        
        # Boutons des périodes
        html.Div([
            dbc.Button('1Y', id='btn-1y', color='light', className='period-btn'),
            dbc.Button('6M', id='btn-6m', color='light', className='period-btn'),
            dbc.Button('Last 60 Days', id='btn-60d', color='light', className='period-btn'),
            dbc.Button('MTD', id='btn-mtd', color='light', className='period-btn'),
            dbc.Button('YTD', id='btn-ytd', color='light', className='period-btn'),
        ], className='period-buttons-container'),
        
        # Cartes récapitulatives (MASI, Profit, Valeur, Rendements)
        create_summary_cards(
            masi_value=22378,  # À remplacer par la valeur réelle
            masi_change=0.18,  # À remplacer par la valeur réelle
            profit=portfolio_metrics['total_profit_loss'],
            profit_change=0.00,  # À calculer
            missed_profit=missed_profits_data['missed_profit'].sum() if not missed_profits_data.empty else 0,
            trades_done=portfolio_metrics['num_transactions'],
            portfolio_value=portfolio_metrics['total_value'],
            invested_amount=portfolio_metrics['total_investment'],
            mom_change=441.75,  # À calculer
            mom_value=43.67e3,  # À calculer
            returns_percent=portfolio_metrics['total_profit_loss_percent'],
            masi_yoy=masi_performance,
            best_performer=best_performer,
            worst_performer=worst_performer
        ),
        
        # Contenu de l'application (tableau + graphique)
        dbc.Row([
            # Tableau du portefeuille
            dbc.Col(
                create_portfolio_table(portfolio_metrics['portfolio_details'], missed_profits_data),
                width=12, md=6, lg=6
            ),
            
            # Graphique de performance
            dbc.Col(
                create_performance_chart(historical_data, transactions_data),
                width=12, md=6, lg=6
            ),
        ], className='app-content'),
        
        # Navigation par onglets
        create_tab_navigation(),
        
        # Store pour les données
        dcc.Store(id='store-historical-data', data=historical_data.to_json(date_format='iso', orient='split')),
        dcc.Store(id='store-transactions-data', data=transactions_data.to_json(date_format='iso', orient='split')),
        dcc.Store(id='store-current-period', data='1Y'),
    ], className='main-container')
    
    return layout
