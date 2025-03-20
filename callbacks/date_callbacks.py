"""Callbacks pour les sélecteurs de date"""
from dash import Input, Output, State, callback_context
from datetime import datetime, timedelta

def register_date_callbacks(app):
    """Enregistre les callbacks pour les sélecteurs de date"""
    
    @app.callback(
        [
            Output('start-date-picker', 'date'),
            Output('end-date-picker', 'date')
        ],
        [
            Input('btn-1y', 'n_clicks'),
            Input('btn-6m', 'n_clicks'),
            Input('btn-60d', 'n_clicks'),
            Input('btn-mtd', 'n_clicks'),
            Input('btn-ytd', 'n_clicks')
        ],
        [State('end-date-picker', 'date')]
    )
    def update_date_range(n1y, n6m, n60d, nmtd, nytd, end_date):
        """
        Met à jour les sélecteurs de date en fonction du bouton de période cliqué
        
        Args:
            n1y (int): Nombre de clics sur le bouton 1Y
            n6m (int): Nombre de clics sur le bouton 6M
            n60d (int): Nombre de clics sur le bouton 60D
            nmtd (int): Nombre de clics sur le bouton MTD
            nytd (int): Nombre de clics sur le bouton YTD
            end_date (str): Date de fin actuelle
        
        Returns:
            tuple: (date_debut, date_fin) au format YYYY-MM-DD
        """
        ctx = callback_context
        if not ctx.triggered:
            # Valeurs par défaut : 1 an
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            return start_date.date().isoformat(), end_date.date().isoformat()
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        end_date = datetime.now() if end_date is None else datetime.strptime(end_date.split('T')[0], '%Y-%m-%d')
        
        if button_id == 'btn-1y':
            start_date = end_date - timedelta(days=365)
        elif button_id == 'btn-6m':
            start_date = end_date - timedelta(days=180)
        elif button_id == 'btn-60d':
            start_date = end_date - timedelta(days=60)
        elif button_id == 'btn-mtd':
            start_date = end_date.replace(day=1)
        elif button_id == 'btn-ytd':
            start_date = end_date.replace(month=1, day=1)
        else:
            start_date = end_date - timedelta(days=365)
        
        # Mettre à jour le store pour la période
        return start_date.date().isoformat(), end_date.date().isoformat()
    
    @app.callback(
        Output('store-current-period', 'data'),
        [
            Input('btn-1y', 'n_clicks'),
            Input('btn-6m', 'n_clicks'),
            Input('btn-60d', 'n_clicks'),
            Input('btn-mtd', 'n_clicks'),
            Input('btn-ytd', 'n_clicks')
        ]
    )
    def update_current_period(n1y, n6m, n60d, nmtd, nytd):
        """
        Met à jour la période actuelle dans le store
        
        Returns:
            str: Période actuelle ('1Y', '6M', 'Last 60 Days', 'MTD', 'YTD')
        """
        ctx = callback_context
        if not ctx.triggered:
            return '1Y'  # Valeur par défaut
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'btn-1y':
            return '1Y'
        elif button_id == 'btn-6m':
            return '6M'
        elif button_id == 'btn-60d':
            return 'Last 60 Days'
        elif button_id == 'btn-mtd':
            return 'MTD'
        elif button_id == 'btn-ytd':
            return 'YTD'
        else:
            return '1Y'  # Valeur par défaut