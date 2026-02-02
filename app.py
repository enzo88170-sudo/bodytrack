import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# ==========================================
# 0. INITIALISATION & PERSISTANCE
# ==========================================
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
if 'historique_poids' not in st.session_state:
    st.session_state['historique_poids'] = {'Date': [], 'Poids': []}

# ==========================================
# 1. CONFIGURATION & DESIGN
# ==========================================
st.set_page_config(page_title="BodyTrack Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto+Condensed:wght@400;700&display=swap');
    .stApp { background-color: #0a0a0a; color: #ffffff; font-family: 'Roboto Condensed', sans-serif; }
    h1, h2, h3 { font-family: 'Bebas Neue', cursive !important; color: #dc2626; letter-spacing: 2px; }
    .card-dark { background: #1a1a1a; border: 1px solid #333; border-radius: 16px; padding: 25px; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important; color: white !important; border-radius: 12px !important; font-weight: 700 !important; width: 100%; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SYSTÈME D'ACCÈS
# ==========================================
if not st.session_state['auth']:
    st.markdown("<h1 style='text-align: center; font-size: 4rem;'>BODYTRACK PRO</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card-dark"><h2>OFFRE PREMIUM</h2><p>Accès illimité aux programmes, vidéos et IA Coach.</p><h3>20€ / UNIQUE</h3></div>', unsafe_allow_html=True)
        if st.button("DÉBLOQUER L'ACCÈS"):
            st.session_state['auth'] = True
            st.rerun()
    with col2:
        st.markdown('<div class="card-dark"><h3>ADMINISTRATION</h3></div>', unsafe_allow_html=True)
        code = st.text_input("Code Secret", type="password")
        if st.button("S'IDENTIFIER"):
            if code == "F12Berlinetta88170":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# ==========================================
# 3. NAVIGATION PRINCIPALE
# ==========================================
tabs = st.tabs(["📊 PROFIL", "💪 TECHNIQUE", "📋 PROGRAMMES", "🍽️ NUTRITION", "⏱️ REPOS", "🤖 IA COACH"])

# --- ONGLET PROFIL ---
with tabs[0]:
    st.markdown("<h2>📊 SUIVI DE PROGRESSION</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        p_val = st.number_input("Poids (kg)", 40.0, 150.0, 75.0)
        if st.button("ENREGISTRER LA PESÉE"):
            st.session_state['historique_poids']['Date'].append(datetime.now().strftime("%d/%m"))
            st.session_state['historique_poids']['Poids'].append(p_val)
            st.success("Poids enregistré !")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.session_state['historique_poids']['Poids']:
            fig = px.line(st.session_state['historique_poids'], x='Date', y='Poids', title="ÉVOLUTION", color_discrete_sequence=['#dc2626'])
            st.plotly_chart(fig, use_container_width=True)

# --- ONGLET TECHNIQUE (VIDÉOS) ---
with tabs[1]:
    st.markdown("<h2>💪 GUIDE TECHNIQUE VIDÉO</h2>", unsafe_allow_html=True)
    exo = st.selectbox("Choisir l'exercice :", ["Squat", "Développé Couché", "Soulevé de Terre"])
    
    st.markdown('<div class="card-dark">', unsafe_allow_html=True)
    if exo == "Squat":
        st.video("https://www.youtube.com/watch?v=ULT9C93f0bQ")
        st.write("**Focus :** Quadriceps et Fessiers. Gardez le dos plat et descendez sous la parallèle.")
        
    elif exo == "Développé Couché":
        st.video("https://www.youtube.com/watch?v=gG-u_XzT3OQ")
        st.write("**Focus :** Pectoraux. Sortez la poitrine et gardez les omoplates serrées.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- ONGLET NUTRITION (CUISINIER IA) ---
with tabs[3]:
    st.markdown("<h2>🍽️ CUISINIER IA & MENUS</h2>", unsafe_allow_html=True)
    col_ia, col_menu = st.columns(2)
    with col_ia:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        ing = st.text_input("Tes ingrédients (ex: poulet, riz) :")
        if st.button("GÉNÉRER RECETTE"):
            st.info(f"IA suggère : Émincé de {ing} aux épices cajun. (650 kcal)")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_menu:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.write("**MENU TYPE 2300 KCAL**")
        st.write("- Matin : 3 œufs + 80g avoine")
        st.write("- Midi : 150g Poulet + 100g Riz + Légumes")
        st.write("- Soir : 150g Saumon + 250g Patate douce")
        st.markdown('</div>', unsafe_allow_html=True)

# --- ONGLET REPOS (CHRONO + JEU) ---
with tabs[4]:
    st.markdown("<h2>⏱️ TEMPS DE REPOS</h2>", unsafe_allow_html=True)
    c_c, c_j = st.columns(2)
    with c_c:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        t_rep = st.number_input("Secondes", 30, 300, 90)
        if st.button("LANCER LE CHRONO"):
            ph = st.empty()
            for i in range(t_rep, -1, -1):
                ph.metric("REPOS", f"{i}s")
                time.sleep(1)
            st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_j:
        st.markdown("<h3>🎮 FLAPPY BICEPS</h3>", unsafe_allow_html=True)
        st.components.v1.html("""
        <canvas id="g" width="300" height="150" style="border:1px solid #dc2626; background:#000;"></canvas>
        <script>
        const c=document.getElementById('g'), x=c.getContext('2d');
        let y=75, v=0;
        function d(){ v+=0.1; y+=v; x.clearRect(0,0,300,150); x.fillStyle="red"; x.fillText("💪", 40, y);
        if(y>150) {y=75; v=0;} requestAnimationFrame(d); }
        window.onclick=()=>v=-3; d();
        </script>
        """, height=180)

# --- ONGLET IA COACH ---
with tabs[5]:
    st.markdown("<h2>🤖 IA COACH PERSONNEL</h2>", unsafe_allow_html=True)
    st.markdown('<div class="card-dark">', unsafe_allow_html=True)
    p_last = st.session_state['historique_poids']['Poids'][-1] if st.session_state['historique_poids']['Poids'] else 75
    st.write(f"Analyse basée sur votre poids de **{p_last}kg**.")
    st.success("Conseil du jour : Augmentez vos charges de 2.5kg sur les exercices polyarticulaires cette semaine.")
    
    st.subheader("Calculateur 1RM")
    w = st.number_input("Poids soulevé", 20, 300, 100)
    r = st.number_input("Répétitions", 1, 15, 5)
    rm = w / (1.0278 - (0.0278 * r))
    st.metric("Ton 1RM estimé", f"{round(rm, 1)} kg")
    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.sidebar.write("🔥 **BODYTRACK PRO v1.0**")
