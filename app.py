import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import numpy as np

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="BODYTRACK PRO", page_icon="💪", layout="wide")

# --- STYLE CSS PERSONNALISÉ (Noir & Rouge Professionnel) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@300;400;700&display=swap');
    
    .stApp { background-color: #0e1117; color: #ffffff; font-family: 'Roboto', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Titres Sportifs */
    h1, h2, h3 { font-family: 'Bebas Neue', cursive; color: #FF0000; letter-spacing: 2px; }
    
    /* Cartes et Conteneurs */
    .st-emotion-cache-12w0qpk { background-color: #1a1c24; border: 1px solid #3e3e3e; border-radius: 10px; padding: 20px; }
    
    /* Boutons */
    .stButton>button { 
        background-color: #FF0000; color: white; border-radius: 5px; 
        font-weight: bold; border: none; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #CC0000; border: none; color: white; transform: scale(1.02); }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #FF0000; }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTÈME D'ACCÈS SÉCURISÉ ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

def check_access():
    if not st.session_state['auth']:
        st.image("https://i.imgur.com/wlyusJ0.png", width=200) # Ton logo Imgur
        st.title("🔥 ACCÈS AU EBOOK PREMIUM")
        st.write("Libérez votre potentiel pour seulement **20€** ou entrez votre code accès.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Payer 20€ (Accès Instantané)"):
                st.session_state['auth'] = True
                st.rerun()
        with col2:
            admin_code = st.text_input("Code Administrateur", type="password")
            if admin_code == "F12Berlinetta88170":
                st.session_state['auth'] = True
                st.rerun()
        st.stop()

check_access()

# --- INITIALISATION DES DONNÉES (Session State) ---
if 'weight_data' not in st.session_state:
    st.session_state['weight_data'] = pd.DataFrame(columns=['Date', 'Poids'])
if 'notes' not in st.session_state:
    st.session_state['notes'] = []

# --- NAVIGATION ---
with st.sidebar:
    st.image("https://i.imgur.com/wlyusJ0.png", width=150)
    st.title("MENU")
    menu = st.radio("Navigation", [
        "📊 Profil & Suivi", "🎯 Objectifs", "📅 Calendrier", 
        "💪 Entraînement", "📋 Programmes", "🍽️ Nutrition & IA", 
        "⏱️ Repos & Jeu", "🤖 Coach IA", "📱 Installation"
    ])

# --- 1. PROFIL & SUIVI ---
if menu == "📊 Profil & Suivi":
    st.header("📊 PROFIL UTILISATEUR")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nom Complet")
        st.number_input("Âge", 14, 99, 25)
        st.number_input("Taille (cm)", 100, 250, 175)
        st.text_input("Exercice Préféré")
        st.text_input("Adresse Mail")
    
    with col2:
        st.subheader("📸 Suivi Visuel")
        st.file_uploader("Importer Photo Avant/Après", type=['jpg', 'png'])
        st.subheader("📏 Mensurations (cm)")
        st.number_input("Tour de bras", 20.0, 60.0, 35.0)
        st.number_input("Tour de taille", 50.0, 150.0, 80.0)

    st.divider()
    st.subheader("📈 Suivi du Poids")
    with st.expander("Ajouter une pesée"):
        new_date = st.date_input("Date")
        new_weight = st.number_input("Poids (kg)", 30.0, 200.0, 75.0)
        if st.button("Enregistrer Pesée"):
            new_entry = pd.DataFrame({'Date': [str(new_date)], 'Poids': [new_weight]})
            st.session_state['weight_data'] = pd.concat([st.session_state['weight_data'], new_entry], ignore_index=True)
    
    if not st.session_state['weight_data'].empty:
        fig = px.line(st.session_state['weight_data'], x='Date', y='Poids', title="Évolution du Poids", markers=True)
        fig.update_traces(line_color='#FF0000')
        st.plotly_chart(fig, use_container_width=True)

# --- 2. OBJECTIFS ---
elif menu == "🎯 Objectifs":
    st.header("🎯 MES OBJECTIFS")
    col1, col2 = st.columns(2)
    
    with col1:
        obj_name = st.text_input("Nom de l'objectif (ex: DC 100kg)")
        current_val = st.number_input("Valeur Actuelle", 0)
        target_val = st.number_input("Valeur Cible", 1)
        
        progress = (current_val / target_val)
        st.write(f"Progression : {progress*100:.1f}%")
        st.progress(progress if progress <= 1.0 else 1.0)
        
    with col2:
        st.subheader("🏆 Performance Target")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = current_val,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': obj_name},
            gauge = {'axis': {'range': [None, target_val]}, 'bar': {'color': "#FF0000"}}
        ))
        st.plotly_chart(fig, use_container_width=True)

# --- 3. ENTRAÎNEMENT ---
elif menu == "💪 Entraînement":
    st.header("💪 TECHNIQUE & ANALYSE")
    
    tab1, tab2, tab3 = st.tabs(["📚 Guide Technique", "📈 Stats Exos", "🧘 Mobilité"])
    
    with tab1:
        exo = st.selectbox("Choisir un exercice", ["Développé Couché", "Squat", "Soulevé de Terre", "Rowing Barre", "Romanian Deadlift"])
        if exo == "Développé Couché":
            st.write("**Position :** Allongé, pieds ancrés au sol, omoplates rétractées.")
            st.write("**Mains :** Largeur supérieure aux épaules, poignets droits.")
            st.info("💡 Gardez les coudes à 45° pour protéger vos épaules.")
            
    
    with tab2:
        st.subheader("Analyse des Performances")
        # Ici on simulerait des données par exo
        st.write("Graphique comparatif des charges par exercice.")
        
    with tab3:
        st.subheader("Routine d'échauffement")
        st.write("1. Mobilisation articulaire (5 min)")
        st.write("2. Foam rolling sur les zones de tension")

# --- 4. REPOS & JEU ---
elif menu == "⏱️ Repos & Jeu":
    st.header("⏱️ ZONE DE RÉCUPÉRATION")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Chronomètre de Repos")
        seconds = st.number_input("Régler le repos (sec)", 30, 300, 90)
        if st.button("Démarrer le repos"):
            ph = st.empty()
            for i in range(seconds, -1, -1):
                ph.write(f"## ⏳ {i} secondes")
                time.sleep(1)
            st.balloons()
            st.error("🚨 TEMPS DE REPOS TERMINÉ, RETOUR AU CHARBON !")

    with col2:
        st.subheader("🚀 Mini-Jeu : Flappy Biceps")
        st.write("Cliquez pour faire voler le biceps entre les planètes !")
        # Note: Un jeu complexe Flappy Bird en pur Streamlit/Python nécessite un composant HTML/JS
        game_code = """
        <canvas id="gameCanvas" width="320" height="480" style="border:2px solid #FF0000; display:block; margin:0 auto;"></canvas>
        <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        let bY = 150, bV = 0, p = [{x:320, y:0}];
        function draw() {
            ctx.fillStyle = "black"; ctx.fillRect(0,0,320,480);
            bV += 0.1; bY += bV; 
            ctx.font = "30px Arial"; ctx.fillText("💪", 50, bY);
            p.forEach(pipe => {
                ctx.fillStyle = "purple"; ctx.beginPath(); ctx.arc(pipe.x, 240, 30, 0, Math.PI*2); ctx.fill();
                pipe.x -= 2;
            });
            if(p[0].x < -50) p.shift();
            if(p.length < 2 && p[0].x < 150) p.push({x:320, y:0});
            requestAnimationFrame(draw);
        }
        canvas.addEventListener('mousedown', () => bV = -3);
        draw();
        </script>
        """
        st.components.v1.html(game_html=game_code, height=500)

# --- 5. NUTRITION & IA ---
elif menu == "🍽️ Nutrition & IA":
    st.header("🍽️ NUTRITION AVANCÉE")
    
    tab1, tab2 = st.tabs(["👨‍🍳 Cuisinier IA", "📊 Tracker Macros"])
    
    with tab1:
        user_envie = st.text_input("De quoi as-tu envie ? (ex: Rapide, Riche en Protéines, Poulet)")
        if st.button("Générer Recette"):
            st.write("### 🍛 Poulet Curry Express (2300kcal menu adapt)")
            st.write("- 200g de poulet, 100g riz basmati, 1/2 avocat.")
            st.write("**Macros:** 45g Prot, 60g Gluc, 15g Lip")

    with tab2:
        st.subheader("Menu 2300 kcal - Journée Type")
        st.table({
            "Repas": ["Matin", "Midi", "Collation", "Soir"],
            "Description": ["Omelette 3 oeufs + Avoine", "Poulet/Riz/Brocolis", "Shaker + Amandes", "Saumon/Patate Douce"]
        })

# --- 6. PROGRAMMES ---
elif menu == "📋 Programmes":
    st.header("📋 PROGRAMMES D'ENTRAÎNEMENT")
    choix = st.selectbox("Choisir un programme", ["Débutant 5J", "PPL 6J", "PR Bench (3J/semaine)"])
    
    if choix == "PR Bench (3J/semaine)":
        st.subheader("🚀 Formule PR Bench")
        st.write("**Lundi :** 4x5 à 75% du PR visé")
        st.write("**Mercredi :** 3x7 à 65% (Pause 2s poitrine)")
        st.write("**Samedi :** Single à 80% + 3x3 à 75%")
        
        pr_target = st.number_input("Objectif PR (kg)", 40, 300, 100)
        st.info(f"Lundi, chargez à : {pr_target*0.75} kg")

# --- 7. INSTALLATION ---
elif menu == "📱 Installation":
    st.header("📱 INSTALLER SUR VOTRE SMARTPHONE")
    st.write("### 🤖 Android (Chrome)")
    st.write("1. Cliquez sur les 3 points en haut à droite.")
    st.write("2. Sélectionnez 'Ajouter à l'écran d'accueil'.")
    st.write("### 🍎 iOS (Safari)")
    st.write("1. Cliquez sur le bouton de partage (carré avec flèche).")
    st.write("2. Sélectionnez 'Sur l'écran d'accueil'.")

# --- FOOTER ---
st.divider()
st.caption("BODYTRACK PRO - Votre corps, votre machine. © 2026")
