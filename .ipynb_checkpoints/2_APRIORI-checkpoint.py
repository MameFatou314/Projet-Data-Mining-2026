import streamlit as st
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

def run_apriori(data):
    st.subheader("🔗 Règles d'association - APRIORI")

    min_support = st.slider("Support minimum", 0.01, 0.2, 0.02)
    min_confidence = st.slider("Confiance minimum", 0.1, 1.0, 0.5)

    # Encodage one-hot attendu
    basket = data.groupby(['InvoiceNo', 'Description'])['Quantity'] \
                 .sum().unstack().fillna(0)

    basket = basket.applymap(lambda x: 1 if x > 0 else 0)

    frequent_itemsets = apriori(
        basket,
        min_support=min_support,
        use_colnames=True
    )

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence
    )

    st.write("📌 Règles générées")
    st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
