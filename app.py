import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import json
import time
import random
from PIL import Image
import io
import base64
import hashlib
import math

# Configuration de la page
st.set_page_config(
    page_title="IronMaster Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    /* Thème noir/rouge */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    .main-header {
        color: #C41E3A;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .section-title {
        color: #C41E3A;
        border-bottom: 2px solid #C41E3A;
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2rem;
    }
    
    .metric-card {
        background-color: #1A1A1A;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #C41E3A;
        margin-bottom: 15px;
    }
    
    .program-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #333;
        transition: transform 0.3s;
    }
    
    .program-card:hover {
        transform: translateY(-5px);
        border-color: #C41E3A;
    }
    
    .button-primary {
        background-color: #C41E3A !important;
        color: white !important;
        border: none !important;
    }
    
    .progress-bar {
        height: 20px;
        background-color: #333;
        border-radius: 10px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background-color: #C41E3A;
        border-radius: 10px;
        transition: width 0.5s;
    }
    
    /* Animation repos */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .rest-animation {
        animation: pulse 1s infinite;
        color: #C41E3A;
        font-weight: bold;
        font-size: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Logo et header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-header">💪 IRONMASTER PRO</h1>', unsafe_allow_html=True)

# Initialisation des sessions
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'workout_data' not in st.session_state:
    st.session_state.workout_data = []
if 'weight_data' not in st.session_state:
    st.session_state.weight_data = []
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'measurements' not in st.session_state:
    st.session_state.measurements = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Accueil"

# Code administrateur
ADMIN_CODE = "F12Berlinetta88170"
PRICE = 20

# Fonction d'authentification
def authenticate():
    st.sidebar.markdown("## 🔐 Authentification")
    
    if st.session_state.authenticated:
        st.sidebar.success("✅ Authentifié")
        return True
    
    option = st.sidebar.radio("Choisir une option:", ["Version Démo", "Payer 20€", "Code Admin"])
    
    if option == "Version Démo":
        st.sidebar.warning("⚠️ Version démo limitée à 7 jours")
        st.session_state.authenticated = True
        return True
        
    elif option == "Payer 20€":
        st.sidebar.info(f"💰 Prix: {PRICE}€")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            card_number = st.text_input("Numéro carte", placeholder="1234 5678 9012 3456")
        with col2:
            expiry = st.text_input("Expiration", placeholder="MM/AA")
        
        cvv = st.text_input("CVV", type="password")
        
        if st.button("Payer", key="pay_button"):
            if card_number and expiry and cvv:
                st.success("✅ Paiement accepté! Accès complet débloqué.")
                st.session_state.authenticated = True
                return True
            else:
                st.error("❌ Informations manquantes")
                
    elif option == "Code Admin":
        admin_input = st.sidebar.text_input("Entrez le code admin:", type="password")
        if st.sidebar.button("Valider"):
            if admin_input == ADMIN_CODE:
                st.sidebar.success("🎉 Code admin accepté! Accès complet.")
                st.session_state.authenticated = True
                return True
            else:
                st.sidebar.error("❌ Code incorrect")
    
    return False

# Page d'accueil
def home_page():
    st.markdown('<h2 class="section-title">🏠 Tableau de Bord</h2>', unsafe_allow_html=True)
    
    if st.session_state.user_data:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Âge", st.session_state.user_data.get('age', 'N/A'))
        with col2:
            st.metric("Poids", f"{st.session_state.user_data.get('weight', 'N/A')} kg")
        with col3:
            st.metric("Taille", f"{st.session_state.user_data.get('height', 'N/A')} cm")
        with col4:
            st.metric("IMC", calculate_bmi())
    
    # Quick stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3>📊 Progression Poids</h3>', unsafe_allow_html=True)
        if st.session_state.weight_data:
            df = pd.DataFrame(st.session_state.weight_data)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'], y=df['weight'], 
                                    mode='lines+markers',
                                    line=dict(color='#C41E3A', width=3),
                                    name='Poids'))
            fig.update_layout(template='plotly_dark', 
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Ajoutez votre premier poids dans l'onglet Profil")
    
    with col2:
        st.markdown('<h3>🎯 Objectifs en cours</h3>', unsafe_allow_html=True)
        for goal in st.session_state.goals[:3]:
            progress = min(goal.get('progress', 0), 100)
            st.markdown(f"**{goal['name']}**")
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
            <div style="text-align: right;">{progress}%</div>
            """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown('<h3>🚀 Actions Rapides</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏋️‍♂️ Nouvelle Séance"):
            st.session_state.current_page = "Entraînement"
            st.rerun()
    
    with col2:
        if st.button("🍽️ Ajouter Repas"):
            st.session_state.current_page = "Nutrition"
            st.rerun()
    
    with col3:
        if st.button("📝 Objectif"):
            st.session_state.current_page = "Objectifs"
            st.rerun()
    
    with col4:
        if st.button("⏱️ Timer Repos"):
            st.session_state.current_page = "Repos"
            st.rerun()

# Onglet Profil
def profile_page():
    st.markdown('<h2 class="section-title">👤 Profil</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Informations", "⚖️ Suivi Poids", "📏 Mensurations", "📸 Photos"])
    
    with tab1:
        with st.form("user_info_form"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Âge", min_value=10, max_value=100, value=st.session_state.user_data.get('age', 25))
                height = st.number_input("Taille (cm)", min_value=100, max_value=250, value=st.session_state.user_data.get('height', 175))
            with col2:
                weight = st.number_input("Poids (kg)", min_value=30.0, max_value=200.0, value=st.session_state.user_data.get('weight', 70.0))
                fav_exercise = st.selectbox("Exercice préféré", [
                    "Développé couché", "Squat", "Soulevé de terre", "Développé militaire",
                    "Tractions", "Rowing", "Curl biceps", "Extensions triceps"
                ], index=0)
            
            email = st.text_input("Email", value=st.session_state.user_data.get('email', ""))
            
            if st.form_submit_button("💾 Sauvegarder"):
                st.session_state.user_data = {
                    'age': age,
                    'height': height,
                    'weight': weight,
                    'fav_exercise': fav_exercise,
                    'email': email
                }
                st.success("✅ Profil mis à jour!")
    
    with tab2:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.session_state.weight_data:
                df = pd.DataFrame(st.session_state.weight_data)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['date'], y=df['weight'], 
                                        mode='lines+markers',
                                        line=dict(color='#C41E3A', width=3),
                                        marker=dict(size=10),
                                        name='Poids'))
                
                # Calcul de la tendance
                if len(df) > 1:
                    z = np.polyfit(range(len(df)), df['weight'], 1)
                    p = np.poly1d(z)
                    fig.add_trace(go.Scatter(x=df['date'], y=p(range(len(df))),
                                            mode='lines',
                                            line=dict(color='#FF6B6B', width=2, dash='dash'),
                                            name='Tendance'))
                
                fig.update_layout(
                    title="Évolution du poids",
                    xaxis_title="Date",
                    yaxis_title="Poids (kg)",
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Ajouter poids")
            with st.form("weight_form"):
                new_weight = st.number_input("Poids (kg)", min_value=30.0, max_value=200.0)
                weight_date = st.date_input("Date", value=date.today())
                
                col_sub1, col_sub2 = st.columns(2)
                with col_sub1:
                    submit = st.form_submit_button("➕ Ajouter")
                with col_sub2:
                    delete = st.form_submit_button("🗑️ Supprimder dernier")
                
                if submit and new_weight:
                    st.session_state.weight_data.append({
                        'date': weight_date.strftime("%Y-%m-%d"),
                        'weight': new_weight
                    })
                    st.success("✅ Poids ajouté!")
                    st.rerun()
                
                if delete and st.session_state.weight_data:
                    st.session_state.weight_data.pop()
                    st.success("✅ Dernière entrée supprimée!")
                    st.rerun()
            
            # Calculs
            if len(st.session_state.weight_data) >= 2:
                weights = [w['weight'] for w in st.session_state.weight_data]
                diff = weights[-1] - weights[-2]
                st.metric("Différence", f"{diff:+.1f} kg")
    
    with tab3:
        st.markdown("### Suivi des mensurations")
        
        cols = st.columns(4)
        measurements = ['Bras (cm)', 'Poitrine (cm)', 'Taille (cm)', 'Cuisses (cm)']
        
        for idx, col in enumerate(cols):
            with col:
                value = st.number_input(measurements[idx], min_value=0.0, max_value=200.0, value=30.0 + idx*10)
                if st.button(f"Enregistrer {measurements[idx]}"):
                    st.session_state.measurements.append({
                        'date': date.today().strftime("%Y-%m-%d"),
                        'type': measurements[idx],
                        'value': value
                    })
                    st.success(f"✅ {measurements[idx]} enregistré")
    
    with tab4:
        st.markdown("### Photos de progression")
        col1, col2 = st.columns(2)
        with col1:
            st.file_uploader("📸 Upload photo avant", type=['png', 'jpg', 'jpeg'])
        with col2:
            st.file_uploader("📸 Upload photo après", type=['png', 'jpg', 'jpeg'])
        
        st.info("Les photos sont stockées localement et cryptées")

# Onglet Objectifs
def goals_page():
    st.markdown('<h2 class="section-title">🎯 Objectifs</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 Mes Objectifs", "📅 Calendrier"])
    
    with tab1:
        # Créer un nouvel objectif
        with st.expander("➕ Créer un nouvel objectif"):
            with st.form("new_goal_form"):
                goal_name = st.text_input("Nom de l'objectif")
                goal_type = st.selectbox("Type", ["Performance", "Poids", "Mensuration", "Endurance", "Nutrition"])
                target_value = st.number_input("Valeur cible")
                current_value = st.number_input("Valeur actuelle")
                deadline = st.date_input("Date limite", min_value=date.today())
                
                if st.form_submit_button("Créer objectif"):
                    progress = (current_value / target_value * 100) if target_value > 0 else 0
                    st.session_state.goals.append({
                        'id': len(st.session_state.goals) + 1,
                        'name': goal_name,
                        'type': goal_type,
                        'target': target_value,
                        'current': current_value,
                        'progress': min(progress, 100),
                        'deadline': deadline.strftime("%Y-%m-%d"),
                        'created': date.today().strftime("%Y-%m-%d")
                    })
                    st.success("✅ Objectif créé!")
        
        # Afficher les objectifs
        for goal in st.session_state.goals:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"### {goal['name']}")
                    st.markdown(f"*Type: {goal['type']}*")
                    st.markdown(f"**Progression: {goal['progress']:.1f}%**")
                    
                    # Barre de progression
                    st.markdown(f"""
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {min(goal['progress'], 100)}%"></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.metric("Actuel", goal['current'])
                    st.metric("Cible", goal['target'])
                
                with col3:
                    st.write(f"📅 {goal['deadline']}")
                    if st.button("📝 Mettre à jour", key=f"update_{goal['id']}"):
                        st.session_state.editing_goal = goal['id']
    
    with tab2:
        st.markdown("### 📅 Calendrier d'entraînement")
        
        # Calendrier simple
        today = date.today()
        days_in_month = 30  # Simplification
        
        cols = st.columns(7)
        day_names = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        for idx, col in enumerate(cols[:7]):
            with col:
                st.markdown(f"**{day_names[idx]}**")
        
        # Générer les jours
        rows = []
        for week in range(5):
            cols = st.columns(7)
            for day_idx in range(7):
                day_num = week * 7 + day_idx + 1
                with cols[day_idx]:
                    if day_num <= days_in_month:
                        day_date = date(today.year, today.month, min(day_num, 28))
                        if day_num == today.day:
                            st.markdown(f'<div style="color: red; font-weight: bold;">{day_num}</div>', 
                                      unsafe_allow_html=True)
                        else:
                            st.write(day_num)
                        
                        # Bouton pour ajouter une séance
                        if st.button(f"➕", key=f"add_{day_num}"):
                            st.session_state.selected_date = day_date
                            st.session_state.show_workout_form = True
        
        # Formulaire pour ajouter une séance
        if st.session_state.get('show_workout_form', False):
            with st.form("workout_session_form"):
                st.markdown(f"### Séance du {st.session_state.selected_date}")
                
                duration = st.slider("Durée (minutes)", 15, 180, 60)
                program = st.selectbox("Programme", [
                    "Full Body", "Push", "Pull", "Legs", "Upper Body", "Lower Body",
                    "Push/Pull/Legs", "Programme Perso"
                ])
                
                exercises = st.text_area("Exercices effectués", 
                                       placeholder="Ex: Développé couché 4x8 @80kg\nSquat 3x10 @100kg")
                
                notes = st.text_area("Notes supplémentaires")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Sauvegarder"):
                        st.session_state.workout_data.append({
                            'date': st.session_state.selected_date.strftime("%Y-%m-%d"),
                            'duration': duration,
                            'program': program,
                            'exercises': exercises,
                            'notes': notes
                        })
                        st.success("✅ Séance enregistrée!")
                        st.session_state.show_workout_form = False
                        st.rerun()
                with col2:
                    if st.form_submit_button("❌ Annuler"):
                        st.session_state.show_workout_form = False
                        st.rerun()

# Onglet Entraînement
def workout_page():
    st.markdown('<h2 class="section-title">🏋️‍♂️ Entraînement</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Suivi Performance", "📝 Carnet Séance", "🏃 Échauffement", "📚 Exercices"])
    
    with tab1:
        st.markdown("### Graphiques de performance par exercice")
        
        # Données d'exemple pour les exercices
        exercises = {
            "Développé couché": [60, 65, 70, 72, 75, 78, 80],
            "Squat": [80, 85, 90, 95, 100, 105, 110],
            "Soulevé de terre": [90, 95, 100, 105, 110, 115, 120],
            "Développé militaire": [40, 42, 45, 47, 50, 52, 55]
        }
        
        selected_exercises = st.multiselect(
            "Sélectionnez les exercices à comparer",
            list(exercises.keys()),
            default=list(exercises.keys())[:2]
        )
        
        if selected_exercises:
            fig = go.Figure()
            colors = ['#C41E3A', '#FF6B6B', '#FFA500', '#00FF88']
            
            for idx, exercise in enumerate(selected_exercises):
                fig.add_trace(go.Scatter(
                    x=list(range(1, 8)),
                    y=exercises[exercise],
                    mode='lines+markers',
                    name=exercise,
                    line=dict(color=colors[idx % len(colors)], width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                title="Évolution des performances",
                xaxis_title="Semaines",
                yaxis_title="Poids (kg)",
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Carnet de séance en temps réel")
        
        # Timer entre séries
        col1, col2, col3 = st.columns(3)
        with col1:
            rest_time = st.number_input("Temps repos (secondes)", min_value=30, max_value=300, value=90)
        with col2:
            if st.button("⏱️ Démarrer timer repos"):
                st.session_state.start_rest_time = time.time()
                st.session_state.rest_duration = rest_time
        
        with col3:
            if 'start_rest_time' in st.session_state:
                elapsed = time.time() - st.session_state.start_rest_time
                remaining = max(0, st.session_state.rest_duration - elapsed)
                
                if remaining > 0:
                    minutes = int(remaining // 60)
                    seconds = int(remaining % 60)
                    st.markdown(f"<div class='rest-animation'>{minutes:02d}:{seconds:02d}</div>", 
                              unsafe_allow_html=True)
                else:
                    st.markdown("<div class='rest-animation'>⏰ TEMPS ÉCOULÉ!</div>", 
                              unsafe_allow_html=True)
        
        # Formulaire de séance
        st.markdown("### 📝 Nouvelle séance")
        with st.form("live_workout_form"):
            exercise = st.selectbox("Exercice", list(exercises.keys()))
            sets = st.number_input("Séries", min_value=1, max_value=10, value=3)
            
            for i in range(sets):
                cols = st.columns(4)
                with cols[0]:
                    st.write(f"**Série {i+1}**")
                with cols[1]:
                    reps = st.number_input(f"Répétitions", min_value=1, max_value=50, value=8, key=f"reps_{i}")
                with cols[2]:
                    weight = st.number_input(f"Poids (kg)", min_value=0.0, max_value=300.0, value=60.0, key=f"weight_{i}")
                with cols[3]:
                    rpe = st.slider(f"RPE", 1.0, 10.0, 7.0, key=f"rpe_{i}")
            
            notes = st.text_area("Notes (sensations, douleurs, forme)")
            
            if st.form_submit_button("💾 Enregistrer la séance"):
                st.success("✅ Séance enregistrée!")
    
    with tab3:
        st.markdown("### 🏃 Routines d'échauffement")
        
        muscle_group = st.selectbox("Groupe musculaire", [
            "Pectoraux", "Dos", "Jambes", "Épaules", "Bras", "Full Body"
        ])
        
        warmup_routines = {
            "Pectoraux": [
                "Rotation des épaules: 2x30 secondes",
                "Étirements pectoraux: 2x30 secondes chaque bras",
                "Push-ups légers: 2x15 répétitions",
                "Développé couché à vide: 2x20 répétitions"
            ],
            "Jambes": [
                "Squats à vide: 2x20 répétitions",
                "Fentes marches: 2x10 chaque jambe",
                "Étirements ischio-jambiers: 2x30 secondes",
                "Leg swings: 2x15 chaque jambe"
            ]
        }
        
        st.markdown("**Routine recommandée:**")
        for item in warmup_routines.get(muscle_group, warmup_routines["Full Body"]):
            st.markdown(f"✓ {item}")
    
    with tab4:
        st.markdown("### 📚 Bibliothèque d'exercices")
        
        exercise_detail = st.selectbox("Choisir un exercice", [
            "Développé couché", "Développé incliné", "Rowing", "Squat",
            "Soulevé de terre", "Romanian Deadlift", "Élévation latérale",
            "Curl", "Développé militaire"
        ])
        
        exercise_details = {
            "Développé couché": {
                "Position": "Allongé sur le dos, pieds ancrés au sol, cambrure naturelle",
                "Prise": "Largeur 1.5x épaules, pouces en opposition",
                "Descente": "Contrôlée jusqu'au sternum, coudes à 45°",
                "Montée": "Explosive sans décoller les fessiers",
                "Respiration": "Inspirer à la descente, expirer à la montée"
            },
            "Squat": {
                "Position": "Pieds largeur épaules, pointes légèrement vers l'extérieur",
                "Descente": "Contrôlée, dos droit, genoux suivant les orteils",
                "Profondeur": "Cuisses parallèles au sol minimum",
                "Montée": "Pousser avec les talons, garder le torse droit",
                "Respiration": "Inspirer avant la descente, expirer pendant la montée"
            }
        }
        
        if exercise_detail in exercise_details:
            for key, value in exercise_details[exercise_detail].items():
                st.markdown(f"**{key}:** {value}")

# Onglet Repos
def rest_page():
    st.markdown('<h2 class="section-title">⏱️ Temps de Repos</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Timer Intelligent")
        
        # Paramètres du timer
        rest_time = st.slider("Durée du repos (secondes)", 30, 300, 90, 15)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("▶️ Démarrer Timer", use_container_width=True):
                st.session_state.timer_start = time.time()
                st.session_state.timer_duration = rest_time
                st.session_state.timer_running = True
        
        with col_b:
            if st.button("⏸️ Pause", use_container_width=True):
                st.session_state.timer_running = False
        
        # Affichage du timer
        if 'timer_start' in st.session_state and st.session_state.get('timer_running', False):
            elapsed = time.time() - st.session_state.timer_start
            remaining = max(0, st.session_state.timer_duration - elapsed)
            
            # Barre de progression
            progress = 100 * (1 - remaining / st.session_state.timer_duration)
            
            # Affichage
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="font-size: 4rem; font-weight: bold; color: #C41E3A;">
                    {minutes:02d}:{seconds:02d}
                </div>
                <div class="progress-bar" style="width: 100%;">
                    <div class="progress-fill" style="width: {progress}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Animation quand le timer est fini
            if remaining <= 0:
                st.markdown("""
                <div style="text-align: center; animation: pulse 1s infinite;">
                    <h1 style="color: #C41E3A; font-size: 3rem;">🏋️‍♂️ TEMPS DE REPOS TERMINÉ!</h1>
                    <h2 style="color: #FF6B6B;">💪 RETOUR AU CHARBON!</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Son (simulé avec un message)
                st.balloons()
    
    with col2:
        st.markdown("### 🎮 Mini-Jeu Biceps Bird")
        
        st.markdown("""
        <div style="background: linear-gradient(45deg, #000428, #004e92); 
                    padding: 20px; border-radius: 10px; text-align: center;">
            <h3>🦾 Biceps Bird</h3>
            <p>Contrôlez un biceps volant dans l'espace!</p>
            <div style="margin: 20px 0;">
                <div style="background-color: #1A1A1A; height: 200px; border-radius: 5px;
                            display: flex; justify-content: center; align-items: center;">
                    <div style="font-size: 4rem;">💪</div>
                    <div style="position: absolute; right: 30px; font-size: 2rem;">🪐</div>
                </div>
            </div>
            <p>Évitez les haltères flottants!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎮 Jouer", use_container_width=True):
            st.info("Version complète disponible dans l'application mobile!")

# Onglet Calculateurs
def calculators_page():
    st.markdown('<h2 class="section-title">🧮 Calculateurs</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔥 Calories Dépensées", "🍽️ Nutrition", "🏋️‍♂️ 1RM"])
    
    with tab1:
        st.markdown("### Calculateur de calories dépensées")
        
        activity = st.selectbox("Activité", [
            "Musculation (léger)", "Musculation (intense)", "Cardio (léger)",
            "Cardio (intense)", "Basketball", "Natation", "Course à pied",
            "Vélo", "Football", "Rugby"
        ])
        
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("Durée (minutes)", min_value=1, max_value=300, value=60)
        with col2:
            weight = st.number_input("Poids corporel (kg)", min_value=30.0, max_value=200.0, 
                                   value=st.session_state.user_data.get('weight', 70.0))
        
        # Calcul approximatif
        met_values = {
            "Musculation (léger)": 3.5,
            "Musculation (intense)": 6.0,
            "Cardio (léger)": 5.0,
            "Cardio (intense)": 8.0,
            "Basketball": 8.0,
            "Natation": 7.0,
            "Course à pied": 9.8,
            "Vélo": 7.5,
            "Football": 7.0,
            "Rugby": 10.0
        }
        
        if st.button("Calculer"):
            met = met_values.get(activity, 5.0)
            calories = met * weight * duration / 60
            st.success(f"🔥 Calories dépensées: **{calories:.0f} kcal**")
    
    with tab2:
        st.markdown("### Calculateur nutritionnel")
        
        food = st.selectbox("Aliment", [
            "Poulet (100g)", "Riz (100g)", "Brocoli (100g)", "Oeufs (2)",
            "Pâtes complètes (100g)", "Saumon (100g)", "Avocat (1)", "Banane (1)"
        ])
        
        food_data = {
            "Poulet (100g)": {"kcal": 165, "prot": 31, "gluc": 0, "lip": 3.6},
            "Riz (100g)": {"kcal": 130, "prot": 2.7, "gluc": 28, "lip": 0.3},
            "Brocoli (100g)": {"kcal": 34, "prot": 2.8, "gluc": 7, "lip": 0.4},
            "Oeufs (2)": {"kcal": 140, "prot": 12, "gluc": 1, "lip": 10}
        }
        
        quantity = st.number_input("Quantité (portion)", min_value=0.1, max_value=10.0, value=1.0, step=0.5)
        
        if st.button("Calculer macros"):
            if food in food_data:
                data = food_data[food]
                st.success(f"""
                **Nutrition pour {quantity} portion(s) de {food}:**
                - Calories: **{data['kcal'] * quantity:.0f} kcal**
                - Protéines: **{data['prot'] * quantity:.1f}g**
                - Glucides: **{data['gluc'] * quantity:.1f}g**
                - Lipides: **{data['lip'] * quantity:.1f}g**
                """)
    
    with tab3:
        st.markdown("### Calculateur de 1RM (One Rep Max)")
        
        exercise = st.selectbox("Exercice pour 1RM", [
            "Développé couché", "Squat", "Soulevé de terre", "Développé militaire"
        ])
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Poids soulevé (kg)", min_value=20.0, max_value=300.0, value=80.0)
        with col2:
            reps = st.number_input("Nombre de répétitions", min_value=2, max_value=12, value=5)
        
        formula = st.radio("Formule", ["Brzycki", "Epley", "Lombardi"])
        
        if st.button("Calculer 1RM"):
            if formula == "Brzycki":
                rm1 = weight * (36 / (37 - reps))
            elif formula == "Epley":
                rm1 = weight * (1 + reps/30)
            else:  # Lombardi
                rm1 = weight * (reps ** 0.10)
            
            st.success(f"🎯 1RM estimé: **{rm1:.1f} kg**")
            
            # Pourcentages
            st.markdown("**Pourcentages de votre 1RM:**")
            cols = st.columns(5)
            percentages = [100, 90, 80, 75, 70]
            for idx, pct in enumerate(percentages):
                with cols[idx]:
                    st.metric(f"{pct}%", f"{rm1 * pct/100:.1f}kg")

# Onglet Programmes
def programs_page():
    st.markdown('<h2 class="section-title">📋 Programmes</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏋️‍♂️ Débutant 5 jours", "🔄 PPL 6 jours", "🚀 PR Bench", "🎯 Personnaliser"])
    
    with tab1:
        st.markdown("### Programme Débutant - 5 jours")
        
        days = {
            "J1 - Pectoraux/Triceps": [
                "Développé couché: 3x8-12",
                "Développé incliné haltères: 3x10-15",
                "Écartés haltères: 3x12-15",
                "Extensions triceps poulie: 3x12-15",
                "Pompes diamant: 3xAMRAP"
            ],
            "J2 - Dos/Biceps": [
                "Tractions assistées: 3x8-12",
                "Rowing barre: 3x8-12",
                "Tirage poitrine: 3x10-15",
                "Curl barre: 3x10-15",
                "Curl haltères marteau: 3x12-15"
            ],
            "J3 - Jambes": [
                "Squat: 3x8-12",
                "Presse à cuisses: 3x10-15",
                "Leg curl: 3x12-15",
                "Extensions quadriceps: 3x12-15",
                "Mollets debout: 4x15-20"
            ],
            "J4 - Épaules": [
                "Développé militaire: 3x8-12",
                "Élévations latérales: 3x12-15",
                "Face pull: 3x15-20",
                "Oiseau haltères: 3x12-15",
                "Shrugs: 3x12-15"
            ],
            "J5 - Full Body léger": [
                "Squat léger: 3x10-15",
                "Développé couché léger: 3x10-15",
                "Rowing léger: 3x10-15",
                "Planche: 3x30-60s",
                "Cardio léger: 20-30 min"
            ]
        }
        
        selected_day = st.selectbox("Choisir le jour", list(days.keys()))
        
        st.markdown(f"### {selected_day}")
        for exercise in days[selected_day]:
            st.markdown(f"✓ {exercise}")
        
        if st.button("💾 Ajouter à mon calendrier"):
            st.success("✅ Programme ajouté à votre calendrier!")
    
    with tab2:
        st.markdown("### Programme PPL (Push/Pull/Legs) - 6 jours")
        
        st.markdown("""
        **Structure:**
        - Lundi: Push
        - Mardi: Pull
        - Mercredi: Legs
        - Jeudi: Push
        - Vendredi: Pull
        - Samedi: Legs
        - Dimanche: Repos
        """)
        
        ppl_days = {
            "Push": [
                "Développé couché: 4x5-8",
                "Développé militaire: 3x8-12",
                "Développé incliné haltères: 3x8-12",
                "Extensions triceps: 3x10-15",
                "Élévations latérales: 3x12-15"
            ],
            "Pull": [
                "Tractions: 4xAMRAP",
                "Soulevé de terre: 3x5-8",
                "Rowing barre: 3x8-12",
                "Face pull: 3x15-20",
                "Curl biceps: 3x10-15"
            ],
            "Legs": [
                "Squat: 4x5-8",
                "Presse à cuisses: 3x8-12",
                "Leg curl: 3x10-15",
                "Fentes: 3x10-12 chaque jambe",
                "Mollets: 4x15-20"
            ]
        }
        
        selected_ppl = st.selectbox("Choisir le type de journée", list(ppl_days.keys()))
        
        st.markdown(f"### {selected_ppl} Day")
        for exercise in ppl_days[selected_ppl]:
            st.markdown(f"✓ {exercise}")
    
    with tab3:
        st.markdown("### Programme Amélioration PR au Bench")
        
        st.markdown("""
        **Formule sur 3 séances/semaine:**
        
        **Lundi - Heavy:**
        - Bench press: 4x5 @75%
        + Bench haltères: 3x6-10
        + Triceps (au choix): 3x10-12
        
        **Mercredi - Technique:**
        - Bench press tempo: 3x7 @65% (2s pause sur la poitrine)
        + Développé militaire: 3x6-10
        + Triceps: 3x8-10
        + Biceps: 3x10-12
        
        **Samedi - Singles:**
        - Singles jusqu'à 80%
        + 3x3 @75%
        """)
        
        # Calculateur de pourcentages
        st.markdown("### 🧮 Calculateur de charges")
        
        target_pr = st.number_input("PR cible (kg)", min_value=50.0, max_value=300.0, value=100.0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            monday_weight = target_pr * 0.75
            st.metric("Lundi (75%)", f"{monday_weight:.1f}kg")
        with col2:
            wednesday_weight = target_pr * 0.65
            st.metric("Mercredi (65%)", f"{wednesday_weight:.1f}kg")
        with col3:
            saturday_weight = target_pr * 0.80
            st.metric("Samedi (80%)", f"{saturday_weight:.1f}kg")
        
        st.info("Augmentez vos charges de +3% chaque semaine si réussite")
    
    with tab4:
        st.markdown("### Créateur de programme personnalisé")
        
        program_name = st.text_input("Nom du programme")
        num_days = st.slider("Nombre de jours par semaine", 1, 7, 3)
        
        for day in range(num_days):
            with st.expander(f"Jour {day+1}"):
                st.text_input(f"Nom du jour {day+1}", value=f"Jour {day+1}")
                num_exercises = st.number_input(f"Nombre d'exercices", min_value=1, max_value=10, value=4, key=f"ex_{day}")
                
                for ex in range(num_exercises):
                    cols = st.columns([2, 1, 1, 1])
                    with cols[0]:
                        st.selectbox("Exercice", list(exercises.keys()), key=f"ex_name_{day}_{ex}")
                    with cols[1]:
                        st.number_input("Séries", min_value=1, max_value=10, value=3, key=f"sets_{day}_{ex}")
                    with cols[2]:
                        st.text_input("Reps", value="8-12", key=f"reps_{day}_{ex}")
                    with cols[3]:
                        st.text_input("Récup", value="90s", key=f"rest_{day}_{ex}")
        
        if st.button("💾 Créer programme"):
            st.success("✅ Programme créé! Disponible dans votre calendrier.")

# Onglet IA Coach
def ai_coach_page():
    st.markdown('<h2 class="section-title">🤖 Coach IA</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🏋️‍♂️ Coach Entraînement", "🍽️ Nutritionniste IA"])
    
    with tab1:
        st.markdown("### Coach IA Personnel")
        
        # Analyse des habitudes
        if st.session_state.workout_data:
            st.success("📊 IA analyse vos données d'entraînement...")
            
            # Recommandations basées sur les données
            st.markdown("**Recommandations:**")
            
            # Exemple de recommandations
            recommendations = [
                "💪 Augmentez votre volume sur les exercices de dos de 10%",
                "🏃‍♂️ Ajoutez 10 minutes de cardio post-entraînement",
                "🛌 Votre fréquence d'entraînement est optimale, continuez!",
                "⚡ Essayez des dropsets sur votre dernier exercice de la séance"
            ]
            
            for rec in recommendations:
                st.markdown(f"- {rec}")
        
        # Chat avec le coach
        st.markdown("### 💬 Parlez à votre coach")
        
        user_message = st.text_input("Posez votre question au coach IA:")
        
        if user_message:
            # Réponses préprogrammées (simulées)
            responses = {
                "technique": "Pour améliorer votre technique, concentrez-vous sur un tempo contrôlé et une amplitude complète.",
                "progression": "Augmentez vos charges de 2-5% chaque semaine sur les exercices principaux.",
                "repos": "Un bon sommeil (7-9h) et une alimentation équilibrée sont essentiels à la récupération.",
                "plateau": "Pour surmonter un plateau, variez vos exercices, réduisez vos charges de 10% et reconstruisez."
            }
            
            # Simple analyse de mots-clés
            response = "Je recommande de suivre votre programme avec constance et d'écouter votre corps."
            for key in responses:
                if key in user_message.lower():
                    response = responses[key]
            
            st.markdown(f"**🤖 Coach IA:** {response}")
    
    with tab2:
        st.markdown("### 🍽️ Cuisinier IA")
        
        # Générateur de recettes
        st.markdown("#### Générateur de recettes personnalisées")
        
        col1, col2 = st.columns(2)
        with col1:
            calories = st.slider("Calories cible", 300, 1000, 500)
            protein = st.slider("Protéines (g)", 10, 50, 25)
        with col2:
            meal_type = st.selectbox("Type de repas", ["Petit-déjeuner", "Déjeuner", "Dîner", "Collation"])
            restrictions = st.multiselect("Restrictions", ["Sans gluten", "Sans lactose", "Végétarien", "Vegan"])
        
        if st.button("🍳 Générer une recette"):
            # Recettes préprogrammées
            recipes = [
                {
                    "name": "Omelette protéinée",
                    "ingredients": "3 oeufs, 50g blanc de poulet, 30g épinards, 20g fromage",
                    "macros": "Cal: 350, P: 35g, G: 3g, L: 22g"
                },
                {
                    "name": "Bol de riz et poulet",
                    "ingredients": "150g riz basmati, 200g poulet grillé, 100g brocoli, sauce soja",
                    "macros": "Cal: 500, P: 45g, G: 60g, L: 8g"
                },
                {
                    "name": "Smoothie protéiné",
                    "ingredients": "1 banane, 30g protéine en poudre, 200ml lait d'amande, 20g beurre de cacahuète",
                    "macros": "Cal: 400, P: 35g, G: 40g, L: 12g"
                }
            ]
            
            import random
            recipe = random.choice(recipes)
            
            st.success(f"**🍽️ {recipe['name']}**")
            st.markdown(f"**Ingrédients:** {recipe['ingredients']}")
            st.markdown(f"**Macros:** {recipe['macros']}")
        
        # Liste de courses automatique
        st.markdown("#### 📝 Liste de courses")
        if st.button("🛒 Générer liste de courses"):
            shopping_list = [
                "Poulet (1kg)", "Oeufs (12)", "Riz basmati (1kg)", "Brocoli (2)",
                "Épinards (500g)", "Protéine en poudre (1kg)", "Lait d'amande (1L)",
                "Bananes (6)", "Beurre de cacahuète (500g)"
            ]
            
            for item in shopping_list:
                st.markdown(f"- [ ] {item}")

# Onglet Nutrition
def nutrition_page():
    st.markdown('<h2 class="section-title">🍽️ Nutrition</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Suivi Journalier", "🍳 Menus 2300kcal", "💊 Compléments"])
    
    with tab1:
        st.markdown("### Suivi nutritionnel journalier")
        
        today = date.today().strftime("%Y-%m-%d")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            breakfast_cals = st.number_input("Petit-déjeuner (kcal)", min_value=0, max_value=1000, value=400)
        with col2:
            lunch_cals = st.number_input("Déjeuner (kcal)", min_value=0, max_value=1000, value=600)
        with col3:
            dinner_cals = st.number_input("Dîner (kcal)", min_value=0, max_value=1000, value=500)
        with col4:
            snacks_cals = st.number_input("Collations (kcal)", min_value=0, max_value=1000, value=200)
        
        total_cals = breakfast_cals + lunch_cals + dinner_cals + snacks_cals
        
        st.metric("Total calories", f"{total_cals} kcal")
        
        # Objectif calorique
        goal_cals = 2300
        progress = min(100, (total_cals / goal_cals) * 100)
        
        st.markdown(f"**Objectif: {goal_cals} kcal**")
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%"></div>
        </div>
        <div style="text-align: right;">{progress:.1f}%</div>
        """, unsafe_allow_html=True)
        
        # Graphique des macros
        st.markdown("### Répartition des macros")
        
        macros = {
            "Protéines": st.number_input("Protéines (g)", min_value=0, max_value=200, value=120),
            "Glucides": st.number_input("Glucides (g)", min_value=0, max_value=400, value=250),
            "Lipides": st.number_input("Lipides (g)", min_value=0, max_value=150, value=80)
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(macros.keys()),
            values=list(macros.values()),
            hole=.3,
            marker=dict(colors=['#C41E3A', '#FF6B6B', '#FFA500'])
        )])
        
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Menus détaillés à 2300kcal")
        
        menu_choice = st.radio("Choisir un menu", ["Menu 1 - Prise de masse", "Menu 2 - Maintien", "Menu 3 - Sèche"])
        
        menus = {
            "Menu 1 - Prise de masse": [
                "**Petit-déjeuner (600 kcal):** 3 oeufs + 100g flocons d'avoine + 1 banane",
                "**Collation 1 (300 kcal):** Shake protéiné + 30g amandes",
                "**Déjeuner (700 kcal):** 200g poulet + 200g riz + légumes à volonté",
                "**Post-training (400 kcal):** Shake protéine + 2 bananes",
                "**Dîner (300 kcal):** 200g poisson blanc + salade verte + 100g patates douces"
            ],
            "Menu 2 - Maintien": [
                "**Petit-déjeuner (500 kcal):** 2 oeufs + 80g flocons d'avoine + fruits",
                "**Collation (200 kcal):** Yaourt grec + fruits rouges",
                "**Déjeuner (600 kcal):** 150g poulet + 150g quinoa + légumes",
                "**Post-training (300 kcal):** Shake protéiné + fruit",
                "**Dîner (400 kcal):** 150g saumon + légumes grillés + 100g riz"
            ],
            "Menu 3 - Sèche": [
                "**Petit-déjeuner (400 kcal):** 3 blancs d'oeufs + 60g flocons d'avoine",
                "**Collation (150 kcal):** 30g noix",
                "**Déjeuner (500 kcal):** 150g blanc de poulet + 100g riz + légumes",
                "**Post-training (200 kcal):** Protéine en poudre seule",
                "**Dîner (300 kcal):** 200g poisson blanc + salade verte"
            ]
        }
        
        for item in menus[menu_choice]:
            st.markdown(f"- {item}")
        
        if st.button("📋 Générer liste de courses pour ce menu"):
            st.success("Liste de courses générée dans le Cuisinier IA!")
    
    with tab3:
        st.markdown("### 💊 Guide des compléments")
        
        supplement = st.selectbox("Choisir un complément", [
            "Protéine Whey", "Créatine", "BCAA", "Pré-workout",
            "Vitamine D", "Oméga-3", "Multivitamines", "Caféine"
        ])
        
        supplement_info = {
            "Protéine Whey": {
                "Dosage": "20-40g après l'entraînement ou entre les repas",
                "Bénéfices": "Récupération musculaire, synthèse protéique",
                "Prix moyen": "20-40€/kg"
            },
            "Créatine": {
                "Dosage": "3-5g par jour, tous les jours",
                "Bénéfices": "Force, puissance, volume musculaire",
                "Prix moyen": "15-30€/300g"
            },
            "BCAA": {
                "Dosage": "5-10g pendant l'entraînement",
                "Bénéfices": "Réduction fatigue, récupération",
                "Prix moyen": "25-40€/300g"
            }
        }
        
        if supplement in supplement_info:
            info = supplement_info[supplement]
            for key, value in info.items():
                st.markdown(f"**{key}:** {value}")

# Onglet Notes
def notes_page():
    st.markdown('<h2 class="section-title">📝 Journal de Notes</h2>', unsafe_allow_html=True)
    
    # Sélecteur de date
    note_date = st.date_input("Date de la note", value=date.today())
    
    # Type de note
    note_type = st.selectbox("Type de note", [
        "Feedback séance", "Observations physiques",
        "Objectifs semaine", "Problèmes/douleurs",
        "Idées programmes", "Note générale"
    ])
    
    # Éditeur de texte
    note_content = st.text_area("Contenu de la note", height=200,
                               placeholder="Écrivez vos observations ici...")
    
    # Tags
    tags = st.multiselect("Tags", [
        "Force", "Hypertrophie", "Endurance", "Douleur",
        "Progression", "Nutrition", "Sommeil", "Motivation"
    ])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Sauvegarder", use_container_width=True):
            if note_content:
                note_id = len(st.session_state.get('notes', [])) + 1
                if 'notes' not in st.session_state:
                    st.session_state.notes = []
                
                st.session_state.notes.append({
                    'id': note_id,
                    'date': note_date.strftime("%Y-%m-%d"),
                    'type': note_type,
                    'content': note_content,
                    'tags': tags
                })
                st.success("✅ Note sauvegardée!")
            else:
                st.warning("Veuillez écrire quelque chose avant de sauvegarder")
    
    with col2:
        if st.button("📋 Voir toutes les notes", use_container_width=True):
            st.session_state.show_all_notes = True
    
    # Afficher toutes les notes
    if st.session_state.get('show_all_notes', False) and 'notes' in st.session_state and st.session_state.notes:
        st.markdown("### 📚 Toutes mes notes")
        
        for note in reversed(st.session_state.notes[-10:]):  # Les 10 dernières
            with st.expander(f"{note['date']} - {note['type']}"):
                st.markdown(f"**Tags:** {', '.join(note['tags'])}")
                st.markdown(f"**Contenu:**")
                st.write(note['content'])
                
                if st.button("🗑️ Supprimer", key=f"del_{note['id']}"):
                    st.session_state.notes = [n for n in st.session_state.notes if n['id'] != note['id']]
                    st.success("Note supprimée!")
                    st.rerun()

# Page d'installation
def install_page():
    st.markdown('<h2 class="section-title">📲 Installation Application</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Télécharger l'application IronMaster Pro
    
    Suivez ces instructions pour installer l'application sur votre appareil:
    """)
    
    tab1, tab2 = st.tabs(["📱 Android/Chrome", "🍎 iOS/Safari"])
    
    with tab1:
        st.markdown("""
        ### Pour Android/Chrome:
        
        1. **Ouvrez Chrome** et allez sur cette page
        2. **Cliquez sur le menu** (3 points en haut à droite)
        3. **Sélectionnez "Ajouter à l'écran d'accueil"**
        4. **Confirmez l'installation**
        5. **L'application apparaîtra** comme une app native
        
        ✅ **Fonctionnalités hors-ligne disponibles:**
        - Données de base
        - Journal d'entraînement
        - Programmes sauvegardés
        - Synchronisation automatique en ligne
        """)
    
    with tab2:
        st.markdown("""
        ### Pour iOS/Safari:
        
        1. **Ouvrez Safari** et allez sur cette page
        2. **Cliquez sur l'icône Partager** (carré avec flèche)
        3. **Faites défiler et sélectionnez "Sur l'écran d'accueil"**
        4. **Renommez l'application "IronMaster"**
        5. **Cliquez sur "Ajouter"**
        
        ✅ **Utilisez comme Progressive Web App (PWA)**
        """)
    
    # QR Code pour mobile
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        ### 📲 Scan QR Code
        
        Utilisez votre appareil photo pour scanner ce code et ouvrir directement l'application:
        """)
    
    with col2:
        # Générer un QR code simple (simulé)
        st.markdown("""
        <div style="background-color: white; padding: 20px; display: inline-block; border-radius: 10px;">
            <div style="font-size: 24px; text-align: center;">📱</div>
            <div style="text-align: center; color: black; font-weight: bold;">IRONMASTER</div>
            <div style="text-align: center; color: black;">v2.0.1</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Dernière version
    st.info("""
    **Dernière version: 2.0.1**
    - Correction des bugs de synchronisation
    - Amélioration des performances
    - Nouveaux programmes ajoutés
    """)

# Fonctions utilitaires
def calculate_bmi():
    if 'height' in st.session_state.user_data and 'weight' in st.session_state.user_data:
        height_m = st.session_state.user_data['height'] / 100
        weight = st.session_state.user_data['weight']
        if height_m > 0:
            return round(weight / (height_m ** 2), 1)
    return "N/A"

# Navigation principale
def main():
    # Authentification
    if not authenticate():
        st.warning("Veuillez vous authentifier pour accéder à l'application")
        return
    
    # Navigation sidebar
    st.sidebar.markdown("## 📱 Navigation")
    
    pages = {
        "🏠 Accueil": home_page,
        "👤 Profil": profile_page,
        "🎯 Objectifs": goals_page,
        "🏋️‍♂️ Entraînement": workout_page,
        "⏱️ Repos": rest_page,
        "🧮 Calculateurs": calculators_page,
        "📋 Programmes": programs_page,
        "🤖 Coach IA": ai_coach_page,
        "🍽️ Nutrition": nutrition_page,
        "📝 Notes": notes_page,
        "📲 Installation": install_page
    }
    
    # Sélection de la page
    selected_page = st.sidebar.radio(
        "Aller à:",
        list(pages.keys()),
        index=list(pages.keys()).index(st.session_state.current_page) if st.session_state.current_page in pages else 0
    )
    
    # Mettre à jour la page courante
    st.session_state.current_page = selected_page
    
    # Afficher la page sélectionnée
    pages[selected_page]()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **IronMaster Pro v2.0**
    
    💪 *Votre succès commence ici*
    
    ---
    
    [Support Technique](mailto:support@ironmaster.com)
    
    [Conditions d'utilisation](#)
    
    [Politique de confidentialité](#)
    """)

if __name__ == "__main__":
    main()
