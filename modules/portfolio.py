"""
Module pour les calculs relatifs au portefeuille
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from modules.data_loader import get_current_prices

def calculate_portfolio_metrics(transactions_data, historical_data, as_of_date=None):
    """
    Calcule les métriques principales du portefeuille incluant la valeur actuelle,
    le profit/perte total et le pourcentage de rendement.
    
    Args:
        transactions_data (pd.DataFrame): Données des transactions contenant les colonnes
            [symbol, quantity, total_investment, purchase_date]
        historical_data (pd.DataFrame): Données historiques des prix contenant les colonnes
            [date, symbol, close]
        as_of_date (datetime, optional): Date à laquelle calculer les métriques.
            Si non spécifié, utilise la date la plus récente disponible.
    
    Returns:
        dict: Métriques du portefeuille contenant:
            - total_value: Valeur totale actuelle du portefeuille
            - total_investment: Montant total investi
            - total_profit_loss: Profit ou perte total
            - total_profit_loss_percent: Pourcentage de rendement
            - portfolio_details: DataFrame avec les métriques par action
    """
    # Si as_of_date n'est pas spécifié, utiliser la date la plus récente
    if as_of_date is None:
        # Standardiser les noms de colonnes pour les données historiques
        from modules.data_loader import standardize_historical_data
        historical_data_renamed = standardize_historical_data(historical_data)
        as_of_date = historical_data_renamed['date'].max()
    
    # Récupérer les prix actuels
    current_prices = get_current_prices(historical_data, as_of_date)
    
    # Standardiser les noms de colonnes pour les transactions
    from modules.data_loader import standardize_transactions_data
    transactions_renamed = standardize_transactions_data(transactions_data)
    
    # Calculer l'investissement total par action
    transactions_renamed['total_investment'] = transactions_renamed['quantity'] * transactions_renamed['purchase_price']
    
    # Agréger les transactions par symbole
    portfolio = transactions_renamed.groupby('symbol').agg({
        'quantity': 'sum',
        'total_investment': 'sum'
    }).reset_index()
    
    # Calculer le prix d'achat moyen
    portfolio['avg_purchase_price'] = portfolio['total_investment'] / portfolio['quantity']
    
    # Fusionner avec les prix actuels
    portfolio = pd.merge(portfolio, current_prices, on='symbol', how='left')
    
    # Calculer la valeur actuelle et le profit/perte
    portfolio['current_value'] = portfolio['quantity'] * portfolio['close']
    portfolio['profit_loss'] = portfolio['current_value'] - portfolio['total_investment']
    portfolio['profit_loss_percent'] = (portfolio['profit_loss'] / portfolio['total_investment']) * 100
    
    # Calculer la valeur totale du portefeuille
    total_value = portfolio['current_value'].sum()
    total_investment = portfolio['total_investment'].sum()
    total_profit_loss = portfolio['profit_loss'].sum()
    total_profit_loss_percent = (total_profit_loss / total_investment) * 100 if total_investment > 0 else 0
    
    # Calculer le nombre de transactions
    num_transactions = len(transactions_data)
    
    # Calculer le montant moyen par transaction
    avg_transaction_amount = total_investment / num_transactions if num_transactions > 0 else 0
    
    # Résultats
    metrics = {
        'total_value': total_value,
        'total_investment': total_investment,
        'total_profit_loss': total_profit_loss,
        'total_profit_loss_percent': total_profit_loss_percent,
        'num_transactions': num_transactions,
        'avg_transaction_amount': avg_transaction_amount,
        'portfolio_details': portfolio
    }
    
    return metrics

def calculate_monthly_change(transactions_data, historical_data, months=1):
    """
    Calcule le changement de valeur du portefeuille sur une période de X mois
    
    Args:
        transactions_data (pd.DataFrame): Données des transactions
        historical_data (pd.DataFrame): Données historiques des prix
        months (int): Nombre de mois à considérer
    
    Returns:
        tuple: (changement_valeur, changement_pourcentage)
    """
    # Date actuelle (dernière date disponible dans les données)
    # Standardiser les noms de colonnes pour les données historiques
    from modules.data_loader import standardize_historical_data
    historical_data_renamed = standardize_historical_data(historical_data)
    current_date = historical_data_renamed['date'].max()
    
    # Date il y a X mois
    past_date = current_date - pd.DateOffset(months=months)
    
    # Filtrer les transactions pour n'inclure que celles avant past_date
    past_transactions = transactions_data[transactions_data['purchase_date'] <= past_date]
    
    if past_transactions.empty:
        return 0, 0
    
    # Calculer la valeur du portefeuille à la date actuelle
    current_metrics = calculate_portfolio_metrics(transactions_data, historical_data, current_date)
    current_value = current_metrics['total_value']
    
    # Calculer la valeur du portefeuille il y a X mois
    past_metrics = calculate_portfolio_metrics(past_transactions, historical_data, past_date)
    past_value = past_metrics['total_value']
    
    # Calculer le changement
    value_change = current_value - past_value
    percent_change = (value_change / past_value) * 100 if past_value > 0 else 0
    
    return value_change, percent_change

def calculate_best_worst_performers(transactions_data, historical_data, period='1Y'):
    """
    Identifie les meilleures et pires performances dans le portefeuille
    
    Args:
        transactions_data (pd.DataFrame): Données des transactions
        historical_data (pd.DataFrame): Données historiques des prix
        period (str): Période d'analyse ('1Y', '6M', 'MTD', 'YTD', 'Last 60 Days')
    
    Returns:
        tuple: (meilleur_performer, pire_performer)
    """
    # Date actuelle (dernière date disponible dans les données)
    # Standardiser les noms de colonnes pour les données historiques
    from modules.data_loader import standardize_historical_data
    historical_data_renamed = standardize_historical_data(historical_data)
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
    
    # Filtrer les données historiques pour la période
    period_data = historical_data[(historical_data['date'] >= start_date) & 
                                 (historical_data['date'] <= current_date)]
    
    # Calculer le rendement pour chaque symbole
    symbols = transactions_data['symbol'].unique()
    performance = []
    
    for symbol in symbols:
        symbol_data = period_data[period_data['symbol'] == symbol]
        
        if len(symbol_data) >= 2:
            start_price = symbol_data.iloc[0]['close']
            end_price = symbol_data.iloc[-1]['close']
            
            percent_change = ((end_price - start_price) / start_price) * 100
            
            performance.append({
                'symbol': symbol,
                'return': percent_change
            })
    
    if not performance:
        return {'symbol': 'N/A', 'return': 0}, {'symbol': 'N/A', 'return': 0}
    
    # Trier par rendement
    performance_df = pd.DataFrame(performance)
    
    best_performer = performance_df.loc[performance_df['return'].idxmax()]
    worst_performer = performance_df.loc[performance_df['return'].idxmin()]
    
    return best_performer.to_dict(), worst_performer.to_dict()

def calculate_index_performance(historical_data, index_symbol, period='1Y'):
    """
    Calcule la performance d'un indice sur une période donnée
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
        index_symbol (str): Symbole de l'indice (ex: '^NSEI' pour Nifty)
        period (str): Période d'analyse ('1Y', '6M', 'MTD', 'YTD', 'Last 60 Days')
    
    Returns:
        float: Performance en pourcentage
    """
    # Date actuelle (dernière date disponible dans les données)
    # Standardiser les noms de colonnes pour les données historiques
    from modules.data_loader import standardize_historical_data
    historical_data_renamed = standardize_historical_data(historical_data)
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
    
    # Filtrer les données pour l'indice
    index_data = historical_data[(historical_data['symbol'] == index_symbol) & 
                                (historical_data['date'] >= start_date) & 
                                (historical_data['date'] <= current_date)]
    
    if len(index_data) < 2:
        return 0
    
    # Calculer le rendement
    start_value = index_data.iloc[0]['close']
    end_value = index_data.iloc[-1]['close']
    
    percent_change = ((end_value - start_value) / start_value) * 100
    
    return percent_change