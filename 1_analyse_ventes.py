# 1_analyse_ventes.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
from datetime import datetime, timedelta

st.set_page_config(page_title="Analyse des Ventes", page_icon="💰", layout="wide")
st.title("💰 Analyse détaillée des ventes")

# Chargement des données
df = load_data()

# Conversion des dates
df['date'] = pd.to_datetime(df['date'])
min_date = df['date'].min().date()
max_date = df['date'].max().date()

# Initialisation des dates dans la session state si pas déjà fait
if 'start_date' not in st.session_state:
    st.session_state.start_date = min_date
if 'end_date' not in st.session_state:
    st.session_state.end_date = max_date

# Filtres
col1, col2, col3 = st.columns(3)
with col1:
    # Date de début
    start_date = st.date_input(
        "Date de début",
        value=st.session_state.start_date,
        min_value=min_date,
        max_value=max_date,
        key="start_date_input"
    )
    # Date de fin
    end_date = st.date_input(
        "Date de fin",
        value=st.session_state.end_date,
        min_value=min_date,
        max_value=max_date,
        key="end_date_input"
    )

    # Mise à jour des dates dans la session state
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date

with col2:
    selected_products = st.multiselect(
        "Produits",
        options=sorted(df['product'].unique()),
        default=None
    )

with col3:
    selected_channels = st.multiselect(
        "Canaux de vente",
        options=sorted(df['channel'].unique()),
        default=None
    )

# Filtrage des données
mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
if selected_products:
    mask &= (df['product'].isin(selected_products))
if selected_channels:
    mask &= (df['channel'].isin(selected_channels))
filtered_df = df[mask].copy()

# Vérification que nous avons des données après filtrage
if filtered_df.empty:
    st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
else:
    # Analyses
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ventes par canal")
        channel_sales = filtered_df.groupby('channel')['revenue'].sum().reset_index()
        channel_sales['revenue'] = channel_sales['revenue'].round(2)
        fig = px.pie(
            channel_sales,
            values='revenue',
            names='channel',
            title="Répartition des ventes par canal"
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Évolution mensuelle")
        monthly_sales = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['revenue'].sum().reset_index()
        monthly_sales['date'] = monthly_sales['date'].astype(str)
        monthly_sales['revenue'] = monthly_sales['revenue'].round(2)
        fig = px.line(
            monthly_sales,
            x='date',
            y='revenue',
            title="Évolution mensuelle des ventes"
        )
        fig.update_layout(
            xaxis_title="Mois",
            yaxis_title="Chiffre d'affaires (€)"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tableau détaillé
    st.subheader("Détails des ventes")
    detailed_df = (filtered_df.groupby(['product', 'channel'])
                  .agg({
                      'revenue': ['sum', 'mean', 'count'],
                      'converted': 'mean'
                  })
                  .round(2)
                  .reset_index())

    # Renommage des colonnes pour plus de clarté
    detailed_df.columns = ['Produit', 'Canal', 'CA Total', 'CA Moyen', 'Nb Ventes', 'Taux Conversion']
    st.dataframe(detailed_df, hide_index=True)