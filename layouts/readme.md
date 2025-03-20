# Equity Portfolio Tracker

Une application web modulaire pour suivre et analyser un portefeuille d'actions, inspirée du design présenté dans l'image de référence.

## Fonctionnalités

- Suivi de la valeur du portefeuille en temps réel
- Analyse des performances par rapport à des indices (Nifty)
- Calcul des profits et pertes
- Analyse des profits manqués (actions vendues trop tôt)
- Graphiques de performance comparative
- Filtrage par période (1Y, 6M, Last 60 Days, MTD, YTD)
- Interface utilisateur réactive et intuitive

## Structure du projet

```
E:\Dash_Claude\
│
├── app.py                  # Point d'entrée principal de l'application
├── config.py               # Configuration (chemins des fichiers, paramètres, etc.)
├── data/                   # Données
│   ├── all_historical_data.csv    # Données historiques des actions
│   ├── transactions.csv           # Transactions du portefeuille
│   └── processed/                 # Dossier pour les données traitées/calculées
│
├── assets/                 # Ressources statiques
│   ├── styles.css          # Styles CSS
│   └── logo.png            # Logo de l'application
│
├── components/             # Composants modulaires de l'interface
│   ├── __init__.py
│   ├── header.py           # En-tête avec logo et titre
│   ├── date_selector.py    # Sélecteur de plage de dates
│   ├── summary_cards.py    # Cartes récapitulatives
│   ├── portfolio_table.py  # Tableau détaillé du portefeuille
│   ├── performance_chart.py # Graphique de performance
│   └── tabs.py             # Onglets pour la navigation
│
├── modules/                # Modules de logique métier
│   ├── __init__.py
│   ├── data_loader.py      # Chargement et préparation des données
│   ├── portfolio.py        # Calculs relatifs au portefeuille
│   ├── performance.py      # Calculs de performance
│   └── utils.py            # Fonctions utilitaires
│
├── layouts/                # Mise en page des différentes sections
│   ├── __init__.py
│   ├── main_layout.py      # Mise en page principale
│   ├── portfolio_value.py  # Page de valeur du portefeuille
│   ├── portfolio_breakdown.py # Page de répartition du portefeuille
│   ├── missed_profit.py    # Page des profits manqués
│   └── buy_high_sell_low.py # Page stratégie d'achat/vente
│
└── callbacks/              # Callbacks pour l'interactivité
    ├── __init__.py
    ├── date_callbacks.py   # Callbacks pour les sélecteurs de date
    ├── portfolio_callbacks.py # Callbacks pour les tables et graphiques du portefeuille
    └── tab_callbacks.py    # Callbacks pour la navigation entre les onglets
```

## Installation et démarrage

1. Assurez-vous d'avoir Python 3.8+ installé
2. Installez les dépendances requises :

```bash
pip install dash dash-bootstrap-components pandas plotly numpy
```

3. Exécutez l'application :

```bash
python app.py
```

4. Ouvrez votre navigateur à l'adresse `http://127.0.0.1:8050/`

## Fichiers de données

L'application utilise deux fichiers CSV principaux :

1. **all_historical_data.csv** : Contient les données historiques des prix des actions
   - Colonnes : date, open, high, low, close, adjusted_close, volume, symbol

2. **transactions.csv** : Contient les transactions du portefeuille
   - Colonnes : Ticker, Nombre_Actions, Prix_Acquisition, Date_Acquisition

## Personnalisation

Pour personnaliser l'application :

- Modifiez `config.py` pour ajuster les paramètres généraux
- Ajoutez vos propres styles dans `assets/styles.css`
- Remplacez le logo dans `assets/logo.png`

## Développement

Pour étendre l'application :

1. Ajoutez de nouveaux composants dans le dossier `components/`
2. Créez de nouvelles vues dans le dossier `layouts/`
3. Implémentez de nouvelles fonctionnalités de calcul dans `modules/`
4. Ajoutez les callbacks nécessaires dans `callbacks/`

## Licence

Ce projet est sous licence MIT.