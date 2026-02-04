import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

def run_apriori(data):
    st.header("🛒 Tableau de bord Apriori")
    
    # --- 1. NETTOYAGE (Strictement selon votre document) ---
    df = data.copy()
    # Suppression des CustomerID manquants
    df = df.dropna(subset=['CustomerID']) 
    
    # Filtrage : Quantité > 0, Prix > 0 et pas d'annulations ('C')
    df_clean = df[
        (df['Quantity'] > 0) & 
        (df['UnitPrice'] > 0) & 
        (~df['InvoiceNo'].astype(str).str.contains('C', na=False))
    ].copy()
    
    # Sélection des colonnes et formatage StockCode
    df_clean["StockCode"] = df_clean["StockCode"].astype(str).str.strip()

    # --- 2. ENCODAGE ---
    # Construction des transactions
    transactions = df_clean.groupby("InvoiceNo")["StockCode"].apply(lambda x: list(set(x))).tolist()
    
    # Encodage
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    base_encoded = pd.DataFrame(te_array, columns=te.columns_)
    
    # Suppression des codes non-commerciaux (Indispensable pour avoir 3676 colonnes)
    cols_a_supprimer = ['POST', 'PADS', 'DOT', 'M', 'BANK CHARGES', 'D', 'CRUK', 'C2']
    base_encoded = base_encoded.drop(columns=[c for c in cols_a_supprimer if c in base_encoded.columns])

    # Affichage des métriques de contrôle
    col1, col2, col3 = st.columns(3)
    col1.metric("Lignes après nettoyage", len(df_clean))
    col2.metric("Transactions (Lignes)", base_encoded.shape[0])
    col3.metric("Produits (Colonnes)", base_encoded.shape[1])

    # --- 3. ALGORITHME ---
    if st.button("Lancer l'analyse et comparer"):
        with st.spinner('Calcul en cours...'):
            frequent_itemsets = apriori(base_encoded, min_support=0.02, use_colnames=True)
            
            if not frequent_itemsets.empty:
                # Génération des règles (Seuil 0.3)
                rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)
                
                # Filtrage final (Confiance >= 0.5 et Lift > 1)
                rules_interessantes = rules[(rules["confidence"] >= 0.5) & (rules["lift"] > 1)].copy()
                
                if not rules_interessantes.empty:
                    # Formatage pour affichage
                    rules_interessantes["antecedents"] = rules_interessantes["antecedents"].apply(lambda x: list(x))
                    rules_interessantes["consequents"] = rules_interessantes["consequents"].apply(lambda x: list(x))
                    
                    st.success(f"✅ {len(rules_interessantes)} règles trouvées.")
                    
                    # Tri par Lift comme dans le notebook
                    res = rules_interessantes[['antecedents', 'consequents', 'support', 'confidence', 'lift']].sort_values(by='lift', ascending=False)
                    st.dataframe(res)
                else:
                    st.warning("Aucune règle ne respecte les filtres (Conf >= 0.5, Lift > 1).")
            else:
                st.error("Aucun itemset trouvé. Essayez de baisser le support.")