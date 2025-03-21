"""Chargement et préparation des données"""
import pandas as pd
import os
import yfinance as yf
from datetime import datetime, timedelta

def standardize_historical_data(historical_data):
    """
    Standardise les noms de colonnes pour les données historiques
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
    
    Returns:
        pd.DataFrame: DataFrame avec les colonnes standardisées
    """
    # Créer une copie pour éviter de modifier l'original
    df = historical_data.copy()
    
    # Réinitialiser l'index pour éviter les problèmes d'index dupliqués
    df = df.reset_index(drop=True)
    
    # Supprimer les doublons éventuels
    if 'symbol' in df.columns and 'date' in df.columns:
        df = df.drop_duplicates(subset=['symbol', 'date'])
    
    # Afficher les colonnes disponibles pour le débogage
    print(f"Colonnes dans standardize_historical_data: {df.columns.tolist()}")
    
    # Vérifier et renommer les colonnes si elles existent
    rename_dict = {}
    
    # Mappings standard
    column_mappings = {
        'Date': 'date',
        'date': 'date',
        'Ticker': 'symbol',
        'symbol': 'symbol',
        'Close': 'close',
        'close': 'close',
        'adjusted_close': 'close'
    }
    
    # Appliquer les mappings
    for old_col, new_col in column_mappings.items():
        if old_col in df.columns:
            rename_dict[old_col] = new_col
    
    # Renommer les colonnes existantes
    df = df.rename(columns=rename_dict)
    
    # S'assurer que les colonnes requises existent
    if 'date' not in df.columns:
        print("Attention: Colonne 'date' non trouvée dans les données historiques")
        df['date'] = pd.NaT
        
    if 'symbol' not in df.columns:
        print("Attention: Colonne 'symbol' non trouvée dans les données historiques")
        # Essayer de trouver une colonne qui pourrait contenir le symbole
        if any('symbol' in col.lower() for col in df.columns):
            symbol_col = next(col for col in df.columns if 'symbol' in col.lower())
            df['symbol'] = df[symbol_col]
        else:
            df['symbol'] = ''
        
    if 'close' not in df.columns:
        print("Attention: Colonne 'close' non trouvée dans les données historiques")
        # Essayer de trouver une colonne qui pourrait contenir le prix de clôture
        if any('close' in col.lower() for col in df.columns):
            close_col = next(col for col in df.columns if 'close' in col.lower())
            try:
                df['close'] = pd.to_numeric(df[close_col], errors='coerce')
            except TypeError:
                print(f"Erreur lors de la conversion de la colonne {close_col} en numérique")
                df['close'] = 0.0
        else:
            df['close'] = 0.0
    else:
        # Convertir la colonne close en numérique
        try:
            df['close'] = pd.to_numeric(df['close'], errors='coerce')
        except TypeError:
            print("Erreur lors de la conversion de la colonne 'close' en numérique")
            # Vérifier le type de la colonne close
            print(f"Type de la colonne 'close': {type(df['close'])}")
            # Si c'est un objet, essayer de le convertir en liste puis en série
            if isinstance(df['close'], object):
                try:
                    close_values = list(df['close'])
                    df['close'] = pd.Series(close_values, index=df.index)
                    df['close'] = pd.to_numeric(df['close'], errors='coerce')
                except:
                    df['close'] = 0.0
            else:
                df['close'] = 0.0
    
    return df

def standardize_transactions_data(transactions_data):
    """
    Standardise les noms de colonnes pour les données de transactions
    
    Args:
        transactions_data (pd.DataFrame): Données des transactions
    
    Returns:
        pd.DataFrame: DataFrame avec les colonnes standardisées
    """
    # Créer une copie pour éviter de modifier l'original
    df = transactions_data.copy()
    
    # Vérifier et renommer les colonnes si elles existent
    rename_dict = {}
    if 'Ticker' in df.columns:
        rename_dict['Ticker'] = 'symbol'
    if 'Nombre_Actions' in df.columns:
        rename_dict['Nombre_Actions'] = 'quantity'
    if 'Prix_Acquisition' in df.columns:
        rename_dict['Prix_Acquisition'] = 'purchase_price'
    if 'Date_Acquisition' in df.columns:
        rename_dict['Date_Acquisition'] = 'purchase_date'
    
    # Renommer les colonnes existantes
    df = df.rename(columns=rename_dict)
    
    # S'assurer que les colonnes requises existent
    if 'symbol' not in df.columns:
        print("Attention: Colonne 'symbol' non trouvée dans les données de transactions")
        df['symbol'] = ''
        
    if 'quantity' not in df.columns:
        print("Attention: Colonne 'quantity' non trouvée dans les données de transactions")
        df['quantity'] = 0
        
    if 'purchase_price' not in df.columns:
        print("Attention: Colonne 'purchase_price' non trouvée dans les données de transactions")
        df['purchase_price'] = 0.0
        
    if 'purchase_date' not in df.columns:
        print("Attention: Colonne 'purchase_date' non trouvée dans les données de transactions")
        df['purchase_date'] = pd.NaT
    
    return df

