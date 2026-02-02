import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Ebook Musculation Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INJECTION DU DESIGN PREMIUM (CSS de ton HTML) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto+Condensed:wght@300;400;700&display=swap');
    
    /* Fond global */
    .stApp { background-color: #0a0a0a; color: #ffffff; font-family: 'Roboto Condensed', sans-serif; }
    
    /* Titres Bebas Neue */
    h1, h2, h3, h4 { 
        font-family: 'Bebas Neue', cursive !important; 
        color: #dc2626; 
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Cartes sombres style Canva */
    .card-dark {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
    }

    /* Boutons dégradés rouges */
    .stButton>button {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 15px !important;
        text-transform: uppercase !important;
        width: 100%;
    }
    
    /* Cacher les éléments Streamlit inutiles */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SYSTÈME D'ACCÈS (Ton code Admin) ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

def login_screen():
    st.markdown("<h1 style='text-align: center; font-size: 4rem;'>MUSCULATION PRO</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("""
        <div class="card-dark">
            <h2 style='color: white;'>ACCÈS COMPLET - 20€</h2>
            <p>✅ Programmes PPL (6j) & Débutant (5j)</p>
            <p>✅ IA Coach & Cuisinier Personnel</p>
            <p>✅ Suivi de Poids & Mensurations</p>
            <p>✅ Accès à vie & Mises à jour</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("DÉBLOQUER VIA STRIPE"):
            st.session_state['auth'] = True
            st.rerun()

    with col2:
        st.markdown("<div class='card-dark'>", unsafe_allow_html=True)
        st.subheader("CONNEXION ADMIN")
        code = st.text_input("Entrez votre code", type="password")
        if st.button("VÉRIFIER LE CODE"):
            if code == "F12Berlinetta88170":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Code invalide")
        st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state['auth']:
    login_screen()
    st.stop()

# --- APPLICATION PRINCIPALE (NAVIGATION) ---
tabs = st.tabs(["📊 PROFIL", "🎯 OBJECTIFS", "💪 ENTRAÎNEMENT", "📋 PROGRAMMES", "🍽️ NUTRITION", "⏱️ REPOS", "🤖 IA COACH"])

# --- SECTION 1 : PROFIL ---
with tabs[0]:
    st.markdown("<h2>📊 MON PROFIL & SUIVI</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.number_input("Poids actuel (kg)", 40.0, 200.0, 75.0, key="p_actuel")
        st.number_input("Taille (cm)", 100, 230, 175)
        st.button("ENREGISTRER MES INFOS")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        df = pd.DataFrame({'Date': ['Semaine 1', 'Semaine 2', 'Semaine 3'], 'Poids': [78, 77.5, 76.9]})
        fig = px.line(df, x='Date', y='Poids', title="ÉVOLUTION DU POIDS", color_discrete_sequence=['#dc2626'])
        st.plotly_chart(fig, use_container_width=True)

# --- SECTION 3 : ENTRAÎNEMENT (FICHES TECHNIQUES) ---
with tabs[2]:
    st.markdown("<h2>💪 GUIDE DES EXERCICES</h2>", unsafe_allow_html=True)
    exo = st.selectbox("Choisir un exercice :", ["Squat", "Développé Couché", "Soulevé de Terre", "Rowing Barre"])
    
    st.markdown('<div class="card-dark">', unsafe_allow_html=True)
    if exo == "Squat":
        st.markdown("### 🦵 SQUAT (REINE DES JAMBES)")
        st.write("**Muscles :** Quadriceps, Fessiers, Gainage.")
        st.write("**Technique :** Pieds largeur d'épaules, dos droit, descendre les hanches sous les genoux.")
    elif exo == "Développé Couché":
        st.markdown("### 🏋️ DÉVELOPPÉ COUCHÉ")
        st.write("**Muscles :** Pectoraux, Triceps, Épaules.")
        st.write("**Technique :** Pieds ancrés, barre au milieu des pecs, coudes à 45°.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 5 : NUTRITION ---
with tabs[4]:
    st.markdown("<h2>🍽️ NUTRITION & CALORIES</h2>", unsafe_allow_html=True)
    col_ia, col_plan = st.columns(2)
    with col_ia:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.subheader("👨‍🍳 CUISINIER IA")
        frigo = st.text_input("Qu'as-tu dans ton frigo ?", "Poulet, Riz, Brocolis")
        if st.button("GÉNÉRER RECETTE"):
            st.success(f"Recette : Bowl Pro {frigo} - 650 kcal, 50g Protéines.")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_plan:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.subheader("📋 MENU TYPE 2300 KCAL")
        st.write("🍳 Matin : 3 oeufs, 80g avoine")
        st.write("🍗 Midi : 150g Poulet, 100g Riz")
        st.write("🐟 Soir : 150g Poisson, 250g Patate douce")
        st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 6 : REPOS & JEU ---
with tabs[5]:
    st.markdown("<h2>⏱️ TEMPS DE REPOS</h2>", unsafe_allow_html=True)
    c_time, c_game = st.columns(2)
    with c_time:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        sec = st.number_input("Régler (sec)", 30, 300, 90)
        if st.button("LANCER LE CHRONO"):
            ph = st.empty()
            for i in range(sec, -1, -1):
                ph.metric("REPOS RESTANT", f"{i}s")
                time.sleep(1)
            st.success("AU BOULOT !")
        st.markdown('</div>', unsafe_allow_html=True)
    with c_game:
        st.markdown("<h3>🎮 MINI-JEU REPOS</h3>", unsafe_allow_html=True)
        st.components.v1.html("""
        <canvas id="g" width="280" height="150" style="border:1px solid #dc2626; background:#000;"></canvas>
        <script>
        const c=document.getElementById('g'), x=c.getContext('2d');
        let y=75, v=0;
        function d(){ v+=0.1; y+=v; x.clearRect(0,0,280,150); x.fillStyle="red"; x.fillText("💪", 40, y);
        if(y>150) {y=75; v=0;} requestAnimationFrame(d); }
        window.onclick=()=>v=-3; d();
        </script>
        """, height=200)

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("🔥 **BODYTRACK PRO v1.5**")
