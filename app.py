import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json
import calendar
from PIL import Image
import io
import base64
import hashlib

# Configuration de la page
st.set_page_config(
    page_title="FitMaster Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour le thème noir/rouge
st.markdown("""
<style>
    .main {
        background-color: #000000;
    }
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #1a0000 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff0000 0%, #cc0000 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #cc0000 0%, #990000 100%);
    }
    h1, h2, h3 {
        color: #ff0000 !important;
        border-bottom: 2px solid #ff0000;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #000000;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: #ffffff;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff0000 !important;
        color: #000000 !important;
    }
    .metric-card {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid #ff0000;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .logo-container {
        text-align: center;
        padding: 20px;
    }
    .logo-img {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 3px solid #ff0000;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de la session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'age': 25,
        'taille': 180,
        'poids': [{'date': '2024-01-01', 'poids': 80}],
        'exercice_prefere': 'Développé couché',
        'email': 'user@example.com',
        'objectifs': [],
        'seances': {},
        'entrainements': {},
        'notes': '',
        'mensurations': {},
        'photos': [],
        'pr_bench': 80,
        'pr_squat': 100,
        'pr_deadlift': 120
    }

if 'weight_data' not in st.session_state:
    st.session_state.weight_data = pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'poids': np.random.normal(80, 2, 30)
    })

# Fonction pour charger le logo
def load_logo():
    # Logo personnalisé - remplacez par votre URL
    logo_url = "https://i.imgur.com/wlyusJ0.png"  # URL de votre logo
    return f'<div class="logo-container"><img src="{logo_url}" class="logo-img" alt="FitMaster Logo"></div>'

# Fonction pour vérifier l'accès premium
def check_premium_access():
    if 'premium_unlocked' not in st.session_state:
        st.session_state.premium_unlocked = False
    
    if st.session_state.premium_unlocked:
        return True
    
    # Code administrateur
    admin_code = st.sidebar.text_input("Code administrateur", type="password", key="admin_code_input")
    if admin_code == "F12Berlinetta88170":
        st.session_state.premium_unlocked = True
        st.sidebar.success("Accès premium activé !")
        time.sleep(1)
        st.rerun()
        return True
    
    return False

# Fonction pour exporter les données
def exporter_donnees():
    """Exporter les données utilisateur"""
    data_str = json.dumps(st.session_state.user_data, indent=2)
    b64 = base64.b64encode(data_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="fitmaster_data.json">📥 Exporter mes données</a>'
    return href

# Navigation avec onglets
logo_html = load_logo()
st.sidebar.markdown(logo_html, unsafe_allow_html=True)
st.sidebar.markdown("# FitMaster Pro")

menu = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Accueil", "👤 Profil", "🎯 Objectifs", "📅 Calendrier", "💪 Entraînement", 
     "⏱️ Repos", "🧮 Calculateurs", "📝 Notes", "📊 Programmes", "🤖 IA Coach",
     "🍎 Nutrition", "🔓 Accès Premium"]
)

# Page d'accueil
if menu == "🏠 Accueil":
    st.title("🏋️‍♂️ FitMaster Pro")
    st.markdown("### Votre assistant personnel d'entraînement")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Utilisateurs actifs", "1,234")
    with col2:
        st.metric("PR moyen développé", "85 kg")
    with col3:
        st.metric("Calories brûlées", "45,678 kcal")
    
    st.markdown("---")
    
    # Téléchargement de l'application
    st.markdown("### 📱 Télécharger l'application")
    
    tab_android, tab_ios, tab_chrome = st.tabs(["Android", "iOS", "Chrome"])
    
    with tab_android:
        st.markdown("""
        **Installation sur Android :**
        1. Ouvrez Chrome
        2. Allez sur fitmaster.com
        3. Cliquez sur ⋮ (menu)
        4. Sélectionnez "Ajouter à l'écran d'accueil"
        5. Nommez l'application et validez
        """)
    
    with tab_ios:
        st.markdown("""
        **Installation sur iOS :**
        1. Ouvrez Safari
        2. Allez sur fitmaster.com
        3. Cliquez sur 📤 (partager)
        4. Sélectionnez "Sur l'écran d'accueil"
        5. Ajoutez et validez
        """)
    
    with tab_chrome:
        st.markdown("""
        **Installation sur Chrome Desktop :**
        1. Cliquez sur ⋮ (menu)
        2. Aller dans "Plus d'outils"
        3. Sélectionnez "Créer un raccourci"
        4. Cochez "Ouvrir en fenêtre"
        5. Cliquez sur Créer
        """)

# Onglet Profil
elif menu == "👤 Profil":
    st.title("👤 Profil Utilisateur")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Âge", min_value=10, max_value=100, value=25)
            taille = st.number_input("Taille (cm)", min_value=100, max_value=250, value=180)
        
        with col2:
            poids_actuel = st.number_input("Poids actuel (kg)", min_value=30, max_value=200, value=80)
            exercice_prefere = st.selectbox(
                "Exercice préféré",
                ["Développé couché", "Squat", "Soulevé de terre", "Développé militaire", "Rowing"]
            )
        
        email = st.text_input("Adresse email", value="user@example.com")
        
        if st.form_submit_button("💾 Sauvegarder le profil"):
            st.session_state.user_data.update({
                'age': age,
                'taille': taille,
                'poids': st.session_state.user_data['poids'] + [{'date': datetime.now().strftime('%Y-%m-%d'), 'poids': poids_actuel}],
                'exercice_prefere': exercice_prefere,
                'email': email
            })
            st.success("Profil mis à jour !")
    
    st.markdown("---")
    
    # Graphique d'évolution du poids
    st.subheader("📈 Évolution du poids")
    
    if st.session_state.user_data['poids']:
        df_poids = pd.DataFrame(st.session_state.user_data['poids'])
        df_poids['date'] = pd.to_datetime(df_poids['date'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_poids['date'],
            y=df_poids['poids'],
            mode='lines+markers',
            name='Poids',
            line=dict(color='#ff0000', width=3),
            marker=dict(size=10, color='#ff0000')
        ))
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            xaxis_title="Date",
            yaxis_title="Poids (kg)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calcul de la différence
        if len(df_poids) >= 2:
            dernier = df_poids.iloc[-1]['poids']
            premier = df_poids.iloc[0]['poids']
            difference = dernier - premier
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Poids actuel", f"{dernier} kg")
            with col2:
                st.metric("Évolution", f"{difference:+.1f} kg")
    
    # Suivi des mensurations
    st.subheader("📏 Suivi des mensurations")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        bras = st.number_input("Tour de bras (cm)", min_value=10, max_value=100, value=35)
    with col2:
        cuisses = st.number_input("Cuisses (cm)", min_value=30, max_value=150, value=55)
    with col3:
        taille_input = st.number_input("Taille (cm)", min_value=30, max_value=150, value=85, key="taille_input")
    with col4:
        poitrine = st.number_input("Poitrine (cm)", min_value=50, max_value=200, value=100)
    
    if st.button("Enregistrer les mensurations", key="save_mensurations"):
        st.session_state.user_data['mensurations'] = {
            'bras': bras,
            'cuisses': cuisses,
            'taille': taille_input,
            'poitrine': poitrine,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        st.success("Mensurations enregistrées !")
    
    # Photos avant/après
    st.subheader("📸 Photos de progression")
    uploaded_photos = st.file_uploader(
        "Ajouter des photos",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True
    )
    
    if uploaded_photos:
        cols = st.columns(min(3, len(uploaded_photos)))
        for idx, photo in enumerate(uploaded_photos[:3]):
            with cols[idx]:
                st.image(photo, caption=f"Photo {idx+1}")

# Onglet Objectifs
elif menu == "🎯 Objectifs":
    st.title("🎯 Objectifs")
    
    # Création d'un objectif
    with st.expander("➕ Nouvel objectif", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            type_objectif = st.selectbox(
                "Type d'objectif",
                ["Prise de masse", "Perte de poids", "Gain de force", "Endurance", "Performance spécifique"]
            )
            exercice_objectif = st.selectbox(
                "Exercice",
                ["Développé couché", "Squat", "Soulevé de terre", "Poids corporel", "Autre"]
            )
        
        with col2:
            valeur_objectif = st.number_input("Valeur cible", min_value=0, value=100)
            date_objectif = st.date_input("Date cible", 
                                         min_value=datetime.now().date(),
                                         value=datetime.now().date() + timedelta(days=30))
        
        if st.button("Définir l'objectif", key="define_goal"):
            nouvel_objectif = {
                'type': type_objectif,
                'exercice': exercice_objectif,
                'valeur': valeur_objectif,
                'date': date_objectif.strftime('%Y-%m-%d'),
                'progress': 0
            }
            st.session_state.user_data['objectifs'].append(nouvel_objectif)
            st.success("Objectif défini !")
    
    # Affichage des objectifs avec jauges
    st.subheader("📊 Suivi des objectifs")
    
    if st.session_state.user_data['objectifs']:
        for idx, obj in enumerate(st.session_state.user_data['objectifs']):
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                st.markdown(f"**{obj['type']}**")
                st.caption(f"{obj['exercice']} - {obj['valeur']}")
            
            with col2:
                progress = min(obj.get('progress', 0), 100)
                st.progress(progress / 100)
                st.caption(f"{progress}% - Objectif: {obj['date']}")
            
            with col3:
                col_delete, col_edit = st.columns(2)
                with col_delete:
                    if st.button("🗑️", key=f"del_{idx}"):
                        st.session_state.user_data['objectifs'].pop(idx)
                        st.rerun()
                with col_edit:
                    if st.button("✏️", key=f"edit_{idx}"):
                        st.session_state.editing_goal = idx
    else:
        st.info("Aucun objectif défini. Créez-en un nouveau !")
    
    # Objectifs multiples
    st.subheader("🎯 Objectifs multiples")
    
    tab_poids, tab_mens, tab_perf = st.tabs(["Poids", "Mensurations", "Performance"])
    
    with tab_poids:
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Objectif poids (kg)", min_value=30, max_value=200, value=75, key="goal_weight")
        with col2:
            st.date_input("Date objectif poids", key="goal_weight_date")
    
    with tab_mens:
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Objectif tour de bras (cm)", value=40, key="goal_arms")
        with col2:
            st.number_input("Objectif tour de taille (cm)", value=80, key="goal_waist")

# Onglet Calendrier
elif menu == "📅 Calendrier":
    st.title("📅 Calendrier des séances")
    
    # Calendrier
    today = datetime.now().date()
    st.subheader(f"Aujourd'hui: {today.strftime('%d/%m/%Y')}")
    
    # Sélection de date
    selected_date = st.date_input("Sélectionnez une date", today, key="calendar_date")
    
    # Entrée de séance
    with st.form("session_form"):
        st.markdown(f"### Séance du {selected_date.strftime('%d/%m/%Y')}")
        
        duree = st.slider("Durée (minutes)", 15, 180, 60, key="session_duration")
        programme = st.text_area("Programme de la séance", 
                               placeholder="Décrivez votre séance...",
                               key="session_program")
        
        exercices = st.multiselect(
            "Exercices réalisés",
            ["Développé couché", "Développé incliné", "Squat", "Soulevé de terre", 
             "Rowing", "Développé militaire", "Curl", "Élévation latérale"],
            default=["Développé couché", "Squat"],
            key="session_exercises"
        )
        
        if st.form_submit_button("💾 Enregistrer la séance"):
            key = selected_date.strftime('%Y-%m-%d')
            st.session_state.user_data['seances'][key] = {
                'date': key,
                'duree': duree,
                'programme': programme,
                'exercices': exercices
            }
            st.success("Séance enregistrée !")
    
    # Affichage du calendrier avec jours actuels en rouge
    st.markdown("---")
    st.subheader("📅 Vue mensuelle")
    
    # Générer les jours du mois
    cal = calendar.Calendar()
    month_days = cal.monthdatescalendar(today.year, today.month)
    
    # Afficher le calendrier
    for week in month_days:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == today:
                    st.markdown(f"<div style='background: red; color: white; padding: 5px; border-radius: 5px; text-align: center;'>{day.day}</div>", 
                              unsafe_allow_html=True)
                elif day.month != today.month:
                    st.markdown(f"<div style='color: #666; text-align: center;'>{day.day}</div>", 
                              unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: center;'>{day.day}</div>", 
                              unsafe_allow_html=True)

# Onglet Entraînement
elif menu == "💪 Entraînement":
    st.title("💪 Suivi d'entraînement")
    
    tabs = st.tabs(["📊 Graphiques", "📝 Carnet", "🎥 Technique", "📋 Historique"])
    
    with tabs[0]:
        # Graphiques par exercice
        st.subheader("📈 Suivi des performances par exercice")
        
        exercices = {
            "Développé couché": [80, 82, 85, 83, 87, 85, 90],
            "Squat": [100, 102, 105, 103, 107, 106, 110],
            "Soulevé de terre": [120, 122, 125, 123, 127, 126, 130],
            "Développé militaire": [60, 62, 65, 63, 67, 65, 70]
        }
        
        selected_exercices = st.multiselect(
            "Sélectionnez les exercices à comparer",
            list(exercices.keys()),
            default=["Développé couché", "Squat"],
            key="exercice_comparison"
        )
        
        if selected_exercices:
            fig = go.Figure()
            
            colors = ['#ff0000', '#ff6666', '#ff9999', '#ffcccc']
            for idx, exo in enumerate(selected_exercices):
                fig.add_trace(go.Scatter(
                    x=list(range(1, 8)),
                    y=exercices[exo],
                    mode='lines+markers',
                    name=exo,
                    line=dict(color=colors[idx % len(colors)], width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                title="Évolution des charges",
                xaxis_title="Séances",
                yaxis_title="Poids (kg)",
                template='plotly_dark',
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        # Carnet de séance en temps réel
        st.subheader("📝 Carnet de séance")
        
        exercice = st.selectbox("Exercice", list(exercices.keys()), key="training_exercise")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            series = st.number_input("Série", min_value=1, max_value=10, value=3, key="training_series")
        with col2:
            reps = st.number_input("Répétitions", min_value=1, max_value=50, value=10, key="training_reps")
        with col3:
            poids = st.number_input("Poids (kg)", min_value=0, max_value=500, value=80, key="training_weight")
        
        notes = st.text_area("Notes (sensations, forme, douleurs)", key="training_notes")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Ajouter la série", key="add_series"):
                if 'entrainements' not in st.session_state.user_data:
                    st.session_state.user_data['entrainements'] = {}
                if exercice not in st.session_state.user_data['entrainements']:
                    st.session_state.user_data['entrainements'][exercice] = []
                
                st.session_state.user_data['entrainements'][exercice].append({
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'series': series,
                    'reps': reps,
                    'poids': poids,
                    'notes': notes
                })
                st.success("Série ajoutée !")
        
        with col2:
            if st.button("⏱️ Timer entre séries", key="series_timer"):
                st.session_state.timer_active = True
    
    with tabs[2]:
        # Description technique des exercices
        st.subheader("🎥 Guide technique des exercices")
        
        exercice_detail = st.selectbox(
            "Sélectionnez un exercice",
            ["Développé couché", "Développé incliné", "Squat", "Soulevé de terre", 
             "Romanian Deadlift", "Rowing", "Développé militaire", "Élévation latérale", "Curl"],
            key="exercise_detail"
        )
        
        if exercice_detail == "Développé couché":
            st.markdown("""
            ### 🏋️ Technique du Développé Couché
            
            **🎯 Position de départ :**
            - Allongé sur le banc, pieds au sol
            - Dos en légère cambrure naturelle
            - Omoplates rétractées et stables
            
            **🤲 Prise :**
            - Largeur d'épaules + 10-15cm
            - Pouces autour de la barre (prise suicide interdite)
            - Poignets alignés avec les avant-bras
            
            **🔄 Exécution :**
            1. Descendre la barre au milieu de la poitrine
            2. Toucher légèrement le torse (sans rebond)
            3. Pousser en ligne droite vers le haut
            4. Bloquer les coudes en haut sans hyperextension
            
            **📐 Angles :**
            - Mains : 45° par rapport au torse
            - Coudes : 75-90° en bas du mouvement
            - Épaules : 45-60° d'abduction
            
            **🌬️ Respiration :** Inspirer à la descente, expirer à la montée
            """)
        elif exercice_detail == "Squat":
            st.markdown("""
            ### 🦵 Technique du Squat
            
            **🎯 Position de départ :**
            - Barre sur les trapèzes (haute) ou deltoïdes postérieurs (basse)
            - Pieds écartés largeur d'épaules
            - Pointes légèrement vers l'extérieur (15-30°)
            
            **⬇️ Descente :**
            - Commencer par les hanches
            - Dos droit, regard devant ou légèrement vers le haut
            - Genoux alignés avec les pieds
            - Descendre jusqu'à parallèle (cuisses // sol)
            
            **⬆️ Remontée :**
            - Pousser avec les talons
            - Garder le torse droit
            - Contracter les fessiers en haut
            
            **📐 Profondeur :**
            - Débutant : jusqu'à parallèle
            - Avancé : ATG (ass to grass)
            """)
        elif exercice_detail == "Soulevé de terre":
            st.markdown("""
            ### ⚡ Technique du Soulevé de Terre
            
            **🎯 Position de départ :**
            - Barre contre les tibias
            - Pieds largeur de hanches
            - Dos droit, hanches basses, épaules au-dessus de la barre
            
            **⬆️ Soulevé :**
            - Pousser avec les jambes (phase 1)
            - Terminer avec les hanches (phase 2)
            - Garder la barre proche du corps
            - Dos contracté et droit
            
            **⬇️ Descente :**
            - Flexion des hanches d'abord
            - Barre contrôle le long des cuisses
            - Repos complet au sol entre reps
            
            **⚙️ Variantes :**
            - Conventionnel : prise mixte/supination
            - Sumo : jambes très écartées
            - Roumain : jambes tendues
            """)
        elif exercice_detail == "Développé militaire":
            st.markdown("""
            ### 💂 Technique du Développé Militaire
            
            **🎯 Position de départ :**
            - Debout ou assis
            - Barre au niveau des clavicules
            - Poignets droits, coudes vers l'avant
            
            **⬆️ Montée :**
            - Pousser verticalement
            - Garder le tronc gainé
            - Passer près du visage (pas d'arc)
            
            **⬇️ Descente :**
            - Contrôler la descente
            - Arrêter au niveau des épaules
            - Répéter sans élan
            
            **🏋️‍♂️ Position :**
            - Debout : plus fonctionnel, engage le gainage
            - Assis : isole mieux les épaules
            """)
    
    with tabs[3]:
        # Historique détaillé
        st.subheader("📋 Historique des entraînements")
        
        if 'entrainements' in st.session_state.user_data and st.session_state.user_data['entrainements']:
            for exo, sessions in st.session_state.user_data['entrainements'].items():
                with st.expander(f"{exo} ({len(sessions)} sessions)"):
                    for session in sessions[-5:]:  # 5 dernières sessions
                        st.write(f"**📅 {session['date']}**")
                        st.write(f"**Séries:** {session['series']}x{session['reps']} @ {session['poids']}kg")
                        if session.get('notes'):
                            st.caption(f"📝 Notes: {session['notes']}")
                        st.markdown("---")
        else:
            st.info("Aucun entraînement enregistré. Commencez à tracker vos séances !")

# Onglet Repos
elif menu == "⏱️ Repos":
    st.title("⏱️ Gestion des temps de repos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Timer de repos
        st.subheader("⏱️ Timer de repos")
        
        minutes = st.number_input("Minutes", min_value=0, max_value=10, value=1, key="rest_minutes")
        seconds = st.number_input("Secondes", min_value=0, max_value=59, value=30, key="rest_seconds")
        
        total_seconds = minutes * 60 + seconds
        
        if 'timer_start' not in st.session_state:
            st.session_state.timer_start = None
            st.session_state.timer_running = False
        
        if st.button("▶️ Démarrer le timer", key="start_timer") and total_seconds > 0:
            st.session_state.timer_start = time.time()
            st.session_state.timer_duration = total_seconds
            st.session_state.timer_running = True
            st.rerun()
        
        if st.session_state.timer_running:
            elapsed = time.time() - st.session_state.timer_start
            remaining = max(0, st.session_state.timer_duration - elapsed)
            
            if remaining > 0:
                mins, secs = divmod(int(remaining), 60)
                timer_text = f"{mins:02d}:{secs:02d}"
                
                # Jauge de progression
                progress = (st.session_state.timer_duration - remaining) / st.session_state.timer_duration
                st.progress(progress)
                
                st.markdown(f"<h1 style='text-align: center; color: red;'>{timer_text}</h1>", 
                          unsafe_allow_html=True)
                
                # Bouton d'arrêt
                if st.button("⏹️ Arrêter", key="stop_timer"):
                    st.session_state.timer_running = False
                    st.rerun()
                
                # Actualiser automatiquement
                time.sleep(1)
                st.rerun()
            else:
                st.session_state.timer_running = False
                st.balloons()
                st.markdown("""
                <div style='text-align: center; padding: 20px; background: red; border-radius: 10px;'>
                    <h1 style='color: white;'>⏰ Temps de repos terminé !</h1>
                    <h2 style='color: white;'>Retour au charbon ! 💪</h2>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # Mini-jeu Flappy Biceps
        st.subheader("🎮 Flappy Biceps")
        
        st.markdown("""
        <div style='border: 2px solid red; padding: 10px; border-radius: 10px; text-align: center; background: #000033;'>
            <h3 style='color: white;'>💪 Flappy Biceps</h3>
            <p style='color: white;'>Espace pour faire un curl !</p>
            <div style='height: 200px; background: linear-gradient(180deg, #000033 0%, #000066 100%); 
                        border-radius: 5px; position: relative; overflow: hidden;'>
                <div style='position: absolute; top: 50%; left: 50px; width: 40px; height: 40px; 
                            background: url(https://img.icons8.com/color/96/muscle.png) center/contain no-repeat;'>
                </div>
                <div style='position: absolute; top: 30%; right: 30px; width: 30px; height: 60px; background: green;'></div>
                <div style='position: absolute; top: 60%; right: 80px; width: 30px; height: 80px; background: green;'></div>
            </div>
            <p style='color: white; margin-top: 10px;'>Appuyez sur ESPACE pour faire un curl !</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Démarrer le jeu", key="start_game"):
            st.info("🎮 Jeu en développement - Version complète bientôt disponible !")
            st.markdown("""
            **🎯 Instructions :**
            - Appuyez sur ESPACE pour faire un curl
            - Évitez les obstacles verts
            - Atteignez le score le plus élevé !
            """)

# Onglet Calculateurs
elif menu == "🧮 Calculateurs":
    st.title("🧮 Calculateurs")
    
    tabs = st.tabs(["🔥 Calories dépensées", "🍽️ Calories consommées", "🏋️‍♂️ 1RM", "📊 Macros"])
    
    with tabs[0]:
        st.subheader("🔥 Calculateur de calories dépensées")
        
        activite = st.selectbox(
            "Activité sportive",
            ["Musculation", "Course à pied", "Natation", "Cyclisme", "Basketball", 
             "Football", "Yoga", "HIIT", "CrossFit", "Marche", "Escalade"],
            key="activity_calc"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            duree = st.number_input("Durée (minutes)", min_value=1, max_value=300, value=60, key="duration_calc")
        with col2:
            intensite = st.select_slider("Intensité", ["Légère", "Modérée", "Intense"], key="intensity_calc")
        
        poids_user = st.session_state.user_data['poids'][-1]['poids'] if st.session_state.user_data['poids'] else 70
        
        if st.button("Calculer", key="calculate_calories"):
            # Facteurs MET approximatifs
            met_values = {
                "Musculation": {"Légère": 3.5, "Modérée": 5.0, "Intense": 6.0},
                "Course à pied": {"Légère": 8.0, "Modérée": 10.0, "Intense": 12.5},
                "Natation": {"Légère": 5.8, "Modérée": 8.0, "Intense": 10.0},
                "Basketball": {"Légère": 6.0, "Modérée": 8.0, "Intense": 10.0},
                "Football": {"Légère": 7.0, "Modérée": 9.0, "Intense": 11.0},
                "Yoga": {"Légère": 2.5, "Modérée": 4.0, "Intense": 6.0},
                "HIIT": {"Légère": 8.0, "Modérée": 10.0, "Intense": 12.0},
                "CrossFit": {"Légère": 8.0, "Modérée": 10.0, "Intense": 12.0},
                "Cyclisme": {"Légère": 4.0, "Modérée": 6.0, "Intense": 10.0},
                "Marche": {"Légère": 2.5, "Modérée": 3.5, "Intense": 5.0},
                "Escalade": {"Légère": 5.0, "Modérée": 7.0, "Intense": 9.0}
            }
            
            met_default = {"Légère": 4.0, "Modérée": 6.0, "Intense": 8.0}
            met = met_values.get(activite, met_default).get(intensite, 5.0)
            calories = met * poids_user * (duree / 60)
            
            st.success(f"**🔥 Calories dépensées : {calories:.0f} kcal**")
            
            # Comparaison
            st.info(f"""
            **📊 Comparaison :**
            - {calories:.0f} kcal = environ {calories/110:.1f} tranches de pain
            - {calories:.0f} kcal = environ {calories/230:.1f} pommes
            - {calories:.0f} kcal = environ {calories/50:.1f} minutes de marche
            """)
    
    with tabs[1]:
        st.subheader("🍽️ Calculateur de repas")
        
        repas = st.text_area("Description du repas", 
                           placeholder="Ex: 200g de poulet, 100g de riz, légumes...",
                           key="meal_description")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            proteines = st.number_input("Protéines (g)", min_value=0.0, value=30.0, step=1.0, key="meal_protein")
        with col2:
            glucides = st.number_input("Glucides (g)", min_value=0.0, value=40.0, step=1.0, key="meal_carbs")
        with col3:
            lipides = st.number_input("Lipides (g)", min_value=0.0, value=20.0, step=1.0, key="meal_fat")
        with col4:
            kcal = st.number_input("Calories (kcal)", min_value=0.0, value=350.0, step=10.0, key="meal_calories")
        
        # Calcul automatique si calories non renseignées
        if kcal == 0 and (proteines > 0 or glucides > 0 or lipides > 0):
            kcal = (proteines * 4) + (glucides * 4) + (lipides * 9)
            st.caption(f"Calories estimées : {kcal:.0f} kcal")
        
        if st.button("Ajouter au journal", key="add_meal"):
            if 'repas' not in st.session_state.user_data:
                st.session_state.user_data['repas'] = []
            
            st.session_state.user_data['repas'].append({
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'description': repas,
                'proteines': proteines,
                'glucides': glucides,
                'lipides': lipides,
                'kcal': kcal
            })
            st.success("Repas enregistré !")
            
            # Résumé
            st.info(f"""
            **📋 Résumé du repas :**
            - Protéines: {proteines}g ({proteines*4:.0f} kcal)
            - Glucides: {glucides}g ({glucides*4:.0f} kcal)
            - Lipides: {lipides}g ({lipides*9:.0f} kcal)
            - **Total: {kcal:.0f} kcal**
            """)
    
    with tabs[2]:
        st.subheader("🏋️‍♂️ Calculateur de 1RM (Rep Max)")
        
        exercice_1rm = st.selectbox(
            "Exercice",
            ["Développé couché", "Squat", "Soulevé de terre", "Développé militaire", "Tractions", "Rowing"],
            key="1rm_exercise"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            poids = st.number_input("Poids soulevé (kg)", min_value=1.0, value=80.0, step=2.5, key="1rm_weight")
        with col2:
            reps = st.number_input("Nombre de répétitions", min_value=1, max_value=20, value=5, key="1rm_reps")
        
        # Formule de Brzycki
        if st.button("Calculer 1RM", key="calculate_1rm"):
            if reps == 1:
                rm1 = poids
            else:
                rm1 = poids / (1.0278 - 0.0278 * reps)
            
            st.metric("🎯 1RM estimé", f"{rm1:.1f} kg")
            
            # Suggestions d'entraînement
            st.info(f"""
            **📊 Suggestions d'entraînement :**
            
            **💪 Force (3-5 reps) :**
            - 90% de 1RM : {rm1*0.9:.1f} kg
            - 85% de 1RM : {rm1*0.85:.1f} kg
            - 80% de 1RM : {rm1*0.8:.1f} kg
            
            **🏋️‍♂️ Hypertrophie (8-12 reps) :**
            - 75% de 1RM : {rm1*0.75:.1f} kg
            - 70% de 1RM : {rm1*0.7:.1f} kg
            - 65% de 1RM : {rm1*0.65:.1f} kg
            
            **💨 Endurance (15-20 reps) :**
            - 60% de 1RM : {rm1*0.6:.1f} kg
            - 55% de 1RM : {rm1*0.55:.1f} kg
            - 50% de 1RM : {rm1*0.5:.1f} kg
            """)
            
            # Graphique
            percentages = [90, 85, 80, 75, 70, 65, 60, 55, 50]
            weights = [rm1 * p/100 for p in percentages]
            
            fig = go.Figure(data=[go.Bar(
                x=[f"{p}%" for p in percentages],
                y=weights,
                marker_color='#ff0000',
                text=[f"{w:.1f}kg" for w in weights],
                textposition='auto'
            )])
            
            fig.update_layout(
                title="Charges recommandées",
                yaxis_title="Poids (kg)",
                height=300,
                template='plotly_dark'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:
        st.subheader("📊 Calculateur de Macros")
        
        col1, col2 = st.columns(2)
        with col1:
            objectif = st.selectbox(
                "Objectif",
                ["Prise de masse", "Perte de poids", "Maintien", "Sèche"],
                key="macros_goal"
            )
            poids_macros = st.number_input("Poids (kg)", min_value=30.0, max_value=200.0, value=80.0, key="macros_weight")
        
        with col2:
            activite_macros = st.selectbox(
                "Niveau d'activité",
                ["Sédentaire", "Légèrement actif", "Modérément actif", "Très actif", "Extrêmement actif"],
                key="macros_activity"
            )
            age_macros = st.number_input("Âge", min_value=10, max_value=100, value=30, key="macros_age")
        
        if st.button("Calculer mes macros", key="calculate_macros"):
            # Calcul du métabolisme de base (Harris-Benedict)
            if st.session_state.user_data.get('sexe') == 'F':
                bmr = 655.1 + (9.563 * poids_macros) + (1.850 * st.session_state.user_data['taille']) - (4.676 * age_macros)
            else:
                bmr = 66.5 + (13.75 * poids_macros) + (5.003 * st.session_state.user_data['taille']) - (6.755 * age_macros)
            
            # Facteur d'activité
            activity_factors = {
                "Sédentaire": 1.2,
                "Légèrement actif": 1.375,
                "Modérément actif": 1.55,
                "Très actif": 1.725,
                "Extrêmement actif": 1.9
            }
            
            tdee = bmr * activity_factors.get(activite_macros, 1.375)
            
            # Ajustement selon l'objectif
            goal_factors = {
                "Prise de masse": 1.2,
                "Perte de poids": 0.8,
                "Maintien": 1.0,
                "Sèche": 0.75
            }
            
            calories_journalieres = tdee * goal_factors.get(objectif, 1.0)
            
            # Répartition des macros
            if objectif == "Prise de masse":
                protein_g = poids_macros * 2.2  # 2.2g/kg
                fat_percent = 0.25  # 25% des calories
                carb_percent = 1 - fat_percent - (protein_g * 4 / calories_journalieres)
            elif objectif == "Perte de poids":
                protein_g = poids_macros * 2.5  # 2.5g/kg
                fat_percent = 0.30  # 30% des calories
                carb_percent = 1 - fat_percent - (protein_g * 4 / calories_journalieres)
            else:
                protein_g = poids_macros * 1.8  # 1.8g/kg
                fat_percent = 0.25  # 25% des calories
                carb_percent = 1 - fat_percent - (protein_g * 4 / calories_journalieres)
            
            fat_g = (calories_journalieres * fat_percent) / 9
            carb_g = (calories_journalieres * carb_percent) / 4
            
            st.success(f"**🎯 Calories quotidiennes : {calories_journalieres:.0f} kcal**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Protéines", f"{protein_g:.0f}g", f"{protein_g*4/calories_journalieres*100:.0f}%")
            with col2:
                st.metric("Glucides", f"{carb_g:.0f}g", f"{carb_g*4/calories_journalieres*100:.0f}%")
            with col3:
                st.metric("Lipides", f"{fat_g:.0f}g", f"{fat_g*9/calories_journalieres*100:.0f}%")
            
            # Diagramme circulaire
            fig = go.Figure(data=[go.Pie(
                labels=['Protéines', 'Glucides', 'Lipides'],
                values=[protein_g*4, carb_g*4, fat_g*9],
                hole=.3,
                marker_colors=['#ff0000', '#ff6666', '#ff9999'],
                textinfo='percent+label'
            )])
            
            fig.update_layout(
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Onglet Notes
elif menu == "📝 Notes":
    st.title("📝 Journal d'entraînement")
    
    tab_notes, tab_stats = st.tabs(["📝 Notes manuscrites", "📊 Statistiques"])
    
    with tab_notes:
        notes = st.text_area(
            "Vos notes d'entraînement",
            height=300,
            placeholder="Notez vos sensations, vos performances, vos douleurs, vos observations...",
            key="training_notes_area",
            value=st.session_state.user_data.get('notes', '')
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Sauvegarder les notes", key="save_notes"):
                st.session_state.user_data['notes'] = notes
                st.success("Notes sauvegardées !")
        with col2:
            if st.button("🗑️ Effacer", key="clear_notes"):
                st.session_state.user_data['notes'] = ''
                st.rerun()
        
        if st.session_state.user_data.get('notes'):
            st.markdown("---")
            st.subheader("📄 Notes précédentes")
            st.write(st.session_state.user_data['notes'])
    
    with tab_stats:
        st.subheader("📊 Statistiques personnelles")
        
        if 'entrainements' in st.session_state.user_data and st.session_state.user_data['entrainements']:
            total_seances = sum(len(sessions) for sessions in st.session_state.user_data['entrainements'].values())
            total_series = sum(sum(s.get('series', 1) for s in sessions) for sessions in st.session_state.user_data['entrainements'].values())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Séances totales", total_seances)
            with col2:
                st.metric("Exercices différents", len(st.session_state.user_data['entrainements']))
            with col3:
                st.metric("Séries totales", total_series)
            
            # Graphique d'activité
            exercice_names = list(st.session_state.user_data['entrainements'].keys())
            session_counts = [len(sessions) for sessions in st.session_state.user_data['entrainements'].values()]
            
            fig = go.Figure(data=[go.Bar(
                x=exercice_names,
                y=session_counts,
                marker_color='#ff0000',
                text=session_counts,
                textposition='auto'
            )])
            
            fig.update_layout(
                title="Séances par exercice",
                xaxis_title="Exercice",
                yaxis_title="Nombre de séances",
                height=400,
                template='plotly_dark'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Dernières séances
            st.subheader("📅 5 dernières séances")
            all_sessions = []
            for exo, sessions in st.session_state.user_data['entrainements'].items():
                for session in sessions:
                    all_sessions.append({
                        'exercice': exo,
                        'date': session['date'],
                        'series': session.get('series', 'N/A'),
                        'reps': session.get('reps', 'N/A'),
                        'poids': session.get('poids', 'N/A')
                    })
            
            # Trier par date
            all_sessions.sort(key=lambda x: x['date'], reverse=True)
            
            for session in all_sessions[:5]:
                st.write(f"**{session['exercice']}** - {session['date']}")
                st.write(f"{session['series']}x{session['reps']} @ {session['poids']}kg")
                st.markdown("---")
        else:
            st.info("Aucune statistique disponible. Commencez à tracker vos entraînements !")

# Onglet Programmes
elif menu == "📊 Programmes":
    st.title("📊 Programmes d'entraînement")
    
    tabs = st.tabs(["🏁 Débutant", "💪 PPL 6 jours", "🔥 Amélioration PR", "🏠 Cardio Maison", "✏️ Personnalisé"])
    
    with tabs[0]:
        st.subheader("🏁 Programme Débutant - 5 jours")
        
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        
        for jour in jours:
            with st.expander(f"{jour}", expanded=(jour=="Lundi")):
                if jour == "Lundi":
                    st.markdown("""
                    **💪 Pectoraux/Triceps**
                    
                    **Échauffement (10min):**
                    - Rameur: 5min
                    - Rotateurs d'épaules: 2x15
                    - Pompes: 2x15
                    
                    **Séance principale:**
                    - Développé couché: 3x8-12 reps
                    - Développé incliné haltères: 3x10-12 reps
                    - Écarté couché: 3x12-15 reps
                    - Extension triceps à la poulie: 3x10-12 reps
                    - Dips assistés: 3xMax reps
                    
                    **📝 Notes:**
                    - Repos: 60-90s entre les séries
                    - Tempo: 2-1-2 (2s descente, 1s pause, 2s montée)
                    """)
                elif jour == "Mardi":
                    st.markdown("""
                    **💪 Dos/Biceps**
                    
                    **Échauffement (10min):**
                    - Rameur: 5min
                    - Écartés bras tendus: 2x15
                    - Tractions assistées: 2xMax
                    
                    **Séance principale:**
                    - Tractions assistées: 4xMax reps
                    - Rowing barre: 3x8-12 reps
                    - Tirage vertical prise serrée: 3x10-12 reps
                    - Curl barre EZ: 3x10-12 reps
                    - Curl marteau: 3x12-15 reps
                    
                    **📝 Notes:**
                    - Focus sur la contraction du dos
                    - Garder le dos droit au rowing
                    """)
                elif jour == "Mercredi":
                    st.markdown("""
                    **💪 Jambes**
                    
                    **Échauffement (10min):**
                    - Vélo: 5min
                    - Squats bodyweight: 2x20
                    - Fentes: 2x10 par jambe
                    
                    **Séance principale:**
                    - Squat: 3x8-12 reps
                    - Presse à cuisses: 3x10-12 reps
                    - Leg curl: 3x12-15 reps
                    - Leg extension: 3x12-15 reps
                    - Mollets debout: 4x15-20 reps
                    
                    **📝 Notes:**
                    - Ne pas verrouiller les genoux
                    - Respirer correctement au squat
                    """)
                elif jour == "Jeudi":
                    st.markdown("""
                    **💪 Épaules/Abdos**
                    
                    **Échauffement (10min):**
                    - Corde à sauter: 5min
                    - Rotateurs externes: 2x15
                    - Élévations latérales légères: 2x15
                    
                    **Séance principale:**
                    - Développé militaire assis: 3x8-12 reps
                    - Élévations latérales: 3x12-15 reps
                    - Face pull: 3x15-20 reps
                    - Crunch: 3x20 reps
                    - Planche: 3x30-60s
                    
                    **📝 Notes:**
                    - Contrôler la descente
                    - Ne pas utiliser d'élan
                    """)
                elif jour == "Vendredi":
                    st.markdown("""
                    **💪 Full Body**
                    
                    **Échauffement (10min):**
                    - Tout le corps: 10min
                    - Mobilité articulaire
                    
                    **Séance principale:**
                    - Soulevé de terre: 3x8-10 reps
                    - Développé couché: 3x8-12 reps
                    - Tractions: 3xMax reps
                    - Squat: 3x10 reps
                    - Curl barre: 3x12 reps
                    
                    **📝 Notes:**
                    - Séance plus légère
                    - Focus sur la technique
                    """)
    
    with tabs[1]:
        st.subheader("💪 Programme PPL - 6 jours")
        
        st.markdown("""
        **📅 Lundi & Jeudi - Push (Poussée)**
        
        **💪 Pectoraux:**
        - Développé couché: 4x5-8 reps
        - Développé incliné haltères: 3x8-12 reps
        - Écarté à la poulie: 3x12-15 reps
        
        **💪 Épaules:**
        - Développé militaire: 3x8-12 reps
        - Élévations latérales: 4x12-15 reps
        - Oiseau: 3x15-20 reps
        
        **💪 Triceps:**
        - Extension triceps à la poulie: 3x10-15 reps
        - Barre au front: 3x8-12 reps
        
        **📅 Mardi & Vendredi - Pull (Tirage)**
        
        **💪 Dos:**
        - Soulevé de terre: 3x5 reps
        - Tractions: 4xMax reps
        - Rowing barre: 3x8-12 reps
        - Tirage horizontal: 3x10-12 reps
        
        **💪 Biceps:**
        - Curl barre EZ: 3x10-12 reps
        - Curl concentration: 3x12-15 reps
        
        **💪 Arrière d'épaules:**
        - Face pull: 3x15-20 reps
        
        **📅 Mercredi & Samedi - Legs (Jambes)**
        
        **💪 Cuisses:**
        - Squat: 4x5-8 reps
        - Presse à cuisses: 3x10-12 reps
        - Fentes: 3x10 par jambe
        
        **💪 Ischios:**
        - Leg curl: 3x12-15 reps
        - RDL (Romanian Deadlift): 3x10-12 reps
        
        **💪 Mollets:**
        - Mollets debout: 4x15-20 reps
        - Mollets assis: 4x15-20 reps
        
        **💪 Abdominaux:**
        - Crunch: 3x20 reps
        - Planche: 3x60s
        - Mountain climbers: 3x30s
        """)
    
    with tabs[2]:
        st.subheader("🔥 Programme Amélioration PR au Bench")
        
        pr_objectif = st.number_input("PR objectif (kg)", min_value=50, max_value=300, value=100, step=5, key="pr_goal")
        
        st.markdown(f"""
        **🎯 Basé sur votre objectif de {pr_objectif}kg:**
        
        **📅 Semaine Type:**
        
        **📌 Lundi (Volume):**
        - Échauffement spécifique: 3x10 @ 50%
        - 4 série de 5 répétitions à {pr_objectif*0.75:.1f}kg (75%)
        - Bench haltère: 3x6-10 reps
        - Triceps barre au front: 3x10-12 reps
        - Pompes diamant: 3xMax
        
        **📌 Mercredi (Technique):**
        - Échauffement: 2x8 @ 50%
        - 3x7 reps à {pr_objectif*0.65:.1f}kg (65%) - tempo 2-1-2
        - Développé militaire: 3x6-10 reps
        - Extension triceps poulie: 3x8-10 reps
        - Curl barre: 3x10-12 reps
        
        **📌 Samedi (Intensité):**
        - Échauffement: pyramide 60-70-80%
        - Single à {pr_objectif*0.8:.1f}kg (80%)
        - 3x3 reps à {pr_objectif*0.75:.1f}kg (75%)
        - Close grip bench: 3x5-8 reps
        
        **📊 Progression:**
        - +2.5% chaque semaine si réussi
        - Reposer 2-3 minutes entre les séries lourdes
        - Focus sur la technique avant la charge
        
        **💡 Conseils:**
        - Travaillez la mobilité scapulaire
        - Renforcez les triceps (70% du développé)
        - Améliorez votre gainage
        """)
        
        if st.button("Générer le programme personnalisé", key="generate_pr_program"):
            st.success(f"🎯 Programme généré pour objectif {pr_objectif}kg !")
            st.balloons()
            
            # Télécharger le programme
            program_text = f"""
            PROGRAMME AMÉLIORATION PR AU BENCH
            Objectif: {pr_objectif}kg
            
            LUNDI (Volume):
            - Échauffement: 3x10 @ {pr_objectif*0.5:.1f}kg
            - 4x5 @ {pr_objectif*0.75:.1f}kg
            - Bench haltère: 3x6-10
            - Triceps: 3x10-12
            
            MERCREDI (Technique):
            - Échauffement: 2x8 @ {pr_objectif*0.5:.1f}kg
            - 3x7 @ {pr_objectif*0.65:.1f}kg (tempo 2-1-2)
            - Développé militaire: 3x6-10
            
            SAMEDI (Intensité):
            - Single @ {pr_objectif*0.8:.1f}kg
            - 3x3 @ {pr_objectif*0.75:.1f}kg
            - Close grip: 3x5-8
            
            Progression: +2.5% par semaine
            """
            
            b64 = base64.b64encode(program_text.encode()).decode()
            href = f'<a href="data:text/plain;base64,{b64}" download="programme_pr_bench.txt">📥 Télécharger le programme</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    with tabs[3]:
        st.subheader("🏠 Programme Cardio à la maison")
        
        st.markdown("""
        **🏃‍♂️ Séance 1 - HIIT (30 minutes):**
        
        **🔥 Échauffement (5min):**
        - Jumping jacks: 1min
        - High knees: 1min
        - Butt kicks: 1min
        - Mountain climbers: 1min
        - Étirements dynamiques: 1min
        
        **💥 Circuit principal (20min):**
        - Burpees: 45s travail / 15s repos
        - Squat jumps: 45s / 15s
        - Push-ups: 45s / 15s
        - Plank jacks: 45s / 15s
        - Lunges sautés: 45s / 15s
        - Repos complet: 1min
        - Répéter le circuit 4 fois
        
        **🧘‍♂️ Retour au calme (5min):**
        - Marche sur place: 2min
        - Étirements statiques: 3min
        
        **🏃‍♀️ Séance 2 - Cardio LISS (45 minutes):**
        
        **🔥 Échauffement (5min):**
        - Marche rapide sur place
        - Rotations articulaires
        
        **🏃‍♂️ Cardio (35min):**
        - Step-ups: 10min
        - Jump rope (corde à sauter): 10min
        - Dancing: 10min
        - Jogging sur place: 5min
        
        **🧘‍♀️ Retour au calme (5min):**
        - Respiration profonde
        - Étirements
        
        **⚡ Séance 3 - Tabata (20 minutes):**
        
        **Format Tabata:**
        - 20s travail MAX
        - 10s repos
        - Répéter 8 fois par exercice
        
        **Exercices:**
        1. Squat thrusters
        2. Push-up to plank
        3. Jump lunges
        4. Russian twists
        
        **💪 Séance 4 - Circuit Full Body (40 minutes):**
        
        **Circuit x4:**
        - Bear crawls: 30s
        - Box jumps (sur marche): 30s
        - Pike push-ups: 30s
        - Superman hold: 30s
        - Bicycle crunches: 30s
        - Repos: 60s entre circuits
        """)
    
    with tabs[4]:
        st.subheader("✏️ Programme Personnalisé")
        
        col1, col2 = st.columns(2)
        with col1:
            jours_semaine = st.slider("Jours par semaine", 3, 7, 4, key="custom_days")
            niveau = st.selectbox("Niveau", ["Débutant", "Intermédiaire", "Avancé"], key="custom_level")
        
        with col2:
            objectif = st.selectbox("Objectif principal", 
                                  ["Prise de masse", "Perte de poids", "Force", "Endurance", "Tonification"],
                                  key="custom_goal")
            focus = st.multiselect(
                "Groupes musculaires à focus",
                ["Pectoraux", "Dos", "Jambes", "Épaules", "Biceps", "Triceps", "Abdominaux"],
                default=["Pectoraux", "Dos", "Jambes"],
                key="custom_focus"
            )
        
        duree_seance = st.slider("Durée séance (min)", 45, 120, 60, key="custom_duration")
        equipment = st.multiselect(
            "Équipement disponible",
            ["Barre + poids", "Haltères", "Machine", "Poids du corps", "Bandes élastiques", "Kettlebell"],
            default=["Barre + poids", "Haltères", "Poids du corps"],
            key="custom_equipment"
        )
        
        if st.button("Créer mon programme", key="create_custom_program"):
            st.success(f"🎯 Programme {niveau} créé pour {jours_semaine} jours/semaine !")
            
            # Générer un programme basique
            program = f"""
            📊 PROGRAMME PERSONNALISÉ
            Niveau: {niveau}
            Jours/semaine: {jours_semaine}
            Objectif: {objectif}
            Focus: {', '.join(focus)}
            Durée/séance: {duree_seance}min
            
            💪 SÉANCE TYPE:
            - Échauffement: 10min
            - Exercices principaux: {duree_seance-20}min
            - Retour au calme: 10min
            
            🏋️‍♂️ EXERCICES RECOMMANDÉS:
            """
            
            if "Pectoraux" in focus:
                program += "\n- Pectoraux: Développé couché, Développé incliné, Écarté"
            if "Dos" in focus:
                program += "\n- Dos: Tractions, Rowing, Tirage vertical"
            if "Jambes" in focus:
                program += "\n- Jambes: Squat, Presse, Fentes, Soulevé de terre"
            if "Épaules" in focus:
                program += "\n- Épaules: Développé militaire, Élévations latérales"
            if "Biceps" in focus:
                program += "\n- Biceps: Curl barre, Curl marteau, Curl concentration"
            if "Triceps" in focus:
                program += "\n- Triceps: Extension poulie, Barre au front, Dips"
            if "Abdominaux" in focus:
                program += "\n- Abdominaux: Crunch, Planche, Mountain climbers"
            
            program += f"\n\n📝 RECOMMANDATIONS:\n- Repos: 60-90s entre séries\n- RPE: 7-8/10\n- Progressive overload chaque semaine"
            
            st.text_area("Votre programme", program, height=300)
            
            # Télécharger
            b64 = base64.b64encode(program.encode()).decode()
            href = f'<a href="data:text/plain;base64,{b64}" download="programme_personnalise.txt">📥 Télécharger le programme</a>'
            st.markdown(href, unsafe_allow_html=True)

# Onglet IA Coach
elif menu == "🤖 IA Coach":
    st.title("🤖 Coach IA Personnel")
    
    if not check_premium_access():
        st.warning("⚠️ Cette fonctionnalité nécessite l'accès premium")
        st.info("Débloquez toutes les fonctionnalités avec le code administrateur ou l'achat premium")
    else:
        st.subheader("🎯 Analyse de vos habitudes")
        
        # Analyse des données utilisateur
        if st.session_state.user_data['poids']:
            dernier_poids = st.session_state.user_data['poids'][-1]['poids']
            premier_poids = st.session_state.user_data['poids'][0]['poids']
            evolution = dernier_poids - premier_poids
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Poids actuel", f"{dernier_poids}kg", f"{evolution:+.1f}kg")
            with col2:
                st.metric("Exercice préféré", st.session_state.user_data['exercice_prefere'])
            with col3:
                st.metric("Objectifs en cours", len(st.session_state.user_data['objectifs']))
        
        # Conseils personnalisés
        st.subheader("💡 Conseils personnalisés")
        
        conseil_type = st.selectbox(
            "Type de conseil",
            ["Nutrition", "Entraînement", "Récupération", "Progression", "Motivation"],
            key="advice_type"
        )
        
        if st.button("🔄 Obtenir des conseils", key="get_advice"):
            with st.spinner("🤖 L'IA analyse vos données..."):
                time.sleep(2)
                
                if conseil_type == "Nutrition":
                    st.success("""
                    **🍎 CONSEILS NUTRITION:**
                    
                    **🎯 Pour votre profil:**
                    - Apport protéique: 2g/kg minimum pour la récupération
                    - Hydratation: 40ml/kg d'eau quotidiennement
                    - Légumes: 500g minimum par jour
                    
                    **🕒 Timing des repas:**
                    - Pré-entraînement (1-2h avant): glucides + protéines
                    - Post-entraînement (30min après): whey protéine + glucides rapides
                    - Dîner: protéines lentes + légumes
                    
                    **🚫 À éviter:**
                    - Sucres ajoutés avant 18h
                    - Repas trop gras avant l'entraînement
                    - Déshydratation
                    """)
                elif conseil_type == "Entraînement":
                    st.success("""
                    **💪 CONSEILS ENTRAÎNEMENT:**
                    
                    **🏋️‍♂️ Pour progresser:**
                    - Variez les angles: incliné/decliné pour les pectoraux
                    - Ajoutez 1 série dégressive à votre dernier exercice
                    - Travaillez la mobilité scapulaire 10min avant développé
                    
                    **📈 Progressive Overload:**
                    - Augmentez les charges de 2.5% chaque semaine
                    - Ajoutez 1 répétition par série
                    - Réduisez le temps de repos de 5s
                    
                    **🎯 Points techniques:**
                    - Tempo contrôlé: 2-1-2 secondes
                    - Amplitude complète
                    - Contraction maximale
                    """)
                elif conseil_type == "Récupération":
                    st.success("""
                    **😴 CONSEILS RÉCUPÉRATION:**
                    
                    **💤 Sommeil:**
                    - 7-8h minimum par nuit
                    - Coucher avant 23h
                    - Chambre à 18-20°C
                    
                    **🛀 Récupération active:**
                    - Étirements légers après chaque séance
                    - Foam rolling 10min/jour
                    - Marche 30min les jours de repos
                    
                    **🍎 Nutrition récupération:**
                    - BCAA pendant l'entraînement long
                    - Magnésium avant le coucher
                    - Oméga-3 quotidiennement
                    """)
                elif conseil_type == "Progression":
                    st.success("""
                    **📈 CONSEILS PROGRESSION:**
                    
                    **🎯 Objectifs SMART:**
                    - Spécifique: "Augmenter mon bench de 5kg"
                    - Mesurable: "Tenir un journal"
                    - Atteignable: "+2.5kg/mois"
                    - Réaliste: "3 séances/semaine"
                    - Temporel: "3 mois"
                    
                    **📊 Tracking:**
                    - Photos mensuelles
                    - Mensurations hebdomadaires
                    - Performances journalières
                    
                    **🔄 Adaptation:**
                    - Changez de programme toutes les 8-12 semaines
                    - Testez votre 1RM chaque trimestre
                    - Écoutez votre corps
                    """)

# Onglet Nutrition
elif menu == "🍎 Nutrition":
    st.title("🍎 Nutrition & Recettes")
    
    if not check_premium_access():
        st.warning("⚠️ Cette fonctionnalité nécessite l'accès premium")
        st.info("Débloquez toutes les fonctionnalités avec le code administrateur ou l'achat premium")
    else:
        tabs = st.tabs(["👨‍🍳 Chef IA", "📅 Tracker quotidien", "🛒 Liste de courses", "📊 Analyse macros", "🍽️ Menus 2300kcal"])
        
        with tabs[0]:
            st.subheader("👨‍🍳 Chef IA - Recettes personnalisées")
            
            col1, col2 = st.columns(2)
            with col1:
                calories = st.slider("Calories par repas", 300, 1000, 600, 50, key="chef_calories")
                proteines = st.slider("Protéines (g)", 20, 80, 40, 5, key="chef_protein")
            
            with col2:
                preferences = st.multiselect(
                    "Préférences/Restrictions",
                    ["Végétarien", "Sans gluten", "Sans lactose", "Paleo", "Keto", "Vegan", "Faible en FODMAP"],
                    key="chef_preferences"
                )
                type_repas = st.selectbox("Type de repas", ["Petit-déjeuner", "Déjeuner", "Dîner", "Collation"], key="chef_meal_type")
            
            if st.button("🍳 Générer une recette", key="generate_recipe"):
                with st.spinner("👨‍🍳 Le chef IA prépare votre recette..."):
                    time.sleep(2)
                    
                    st.success(f"""
                    **🍗 RECETTE POUR {type_repas.upper()}**
                    
                    **🎯 Spécifications:**
                    - Calories: {calories}kcal
                    - Protéines: {proteines}g
                    - Restrictions: {', '.join(preferences) if preferences else 'Aucune'}
                    
                    **📝 Ingrédients:**
                    - 200g de blanc de poulet (ou tofu si végétarien)
                    - 150g de brocolis
                    - 100g de patates douces
                    - 30g d'amandes
                    - 1 cuillère à soupe d'huile d'olive
                    - Épices au choix (curcuma, paprika, ail)
                    
                    **👨‍🍳 Préparation:**
                    1. Préchauffer le four à 200°C
                    2. Couper les légumes et la protéine en morceaux
                    3. Assaisonner et arroser d'huile d'olive
                    4. Cuire 25-30 minutes jusqu'à dorure
                    5. Parsemer d'amandes concassées
                    6. Servir chaud
                    
                    **📊 Macros:**
                    - Protéines: {proteines}g
                    - Glucides: 45g
                    - Lipides: 20g
                    - Fibres: 8g
                    
                    **💡 Astuces:**
                    - Doublez les quantités pour meal prep
                    - Ajoutez du citron pour plus de saveur
                    - Servez avec du riz basmati si besoin de plus de glucides
                    """)
        
        with tabs[1]:
            st.subheader("📅 Tracker nutritionnel quotidien")
            
            today = datetime.now().strftime('%d/%m/%Y')
            st.markdown(f"### 🗓️ Aujourd'hui: {today}")
            
            # Repas de la journée
            repas_types = ["Petit-déjeuner", "Collation 1", "Déjeuner", "Collation 2", "Dîner", "Collation 3"]
            
            total_calories = 0
            total_protein = 0
            total_carbs = 0
            total_fat = 0
            
            for repas in repas_types:
                with st.expander(f"🍽️ {repas}", expanded=(repas=="Petit-déjeuner")):
                    col1, col2 = st.columns(2)
                    with col1:
                        desc = st.text_input(f"Description {repas}", key=f"meal_{repas}")
                    with col2:
                        cals = st.number_input(f"Calories {repas}", 0, 2000, 0, 50, key=f"cals_{repas}")
                    
                    if cals > 0:
                        total_calories += cals
            
            # Résumé de la journée
            st.markdown("---")
            st.subheader("📊 Résumé de la journée")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Calories", f"{total_calories}")
                st.progress(min(total_calories/2500, 1.0))
            with col2:
                protein_input = st.number_input("Protéines (g)", 0, 300, 0, 10, key="daily_protein")
                total_protein = protein_input
            with col3:
                carbs_input = st.number_input("Glucides (g)", 0, 500, 0, 10, key="daily_carbs")
                total_carbs = carbs_input
            with col4:
                fat_input = st.number_input("Lipides (g)", 0, 200, 0, 5, key="daily_fat")
                total_fat = fat_input
            
            # Graphique de la semaine
            st.markdown("---")
            st.subheader("📈 Évolution sur 7 jours")
            
            jours = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
            calories_semaine = [2200, 2100, 2300, 2150, 2400, 2000, 1900]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=jours,
                y=calories_semaine,
                mode='lines+markers',
                name='Calories',
                line=dict(color='#ff0000', width=3),
                marker=dict(size=10)
            ))
            
            fig.add_hline(y=2300, line_dash="dash", line_color="white", annotation_text="Objectif 2300kcal")
            
            fig.update_layout(
                title="Calories sur 7 jours",
                height=300,
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tabs[2]:
            st.subheader("🛒 Liste de courses automatique")
            
            semaine_type = st.selectbox(
                "Type de semaine",
                ["Standard", "Prise de masse", "Perte de poids", "Végétarien", "Sans lactose"],
                key="shopping_type"
            )
            
            personnes = st.slider("Nombre de personnes", 1, 6, 1, key="shopping_people")
            
            if st.button("🔄 Générer la liste de courses", key="generate_shopping"):
                with st.spinner("🛒 Génération de la liste..."):
                    time.sleep(1)
                    
                    st.markdown(f"""
                    **📝 LISTE DE COURSES HEBDOMADAIRE**
                    **Type:** {semaine_type} | **Personnes:** {personnes}
                    
                    **🥩 PROTÉINES ({personnes*1.5}kg):**
                    - Poulet blanc: {personnes*1.0}kg
                    - Œufs: {personnes*12} unités
                    - Thon en boîte: {personnes*4} boîtes
                    - Yaourt grec 0%: {personnes*1.0}kg
                    - Fromage blanc: {personnes*0.5}kg
                    
                    **🥦 LÉGUMES ({personnes*5}kg):**
                    - Brocolis: {personnes*1.0}kg
                    - Épinards: {personnes*0.5}kg
                    - Patates douces: {personnes*2.0}kg
                    - Carottes: {personnes*1.0}kg
                    - Oignons: {personnes*0.5}kg
                    - Ail: {personnes*0.1}kg
                    - Salade verte: {personnes*0.5}kg
                    
                    **🍎 FRUITS ({personnes*3}kg):**
                    - Bananes: {personnes*8} unités
                    - Pommes: {personnes*6} unités
                    - Baies surgelées: {personnes*0.5}kg
                    - Avocats: {personnes*4} unités
                    
                    **🌾 CÉRÉALES ({personnes*2}kg):**
                    - Riz basmati: {personnes*1.0}kg
                    - Flocons d'avoine: {personnes*1.0}kg
                    - Pâtes complètes: {personnes*0.5}kg
                    - Pain complet: {personnes*1} baguette
                    
                    **🥜 NOIX & GRAINES ({personnes*0.5}kg):**
                    - Amandes: {personnes*0.3}kg
                    - Noix: {personnes*0.2}kg
                    - Graines de chia: {personnes*0.1}kg
                    
                    **🧂 CONDIMENTS:**
                    - Huile d'olive: 1L
                    - Vinaigre balsamique: 500ml
                    - Épices diverses
                    - Sel rose de l'Himalaya
                    - Poivre noir
                    
                    **💧 BOISSONS:**
                    - Eau minérale: {personnes*8}L
                    - Café/thé: au choix
                    """)
                    
                    # Télécharger la liste
                    shopping_list = f"Liste de courses - {semaine_type} - {personnes} personnes\n\n"
                    shopping_list += "PROTÉINES:\n"
                    shopping_list += f"- Poulet blanc: {personnes*1.0}kg\n"
                    shopping_list += f"- Œufs: {personnes*12} unités\n"
                    shopping_list += f"- Thon: {personnes*4} boîtes\n\n"
                    
                    shopping_list += "LÉGUMES:\n"
                    shopping_list += f"- Brocolis: {personnes*1.0}kg\n"
                    shopping_list += f"- Patates douces: {personnes*2.0}kg\n\n"
                    
                    shopping_list += "FRUITS:\n"
                    shopping_list += f"- Bananes: {personnes*8} unités\n"
                    shopping_list += f"- Pommes: {personnes*6} unités\n"
                    
                    b64 = base64.b64encode(shopping_list.encode()).decode()
                    href = f'<a href="data:text/plain;base64,{b64}" download="liste_courses.txt">📥 Télécharger la liste</a>'
                    st.markdown(href, unsafe_allow_html=True)
        
        with tabs[3]:
            st.subheader("📊 Analyse des macros")
            
            total_calories = 2300
            
            # Entrée des macros
            col1, col2, col3 = st.columns(3)
            with col1:
                protein_input = st.number_input("Protéines (g)", 0, 300, 150, 10, key="macro_protein")
            with col2:
                carb_input = st.number_input("Glucides (g)", 0, 500, 250, 10, key="macro_carbs")
            with col3:
                fat_input = st.number_input("Lipides (g)", 0, 200, 85, 5, key="macro_fat")
            
            # Calcul des pourcentages
            protein_cals = protein_input * 4
            carb_cals = carb_input * 4
            fat_cals = fat_input * 9
            
            total_input_cals = protein_cals + carb_cals + fat_cals
            
            protein_percent = (protein_cals / total_input_cals * 100) if total_input_cals > 0 else 0
            carb_percent = (carb_cals / total_input_cals * 100) if total_input_cals > 0 else 0
            fat_percent = (fat_cals / total_input_cals * 100) if total_input_cals > 0 else 0
            
            # Affichage des métriques
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Calories totales", f"{total_input_cals:.0f}")
            with col2:
                st.metric("Protéines", f"{protein_input}g", f"{protein_percent:.1f}%")
                st.progress(protein_percent/100)
            with col3:
                st.metric("Glucides", f"{carb_input}g", f"{carb_percent:.1f}%")
                st.progress(carb_percent/100)
            with col4:
                st.metric("Lipides", f"{fat_input}g", f"{fat_percent:.1f}%")
                st.progress(fat_percent/100)
            
            # Diagramme circulaire
            labels = ['Protéines', 'Glucides', 'Lipides']
            values = [protein_cals, carb_cals, fat_cals]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.3,
                marker_colors=['#ff0000', '#ff6666', '#ff9999'],
                textinfo='percent+label',
                textposition='inside'
            )])
            
            fig.update_layout(
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommandations
            st.subheader("🎯 Recommandations")
            
            if protein_percent < 25:
                st.warning("⚠️ Apport protéique faible. Cible: 25-35%")
            elif protein_percent > 40:
                st.warning("⚠️ Apport protéique très élevé")
            else:
                st.success("✅ Apport protéique optimal")
            
            if carb_percent < 40:
                st.warning("⚠️ Apport glucidique faible pour l'énergie")
            elif carb_percent > 60:
                st.warning("⚠️ Apport glucidique très élevé")
            else:
                st.success("✅ Apport glucidique optimal")
            
            if fat_percent < 20:
                st.warning("⚠️ Apport lipidique faible pour les hormones")
            elif fat_percent > 35:
                st.warning("⚠️ Apport lipidique élevé")
            else:
                st.success("✅ Apport lipidique optimal")
        
        with tabs[4]:
            st.subheader("🍽️ Menus à 2300kcal")
            
            menu_choice = st.selectbox(
                "Choisir un menu",
                ["Menu 1 - Prise de masse", "Menu 2 - Équilibré", "Menu 3 - Haute protéine", "Menu 4 - Végétarien"],
                key="menu_choice"
            )
            
            if menu_choice == "Menu 1 - Prise de masse":
                st.markdown("""
                **📊 MENU PRISE DE MASSE - 2300kcal**
                
                **🌅 Petit-déjeuner (600kcal):**
                - Flocons d'avoine: 100g (350kcal)
                - Whey protéine: 30g (120kcal)
                - Banane: 1 moyenne (100kcal)
                - Amandes: 30g (180kcal)
                - Eau: 500ml
                
                **🍽️ Déjeuner (800kcal):**
                - Riz basmati: 200g cuit (260kcal)
                - Poulet: 200g (330kcal)
                - Brocolis: 200g (70kcal)
                - Huile d'olive: 1 cuillère à soupe (120kcal)
                - Avocat: 1/2 (120kcal)
                
                **🕒 Collation (300kcal):**
                - Yaourt grec 0%: 200g (120kcal)
                - Miel: 20g (60kcal)
                - Noix: 20g (120kcal)
                
                **🌙 Dîner (600kcal):**
                - Patate douce: 200g (180kcal)
                - Saumon: 150g (300kcal)
                - Salade verte: 100g (30kcal)
                - Vinaigrette légère: 2 cuillères (90kcal)
                
                **📋 Total: 2300kcal | P: 180g | G: 220g | L: 80g**
                """)
            elif menu_choice == "Menu 2 - Équilibré":
                st.markdown("""
                **📊 MENU ÉQUILIBRÉ - 2300kcal**
                
                **🌅 Petit-déjeuner (550kcal):**
                - Pain complet: 2 tranches (200kcal)
                - Œufs: 2 unités (140kcal)
                - Avocat: 1/2 (120kcal)
                - Fruit de saison: 1 (90kcal)
                
                **🍽️ Déjeuner (850kcal):**
                - Quinoa: 150g cuit (220kcal)
                - Steak haché 5%: 150g (250kcal)
                - Légumes variés: 250g (100kcal)
                - Vinaigrette: légère (80kcal)
                - Fromage: 30g (100kcal)
                
                **🕒 Collation (200kcal):**
                - Fromage blanc 0%: 150g (90kcal)
                - Compote sans sucre: 100g (80kcal)
                - Cannelle: au goût (30kcal)
                
                **🌙 Dîner (700kcal):**
                - Pâtes complètes: 150g (500kcal)
                - Thon au naturel: 150g (150kcal)
                - Sauce tomate: 100g (50kcal)
                
                **📋 Total: 2300kcal | P: 160g | G: 240g | L: 70g**
                """)

# Onglet Accès Premium
elif menu == "🔓 Accès Premium":
    st.title("🔓 Accès Premium")
    
    if check_premium_access():
        st.success("✅ Vous avez déjà accès à toutes les fonctionnalités premium !")
        
        st.markdown("""
        <div style='background: rgba(255, 0, 0, 0.1); padding: 20px; border-radius: 10px; border: 2px solid #ff0000;'>
        <h3 style='color: white;'>🎉 Fonctionnalités Premium débloquées:</h3>
        
        **🤖 Coach IA Personnel:**
        - Analyse avancée de vos données
        - Conseils personnalisés en temps réel
        - Adaptation automatique des programmes
        
        **👨‍🍳 Chef IA Nutrition:**
        - Recettes sur mesure selon vos macros
        - Plans alimentaires complets
        - Liste de courses intelligente
        
        **📊 Programmes Avancés:**
        - Programmes personnalisés PPL
        - Suivi de progression détaillé
        - Adaptation automatique des charges
        
        **📈 Analytics Premium:**
        - Graphiques avancés
        - Export de données
        - Comparaisons détaillées
        
        **🎮 Fonctionnalités Exclusives:**
        - Jeux d'entraînement
        - Communauté premium
        - Support prioritaire
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("🔒 Fonctionnalités premium verrouillées")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div style='background: rgba(255, 0, 0, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #ff0000;'>
            <h3 style='color: white;'>🚀 Passez à la version premium</h3>
            
            **🎯 Ce que vous obtenez:**
            - Coach IA personnel 24/7
            - Chef IA nutrition avec recettes illimitées
            - Programmes d'entraînement sur mesure
            - Analytics avancés
            - Support prioritaire
            - Mises à jour gratuites
            - Contenu exclusif
            
            **💰 Prix: 20€ - Paiement unique**
            <p style='color: #ccc; font-size: 0.9em;'>(Accès à vie - Pas d'abonnement)</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💳 Acheter maintenant - 20€", key="buy_premium"):
                st.info("""
                **💳 Intégration de paiement à venir:**
                - Stripe
                - PayPal
                - Carte bancaire
                - Crypto
                
                **🆓 Pour tester immédiatement, utilisez le code administrateur.**
                """)
        
        with col2:
            st.markdown("""
            <div style='background: rgba(0, 0, 0, 0.5); padding: 20px; border-radius: 10px; border: 1px solid #ff0000;'>
            <h3 style='color: white;'>🔑 Code administrateur</h3>
            
            <p style='color: #ccc;'>Entrez le code pour débloquer gratuitement:</p>
            </div>
            """, unsafe_allow_html=True)
            
            code_input = st.text_input(" ", type="password", key="admin_code_final", label_visibility="collapsed")
            
            if st.button("🔓 Déverrouiller avec code", key="unlock_code"):
                if code_input == "F12Berlinetta88170":
                    st.session_state.premium_unlocked = True
                    st.success("✅ Accès premium activé !")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Code incorrect")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p style='font-size: 1.2em; margin-bottom: 10px;'>🏋️‍♂️ FitMaster Pro © 2024</p>
    <p style='margin-bottom: 5px;'>Votre assistant personnel d'entraînement</p>
    <p style='margin-bottom: 5px;'>📧 support@fitmaster.com | 📞 +33 1 23 45 67 89</p>
    <div style='margin-top: 15px;'>
        <a href="#" style='color: #ff0000; margin: 0 15px; text-decoration: none;'>📄 Conditions</a> | 
        <a href="#" style='color: #ff0000; margin: 0 15px; text-decoration: none;'>🔒 Confidentialité</a> | 
        <a href="#" style='color: #ff0000; margin: 0 15px; text-decoration: none;'>📞 Contact</a> | 
        <a href="#" style='color: #ff0000; margin: 0 15px; text-decoration: none;'>💼 À propos</a>
    </div>
    <p style='margin-top: 15px; font-size: 0.8em; color: #888;'>Version 2.0.0 | Dernière mise à jour: 2024</p>
</div>
""", unsafe_allow_html=True)

# Sidebar supplémentaire
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔧 Outils")
    
    if st.button("🔄 Actualiser l'application", key="refresh_app"):
        st.rerun()
    
    # Export de données
    export_html = exporter_donnees()
    st.markdown(export_html, unsafe_allow_html=True)
    
    # Import de données
    st.markdown("---")
    st.markdown("### 📤 Import de données")
    uploaded_file = st.file_uploader("Choisir un fichier JSON", type=['json'], key="data_import")
    if uploaded_file:
        try:
            data = json.load(uploaded_file)
            st.session_state.user_data.update(data)
            st.success("✅ Données importées avec succès !")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Erreur lors de l'importation: {str(e)}")
    
    st.markdown("---")
    st.markdown("### 📊 Statistiques rapides")
    
    if st.session_state.user_data['poids']:
        poids_actuel = st.session_state.user_data['poids'][-1]['poids']
        st.metric("📈 Poids actuel", f"{poids_actuel} kg")
    
    if st.session_state.user_data.get('objectifs'):
        st.metric("🎯 Objectifs actifs", len(st.session_state.user_data['objectifs']))
    
    if st.session_state.user_data.get('entrainements'):
        total_series = sum(len(sessions) for sessions in st.session_state.user_data['entrainements'].values())
        st.metric("💪 Séries réalisées", total_series)
    
    st.markdown("---")
    st.markdown("### ⚙️ Paramètres")
    
    theme = st.selectbox("🎨 Thème", ["Sombre", "Clair"], index=0, key="theme_select")
    notifications = st.checkbox("🔔 Notifications", value=True, key="notifications")
    auto_save = st.checkbox("💾 Sauvegarde auto", value=True, key="auto_save")
    
    if st.button("💾 Sauvegarder paramètres", key="save_settings"):
        st.success("✅ Paramètres sauvegardés !")
    
    # Bouton de réinitialisation
    st.markdown("---")
    if st.button("🗑️ Réinitialiser données", key="reset_data"):
        st.session_state.user_data = {
            'age': 25,
            'taille': 180,
            'poids': [{'date': '2024-01-01', 'poids': 80}],
            'exercice_prefere': 'Développé couché',
            'email': 'user@example.com',
            'objectifs': [],
            'seances': {},
            'entrainements': {},
            'notes': '',
            'mensurations': {},
            'photos': [],
            'pr_bench': 80,
            'pr_squat': 100,
            'pr_deadlift': 120
        }
        st.success("✅ Données réinitialisées !")
        time.sleep(1)
        st.rerun()
