"""
Composant de sélection de dates
"""
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_date_selector(start_date, end_date):
    """
    Crée un sélecteur de plage de dates
    
    Args:
        start_date (str): Date de début par défaut (format YYYY-MM-DD)
        end_date (str): Date de fin par défaut (format YYYY-MM-DD)
    
    Returns:
        dash.html.Div: Composant de sélection de dates
    """
    date_selector = html.Div([
        dbc.Row([
            # Sélecteur de date de début
            dbc.Col(
                html.Div([
                    dcc.DatePickerSingle(
                        id='start-date-picker',
                        date=start_date,
                        display_format='DD-MM-YYYY',
                        placeholder='Date de début',
                        className='date-picker',
                        clearable=False
                    ),
                    html.I(className="fa fa-calendar calendar-icon")
                ], className="date-picker-container"),
                width=6, lg=3, className="date-col"
            ),
            
            # Sélecteur de date de fin
            dbc.Col(
                html.Div([
                    dcc.DatePickerSingle(
                        id='end-date-picker',
                        date=end_date,
                        display_format='DD-MM-YYYY',
                        placeholder='Date de fin',
                        className='date-picker',
                        clearable=False
                    ),
                    html.I(className="fa fa-calendar calendar-icon")
                ], className="date-picker-container"),
                width=6, lg=3, className="date-col"
            ),
        ], className="date-selector-row", justify="start")
    ], className="date-selector-container")
    
    return date_selector
