import pickle

import os

os.makedirs("models", exist_ok=True)

with open("models/apriori_rules.pkl", "wb") as f:

|

pickle.dump(rules, f)

Astou Leye
23 h 57
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Analyse descriptive des données e-commerce")

st.markdown("""
Cette page permet d’explorer la base de données e-commerce
avant l’application des modèles de Data Mining.
""")

# Upload du fichier
uploaded_file = st.file_uploader(
    "📂 Charger la base de données (CSV ou Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Lecture du fichier
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Base de données chargée avec succès")

    # Aperçu
    st.subheader("🔍 Aperçu des données")
    st.dataframe(df.head())

    # Dimensions
    st.subheader("📐 Dimensions de la base")
    st.write(f"Nombre de lignes : {df.shape[0]}")
    st.write(f"Nombre de colonnes : {df.shape[1]}")

    # Types de données
    st.subheader("📊 Types des variables")
    st.dataframe(df.dtypes)

    # Statistiques descriptives
    st.subheader("📉 Statistiques descriptives")
    st.dataframe(df.describe())

    # Visualisation simple
    if "Quantity" in df.columns:
        st.subheader("📦 Distribution des quantités")
        plt.figure()
        df["Quantity"].hist(bins=30)
        plt.xlabel("Quantité")
        plt.ylabel("Fréquence")
        st.pyplot(plt)

    if "UnitPrice" in df.columns:
        st.subheader("💰 Distribution des prix unitaires")
        plt.figure()
        df["UnitPrice"].hist(bins=30)
        plt.xlabel("Prix unitaire")
        plt.ylabel("Fréquence")
        st.pyplot(plt)

else:
    st.warning("Veuillez charger un fichier pour commencer l’analyse.")