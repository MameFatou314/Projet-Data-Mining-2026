import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from style_utils import apply_magnificent_style, show_page_title

# Configuration de la page
st.set_page_config(page_title="Types de Models", layout="wide", page_icon="🚀")

# Menu latéral
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>🚀 Types de Models</h2>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Analyse Descriptive", "APRIORI", "K-means", "RFM"],
        icons=["bar-chart", "cart-check", "diagram-3", "people"],
        default_index=0,
        styles={
            "nav-link-selected": {"background-color": "#1e3a8a"},
        }
    )
    
    st.divider()
    file = st.file_uploader("📂 Charger les données (CSV ou Excel)", type=["csv", "xlsx"])

# LOGIQUE D'AFFICHAGE
if file is not None:
    # --- STYLE POUR LES PAGES DE TRAVAIL (SANS IMAGE) ---
    apply_magnificent_style(only_home=False)

    @st.cache_data
    def load_data(f):
        if f.name.endswith(".csv"):
            return pd.read_csv(f, encoding='ISO-8859-1')
        return pd.read_excel(f)
    
    data = load_data(file)

    if selected == "Analyse Descriptive":
     #   show_page_title("Analyse Descriptive", "Visualisation et exploration des données")
      #  st.subheader("🔍 Aperçu du Dataset")
       # st.dataframe(data.head(15), use_container_width=True)

     if selected == "Analyse Descriptive":
      from analyse_Descriptive import run_analyse_descriptive
     run_analyse_descriptive(data) # <--- 'data' doit être entre parenthèses

    elif selected == "APRIORI":
        show_page_title("Modèle APRIORI", "Règles d'association")
        from apriori_model import run_apriori
        run_apriori(data)

    elif selected == "K-means":
        show_page_title("Segmentation K-means", "Regroupement des clients")
        from kmeans_model import run_kmeans
        run_kmeans(data)

    elif selected == "RFM":
        show_page_title("Segmentation RFM", "Analyse de la fidélité")
        from rfm_model import run_rfm
        run_rfm(data)
else:
    # --- STYLE POUR L'ACCUEIL (AVEC IMAGE DE FOND) ---
    apply_magnificent_style(only_home=True)
    
    # Espace pour descendre le texte au milieu de l'image
    st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)
    
    # Affichage du Titre et Sous-titre centrés via style_utils
    show_page_title("ANALYSE DES DONNÉES E-COMMERCE", "Exploration et Segmentation du Catalogue")

    # Conteneur pour le message de bienvenue centré
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <p style="font-size: 1.2rem; color: #1e3a8a; background-color: rgba(255,255,255,0.7); padding: 20px; border-radius: 15px;">
                    👋 <b>Bienvenue !</b><br>
                    Veuillez charger votre base de données dans le menu latéral pour activer l'analyse et supprimer l'image de fond.
                </p>
            </div>
        """, unsafe_allow_html=True)