# Suivi de Portefeuille d'Actions

Une application web interactive pour suivre et analyser votre portefeuille d'actions.

## Fonctionnalités

- **Tableau de bord complet**: Visualisez la valeur de votre portefeuille, les profits/pertes et les performances
- **Analyse comparative**: Comparez votre performance avec l'indice MASI
- **Suivi des transactions**: Enregistrez et suivez toutes vos transactions d'achat et de vente
- **Analyse des profits manqués**: Identifiez les opportunités manquées sur les actions vendues
- **Visualisations interactives**: Graphiques et tableaux pour une analyse approfondie

## Technologies utilisées

- **Backend**: Python, Dash, Pandas
- **Frontend**: HTML, CSS, JavaScript
- **Visualisation**: Plotly
- **Style**: Dash Bootstrap Components

## Installation

1. Clonez ce dépôt:
   ```
   git clone https://github.com/votre-utilisateur/equity-portfolio-tracker.git
   cd equity-portfolio-tracker
   ```

2. Installez les dépendances:
   ```
   pip install -r requirements.txt
   ```

3. Lancez l'application:
   ```
   python app.py
   ```

4. Ouvrez votre navigateur à l'adresse `http://localhost:8050`

## Structure du projet

- `app.py`: Point d'entrée principal de l'application
- `config.py`: Configuration de l'application
- `data/`: Données du portefeuille et historiques
  - `transactions.csv`: Enregistrement des transactions
  - `all_historical_data.csv`: Données historiques des prix
- `modules/`: Modules de traitement des données
- `components/`: Composants UI réutilisables
- `layouts/`: Mises en page pour les différentes vues
- `callbacks/`: Fonctions de callback pour l'interactivité
- `assets/`: Ressources statiques (CSS, images)

## Utilisation

1. Importez vos transactions dans `data/transactions.csv`
2. Importez les données historiques dans `data/all_historical_data.csv`
3. Lancez l'application et explorez votre portefeuille

## Personnalisation

Vous pouvez personnaliser l'application en modifiant:
- Les couleurs et styles dans `assets/styles.css`
- Les paramètres de configuration dans `config.py`
- Les composants UI dans le dossier `components/`

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
