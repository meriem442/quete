# utils.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_data():
    """Génère des données factices pour l'exemple"""
    # Création de dates
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')

    # Création du DataFrame
    n_records = 10000

    df = pd.DataFrame({
        'date': np.random.choice(dates, n_records),
        'customer_id': np.random.randint(1, 1000, n_records),
        'product': np.random.choice(['Produit A', 'Produit B', 'Produit C', 'Produit D', 'Produit E'], n_records),
        'channel': np.random.choice(['Web', 'Mobile', 'Magasin', 'Partenaire'], n_records),
        'revenue': np.random.normal(100, 30, n_records),
        'converted': np.random.choice([0, 1], n_records, p=[0.7, 0.3]),
        'order_id': range(1, n_records + 1)
    })

    # Ajustements
    df['revenue'] = df['revenue'].clip(lower=0)  # Pas de revenus négatifs
    df = df.sort_values('date')

    return df

def style_metric_cards():
    """Retourne le style CSS pour les cartes de métriques"""
    return """
        <style>
            [data-testid="stMetricLabel"] {
                min-height: 0px;
                max-height: 50px;
                font-size: 20px;
            }
            [data-testid="stMetricValue"] {
                font-size: 28px;
            }
        </style>
    """