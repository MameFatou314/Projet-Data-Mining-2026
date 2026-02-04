import streamlit as st
import pandas as pd

def run_rfm(data):
    st.subheader("💎 Segmentation RFM")

    snapshot_date = data['InvoiceDate'].max()

    rfm = data.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'count',
        'TotalPrice': 'sum'
    })

    rfm.columns = ['Recency', 'Frequency', 'Monetary']

    rfm['R'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
    rfm['F'] = pd.qcut(rfm['Frequency'], 4, labels=[1,2,3,4])
    rfm['M'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])

    rfm['RFM_Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)

    st.write("📌 Résultats RFM")
    st.dataframe(rfm.head())
