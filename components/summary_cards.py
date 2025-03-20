# Cartes récapitulatives (Nifty, Profit, Valeur actuelle, Rendements)
"""
Composant des cartes récapitulatives
"""
import dash
from dash import html
import dash_bootstrap_components as dbc
from modules.utils import format_currency, format_percentage

def create_summary_cards(
    nifty_value,
    nifty_change,
    profit,
    profit_change,
    missed_profit,
    trades_done,
    portfolio_value,
    invested_amount,
    mom_change,
    mom_value,
    returns_percent,
    nifty_yoy,
    best_performer,
    worst_performer
):
    """
    Crée les cartes récapitulatives pour l'application
    
    Args:
        nifty_value (float): Valeur actuelle de l'indice Nifty
        nifty_change (float): Changement en pourcentage de l'indice Nifty
        profit (float): Profit total du portefeuille
        profit_change (float): Changement du profit sur la période
        missed_profit (float): Profit manqué (actions vendues)
        trades_done (int): Nombre de transactions effectuées
        portfolio_value (float): Valeur actuelle du portefeuille
        invested_amount (float): Montant total investi
        mom_change (float): Changement mois sur mois en pourcentage
        mom_value (float): Changement mois sur mois en valeur
        returns_percent (float): Rendement total en pourcentage
        nifty_yoy (float): Rendement de l'indice Nifty sur un an
        best_performer (dict): Meilleure performance {'symbol': str, 'return': float}
        worst_performer (dict): Pire performance {'symbol': str, 'return': float}
    
    Returns:
        dash.html.Div: Composant avec les cartes récapitulatives
    """
    # Fonction pour formater les changements avec flèche
    def format_change_with_arrow(change):
        if change > 0:
            arrow = "↑"
            color = "#00FF7F"  # Vert
        elif change < 0:
            arrow = "↓"
            color = "#FF4500"  # Rouge
        else:
            arrow = ""
            color = "#FFFFFF"  # Blanc
        
        return [
            html.Span(f"{format_percentage(abs(change))} ", style={"color": color}),
            html.Span(arrow, style={"color": color})
        ]
    
    summary_cards = html.Div([
        dbc.Row([
            # Carte Nifty
            dbc.Col(
                dbc.Card([
                    html.H4("Nifty", className="card-title"),
                    html.H2(f"{nifty_value:,}", className="card-value"),
                    html.Div([
                        *format_change_with_arrow(nifty_change),
                        html.Span(f"{nifty_change:.2f}", className="change-value")
                    ], className="change-container")
                ], className="summary-card"),
                width=12, md=6, lg=3
            ),
            
            # Carte Profit
            dbc.Col(
                dbc.Card([
                    html.H4("Profit", className="card-title"),
                    html.H2(format_currency(profit), className="card-value"),
                    html.Div([
                        html.Div([
                            html.Span("Change (MoM): "),
                            *format_change_with_arrow(profit_change),
                            html.Span(format_currency(24.86e3), className="mom-value")
                        ], className="profit-change"),
                        html.Div([
                            html.Span("Missed Profit (Sold Assets): "),
                            html.Span(format_currency(missed_profit), className="missed-profit", 
                                     style={"color": "#FF4500"})
                        ], className="missed-profit-container"),
                        html.Div([
                            html.Span("Trades Done: "),
                            html.Span(f"{trades_done}", className="trades-done")
                        ], className="trades-container")
                    ], className="profit-details")
                ], className="summary-card"),
                width=12, md=6, lg=3
            ),
            
            # Carte Valeur du Portefeuille
            dbc.Col(
                dbc.Card([
                    html.H4("Current Portfolio Value", className="card-title"),
                    html.H2(format_currency(portfolio_value), className="card-value"),
                    html.Div([
                        html.Div([
                            html.Span("Invested Amount: "),
                            html.Span(format_currency(invested_amount), className="invested-amount")
                        ], className="invested-container"),
                        html.Div([
                            html.Span("Change (MoM): "),
                            *format_change_with_arrow(mom_change),
                            html.Span(format_currency(mom_value), className="mom-value")
                        ], className="portfolio-change")
                    ], className="portfolio-details")
                ], className="summary-card"),
                width=12, md=6, lg=3
            ),
            
            # Carte Rendements
            dbc.Col(
                dbc.Card([
                    html.H4("Returns", className="card-title"),
                    html.H2(format_percentage(returns_percent), className="card-value",
                           style={"color": "#00FF7F" if returns_percent > 0 else "#FF4500"}),
                    html.Div([
                        html.Div([
                            html.Span("Nifty (YoY): "),
                            *format_change_with_arrow(nifty_yoy)
                        ], className="nifty-returns"),
                        html.Div([
                            html.Span("Best Performer: "),
                            html.Span(best_performer['symbol'], className="best-performer-symbol"),
                            html.Span(format_percentage(best_performer['return']), 
                                     className="best-performer-return",
                                     style={"color": "#00FF7F"})
                        ], className="best-performer-container"),
                        html.Div([
                            html.Span("Worst Performer: "),
                            html.Span(worst_performer['symbol'], className="worst-performer-symbol"),
                            html.Span(format_percentage(worst_performer['return']), 
                                     className="worst-performer-return",
                                     style={"color": "#FF4500"})
                        ], className="worst-performer-container")
                    ], className="returns-details")
                ], className="summary-card"),
                width=12, md=6, lg=3
            )
        ], className="summary-cards-row")
    ], className="summary-cards-container")
    
    return summary_cards