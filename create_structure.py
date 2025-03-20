import os
import pathlib

def create_structure(base_path="E:\\Dash_Claude"):
    """Crée la structure de dossiers et fichiers décrite dans Structure.txt"""
    
    # Assurer que le chemin de base existe
    os.makedirs(base_path, exist_ok=True)
    
    # Structure de fichiers et dossiers à créer
    structure = {
        "app.py": "# Point d'entrée principal de l'application\n",
        "config.py": "# Configuration (chemins des fichiers, paramètres, etc.)\n",
        "data": {
            "all_historical_data.csv": "",
            "transactions.csv": "Ticker,Nombre_Actions,Prix_Acquisition,Date_Acquisition\n",
            "processed": {}
        },
        "assets": {
            "styles.css": "/* Styles CSS de l'application */\n",
            "logo.png": None  # Marqueur pour un fichier binaire
        },
        "components": {
            "__init__.py": "",
            "header.py": "# En-tête avec logo et titre\n",
            "date_selector.py": "# Sélecteur de plage de dates\n",
            "summary_cards.py": "# Cartes récapitulatives (Nifty, Profit, Valeur actuelle, Rendements)\n",
            "portfolio_table.py": "# Tableau détaillé du portefeuille\n",
            "performance_chart.py": "# Graphique de performance\n",
            "tabs.py": "# Onglets pour la navigation\n"
        },
        "modules": {
            "__init__.py": "",
            "data_loader.py": "# Chargement et préparation des données\n",
            "portfolio.py": "# Calculs relatifs au portefeuille\n",
            "performance.py": "# Calculs de performance\n",
            "utils.py": "# Fonctions utilitaires\n"
        },
        "layouts": {
            "__init__.py": "",
            "main_layout.py": "# Mise en page principale\n",
            "portfolio_value.py": "# Page de valeur du portefeuille\n",
            "portfolio_breakdown.py": "# Page de répartition du portefeuille\n",
            "missed_profit.py": "# Page des profits manqués\n",
            "buy_high_sell_low.py": "# Page stratégie d'achat/vente\n"
        },
        "callbacks": {
            "__init__.py": "",
            "date_callbacks.py": "# Callbacks pour les sélecteurs de date\n",
            "portfolio_callbacks.py": "# Callbacks pour les tables et graphiques du portefeuille\n",
            "tab_callbacks.py": "# Callbacks pour la navigation entre les onglets\n"
        }
    }
    
    def create_entry(current_path, name, entry):
        """Crée récursivement les dossiers et fichiers selon la structure définie"""
        full_path = os.path.join(current_path, name)
        
        if isinstance(entry, dict):
            # C'est un dossier avec des sous-éléments
            os.makedirs(full_path, exist_ok=True)
            for sub_name, sub_entry in entry.items():
                create_entry(full_path, sub_name, sub_entry)
        elif entry is None:
            # C'est un fichier binaire (comme une image), on le crée vide
            if not os.path.exists(full_path):
                with open(full_path, 'wb') as f:
                    pass  # Créer un fichier binaire vide
        else:
            # C'est un fichier texte avec contenu
            if not os.path.exists(full_path):
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(entry)
    
    # Créer la structure
    for name, entry in structure.items():
        create_entry(base_path, name, entry)
    
    print(f"Structure créée avec succès dans {base_path}")
    
    # Ajouter des données exemple dans transactions.csv
    transactions_path = os.path.join(base_path, "data", "transactions.csv")
    sample_data = """Ticker,Nombre_Actions,Prix_Acquisition,Date_Acquisition
AKT,5,1048.00,2024-10-02
AKT,3,1180.00,2025-02-11
MNG,3,2850.00,2024-11-13
JET,5,1365.00,2024-10-07
JET,5,1900.00,2024-12-12
MSA,8,579.00,2025-10-07
TQM,5,1487.00,2025-02-11
TGC,10,417.00,2024-10-02
TGC,5,537.00,2025-01-22
IAM,20,114.90,2025-02-26
"""
    with open(transactions_path, 'w', encoding='utf-8') as f:
        f.write(sample_data)
    
    # Créer un fichier app.py avec un contenu basique
    app_content = """# Point d'entrée principal de l'application Dash
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.main_layout import create_layout

# Initialiser l'application Dash
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)

# Configurer le titre de l'application
app.title = "Tableau de bord du Portefeuille"

# Créer la mise en page principale
app.layout = create_layout()

# Import des callbacks après la création de la mise en page
from callbacks.date_callbacks import register_callbacks as register_date_callbacks
from callbacks.portfolio_callbacks import register_callbacks as register_portfolio_callbacks
from callbacks.tab_callbacks import register_callbacks as register_tab_callbacks

# Enregistrer les callbacks
register_date_callbacks(app)
register_portfolio_callbacks(app)
register_tab_callbacks(app)

# Point d'entrée principal
if __name__ == "__main__":
    app.run_server(debug=True)
"""
    
    with open(os.path.join(base_path, "app.py"), 'w', encoding='utf-8') as f:
        f.write(app_content)
    
    # Créer un contenu de base pour modules/data_loader.py
    data_loader_content = """# Chargement et préparation des données
import pandas as pd
import os
from config import DATA_DIR

def load_transactions():
    # Charge les données de transactions depuis transactions.csv
    transactions_path = os.path.join(DATA_DIR, 'transactions.csv')
    if os.path.exists(transactions_path):
        df = pd.read_csv(transactions_path)
        # Convertir la colonne de date en datetime
        df['Date_Acquisition'] = pd.to_datetime(df['Date_Acquisition'])
        # Ajouter une colonne 'Type' par défaut à 'achat'
        if 'Type' not in df.columns:
            df['Type'] = 'achat'
        # Ajouter un ID unique si non présent
        if 'id' not in df.columns:
            df['id'] = range(1, len(df) + 1)
        return df
    else:
        # Retourner un DataFrame vide avec les colonnes attendues
        return pd.DataFrame(columns=['id', 'Ticker', 'Nombre_Actions', 'Prix_Acquisition', 'Date_Acquisition', 'Type'])

def load_historical_data():
    # Charge les données historiques des actions
    hist_data_path = os.path.join(DATA_DIR, 'all_historical_data.csv')
    if os.path.exists(hist_data_path):
        df = pd.read_csv(hist_data_path)
        # Convertir la colonne de date en datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        # Retourner un DataFrame vide avec les colonnes attendues
        return pd.DataFrame(columns=['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume'])
"""
    
    with open(os.path.join(base_path, "modules", "data_loader.py"), 'w', encoding='utf-8') as f:
        f.write(data_loader_content)
    
    # Créer un contenu de base pour config.py
    config_content = """# Configuration de l'application
import os

# Chemins des dossiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# S'assurer que les dossiers existent
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Paramètres de l'application
APP_TITLE = "Tableau de bord du Portefeuille"
DEFAULT_TICKER = "All"  # Ticker par défaut pour les filtres
DATE_FORMAT = "%Y-%m-%d"  # Format de date

# Couleurs du thème
COLORS = {
    'primary': '#3a86ff',
    'secondary': '#8338ec',
    'accent': '#ff006e',
    'light': '#f8f9fa',
    'dark': '#212529',
    'success': '#38b000',
    'danger': '#e63946',
    'warning': '#ffb703',
}
"""
    
    with open(os.path.join(base_path, "config.py"), 'w', encoding='utf-8') as f:
        f.write(config_content)

if __name__ == "__main__":
    create_structure()