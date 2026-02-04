import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def run_kmeans(data):
    st.subheader("📊 Segmentation des clients (Variables Notebook)")

    # =========================
    # 1. Nettoyage (identique au notebook)
    # =========================
    data = data.dropna(subset=["CustomerID", "Quantity", "UnitPrice"])
    data = data[(data["Quantity"] > 0) & (data["UnitPrice"] > 0)]

    # =========================
    # 2. Création des variables du Notebook
    # =========================
    # On agrège pour obtenir la Quantité Totale et le Prix Unitaire Moyen par client
    customer_data = data.groupby("CustomerID").agg({
        "Quantity": "sum",
        "UnitPrice": "mean"
    })

    # On renomme pour correspondre au notebook
    customer_data.columns = ["QuantiteTotal", "PrixUnitaireMoyen"]

    # =========================
    # 3. Normalisation
    # =========================
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(customer_data)

    # =========================
    # 4. Paramétrage K-means
    # =========================
    k = st.slider("🔢 Nombre de clusters", min_value=2, max_value=6, value=3)
    
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    clusters = model.fit_predict(X_scaled)
    customer_data["Cluster"] = clusters

    # =========================
    # 5. Visualisation (Style Notebook)
    # =========================
    st.write("### 📈 Visualisation des segments")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Définition des noms si k=3 (comme dans votre notebook)
    if k == 3:
        noms_clusters = {0: "Clients Standards", 1: "Acheteurs de Luxe", 2: "Grossistes"}
    else:
        noms_clusters = {i: f"Cluster {i}" for i in range(k)}

    scatter = ax.scatter(
        customer_data['QuantiteTotal'], 
        customer_data['PrixUnitaireMoyen'], 
        c=customer_data['Cluster'], 
        cmap='viridis',
        alpha=0.6
    )

    ax.legend(handles=scatter.legend_elements()[0], labels=list(noms_clusters.values()))
    ax.set_xlabel("Quantité totale achetée")
    ax.set_ylabel("Prix moyen unitaire")
    ax.set_title(f"Segmentation K-means (k={k})")
    ax.grid(True, linestyle='--', alpha=0.5)

    st.pyplot(fig)

    # =========================
    # 6. Tableaux de données
    # =========================
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📌 **Aperçu des données**")
        st.dataframe(customer_data.head())

    with col2:
        st.write("📊 **Moyennes par cluster**")
        st.dataframe(customer_data.groupby("Cluster").mean())

    return customer_data