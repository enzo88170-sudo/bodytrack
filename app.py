import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- CONFIGURATION & DESIGN ---
st.set_page_config(page_title="BodyTrack Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0f0f0f; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 2px solid #e60000; }
    h1, h2, h3 { color: #e60000; font-family: 'Arial Black'; }
    .stButton>button { background-color: #e60000; color: white; width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SECURITE : CODE ADMIN CACHÉ ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

def verifier_acces():
    st.image("https://i.imgur.com/wlyusJ0.png", width=150)
    st.title("🔴 BODYTRACK PRO - ACCÈS")
    code = st.text_input("Entrez le code d'accès ou Admin", type="password")
    if st.button("Débloquer l'Ebook (20€)"):
        if code == "F12Berlinetta88170": # Ton code admin
            st.session_state['auth'] = True
            st.rerun()
        else:
            st.error("Code invalide ou paiement requis.")

if not st.session_state['auth']:
    verifier_acces()
    st.stop()

# --- NAVIGATION ---
menu = ["👤 Profil", "📈 Entraînement", "🎯 Objectifs", "📅 Calendrier", "⏱️ Repos & Jeu", "🥗 Nutrition", "🤖 IA Coach"]
page = st.sidebar.selectbox("Menu Principal", menu)

# --- ONGLET PROFIL ---
if page == "👤 Profil":
    st.header("Mon Profil Sportif")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Âge", 14, 99)
        taille = st.number_input("Taille (cm)", 100, 250)
        poids_actuel = st.number_input("Poids (kg)", 30.0, 200.0)
    with col2:
        mail = st.text_input("Email")
        exo_pref = st.text_input("Exercice Préféré")
    
    st.subheader("Suivi du Poids")
    # Simulation de données pour le graphique en points
    data = pd.DataFrame({'Date': ['01/01', '08/01', '15/01'], 'Poids': [80.0, 79.5, 78.8]})
    fig = px.scatter(data, x='Date', y='Poids', title="Évolution du poids", color_discrete_sequence=['#e60000'])
    st.plotly_chart(fig)

# --- ONGLET REPOS & JEU ---
elif page == "⏱️ Repos & Jeu":
    st.header("Chronomètre de Repos")
    t = st.number_input("Secondes :", value=90)
    if st.button("Lancer le repos"):
        prog = st.progress(100)
        for i in range(t, 0, -1):
            time.sleep(1)
            prog.progress(int((i/t)*100))
        st.success("🔥 TEMPS DE REPOS TERMINÉ, RETOUR AU CHARBON !")
    
    st.markdown("---")
    st.subheader("🕹️ Mini-jeu : Biceps Space (Flappy)")
    st.info("Utilisez les flèches pour faire voler le biceps entre les planètes (En cours de développement)")

# --- ONGLET NUTRITION ---
elif page == "🥗 Nutrition":
    st.header("Cuisinier IA & Macros")
    if st.button("Générer une recette (2300 kcal)"):
        st.code("""
        MENU DU JOUR :
        - Matin : Bowlcake Avoine/Chocolat (550 kcal)
        - Midi : Poulet Curry, Riz Basmati, Courgettes (750 kcal)
        - Soir : Pavé de Saumon, Patates douces (1000 kcal)
        """)

# --- BOUTON TÉLÉCHARGEMENT ---
st.sidebar.markdown("---")
if st.sidebar.button("📲 Télécharger l'App"):
    st.info("Pour installer : \n1. Chrome (Android) : Menu > Installer l'app\n2. Safari (iOS) : Partager > Sur l'écran d'accueil")
