"""
Configuration de l'application
"""
import os

# Chemin de base de l'application
BASE_PATH = "E:\\Dash_Claude"

# Chemins des fichiers de données
DATA_PATH = os.path.join(BASE_PATH, "data")
HISTORICAL_DATA_PATH = os.path.join(DATA_PATH, "all_historical_data.csv")
TRANSACTIONS_DATA_PATH = os.path.join(DATA_PATH, "transactions.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_PATH, "processed")

# Créer le dossier processed s'il n'existe pas
if not os.path.exists(PROCESSED_DATA_PATH):
    os.makedirs(PROCESSED_DATA_PATH)

# Configuration des couleurs de l'application
COLORS = {
    "background": "#1E1E1E",
    "card_background": "#333333",
    "text": "#FFFFFF",
    "accent": "#00CED1",  # Cyan
    "positive": "#00FF7F",  # Vert
    "negative": "#FF4500",  # Rouge
    "neutral": "#808080",   # Gris
}

# Configuration des périodes disponibles
TIME_PERIODS = {
    "1Y": 365,
    "6M": 180,
    "Last 60 Days": 60,
    "MTD": 30,  # Month to date
    "YTD": 0,   # Year to date (calculé dynamiquement)
}

# Configuration des indices de référence
INDICES = {
    "MASI": "^MASI",
}

# Configuration des styles communs
CARD_STYLE = {
    "background-color": COLORS["card_background"],
    "border-radius": "10px",
    "padding": "15px",
    "margin": "10px",
    "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
}

HEADER_STYLE = {
    "color": COLORS["accent"],
    "font-weight": "bold",
    "margin-bottom": "10px",
}

VALUE_STYLE = {
    "font-size": "28px",
    "font-weight": "bold",
    "margin": "10px 0",
}

CHANGE_POSITIVE_STYLE = {
    "color": COLORS["positive"],
    "font-weight": "bold",
}

CHANGE_NEGATIVE_STYLE = {
    "color": COLORS["negative"],
    "font-weight": "bold",
}
