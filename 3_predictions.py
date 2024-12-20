# 3_predictions.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="Prédictions", page_icon="🔮", layout="wide")
st.title("🔮 Prédictions et tendances")

# Chargement des données
df = load_data()

# Préparation des données pour les prédictions
df['month_num'] = df['date'].dt.year * 12 + df['date'].dt.month
monthly_sales = df.groupby('month_num')['revenue'].sum().reset_index()

# Modèle simple de prédiction
X = monthly_sales['month_num'].values.reshape(-1, 1)
y = monthly_sales['revenue'].values

model = LinearRegression()
model.fit(X, y)

# Prédiction pour les 6 prochains mois
future_months = np.array(range(X[-1][0] + 1, X[-1][0] + 7)).reshape(-1, 1)
predictions = model.predict(future_months)

# Création du DataFrame pour l'affichage
forecast_df = pd.DataFrame({
    'month_num': future_months.flatten(),
    'revenue': predictions,
    'type': 'Prédiction'
})

historical_df = pd.DataFrame({
    'month_num': X.flatten(),
    'revenue': y,
    'type': 'Historique'
})

plot_df = pd.concat([historical_df, forecast_df])

# Affichage des prédictions
st.subheader("Prévisions des ventes")
fig = px.line(
    plot_df,
    x='month_num',
    y='revenue',
    color='type',
    title="Prévisions des ventes pour les 6 prochains mois",
    labels={'revenue': 'Chiffre d\'affaires', 'month_num': 'Mois'}
)
st.plotly_chart(fig, use_container_width=True)

# Métriques de prédiction
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Chiffre d'affaires prévu (prochain mois)",
        f"{predictions[0]:,.0f} €",
        f"{((predictions[0] - y[-1]) / y[-1] * 100):.1f}%"
    )

with col2:
    st.metric(
        "Croissance moyenne prévue",
        f"{((predictions[-1] - predictions[0]) / predictions[0] * 100):.1f}%",
        "Tendance sur 6 mois"
    )

# Indicateurs de confiance
st.subheader("Indicateurs de confiance")
confidence = model.score(X, y)
st.progress(confidence)
st.caption(f"R² Score: {confidence:.2f}")