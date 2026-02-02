import streamlit as st
import pandas as pd
import plotly.express as px
import time
import streamlit.components.v1 as components
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="BODYTRACK PRO", page_icon="💪", layout="wide")

# --- INITIALISATION DES VARIABLES ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'poids_history' not in st.session_state: st.session_state['poids_history'] = {'Date': [], 'Poids': []}

# --- FONCTION D'INTÉGRATION CANVA ---
def afficher_canva(lien_embed, hauteur=800):
    # On s'assure que le lien finit par ?embed pour l'affichage
    if "view?embed" not in lien_embed:
        lien_embed = lien_embed.replace("/view", "/view?embed")
    
    components.html(
        f"""
        <iframe loading="lazy" 
            style="width: 100%; height: {hauteur}px; border: none; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.5);" 
            src="{lien_embed}" 
            allowfullscreen="allowfullscreen" 
            allow="fullscreen">
        </iframe>
        """,
        height=hauteur,
    )

# --- DESIGN CSS NOIR & ROUGE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@400;700&display=swap');
    .stApp { background-color: #0a0a0a; color: #ffffff; font-family: 'Roboto', sans-serif; }
    h1, h2, h3 { font-family: 'Bebas Neue', cursive; color: #dc2626; letter-spacing: 2px; }
    .stButton>button { background-color: #dc2626; color: white; border-radius: 8px; font-weight: bold; border: none; width: 100%; height: 3em; transition: 0.3s; }
    .stButton>button:hover { background-color: #ff0000; transform: scale(1.02); }
    [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #dc2626; }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTÈME D'ACCÈS ---
if not st.session_state['auth']:
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🔴 ACCÈS BODYTRACK PREMIUM</h1>", unsafe_allow_html=True)
    st.image("https://i.imgur.com/wlyusJ0.png", width=200)
    
    col_pay, col_admin = st.columns(2)
    with col_pay:
        st.markdown("### ÉBOOK COMPLET - 20€")
        st.write("Programmes, Nutrition IA, Suivi de Force et plus encore.")
        if st.button("DÉBLOQUER VIA STRIPE"):
            st.session_state['auth'] = True
            st.rerun()
            
    with col_admin:
        st.markdown("### CODE ACCÈS")
        code_input = st.text_input("Entrez votre code", type="password")
        if st.button("S'IDENTIFIER"):
            if code_input == "F12Berlinetta88170":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Code invalide.")
    st.stop()

# --- NAVIGATION ---
with st.sidebar:
    st.image("https://i.imgur.com/wlyusJ0.png", width=120)
    menu = st.radio("NAVIGATION", [
        "📊 Profil & Suivi", 
        "💪 Entraînement", 
        "📋 Programmes", 
        "🍽️ Nutrition", 
        "⏱️ Repos & Jeu", 
        "📱 Installation"
    ])

# ==========================================
# 1. PROFIL & SUIVI
# ==========================================
if menu == "📊 Profil & Suivi":
    st.header("📊 MON PROFIL")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Nom / Pseudo")
        p_val = st.number_input("Poids actuel (kg)", 40.0, 150.0, 75.0)
        if st.button("ENREGISTRER PESÉE"):
            now = datetime.now().strftime("%d/%m")
            st.session_state['poids_history']['Date'].append(now)
            st.session_state['poids_history']['Poids'].append(p_val)
            st.success("Donnée enregistrée !")
            
    with c2:
        if st.session_state['poids_history']['Poids']:
            df = pd.DataFrame(st.session_state['poids_history'])
            fig = px.line(df, x='Date', y='Poids', title="ÉVOLUTION DU POIDS", markers=True)
            fig.update_traces(line_color='#dc2626')
            st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 2. ENTRAÎNEMENT (CANVA)
# ==========================================
elif menu == "💪 Entraînement":
    st.header("💪 TECHNIQUE DES EXERCICES")
    st.write("Consulte tes fiches techniques interactives :")
    # Emplacement pour ton Canva Technique
    lien_tech = "https://www.canva.com/design/DAG_QbeW4SU/jqXSEY7jaMUEBLxttSGZRQ/view"
    afficher_canva(lien_tech, hauteur=800)

# ==========================================
# 3. PROGRAMMES (CANVA)
# ==========================================
elif menu == "📋 Programmes":
    st.header("📋 TES PROGRAMMES")
    # Emplacement pour ton Canva Programmes
    lien_prog = "https://www.canva.com/design/DAG_QbeW4SU/jqXSEY7jaMUEBLxttSGZRQ/view"
    afficher_canva(lien_prog, hauteur=900)

# ==========================================
# 4. NUTRITION (TON LIEN CANVA)
# ==========================================
elif menu == "🍽️ Nutrition":
    st.header("🍽️ NUTRITION & MENUS")
    st.write("Voici tes menus personnalisés :")
    # TON LIEN SPÉCIFIQUE
    lien_nutri = "https://www.canva.com/design/DAG_QbeW4SU/jqXSEY7jaMUEBLxttSGZRQ/view"
    afficher_canva(lien_nutri, hauteur=800)

# ==========================================
# 5. REPOS & JEU
# ==========================================
elif menu == "⏱️ Repos & Jeu":
    st.header("⏱️ CHRONO & DIVERTISSEMENT")
    col_t, col_g = st.columns(2)
    with col_t:
        sec = st.number_input("Repos (secondes)", 30, 300, 90)
        if st.button("LANCER LE REPOS"):
            placeholder = st.empty()
            for i in range(sec, -1, -1):
                placeholder.write(f"## ⏳ {i}s")
                time.sleep(1)
            st.error("🚨 TEMPS DE REPOS TERMINÉ ! AU BOULOT !")
    with col_g:
        st.subheader("🎮 FLAPPY BICEPS")
        st.components.v1.html("""
        <canvas id='g' width='300' height='200' style='border:1px solid #dc2626; background:black;'></canvas>
        <script>
        var c=document.getElementById('g').getContext('2d'), y=100, v=0;
        function draw(){ v+=0.1; y+=v; c.clearRect(0,0,300,200); c.fillStyle='white'; c.fillText('💪', 50, y);
        if(y>200){y=100; v=0;} requestAnimationFrame(draw); }
        window.onclick=()=>v=-3; draw();
        </script>
        """, height=250)

# ==========================================
# 6. INSTALLATION MOBILE
# ==========================================
elif menu == "📱 Installation":
    st.header("📱 INSTALLER L'APPLICATION")
    st.write("Transformez cet ebook en application mobile :")
    
    st.markdown("""
    ### 🍎 iOS (iPhone/iPad)
    1. Ouvrez ce lien dans **Safari**.
    2. Cliquez sur le bouton **Partager** (carré avec flèche).
    3. Faites défiler et cliquez sur **Sur l'écran d'accueil**.

    ### 🤖 Android
    1. Ouvrez ce lien dans **Chrome**.
    2. Cliquez sur les **3 points** en haut à droite.
    3. Cliquez sur **Installer l'application** ou **Ajouter à l'écran d'accueil**.
    """)
