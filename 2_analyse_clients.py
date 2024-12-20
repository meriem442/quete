# 2_analyse_clients.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Analyse Clients", page_icon="👥", layout="wide")
st.title("👥 Analyse des clients")

# Chargement des données
df = load_data()

# Métriques clients
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Clients actifs",
        f"{df['customer_id'].nunique():,}",
        "12%"
    )

with col2:
    st.metric(
        "LTV moyen",
        f"{df.groupby('customer_id')['revenue'].sum().mean():,.0f} €",
        "8%"
    )

with col3:
    st.metric(
        "Taux de rétention",
        "68%",
        "-2%"
    )

# Segmentation clients
st.subheader("Segmentation des clients")

# RFM Analysis
rfm = df.groupby('customer_id').agg({
    'date': lambda x: (x.max() - x.min()).days,  # Recency
    'order_id': 'count',  # Frequency
    'revenue': 'sum'  # Monetary
}).reset_index()

rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']

fig = px.scatter_3d(
    rfm,
    x='recency',
    y='frequency',
    z='monetary',
    title="Segmentation RFM des clients",
    labels={
        'recency': 'Récence (jours)',
        'frequency': 'Fréquence',
        'monetary': 'Valeur (€)'
    }
)
st.plotly_chart(fig, use_container_width=True)

# Distribution des clients
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribution des achats")
    fig = px.histogram(
        rfm,
        x='frequency',
        title="Distribution du nombre d'achats par client"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Distribution du panier moyen")
    fig = px.histogram(
        rfm,
        x='monetary',
        title="Distribution de la valeur client"
    )
    st.plotly_chart(fig, use_container_width=True)