# Callbacks pour les tables et graphiques du portefeuille
"""
Callbacks pour le portefeuille
"""
from dash import Input, Output, State
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px

from modules.portfolio import calculate_portfolio_metrics, calculate_best_worst_performers
from modules.performance import calculate_comparative_performance, calculate_missed_profit
from modules.data_loader import get_current_prices
from modules.utils import format_currency, format_percentage

def register_portfolio_callbacks(app):
    """
    Enregistre les callbacks liés au portefeuille
    
    Args:
        app (dash.Dash): Application Dash
    """
    @app.callback(
        Output('portfolio-table', 'data'),
        [
            Input('store-current-period', 'data'),
            Input('start-date-picker', 'date'),
            Input('end-date-picker', 'date')
        ],
        [
            State('store-historical-data', 'data'),
            State('store-transactions-data', 'data')
        ]
    )
    def update_portfolio_table(period, start_date, end_date, historical_data_json, transactions_data_json):
        """
        Met à jour le tableau du portefeuille en fonction de la période sélectionnée
        """
        # Convertir les données JSON en DataFrames
        try:
            historical_data = pd.read_json(historical_data_json, orient='split')
            transactions_data = pd.read_json(transactions_data_json, orient='split')
            
            # Convertir les dates
            historical_data['date'] = pd.to_datetime(historical_data['Date'])
            transactions_data['purchase_date'] = pd.to_datetime(transactions_data['Date_Acquisition'])
        except Exception as e:
            # En cas d'erreur, retourner un tableau vide
            return []
        
        # Filtrer les données selon la période
        end_date = pd.to_datetime(end_date)
        
        # Filtrer les transactions jusqu'à end_date
        filtered_transactions = transactions_data[transactions_data['purchase_date'] <= end_date]
        
        # Calculer les métriques du portefeuille
        try:
            portfolio_metrics = calculate_portfolio_metrics(filtered_transactions, historical_data, end_date)
        except Exception as e:
            # En cas d'erreur, retourner un tableau vide
            return []
        
        # Calculer les profits manqués
        try:
            missed_profits = calculate_missed_profit(historical_data, filtered_transactions)
        except Exception as e:
            # En cas d'erreur, créer un DataFrame vide
            missed_profits = pd.DataFrame(columns=['symbol', 'missed_profit'])
        
        # Fusionner les données
        portfolio_details = portfolio_metrics['portfolio_details'].copy()
        
        # Joindre les profits manqués
        if not missed_profits.empty and not portfolio_details.empty:
            portfolio_details = pd.merge(
                portfolio_details,
                missed_profits[['symbol', 'missed_profit']],
                on='symbol',
                how='left'
            )
            # Remplacer les valeurs NaN par 0
            portfolio_details['missed_profit'] = portfolio_details['missed_profit'].fillna(0)
        else:
            if not portfolio_details.empty:
                portfolio_details['missed_profit'] = 0
        
        # Sélectionner et renommer les colonnes
        if not portfolio_details.empty:
            table_data = portfolio_details[['symbol', 'close', 'quantity', 'missed_profit']]
            table_data = table_data.rename(columns={
                'symbol': 'Symbol',
                'close': 'Current Price',
                'quantity': 'Quantity',
                'missed_profit': 'Missed Profit'
            })
        
            # Formatage des valeurs
            table_data['Current Price'] = table_data['Current Price'].apply(lambda x: format_currency(x, ""))
            table_data['Missed Profit'] = table_data['Missed Profit'].apply(lambda x: format_currency(x))
            
            # Calcul du total
            total_row = {
                'Symbol': 'Total',
                'Current Price': format_currency(table_data['Current Price'].apply(lambda x: float(x.replace('₹', '').replace(',', ''))).sum(), ""),
                'Quantity': int(table_data['Quantity'].sum()),
                'Missed Profit': format_currency(table_data['Missed Profit'].apply(lambda x: float(x.replace('₹', '').replace(',', ''))).sum())
            }
            
            # Ajouter la ligne de total
            table_data = pd.concat([table_data, pd.DataFrame([total_row])], ignore_index=True)
            
            return table_data.to_dict('records')
        else:
            # Retourner un tableau vide
            return []