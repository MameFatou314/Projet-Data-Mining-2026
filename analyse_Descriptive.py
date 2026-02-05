import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_analyse_descriptive(df):
    """Affiche l'analyse brute, puis propose le nettoyage"""
    
    # --- TITRE DE LA SECTION ---
    st.markdown("### 📋 Exploration des données brutes (Avant nettoyage)")
    st.write("Cette étape permet d'identifier la qualité initiale de votre fichier CSV/Excel.")

    # --- 1. INDICATEURS DE STRUCTURE ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Lignes totales", f"{df.shape[0]:,}")
    with col2:
        st.metric("Colonnes", df.shape[1])
    with col3:
        # On vérifie si les colonnes nécessaires existent pour le C.A.
        if "UnitPrice" in df.columns and "Quantity" in df.columns:
            ca_brut = (df["UnitPrice"] * df["Quantity"]).sum()
            st.metric("Valeur Brute Totale", f"{ca_brut:,.0f} €")

    st.divider()

    # --- 2. IDENTIFICATION DES ANOMALIES ---
    st.subheader("⚠️ Diagnostic de la base")
    
    # Calcul des erreurs potentielles
    neg_qty = df[df['Quantity'] < 0].shape[0] if 'Quantity' in df.columns else 0
    neg_price = df[df['UnitPrice'] < 0].shape[0] if 'UnitPrice' in df.columns else 0
    missing_cust = df['CustomerID'].isnull().sum() if 'CustomerID' in df.columns else 0
    doublons = df.duplicated().sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.error(f"Retours/Négatifs\n\n**{neg_qty}**")
    c2.error(f"Prix aberrants\n\n**{neg_price}**")
    c3.warning(f"Clients inconnus\n\n**{missing_cust}**")
    c4.warning(f"Doublons\n\n**{doublons}**")

    # --- 3. DISTRIBUTIONS BRUTES ---
    st.subheader("📊 Visualisation des écarts (Boxplots)")
    col_x, col_y = st.columns(2)
    
    with col_x:
        if 'Quantity' in df.columns:
            fig, ax = plt.subplots(figsize=(5, 2))
            sns.boxplot(x=df['Quantity'], color='#1e3a8a', ax=ax)
            ax.set_title("Dispersion des Quantités")
            st.pyplot(fig)

    with col_y:
        if 'UnitPrice' in df.columns:
            fig, ax = plt.subplots(figsize=(5, 2))
            sns.boxplot(x=df['UnitPrice'], color='#ef4444', ax=ax)
            ax.set_title("Dispersion des Prix")
            st.pyplot(fig)

    # --- 4. STATISTIQUES ET APERÇU ---
    with st.expander("📂 Voir les statistiques descriptives complètes"):
        st.dataframe(df.describe(), use_container_width=True)
    
    st.divider()

    # --- 5. BOUTON POUR PASSER À L'ANALYSE NETTOYÉE ---
    st.subheader("🚀 Analyse Décisionnelle (Données filtrées)")
    if st.checkbox("Cliquer ici pour nettoyer les données et voir l'analyse pertinente"):
        # Nettoyage
        df_clean = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)].drop_duplicates().copy()
        
        st.success(f"Données nettoyées ! Il reste {df_clean.shape[0]:,} lignes valides.")
        
        # Ici on peut ajouter les graphiques pertinents (Top 10, Pays, etc.)
        st.bar_chart(df_clean['Description'].value_counts().head(10))