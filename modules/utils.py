"""
Module d'utilitaires pour le formatage et les opérations communes
"""

def format_currency(value, prefix="₹"):
    """
    Formate une valeur monétaire avec symbole et séparateurs
    
    Args:
        value (float): Valeur à formater
        prefix (str, optional): Symbole monétaire à utiliser. Par défaut "₹".
    
    Returns:
        str: Chaîne formatée
    """
    if value is None:
        return f"{prefix}0"
    
    # Gérer les nombres négatifs
    is_negative = value < 0
    abs_value = abs(value)
    
    # Formater avec séparateur de milliers et 2 décimales
    formatted = "{:,.2f}".format(abs_value)
    
    # Ajouter le signe négatif et le préfixe
    if is_negative:
        return f"-{prefix}{formatted}"
    else:
        return f"{prefix}{formatted}"

def format_percentage(value, digits=2):
    """
    Formate une valeur en pourcentage
    
    Args:
        value (float): Valeur à formater
        digits (int, optional): Nombre de décimales. Par défaut 2.
    
    Returns:
        str: Chaîne formatée
    """
    if value is None:
        return "0.00%"
    
    # Formater avec le nombre de décimales spécifié
    return f"{value:.{digits}f}%"