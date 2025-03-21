from dash import Input, Output, State, html, dcc, dash_table, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def register_all_callbacks(app, historical_data, transactions_data):
    """
    Enregistre tous les callbacks de l'application
    """
    
    # Callback pour changer le contenu des onglets
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "active_tab"),
    )
    def render_tab_content(active_tab):
        """Affiche le contenu de l'onglet sélectionné"""
        try:
            if active_tab == "tab-overview":
                return render_overview_tab(historical_data, transactions_data)
            elif active_tab == "tab-transactions":
                return render_transactions_tab(transactions_data)
            elif active_tab == "tab-analysis":
                return render_analysis_tab(historical_data, transactions_data)
            else:
                return html.Div("Onglet non reconnu")
        except Exception as e:
            import traceback
            print(f"Erreur dans le callback render_tab_content: {e}")
            print(traceback.format_exc())
            return html.Div([
                html.H4("Une erreur s'est produite lors du chargement de cet onglet"),
                html.P(f"Détails de l'erreur: {str(e)}")
            ])

def render_overview_tab(historical_data, transactions_data):
    """Affiche l'onglet Vue d'ensemble"""
    from dash import html, dcc
    import dash_bootstrap_components as dbc
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    
    # Si les données sont vides, afficher un message
    if historical_data.empty or transactions_data.empty:
        return html.Div([
            html.H3("Données non disponibles"),
            html.P("Veuillez charger des données historiques et des transactions.")
        ])
    
    # Calculer la valeur actuelle du portefeuille
    # Obtenir les derniers prix pour chaque action
    latest_prices = {}
    for symbol in historical_data['Symbol'].unique():
        symbol_data = historical_data[historical_data['Symbol'] == symbol]
        latest_date = symbol_data['Date'].max()
        latest_price = symbol_data[symbol_data['Date'] == latest_date]['Close'].values[0]
        latest_prices[symbol] = latest_price
    
    # Calculer les positions actuelles basées sur les transactions
    positions = {}
    for symbol in transactions_data['Symbol'].unique():
        symbol_transactions = transactions_data[transactions_data['Symbol'] == symbol]
        quantity = 0
        cost_basis = 0
        
        for _, transaction in symbol_transactions.iterrows():
            if transaction['Type'] == 'BUY':
                cost_basis += transaction['Quantity'] * transaction['Price']
                quantity += transaction['Quantity']
            elif transaction['Type'] == 'SELL':
                # Méthode FIFO simplifiée pour le coût
                cost_basis = cost_basis * (1 - transaction['Quantity'] / quantity)
                quantity -= transaction['Quantity']
        
        if quantity > 0:
            current_value = quantity * latest_prices[symbol]
            profit_loss = current_value - cost_basis
            profit_loss_pct = (profit_loss / cost_basis) * 100 if cost_basis > 0 else 0
            
            positions[symbol] = {
                'Quantité': quantity,
                'Prix moyen': cost_basis / quantity if quantity > 0 else 0,
                'Prix actuel': latest_prices[symbol],
                'Valeur actuelle': current_value,
                'Gain/Perte': profit_loss,
                'Gain/Perte %': profit_loss_pct
            }
    
    # Créer un DataFrame des positions
    positions_df = pd.DataFrame.from_dict(positions, orient='index')
    positions_df.reset_index(inplace=True)
    positions_df.rename(columns={'index': 'Symbole'}, inplace=True)
    
    # Calculer la valeur totale du portefeuille
    total_value = positions_df['Valeur actuelle'].sum()
    
    # Créer un graphique en camembert pour la répartition du portefeuille
    fig_pie = px.pie(
        positions_df, 
        values='Valeur actuelle', 
        names='Symbole',
        title='Répartition du portefeuille',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Plasma_r
    )
    
    # Créer un graphique à barres pour les gains/pertes
    fig_bar = px.bar(
        positions_df,
        x='Symbole',
        y='Gain/Perte',
        title='Gains/Pertes par action',
        color='Gain/Perte',
        color_continuous_scale=['red', 'green'],
        text='Gain/Perte %'
    )
    fig_bar.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    
    # Créer le layout de l'onglet Vue d'ensemble
    return html.Div([
        html.H3("Vue d'ensemble du portefeuille"),
        
        # Cartes de résumé
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Valeur totale", className="card-title"),
                        html.H3(f"{total_value:.2f} €", className="card-text text-primary")
                    ])
                ]),
                width=4
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Nombre d'actions", className="card-title"),
                        html.H3(f"{len(positions)}", className="card-text text-info")
                    ])
                ]),
                width=4
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Gain/Perte totale", className="card-title"),
                        html.H3(
                            f"{positions_df['Gain/Perte'].sum():.2f} €", 
                            className=f"card-text {'text-success' if positions_df['Gain/Perte'].sum() >= 0 else 'text-danger'}"
                        )
                    ])
                ]),
                width=4
            ),
        ], className="mb-4"),
        
        # Graphiques
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_pie), width=6),
            dbc.Col(dcc.Graph(figure=fig_bar), width=6),
        ], className="mb-4"),
        
        # Tableau des positions
        html.H4("Détail des positions"),
        dash_table.DataTable(
            id='positions-table',
            columns=[
                {"name": "Symbole", "id": "Symbole"},
                {"name": "Quantité", "id": "Quantité", "type": "numeric", "format": {"specifier": ".0f"}},
                {"name": "Prix moyen", "id": "Prix moyen", "type": "numeric", "format": {"specifier": ".2f"}},
                {"name": "Prix actuel", "id": "Prix actuel", "type": "numeric", "format": {"specifier": ".2f"}},
                {"name": "Valeur actuelle", "id": "Valeur actuelle", "type": "numeric", "format": {"specifier": ".2f"}},
                {"name": "Gain/Perte", "id": "Gain/Perte", "type": "numeric", "format": {"specifier": ".2f"}},
                {"name": "Gain/Perte %", "id": "Gain/Perte %", "type": "numeric", "format": {"specifier": ".2f"}}
            ],
            data=positions_df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{Gain/Perte} > 0',
                        'column_id': 'Gain/Perte'
                    },
                    'color': 'green'
                },
                {
                    'if': {
                        'filter_query': '{Gain/Perte} < 0',
                        'column_id': 'Gain/Perte'
                    },
                    'color': 'red'
                },
                {
                    'if': {
                        'filter_query': '{Gain/Perte %} > 0',
                        'column_id': 'Gain/Perte %'
                    },
                    'color': 'green'
                },
                {
                    'if': {
                        'filter_query': '{Gain/Perte %} < 0',
                        'column_id': 'Gain/Perte %'
                    },
                    'color': 'red'
                }
            ]
        )
    ])

def render_transactions_tab(transactions_data):
    """Affiche l'onglet Transactions"""
    from dash import html, dash_table
    
    # Si les données sont vides, afficher un message
    if transactions_data.empty:
        return html.Div([
            html.H3("Aucune transaction disponible"),
            html.P("Veuillez ajouter des transactions.")
        ])
    
    # Sinon, afficher le tableau des transactions
    return html.Div([
        html.H3("Historique des transactions"),
        dash_table.DataTable(
            id='transactions-table',
            columns=[{"name": i, "id": i} for i in transactions_data.columns],
            data=transactions_data.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'fontWeight': 'bold'
            }
        )
    ])

def render_analysis_tab(historical_data, transactions_data):
    """Affiche l'onglet Analyse"""
    from dash import html, dcc
    
    # Si les données sont vides, afficher un message
    if historical_data.empty:
        return html.Div([
            html.H3("Données non disponibles pour l'analyse"),
            html.P("Veuillez charger des données historiques.")
        ])
    
    # Sinon, afficher un graphique simple
    fig = px.line(historical_data, x='Date', y='Close', color='Symbol',
                 title='Évolution des prix de clôture')
    
    return html.Div([
        html.H3("Analyse du portefeuille"),
        dcc.Graph(figure=fig)
    ])