def load_data():
    """
    Charge les données historiques et les transactions de la Bourse de Casablanca
    
    Returns:
        tuple: (historical_data, transactions_data)
    """
    # Chemins des fichiers de données
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    # Vérifier que le dossier data existe
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Dossier data créé: {data_dir}")
        return pd.DataFrame(), pd.DataFrame()
    
    # Lister tous les fichiers CSV dans le dossier data
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("Aucun fichier CSV trouvé dans le dossier data.")
        return pd.DataFrame(), pd.DataFrame()
    
    print(f"Fichiers CSV trouvés: {csv_files}")
    
    # Charger les données historiques
    historical_file = os.path.join(data_dir, 'historical_data.csv')
    if os.path.exists(historical_file):
        try:
            print(f"Chargement des données historiques depuis historical_data.csv")
            # Utiliser sep=';' pour les fichiers CSV avec séparateur point-virgule
            historical_data = pd.read_csv(historical_file, sep=';')
            
            # Convertir la colonne Date en datetime
            if 'Date' in historical_data.columns:
                historical_data['Date'] = pd.to_datetime(historical_data['Date'], format='%d/%m/%Y', errors='coerce')
            
            print(f"Données historiques chargées: {len(historical_data)} lignes, {historical_data['Symbol'].nunique()} symboles")
        except Exception as e:
            print(f"Erreur lors du chargement de historical_data.csv: {e}")
            historical_data = pd.DataFrame()
    else:
        print("Fichier historical_data.csv non trouvé")
        historical_data = pd.DataFrame()
    
    # Charger les données de transactions
    transactions_file = os.path.join(data_dir, 'transactions.csv')
    if os.path.exists(transactions_file):
        try:
            print(f"Chargement des transactions depuis transactions.csv")
            # Utiliser sep=';' pour les fichiers CSV avec séparateur point-virgule
            transactions_data = pd.read_csv(transactions_file, sep=';')
            
            # Convertir la colonne Date en datetime
            if 'Date' in transactions_data.columns:
                transactions_data['Date'] = pd.to_datetime(transactions_data['Date'], format='%d/%m/%Y', errors='coerce')
            
            print(f"Transactions chargées: {len(transactions_data)} lignes")
        except Exception as e:
            print(f"Erreur lors du chargement de transactions.csv: {e}")
            transactions_data = pd.DataFrame()
    else:
        print("Fichier transactions.csv non trouvé")
        transactions_data = pd.DataFrame()
    
    return historical_data, transactions_data

def standardize_transaction_type(type_str):
    """
    Standardise les types de transactions en BUY ou SELL
    
    Args:
        type_str: Type de transaction original
        
    Returns:
        str: 'BUY' ou 'SELL'
    """
    if not isinstance(type_str, str):
        return 'BUY'  # Valeur par défaut
    
    type_lower = type_str.lower()
    
    if 'buy' in type_lower or 'achat' in type_lower or 'acheter' in type_lower:
        return 'BUY'
    elif 'sell' in type_lower or 'vente' in type_lower or 'vendre' in type_lower:
        return 'SELL'
    else:
        return 'BUY'  # Valeur par défaut

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
    try:
        # Standardiser les noms de colonnes pour les données historiques
        historical_data_renamed = standardize_historical_data(historical_data)
        
        # Réinitialiser l'index pour éviter les problèmes d'index dupliqués
        historical_data_renamed = historical_data_renamed.reset_index(drop=True)
        
        # Supprimer les doublons éventuels
        if 'symbol' in historical_data_renamed.columns and 'date' in historical_data_renamed.columns:
            historical_data_renamed = historical_data_renamed.drop_duplicates(subset=['symbol', 'date'])
        
        # Vérifier si la colonne 'date' est de type datetime
        if 'date' in historical_data_renamed.columns and not pd.api.types.is_datetime64_any_dtype(historical_data_renamed['date']):
            historical_data_renamed['date'] = pd.to_datetime(historical_data_renamed['date'], errors='coerce')
        
        # Vérifier si as_of_date est de type datetime
        if not isinstance(as_of_date, pd.Timestamp) and not isinstance(as_of_date, pd.DatetimeIndex):
            as_of_date = pd.to_datetime(as_of_date, errors='coerce')
        
        # Créer une méthode alternative pour filtrer les données
        filtered_data = historical_data_renamed.copy()
        filtered_data = filtered_data[filtered_data['date'].notna()]
        filtered_data = filtered_data[filtered_data['date'] <= as_of_date]
        
        # Si filtered_data est vide, retourner un DataFrame vide
        if filtered_data.empty:
            print("Aucune donnée trouvée pour la date spécifiée")
            return pd.DataFrame(columns=['symbol', 'close'])
        
        # Obtenir le prix le plus récent pour chaque action
        # Utiliser une méthode plus robuste pour le groupby
        latest_prices = filtered_data.sort_values('date')
        
        # Créer un DataFrame pour stocker les résultats
        result = []
        for symbol in filtered_data['symbol'].unique():
            symbol_data = filtered_data[filtered_data['symbol'] == symbol]
            if not symbol_data.empty:
                latest_row = symbol_data.iloc[-1]
                result.append({
                    'symbol': symbol,
                    'close': latest_row['close']
                })
        
        # Convertir la liste en DataFrame
        latest_prices = pd.DataFrame(result)
        
        # Si latest_prices est vide, retourner un DataFrame vide
        if latest_prices.empty:
            print("Aucun prix récent trouvé")
            return pd.DataFrame(columns=['symbol', 'close'])
        
        return latest_prices
    
    except Exception as e:
        print(f"Erreur dans get_current_prices: {e}")
        # En cas d'erreur, retourner un DataFrame vide
        return pd.DataFrame(columns=['symbol', 'close'])


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
