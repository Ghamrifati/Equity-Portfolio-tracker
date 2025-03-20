# Page de valeur du portefeuille
"""
Layout pour la vue Valeur du Portefeuille
"""
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from modules.portfolio import calculate_portfolio_metrics
from modules.utils import format_currency, format_percentage

def create_portfolio_value_layout(historical_data, transactions_data, period='1Y'):
    """
    Crée le layout pour la vue Valeur du Portefeuille
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
        transactions_data (pd.DataFrame): Données des transactions
        period (str): Période d'analyse ('1Y', '6M', 'MTD', 'YTD', 'Last 60 Days')
    
    Returns:
        dash.html.Div: Layout de la vue Valeur du Portefeuille
    """
    # Calculer les métriques du portefeuille
    portfolio_metrics = calculate_portfolio_metrics(transactions_data, historical_data)
    
    # Données du portefeuille
    portfolio_details = portfolio_metrics['portfolio_details']
    
    # Créer un graphique en anneau pour la répartition du portefeuille
    if not portfolio_details.empty:
        # Préparer les données pour le graphique
        portfolio_details['percentage'] = (portfolio_details['current_value'] / portfolio_metrics['total_value']) * 100
        
        # Créer le graphique
        fig = go.Figure(data=[go.Pie(
            labels=portfolio_details['symbol'],
            values=portfolio_details['current_value'],
            hole=.4,
            textinfo='label+percent',
            marker=dict(
                colors=px.colors.qualitative.Bold,
                line=dict(color='#333333', width=2)
            )
        )])
        
        # Mise en page
        fig.update_layout(
            title="Portfolio Allocation",
            template="plotly_dark",
            paper_bgcolor="#333333",
            plot_bgcolor="#333333",
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
    else:
        # Créer un graphique vide
        fig = go.Figure()
        fig.update_layout(
            title="No portfolio data available",
            template="plotly_dark",
            paper_bgcolor="#333333",
            plot_bgcolor="#333333",
            margin=dict(l=20, r=20, t=40, b=20),
        )
    
    # Créer un tableau récapitulatif
    summary_table = html.Div([
        html.H4("Portfolio Summary", className="summary-title"),
        html.Table([
            html.Tr([html.Td("Total Investment"), html.Td(format_currency(portfolio_metrics['total_investment']))]),
            html.Tr([html.Td("Current Value"), html.Td(format_currency(portfolio_metrics['total_value']))]),
            html.Tr([html.Td("Total Profit/Loss"), html.Td(format_currency(portfolio_metrics['total_profit_loss']))]),
            html.Tr([html.Td("Return"), html.Td(format_percentage(portfolio_metrics['total_profit_loss_percent']))]),
            html.Tr([html.Td("Number of Stocks"), html.Td(str(len(portfolio_details)))]),
            html.Tr([html.Td("Number of Transactions"), html.Td(str(portfolio_metrics['num_transactions']))]),
            html.Tr([html.Td("Average Transaction Amount"), html.Td(format_currency(portfolio_metrics['avg_transaction_amount']))])
        ], className="summary-table")
    ], className="summary-container")
    
    # Créer le layout
    layout = html.Div([
        dbc.Row([
            # Tableau récapitulatif
            dbc.Col(
                summary_table,
                width=12, md=4, lg=3
            ),
            
            # Graphique de répartition
            dbc.Col(
                dcc.Graph(
                    id='allocation-chart',
                    figure=fig,
                    config={
                        'displayModeBar': False,
                        'responsive': True
                    },
                    className="allocation-chart"
                ),
                width=12, md=8, lg=9
            ),
        ], className="portfolio-value-row"),
        
        # Tableau détaillé des positions
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H4("Portfolio Details", className="details-title"),
                    dash_table.DataTable(
                        id='portfolio-details-table',
                        columns=[
                            {'name': 'Symbol', 'id': 'symbol'},
                            {'name': 'Quantity', 'id': 'quantity', 'type': 'numeric'},
                            {'name': 'Avg Purchase Price', 'id': 'avg_purchase_price', 'type': 'numeric'},
                            {'name': 'Current Price', 'id': 'close', 'type': 'numeric'},
                            {'name': 'Current Value', 'id': 'current_value', 'type': 'numeric'},
                            {'name': 'Profit/Loss', 'id': 'profit_loss', 'type': 'numeric'},
                            {'name': 'Return (%)', 'id': 'profit_loss_percent', 'type': 'numeric'}
                        ],
                        data=portfolio_details.to_dict('records') if not portfolio_details.empty else [],
                        style_table={
                            'overflowX': 'auto',
                            'backgroundColor': '#333333',
                            'borderRadius': '10px',
                        },
                        style_header={
                            'backgroundColor': '#444444',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                            'border': 'none',
                            'padding': '10px',
                        },
                        style_cell={
                            'backgroundColor': '#333333',
                            'color': 'white',
                            'border': 'none',
                            'padding': '10px',
                            'font-size': '14px',
                        },
                        style_data_conditional=[
                            # Style pour les valeurs positives
                            {
                                'if': {
                                    'column_id': 'profit_loss',
                                    'filter_query': '{profit_loss} > 0'
                                },
                                'color': '#00FF7F',
                            },
                            # Style pour les valeurs négatives
                            {
                                'if': {
                                    'column_id': 'profit_loss',
                                    'filter_query': '{profit_loss} < 0'
                                },
                                'color': '#FF4500',
                            },
                            # Style pour les pourcentages positifs
                            {
                                'if': {
                                    'column_id': 'profit_loss_percent',
                                    'filter_query': '{profit_loss_percent} > 0'
                                },
                                'color': '#00FF7F',
                            },
                            # Style pour les pourcentages négatifs
                            {
                                'if': {
                                    'column_id': 'profit_loss_percent',
                                    'filter_query': '{profit_loss_percent} < 0'
                                },
                                'color': '#FF4500',
                            },
                        ],
                        style_cell_conditional=[
                            {'if': {'column_id': 'symbol'}, 'textAlign': 'left', 'width': '15%'},
                            {'if': {'column_id': 'quantity'}, 'textAlign': 'right', 'width': '10%'},
                            {'if': {'column_id': 'avg_purchase_price'}, 'textAlign': 'right', 'width': '15%'},
                            {'if': {'column_id': 'close'}, 'textAlign': 'right', 'width': '15%'},
                            {'if': {'column_id': 'current_value'}, 'textAlign': 'right', 'width': '15%'},
                            {'if': {'column_id': 'profit_loss'}, 'textAlign': 'right', 'width': '15%'},
                            {'if': {'column_id': 'profit_loss_percent'}, 'textAlign': 'right', 'width': '15%'},
                        ],
                        sort_action='native',
                        filter_action='native',
                        page_action='native',
                        page_size=10,
                    )
                ], className="details-container"),
                width=12
            ),
        ], className="details-row")
    ], className="portfolio-value-container")
    
    return layout