# Tableau détaillé du portefeuille
"""
Composant du tableau du portefeuille
"""
import dash
from dash import html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from modules.utils import format_currency, format_percentage

def create_portfolio_table(portfolio_data, missed_profits_data):
    """
    Crée un tableau détaillé du portefeuille
    
    Args:
        portfolio_data (pd.DataFrame): Données du portefeuille
        missed_profits_data (pd.DataFrame): Données des profits manqués
    
    Returns:
        dash.html.Div: Composant de tableau du portefeuille
    """
    # Fusion des données du portefeuille avec les profits manqués
    if not missed_profits_data.empty and not portfolio_data.empty:
        table_data = pd.merge(
            portfolio_data,
            missed_profits_data[['symbol', 'missed_profit']],
            on='symbol',
            how='left'
        )
    else:
        table_data = portfolio_data.copy()
        if 'missed_profit' not in table_data.columns:
            table_data['missed_profit'] = 0
    
    # Sélection et renommage des colonnes
    if not table_data.empty:
        table_data = table_data[['symbol', 'close', 'quantity', 'missed_profit']]
        table_data = table_data.rename(columns={
            'symbol': 'Symbol',
            'close': 'Current Price',
            'quantity': 'Quantity',
            'missed_profit': 'Missed Profit'
        })
    
        # Formatage des valeurs
        table_data['Current Price'] = table_data['Current Price'].apply(lambda x: format_currency(x, ""))
        table_data['Missed Profit'] = table_data['Missed Profit'].apply(format_currency)
        
        # Calcul du total
        total_row = pd.DataFrame({
            'Symbol': ['Total'],
            'Current Price': [format_currency(table_data['Current Price'].sum(), "")],
            'Quantity': [table_data['Quantity'].sum()],
            'Missed Profit': [format_currency(table_data['Missed Profit'].sum())]
        })
        
        # Ajout de la ligne de total
        table_data = pd.concat([table_data, total_row])
    else:
        # Créer un DataFrame vide avec les bonnes colonnes
        table_data = pd.DataFrame(columns=['Symbol', 'Current Price', 'Quantity', 'Missed Profit'])
    
    portfolio_table = html.Div([
        html.Div([
            html.H3("Symbol", className="table-header"),
            html.H3("Current Price", className="table-header"),
            html.H3("Quantity", className="table-header"),
            html.H3("Missed Profit", className="table-header", style={"text-align": "right"}),
        ], className="table-header-row"),
        
        # Tableau avec dash_table
        dash_table.DataTable(
            id='portfolio-table',
            columns=[
                {'name': 'Symbol', 'id': 'Symbol'},
                {'name': 'Current Price', 'id': 'Current Price'},
                {'name': 'Quantity', 'id': 'Quantity', 'type': 'numeric'},
                {'name': 'Missed Profit', 'id': 'Missed Profit', 'type': 'text'},
            ],
            data=table_data.to_dict('records'),
            style_table={
                'overflowX': 'auto',
                'backgroundColor': '#333333',
                'borderRadius': '10px',
            },
            style_header={
                'backgroundColor': '#333333',
                'display': 'none',  # Cacher l'en-tête car nous utilisons notre propre en-tête
            },
            style_cell={
                'backgroundColor': '#333333',
                'color': 'white',
                'border': 'none',
                'padding': '10px',
                'font-size': '14px',
            },
            style_data_conditional=[
                # Style pour la ligne de total
                {
                    'if': {'filter_query': '{Symbol} = "Total"'},
                    'fontWeight': 'bold',
                    'backgroundColor': '#444444',
                },
                # Style pour les valeurs négatives (profits manqués)
                {
                    'if': {
                        'column_id': 'Missed Profit',
                        'filter_query': '{Missed Profit} contains "-"'
                    },
                    'color': '#FF4500',
                },
                # Style pour les profits manqués positifs (avec "$" mais pas "-")
                {
                    'if': {
                        'column_id': 'Missed Profit',
                        'filter_query': '{Missed Profit} contains "₹" && !({Missed Profit} contains "-")'
                    },
                    'color': '#00FF7F',
                },
            ],
            style_cell_conditional=[
                {'if': {'column_id': 'Symbol'}, 'textAlign': 'left', 'width': '25%'},
                {'if': {'column_id': 'Current Price'}, 'textAlign': 'right', 'width': '25%'},
                {'if': {'column_id': 'Quantity'}, 'textAlign': 'right', 'width': '25%'},
                {'if': {'column_id': 'Missed Profit'}, 'textAlign': 'right', 'width': '25%'},
            ],
        ),
    ], className="portfolio-table-container")
    
    return portfolio_table