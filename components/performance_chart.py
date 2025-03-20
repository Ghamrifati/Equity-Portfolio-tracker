# Graphique de performance
"""
Composant du graphique de performance
"""
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from modules.performance import calculate_comparative_performance

def create_performance_chart(historical_data, transactions_data, period='1Y'):
    """
    Crée un graphique de performance comparative
    
    Args:
        historical_data (pd.DataFrame): Données historiques des prix
        transactions_data (pd.DataFrame): Données des transactions
        period (str): Période d'analyse ('1Y', '6M', 'MTD', 'YTD', 'Last 60 Days')
    
    Returns:
        dash.html.Div: Composant de graphique de performance
    """
    # Calculer les performances comparatives
    comp_performance = calculate_comparative_performance(historical_data, transactions_data, '^NSEI', period)
    
    # Si aucune donnée n'est disponible, créer un graphique vide
    if comp_performance.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No performance data available",
            template="plotly_dark",
            paper_bgcolor="#333333",
            plot_bgcolor="#333333",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
        )
    else:
        # Rebaser les performances à 0% au début de la période
        first_portfolio_value = comp_performance['cumulative_portfolio_return'].iloc[0] or 0
        first_benchmark_value = comp_performance['cumulative_benchmark_return'].iloc[0] or 0
        
        comp_performance['portfolio_return_rebased'] = comp_performance['cumulative_portfolio_return'] - first_portfolio_value
        comp_performance['benchmark_return_rebased'] = comp_performance['cumulative_benchmark_return'] - first_benchmark_value
        
        # Créer le graphique
        fig = go.Figure()
        
        # Ajouter la courbe du portefeuille
        fig.add_trace(go.Scatter(
            x=comp_performance['date'],
            y=comp_performance['portfolio_return_rebased'],
            mode='lines',
            name='Portfolio',
            line=dict(color='#FD3216', width=2),
        ))
        
        # Ajouter la courbe de l'indice de référence
        fig.add_trace(go.Scatter(
            x=comp_performance['date'],
            y=comp_performance['benchmark_return_rebased'],
            mode='lines',
            name='NIFTY',
            line=dict(color='#FFA15A', width=2),
        ))
        
        # Mise en page du graphique
        fig.update_layout(
            title="Performance Comparison",
            template="plotly_dark",
            paper_bgcolor="#333333",
            plot_bgcolor="#333333",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                title=None,
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                showticklabels=True,
            ),
            yaxis=dict(
                title="Return (%)",
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                zeroline=True,
                zerolinecolor='rgba(255, 255, 255, 0.5)',
                tickformat='.1f',
                ticksuffix='%',
            ),
            hovermode="x unified"
        )
    
    # Ajout du sélecteur de stock
    stock_selector = html.Div([
        html.H4("Stocks", className="stocks-title"),
        html.Div([
            html.H4("Select Stock", className="select-stock-title"),
            dcc.Dropdown(
                id='stock-selector',
                options=[
                    {'label': 'Multiple selections', 'value': 'multiple'},
                    {'label': 'INFY', 'value': 'INFY'},
                    {'label': 'HDFCBANK', 'value': 'HDFCBANK'},
                    {'label': 'IREDA', 'value': 'IREDA'},
                    {'label': 'IRFC', 'value': 'IRFC'},
                ],
                value='multiple',
                clearable=False,
                searchable=False,
                className='stock-dropdown'
            )
        ], className="stock-selector-container")
    ], className="stocks-container")
    
    performance_chart = html.Div([
        html.Div([
            stock_selector,
            dcc.Graph(
                id='performance-graph',
                figure=fig,
                config={
                    'displayModeBar': False,
                    'responsive': True
                },
                className="performance-graph"
            )
        ], className="performance-chart-inner")
    ], className="performance-chart-container")
    
    return performance_chart
