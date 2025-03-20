"""Chargement et préparation des données"""
import pandas as pd
import os

def standardize_historical_data(historical_data):
    """
    Standardise les noms de colonnes pour les données historiques
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
    
    Returns:
        pd.DataFrame: DataFrame avec les colonnes standardisées
    """
    return historical_data.rename(columns={
        'Date': 'date',
        'Ticker': 'symbol',
        'Close': 'close'
    })

def standardize_transactions_data(transactions_data):
    """
    Standardise les noms de colonnes pour les données de transactions
    
    Args:
        transactions_data (pd.DataFrame): Données des transactions
    
    Returns:
        pd.DataFrame: DataFrame avec les colonnes standardisées
    """
    return transactions_data.rename(columns={
        'Ticker': 'symbol',
        'Nombre_Actions': 'quantity',
        'Prix_Acquisition': 'purchase_price',
        'Date_Acquisition': 'purchase_date'
    })

def load_data():
    """Charge les données historiques et les transactions"""
    try:
        # Essayer d'abord le chemin avec le dossier data/
        historical_data = pd.read_csv('data/all_historical_data.csv')
    except FileNotFoundError:
        # Sinon, essayer le chemin à la racine
        try:
            historical_data = pd.read_csv('all_historical_data.csv')
        except FileNotFoundError:
            # Créer un DataFrame vide avec la structure correcte
            historical_data = pd.DataFrame(columns=['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume'])
    
    # Convertir les dates
    historical_data['Date'] = pd.to_datetime(historical_data['Date'])
    
    try:
        # Essayer d'abord le chemin avec le dossier data/
        transactions_data = pd.read_csv('data/transactions.csv')
    except FileNotFoundError:
        # Sinon, essayer le chemin à la racine
        try:
            transactions_data = pd.read_csv('transactions.csv')
        except FileNotFoundError:
            # Créer un DataFrame vide avec la structure correcte
            transactions_data = pd.DataFrame(columns=['Ticker', 'Nombre_Actions', 'Prix_Acquisition', 'Date_Acquisition'])
    
    # Convertir les dates
    transactions_data['Date_Acquisition'] = pd.to_datetime(transactions_data['Date_Acquisition'])
    
    return historical_data, transactions_data

def get_current_prices(historical_data, as_of_date):
    """
    Récupère les prix de clôture les plus récents pour chaque action à une date donnée
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix contenant les colonnes
            [Date, Ticker, Close]
        as_of_date (datetime): Date à laquelle récupérer les prix
    
    Returns:
        pd.DataFrame: DataFrame contenant les colonnes [symbol, close]
    """
    # Standardiser les noms de colonnes pour les données historiques
    historical_data_renamed = standardize_historical_data(historical_data)
    
    # Filtrer les données jusqu'à la date spécifiée
    filtered_data = historical_data_renamed[historical_data_renamed['date'] <= as_of_date]
    
    # Si filtered_data est vide, retourner un DataFrame vide
    if filtered_data.empty:
        return pd.DataFrame(columns=['symbol', 'close'])
    
    # Obtenir le prix le plus récent pour chaque action
    latest_prices = filtered_data.sort_values('date').groupby('symbol').last().reset_index()
    
    # Sélectionner uniquement les colonnes nécessaires
    return latest_prices[['symbol', 'close']]


def calculate_portfolio_value(historical_data, transactions_data, as_of_date=None):
    """
    Calcule la valeur du portefeuille à une date donnée
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
        transactions_data (pd.DataFrame): Données des transactions
        as_of_date (datetime, optional): Date à laquelle calculer la valeur.
            Si non spécifié, utilise la date la plus récente disponible.
    
    Returns:
        float: Valeur totale du portefeuille
    """
    # Standardiser les noms de colonnes pour les transactions
    transactions_renamed = standardize_transactions_data(transactions_data)
    
    # Calculer l'investissement total par action
    transactions_renamed['total_investment'] = transactions_renamed['quantity'] * transactions_renamed['purchase_price']
    
    # Si as_of_date n'est pas spécifié, utiliser la date la plus récente
    if as_of_date is None:
        historical_data_renamed = standardize_historical_data(historical_data)
        as_of_date = historical_data_renamed['date'].max()
    
    # Récupérer les prix actuels
    current_prices = get_current_prices(historical_data, as_of_date)
    
    # Filtrer les transactions jusqu'à la date spécifiée
    filtered_transactions = transactions_renamed[transactions_renamed['purchase_date'] <= as_of_date]
    
    # Si filtered_transactions est vide, retourner 0
    if filtered_transactions.empty:
        return 0.0
    
    # Agréger les transactions par symbole
    portfolio = filtered_transactions.groupby('symbol').agg({
        'quantity': 'sum',
        'total_investment': 'sum'
    }).reset_index()
    
    # Fusionner avec les prix actuels
    portfolio = pd.merge(portfolio, current_prices, on='symbol', how='left')
    
    # Si portfolio est vide après la fusion, retourner 0
    if portfolio.empty:
        return 0.0
    
    # Remplacer les valeurs NaN par 0
    portfolio['close'] = portfolio['close'].fillna(0)
    
    # Calculer la valeur actuelle
    portfolio['current_value'] = portfolio['quantity'] * portfolio['close']
    
    # Calculer la valeur totale du portefeuille
    total_value = portfolio['current_value'].sum()
    
    return total_value

def get_missed_profits(historical_data, transactions_data):
    """
    Calcule les profits manqués en raison de ventes prématurées
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
        transactions_data (pd.DataFrame): Données des transactions
    
    Returns:
        pd.DataFrame: DataFrame contenant les profits manqués par action
    """
    from modules.performance import calculate_missed_profit
    return calculate_missed_profit(historical_data, transactions_data)