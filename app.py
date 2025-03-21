import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import des modules
from modules.data_loader import load_data
from layouts.main_layout import create_layout
from callbacks.register_callbacks import register_all_callbacks

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
historical_data, transactions_data = load_data()

# À ajouter après avoir chargé historical_data
print("Colonnes disponibles dans historical_data:", historical_data.columns.tolist())
print("Premières lignes de historical_data:")
print(historical_data.head())

# Création du layout principal
app.layout = create_layout(historical_data, transactions_data)

# Enregistrement des callbacks
register_all_callbacks(app, historical_data, transactions_data)

# Point d'entrée pour l'exécution
if __name__ == "__main__":
    app.run_server(debug=True)