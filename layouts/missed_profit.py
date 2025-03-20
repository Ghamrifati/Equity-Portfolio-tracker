# Page des profits manqués
"""
Layout pour la vue des profits manqués
"""
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from modules.performance import calculate_missed_profit
from modules.utils import format_currency, format_percentage

def create_missed_profit_layout(historical_data, transactions_data):
    """
    Crée le layout pour la vue des profits manqués
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
        transactions_data (pd.DataFrame): Données des transactions
    
    Returns:
        dash.html.Div: Layout de la vue des profits manqués
    """
    # Calculer les profits manqués
    missed_profits = calculate_missed_profit(historical_data, transactions_data)
    
    # Vérifier si des données sont disponibles
    if missed_profits.empty:
        # Layout pour aucune donnée
        layout = html.Div([
            html.H3("Missed Profit Analysis", className="missed-profit-title"),
            html.Div([
                html.P("No missed profit data available.", className="no-data-message")
            ], className="no-data-container")
        ], className="missed-profit-container")
        
        return layout
    
    # Calculer le total des profits manqués
    total_missed_profit = missed_profits['missed_profit'].sum()
    
    # Créer un graphique à barres pour les profits manqués par action
    fig = px.bar(
        missed_profits,
        x='symbol',
        y='missed_profit',
        color='missed_profit',
        color_continuous_scale='RdYlGn_r',  # Échelle de couleur du rouge au vert (inversée)
        labels={'symbol': 'Symbol', 'missed_profit': 'Missed Profit'},
        title='Missed Profit by Stock'
    )
    
    # Mise en page du graphique
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#333333",
        plot_bgcolor="#333333",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            title=None,
            tickangle=-45,
            showgrid=False,
        ),
        yaxis=dict(
            title="Amount",
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
        ),
        coloraxis_showscale=False
    )
    
    # Ajouter une ligne pour la moyenne
    avg_missed_profit = missed_profits['missed_profit'].mean()
    fig.add_hline(
        y=avg_missed_profit,
        line_dash="dash",
        line_color="#FFFFFF",
        annotation_text=f"Avg: {format_currency(avg_missed_profit)}",
        annotation_position="top right"
    )
    
    # Ajouter du texte sur chaque barre
    fig.update_traces(
        texttemplate='%{y:,.2f}',
        textposition='outside',
        textfont=dict(color='white')
    )
    
    # Créer un graphique en camembert pour la répartition des profits manqués
    pie_fig = px.pie(
        missed_profits,
        values='missed_profit',
        names='symbol',
        title='Proportion of Missed Profits',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    # Mise en page du graphique en camembert
    pie_fig.update_layout(
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
    
    # Créer un tableau détaillé des profits manqués
    missed_profits_table = html.Div([
        html.H4("Detailed Missed Profit Analysis", className="table-title"),
        dash_table.DataTable(
            id='missed-profits-table',
            columns=[
                {'name': 'Symbol', 'id': 'symbol'},
                {'name': 'Quantity', 'id': 'quantity', 'type': 'numeric', 'format': {'specifier': ',d'}},
                {'name': 'Current Price', 'id': 'current_price', 'type': 'numeric', 'format': {'specifier': ',.2f'}},
                {'name': 'Highest Price', 'id': 'highest_price', 'type': 'numeric', 'format': {'specifier': ',.2f'}},
                {'name': 'Price Difference', 'id': 'price_diff', 'type': 'numeric', 'format': {'specifier': ',.2f'}},
                {'name': 'Missed Profit', 'id': 'missed_profit', 'type': 'numeric', 'format': {'specifier': ',.2f'}}
            ],
            data=missed_profits.assign(
                price_diff=missed_profits['highest_price'] - missed_profits['current_price']
            ).to_dict('records'),
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
                # Style pour les profits manqués élevés
                {
                    'if': {
                        'column_id': 'missed_profit',
                        'filter_query': '{missed_profit} > 1000'
                    },
                    'color': '#FF4500',
                    'fontWeight': 'bold',
                },
                # Style pour les différences de prix élevées
                {
                    'if': {
                        'column_id': 'price_diff',
                        'filter_query': '{price_diff} > 100'
                    },
                    'color': '#FF4500',
                    'fontWeight': 'bold',
                },
            ],
            style_cell_conditional=[
                {'if': {'column_id': 'symbol'}, 'textAlign': 'left', 'width': '15%'},
                {'if': {'column_id': 'quantity'}, 'textAlign': 'right', 'width': '15%'},
                {'if': {'column_id': 'current_price'}, 'textAlign': 'right', 'width': '15%'},
                {'if': {'column_id': 'highest_price'}, 'textAlign': 'right', 'width': '15%'},
                {'if': {'column_id': 'price_diff'}, 'textAlign': 'right', 'width': '15%'},
                {'if': {'column_id': 'missed_profit'}, 'textAlign': 'right', 'width': '20%'},
            ],
            sort_action='native',
            filter_action='native',
            page_action='none',
        )
    ], className="missed-profits-table-container")
    
    # Créer le layout complet
    layout = html.Div([
        # En-tête avec le total des profits manqués
        html.Div([
            html.H3("Missed Profit Analysis", className="missed-profit-title"),
            html.Div([
                html.Span("Total Missed Profit: ", className="missed-profit-label"),
                html.Span(format_currency(total_missed_profit), 
                         className="missed-profit-value",
                         style={"color": "#FF4500" if total_missed_profit > 0 else "#FFFFFF"})
            ], className="missed-profit-total")
        ], className="missed-profit-header"),
        
        # Graphiques
        dbc.Row([
            # Graphique à barres
            dbc.Col(
                dcc.Graph(
                    id='missed-profit-bar',
                    figure=fig,
                    config={
                        'displayModeBar': False,
                        'responsive': True
                    },
                    className="missed-profit-chart"
                ),
                width=12, lg=8
            ),
            
            # Graphique en camembert
            dbc.Col(
                dcc.Graph(
                    id='missed-profit-pie',
                    figure=pie_fig,
                    config={
                        'displayModeBar': False,
                        'responsive': True
                    },
                    className="missed-profit-pie"
                ),
                width=12, lg=4
            ),
        ], className="missed-profit-charts-row"),
        
        # Tableau détaillé
        dbc.Row([
            dbc.Col(
                missed_profits_table,
                width=12
            ),
        ], className="missed-profit-table-row"),
        
        # Section de conseils
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H4("Insights & Recommendations", className="insights-title"),
                    html.Ul([
                        html.Li([
                            html.Strong("Set Profit Targets: "),
                            "Consider setting specific profit targets for each stock and implement stop-loss orders."
                        ]),
                        html.Li([
                            html.Strong("High Volatility Stocks: "),
                            f"Focus on {missed_profits['symbol'].iloc[missed_profits['missed_profit'].argmax()]} which shows the highest missed profit potential."
                        ]),
                        html.Li([
                            html.Strong("Market Timing: "),
                            "Analyze your historical selling patterns to identify potential timing improvements."
                        ]),
                        html.Li([
                            html.Strong("Profit Taking Strategy: "),
                            "Consider partial profit taking during price surges instead of all-or-nothing approach."
                        ]),
                    ], className="insights-list")
                ], className="insights-container"),
                width=12
            ),
        ], className="insights-row"),
    ], className="missed-profit-container")
    
    return layout