import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

def run_kmeans(data):
    st.subheader("📦 Segmentation Clients - K-means")

    cols = st.multiselect(
        "Choisir les variables",
        data.select_dtypes(include=['int64', 'float64']).columns
    )

    k = st.slider("Nombre de clusters", 2, 10, 4)

    if len(cols) >= 2:
        X = data[cols]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = KMeans(n_clusters=k, n_init=10, random_state=42)
        clusters = model.fit_predict(X_scaled)

        data['Cluster'] = clusters

        st.write("📌 Résumé des clusters")
        st.dataframe(data.groupby('Cluster')[cols].mean())
    else:
        st.warning("Sélectionnez au moins deux variables")
