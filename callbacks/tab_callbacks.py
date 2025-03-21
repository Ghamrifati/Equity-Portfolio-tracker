"""
Callbacks pour la navigation par onglets
"""
from dash import Input, Output, State, html, ALL
import dash_bootstrap_components as dbc

def register_tab_callbacks(app):
    """
    Enregistre les callbacks pour la navigation par onglets
    
    Args:
        app (dash.Dash): Application Dash
    """
    # Liste des boutons d'onglets
    tab_buttons = [
        'btn-portfolio-value',
        'btn-portfolio-breakdown',
        'btn-missed-profit',
        'btn-buy-high-sell-low',
        'btn-masi',
        'btn-stocks'
    ]
    
    @app.callback(
        [Output(btn, 'className') for btn in tab_buttons],
        [Input(btn, 'n_clicks') for btn in tab_buttons],
        [State(btn, 'className') for btn in tab_buttons]
    )
    def update_active_tab(*args):
        """
        Met à jour la classe active du bouton d'onglet cliqué
        
        Returns:
            list: Nouvelles classes pour chaque bouton
        """
        # Diviser les arguments en clics et classes
        n_clicks = args[:len(tab_buttons)]
        current_classes = args[len(tab_buttons):]
        
        # Vérifier si un bouton a été cliqué
        ctx = app.callback_context
        if not ctx.triggered:
            # Si aucun bouton n'a été cliqué, conserver l'état actuel
            return list(current_classes)
        
        # Identifier le bouton cliqué
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Mise à jour des classes
        new_classes = []
        for i, btn in enumerate(tab_buttons):
            if btn == button_id:
                # Ajouter la classe 'active' au bouton cliqué
                current_class = current_classes[i]
                if 'active' not in current_class:
                    new_classes.append(current_class + ' active')
                else:
                    new_classes.append(current_class)
            else:
                # Retirer la classe 'active' des autres boutons
                current_class = current_classes[i]
                new_classes.append(current_class.replace(' active', ''))
        
        return new_classes
