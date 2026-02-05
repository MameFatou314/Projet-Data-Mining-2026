import streamlit as st
import base64

def get_base64_of_bin_file(bin_file):
    """Convertit l'image locale en base64 pour le CSS"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def apply_magnificent_style(only_home=False):
    """Applique le design global avec gestion de l'image de fond"""
    if only_home:
        try:
            bin_str = get_base64_of_bin_file('home_img.jpeg')
            st.markdown(f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), 
                                  url("data:image/jpeg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """, unsafe_allow_html=True)
        except:
            st.markdown("<style>.stApp {{ background-color: #f8faff; }}</style>", unsafe_allow_html=True)
    else:
        st.markdown("<style>.stApp {{ background-color: #ffffff; }}</style>", unsafe_allow_html=True)

    # Style des textes (Poppins)
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
        .main-title {{ font-size: 45px; font-weight: 800; color: #1e3a8a; text-align: center; }}
        .custom-subtitle {{ text-align: center; font-size: 20px; color: #475569; margin-bottom: 30px; }}
        </style>
    """, unsafe_allow_html=True)

# CETTE FONCTION MANQUAIT ET CAUSAIT L'ERREUR :
def show_page_title(title, subtitle):
    """Affiche le titre et le sous-titre stylisés sur chaque page"""
    st.markdown(f'<p class="main-title">{title}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="custom-subtitle">✨ {subtitle}</p>', unsafe_allow_html=True)