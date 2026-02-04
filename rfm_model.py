import streamlit as st
import pandas as pd
import datetime as dt

def run_rfm(data):
    st.header("💳 Analyse RFM")

    # --- 1. NETTOYAGE STRICT ---
    df = data.copy()
    df = df.dropna(subset=['CustomerID'])
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    df = df[~df['InvoiceNo'].astype(str).str.contains('C', na=False)]
    
    # Conversion date
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Date de référence = Max du dataset + 1 jour
    ref_date = df['InvoiceDate'].max() + dt.timedelta(days=1)

    # --- 2. CALCUL RFM ---
    df['TotalSum'] = df['Quantity'] * df['UnitPrice']
    
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (ref_date - x.max()).days,
        'InvoiceNo': 'nunique', # Utiliser nunique pour compter les factures uniques
        'TotalSum': 'sum'
    }).reset_index()

    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

    # --- 3. SCORING (IDENTIQUE NOTEBOOK) ---
    # R score : labels=[5, 4, 3, 2, 1] car petite récence = meilleur score
    rfm["R_score"] = pd.qcut(rfm["Recency"].rank(method='first'), 5, labels=["5", "4", "3", "2", "1"]).astype(str)
    
    # F et M score : labels=[1, 2, 3, 4, 5] car grosse fréquence/valeur = meilleur score
    rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method='first'), 5, labels=["1", "2", "3", "4", "5"]).astype(str)
    rfm["M_score"] = pd.qcut(rfm["Monetary"].rank(method='first'), 5, labels=["1", "2", "3", "4", "5"]).astype(str)

    rfm["RFM_Score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

    # --- 4. SEGMENTATION ---
    def segment_rfm(row):
        if row["R_score"] == "5" and row["F_score"] == "5" and row["M_score"] == "5":
            return "Clients champions"
        elif row["R_score"] >= "4" and row["F_score"] >= "4":
            return "Clients fidèles"
        elif row["R_score"] >= "4":
            return "Clients récents"
        elif row["F_score"] >= "4":
            return "Clients fréquents"
        elif row["M_score"] >= "4":
            return "Clients à forte valeur"
        elif row["R_score"] <= "2":
            return "Clients à risque"
        else:
            return "Clients standards"

    rfm["Segment"] = rfm.apply(segment_rfm, axis=1)

    # --- 5. AFFICHAGE ---
    st.write("### Tableau RFM final")
    st.dataframe(rfm.head(10))
    
    # Distribution des segments
    st.write("### Répartition des segments")
    st.bar_chart(rfm['Segment'].value_counts())