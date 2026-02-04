import streamlit as st
import pandas as pd
from apriori_model import run_apriori
from kmeans_model import run_kmeans
from rfm_model import run_rfm

st.set_page_config(page_title="Projet Data Mining 2026", layout="wide")

st.title("🚀 Application de Data Mining – E-commerce")

# 1. Menu latéral
menu = st.sidebar.selectbox(
    "Choisir une analyse", 
    ["Analyse descriptive", "APRIORI", "K-means", "RFM"]
)

# 2. Chargement du fichier
file = st.sidebar.file_uploader("Charger un fichier CSV ou Excel", type=["csv", "xlsx"])

if file is not None:
    # Lecture du fichier
    if file.name.endswith(".csv"):
        data = pd.read_csv(file, encoding='ISO-8859-1', low_memory=False)
    else:
        data = pd.read_excel(file)

    # 3. Logique d'affichage (Vérifiez bien l'alignement ici)
    if menu == "Analyse descriptive":
        st.subheader("📊 Aperçu des données")
        st.write(data.head())
        st.write("Dimensions du fichier brut :", data.shape)
    
    elif menu == "APRIORI":
        run_apriori(data)

    elif menu == "K-means":
        st.info("Module K-means sélectionné")
        run_kmeans(data) 

    elif menu == "RFM":
        st.info("Module RFM sélectionné")
        run_rfm(data) # L'espace en trop a été supprimé ici
        
else:
    st.info("Veuillez charger un fichier pour commencer")