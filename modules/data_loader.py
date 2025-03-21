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
    """Charge les données historiques et les transactions"""
    try:
        # Essayer d'abord le chemin avec le dossier data/
        historical_data = pd.read_csv('data/all_historical_data.csv', sep=';', on_bad_lines='skip')
    except FileNotFoundError:
        # Sinon, essayer le chemin à la racine
        try:
            historical_data = pd.read_csv('all_historical_data.csv', sep=';', on_bad_lines='skip')
        except FileNotFoundError:
            # Créer un DataFrame vide avec la structure correcte
            historical_data = pd.DataFrame(columns=['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume'])
    except Exception as e:
        print(f"Erreur lors du chargement des données historiques: {e}")
        # Essayer avec des options plus robustes
        try:
            historical_data = pd.read_csv('data/historical_data.csv', sep=';', on_bad_lines='skip')
        except:
            # Créer un DataFrame vide avec la structure correcte
            historical_data = pd.DataFrame(columns=['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume'])
    
    # Afficher les informations sur les colonnes pour le débogage
    print(f"Colonnes disponibles dans historical_data: {historical_data.columns.tolist()}")
    print("Premières lignes de historical_data:")
    print(historical_data.head())
    
    # Vérifier et convertir les dates
    if 'Date' in historical_data.columns:
        historical_data['Date'] = pd.to_datetime(historical_data['Date'], errors='coerce')
    elif 'date' in historical_data.columns:
        historical_data['Date'] = historical_data['date']
        historical_data['Date'] = pd.to_datetime(historical_data['Date'], errors='coerce')
    else:
        print("Attention: Colonne 'Date' non trouvée dans les données historiques")
        # Créer une colonne Date vide si elle n'existe pas
        historical_data['Date'] = pd.NaT
        
    # Convertir les dates au format DD/MM/YYYY
    for col in ['date', 'Date']:
        if col in historical_data.columns:
            try:
                # Essayer de convertir les dates au format DD/MM/YYYY
                historical_data[col] = pd.to_datetime(historical_data[col], format='%d/%m/%Y', errors='coerce')
            except:
                # Si ça échoue, essayer le format par défaut
                historical_data[col] = pd.to_datetime(historical_data[col], errors='coerce')
        
    # Extraire les colonnes à partir de la première colonne si elle contient des séparateurs
    if len(historical_data.columns) > 0 and ';' in str(historical_data.columns[0]):
        # La première colonne contient probablement toutes les données
        first_col = historical_data.columns[0]
        if isinstance(first_col, str) and ';' in first_col:
            # Extraire les noms de colonnes
            col_names = first_col.split(';')
            
            # Vérifier si la première ligne contient des données
            if len(historical_data) > 0:
                # Extraire les données de la première colonne
                data_rows = []
                for _, row in historical_data.iterrows():
                    first_cell = str(row[first_col])
                    if ';' in first_cell:
                        values = first_cell.split(';')
                        data_rows.append(values)
                
                # Créer un nouveau DataFrame avec les colonnes extraites
                if data_rows:
                    new_df = pd.DataFrame(data_rows, columns=col_names)
                    
                    # Remplacer historical_data par le nouveau DataFrame
                    historical_data = new_df
                    
                    # Afficher les nouvelles colonnes
                    print(f"Nouvelles colonnes extraites: {historical_data.columns.tolist()}")
                    print("Premières lignes après extraction:")
                    print(historical_data.head())
    
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
    
    # Vérifier et convertir les dates
    if 'Date_Acquisition' in transactions_data.columns:
        transactions_data['Date_Acquisition'] = pd.to_datetime(transactions_data['Date_Acquisition'])
    elif 'purchase_date' in transactions_data.columns:
        transactions_data['Date_Acquisition'] = transactions_data['purchase_date']
        transactions_data['Date_Acquisition'] = pd.to_datetime(transactions_data['Date_Acquisition'])
    else:
        print("Attention: Colonne 'Date_Acquisition' non trouvée dans les données de transactions")
        # Créer une colonne Date_Acquisition vide si elle n'existe pas
        transactions_data['Date_Acquisition'] = pd.NaT
    
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
