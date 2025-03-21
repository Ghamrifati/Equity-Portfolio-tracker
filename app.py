import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import sys

# Vérification de la structure du projet
required_folders = ['modules', 'layouts', 'callbacks']
for folder in required_folders:
    folder_path = os.path.join(os.path.dirname(__file__), folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Dossier créé: {folder}")

# Import des modules
try:
    from modules.data_loader import load_data
    from layouts.main_layout import create_layout
    from callbacks.register_callbacks import register_all_callbacks
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    print("Création des fichiers manquants...")
    # Création des fichiers manquants si nécessaire
    sys.exit(1)

# Initialisation de l'application Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],  # Utilisation d'un thème sombre
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# Configuration du titre
app.title = "Equity Portfolio Tracker"

# Chargement des données
try:
    historical_data, transactions_data = load_data()
    
    # Informations de débogage
    print("Colonnes disponibles dans historical_data:", historical_data.columns.tolist())
    print("Premières lignes de historical_data:")
    print(historical_data.head())
except Exception as e:
    print(f"Erreur lors du chargement des données: {e}")
    import pandas as pd
    historical_data = pd.DataFrame()
    transactions_data = pd.DataFrame()

# Création du layout principal
app.layout = create_layout(historical_data, transactions_data)

# Enregistrement des callbacks
register_all_callbacks(app, historical_data, transactions_data)

# Point d'entrée pour l'exécution
if __name__ == "__main__":
    app.run(debug=True)  # Changed from app.run_server to app.run