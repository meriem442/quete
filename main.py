# main.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, style_metric_cards

st.set_page_config(
    page_title="Dashboard Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
    }
    [data-testid="stMetricLabel"] {
        min-height: 0px;
        max-height: 50px;
        font-size: 20px;
    }
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.title("📊 Dashboard Analytics")
st.markdown("### Vue d'ensemble des performances")

# Chargement des données
df = load_data()

# Calcul des métriques avec gestion des deltas
daily_revenue = df.groupby('date')['revenue'].sum().reset_index()
current_revenue = daily_revenue['revenue'].sum()
previous_revenue = daily_revenue['revenue'].shift(1).sum()
revenue_delta = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue != 0 else 0

daily_customers = df.groupby('date')['customer_id'].nunique().reset_index()
current_customers = daily_customers['customer_id'].sum()
previous_customers = daily_customers['customer_id'].shift(1).sum()
customers_delta = ((current_customers - previous_customers) / previous_customers * 100) if previous_customers != 0 else 0

# Layout en colonnes pour les métriques
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Chiffre d'affaires total",
        value=f"{current_revenue:,.0f} €",
        delta=f"{revenue_delta:.1f}%"
    )

with col2:
    st.metric(
        label="Nombre de clients",
        value=f"{df['customer_id'].nunique():,}",
        delta=f"{customers_delta:.1f}%"
    )

with col3:
    st.metric(
        label="Panier moyen",
        value=f"{df['revenue'].mean():,.0f} €",
        delta=None
    )

with col4:
    st.metric(
        label="Taux de conversion",
        value=f"{(df['converted'].mean() * 100):.1f}%",
        delta=None
    )

# Graphiques
col1, col2 = st.columns(2)

with col1:
    st.subheader("Évolution des ventes")
    fig = px.line(
        df.groupby('date')['revenue'].sum().reset_index(),
        x='date',
        y='revenue',
        title="Évolution du chiffre d'affaires"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 10 Produits")
    top_products = df.groupby('product')['revenue'].sum().sort_values(ascending=True).tail(10)
    fig = px.bar(
        top_products,
        orientation='h',
        title="Top 10 des produits par chiffre d'affaires"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)