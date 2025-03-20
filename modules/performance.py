"""
Module pour les calculs de performance
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from modules.data_loader import standardize_historical_data, standardize_transactions_data

def calculate_comparative_performance(historical_data, transactions_data, benchmark_symbol='^NSEI', period='1Y'):
    """
    Calcule la performance comparative entre le portefeuille et un indice de référence
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
        transactions_data (pd.DataFrame): Données des transactions
        benchmark_symbol (str): Symbole de l'indice de référence
        period (str): Période d'analyse ('1Y', '6M', 'MTD', 'YTD', 'Last 60 Days')
    
    Returns:
        pd.DataFrame: DataFrame contenant les performances jour par jour
    """
    # Standardiser les noms de colonnes
    historical_data_renamed = standardize_historical_data(historical_data)
    transactions_renamed = standardize_transactions_data(transactions_data)
    
    # Date actuelle (dernière date disponible dans les données)
    current_date = historical_data_renamed['date'].max()
    
    # Déterminer la date de début selon la période
    if period == '1Y':
        start_date = current_date - pd.DateOffset(years=1)
    elif period == '6M':
        start_date = current_date - pd.DateOffset(months=6)
    elif period == 'MTD':
        start_date = current_date.replace(day=1)
    elif period == 'YTD':
        start_date = current_date.replace(month=1, day=1)
    elif period == 'Last 60 Days':
        start_date = current_date - pd.DateOffset(days=60)
    else:
        start_date = current_date - pd.DateOffset(years=1)  # Par défaut 1 an
    
    # Filtrer les données pour la période
    period_data = historical_data_renamed[(historical_data_renamed['date'] >= start_date) & 
                                        (historical_data_renamed['date'] <= current_date)]
    
    # Filtrer les données de l'indice de référence
    benchmark_data = period_data[period_data['symbol'] == benchmark_symbol]
    
    if benchmark_data.empty:
        return pd.DataFrame()  # Retourner un DataFrame vide si pas de données d'indice
    
    # Préparer les données pour le calcul du rendement du portefeuille
    unique_dates = sorted(period_data['date'].unique())
    dates_with_values = []
    portfolio_returns = []
    benchmark_returns = []
    
    # Recalculer la valeur du portefeuille pour chaque date
    for date in unique_dates:
        # Filtrer les transactions jusqu'à cette date
        transactions_at_date = transactions_renamed[transactions_renamed['purchase_date'] <= date]
        
        if not transactions_at_date.empty:
            # Calculer la valeur initiale du portefeuille
            portfolio_value_initial = transactions_at_date['quantity'].sum() * transactions_at_date['purchase_price'].mean()
            
            # Obtenir les prix actuels
            current_prices = period_data[(period_data['date'] == date)]
            
            # Fusionner avec les transactions
            portfolio_df = pd.merge(
                transactions_at_date,
                current_prices[['symbol', 'close', 'date']],
                on='symbol',
                how='inner'
            )
            
            # Calculer la valeur actuelle
            if not portfolio_df.empty:
                portfolio_value_current = (portfolio_df['quantity'] * portfolio_df['close']).sum()
                
                # Calculer le rendement du portefeuille
                portfolio_return = ((portfolio_value_current / portfolio_value_initial) - 1) * 100
                
                # Obtenir le rendement de l'indice
                benchmark_value = benchmark_data[benchmark_data['date'] == date]['close'].values
                if len(benchmark_value) > 0:
                    benchmark_initial = benchmark_data['close'].iloc[0]
                    benchmark_return = ((benchmark_value[0] / benchmark_initial) - 1) * 100
                    
                    # Enregistrer les rendements
                    dates_with_values.append(date)
                    portfolio_returns.append(portfolio_return)
                    benchmark_returns.append(benchmark_return)
    
    # Créer le DataFrame final
    if len(dates_with_values) > 0:
        performance_df = pd.DataFrame({
            'date': dates_with_values,
            'cumulative_portfolio_return': portfolio_returns,
            'cumulative_benchmark_return': benchmark_returns
        })
        
        return performance_df
    else:
        return pd.DataFrame()

def calculate_missed_profit(historical_data, transactions_data):
    """
    Calcule les profits manqués en raison de ventes prématurées
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
        transactions_data (pd.DataFrame): Données des transactions
    
    Returns:
        pd.DataFrame: DataFrame contenant les profits manqués par action
    """
    # Standardiser les noms de colonnes
    historical_data_renamed = standardize_historical_data(historical_data)
    transactions_renamed = standardize_transactions_data(transactions_data)
    
    # Date actuelle (dernière date disponible dans les données)
    current_date = historical_data_renamed['date'].max()
    
    # Récupérer les prix actuels
    latest_prices = historical_data_renamed.sort_values('date').groupby('symbol').last().reset_index()
    
    # Identifier les actions vendues (si le type de transaction est disponible)
    if 'Type' in transactions_renamed.columns:
        sold_stocks = transactions_renamed[transactions_renamed['Type'] == 'vente']
    else:
        # Si le type n'est pas disponible, on suppose qu'il n'y a pas de ventes
        # On crée un DataFrame vide avec les bonnes colonnes
        return pd.DataFrame(columns=['symbol', 'quantity_sold', 'sell_price', 'current_price', 'missed_profit'])
    
    if sold_stocks.empty:
        return pd.DataFrame(columns=['symbol', 'quantity_sold', 'sell_price', 'current_price', 'missed_profit'])
    
    # Agréger les ventes par symbole
    sold_summary = sold_stocks.groupby('symbol').agg({
        'quantity': 'sum',
        'purchase_price': 'mean'  # Prix de vente moyen
    }).reset_index()
    
    # Renommer les colonnes pour plus de clarté
    sold_summary = sold_summary.rename(columns={
        'quantity': 'quantity_sold',
        'purchase_price': 'sell_price'
    })
    
    # Fusionner avec les prix actuels
    missed_profits = pd.merge(
        sold_summary,
        latest_prices[['symbol', 'close']],
        on='symbol',
        how='left'
    )
    
    # Calculer le profit manqué
    missed_profits['missed_profit'] = missed_profits['quantity_sold'] * (missed_profits['close'] - missed_profits['sell_price'])
    
    # Sélectionner uniquement les actions avec un profit manqué positif
    missed_profits = missed_profits[missed_profits['missed_profit'] > 0]
    
    # Renommer pour plus de clarté
    missed_profits = missed_profits.rename(columns={
        'close': 'current_price'
    })
    
    return missed_profits