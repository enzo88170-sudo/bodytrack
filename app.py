import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
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
    # Logo placeholder - remplacez par votre logo
    return "🏋️‍♂️"

# Navigation avec onglets
logo = load_logo()
st.sidebar.markdown(f"# {logo} FitMaster Pro")

menu = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Accueil", "👤 Profil", "🎯 Objectifs", "📅 Calendrier", "💪 Entraînement", 
     "⏱️ Repos", "🧮 Calculateurs", "📝 Notes", "📊 Programmes", "🤖 IA Coach",
     "🍎 Nutrition", "🔓 Accès Premium"]
)

# Fonctionnalité d'accès premium
def check_premium_access():
    if 'premium_unlocked' not in st.session_state:
        st.session_state.premium_unlocked = False
    
    if st.session_state.premium_unlocked:
        return True
    
    # Code administrateur
    admin_code = st.sidebar.text_input("Code administrateur", type="password")
    if admin_code == "F12Berlinetta88170":
        st.session_state.premium_unlocked = True
        st.sidebar.success("Accès premium activé !")
        return True
    
    # Paiement
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("💰 Premium - 20€"):
            st.info("Fonctionnalité de paiement à implémenter")
    with col2:
        if st.button("🆓 Démo"):
            return False
    
    return False

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
        3. Cliquez sur 📤
        4. Sélectionnez "Sur l'écran d'accueil"
        5. Ajoutez et validez
        """)
    
    with tab_chrome:
        st.markdown("""
        **Installation sur Chrome Desktop :**
        1. Cliquez sur ⋮
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
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400
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
        taille = st.number_input("Taille (cm)", min_value=30, max_value=150, value=85)
    with col4:
        poitrine = st.number_input("Poitrine (cm)", min_value=50, max_value=200, value=100)
    
    if st.button("Enregistrer les mensurations"):
        st.session_state.user_data['mensurations'] = {
            'bras': bras,
            'cuisses': cuisses,
            'taille': taille,
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
        
        if st.button("Définir l'objectif"):
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
    
    for idx, obj in enumerate(st.session_state.user_data['objectifs']):
        col1, col2, col3 = st.columns([2, 3, 1])
        
        with col1:
            st.markdown(f"**{obj['type']}**")
            st.caption(f"{obj['exercice']} - {obj['valeur']} kg")
        
        with col2:
            progress = min(obj['progress'], 100)
            st.progress(progress / 100)
            st.caption(f"{progress}% - Objectif: {obj['date']}")
        
        with col3:
            if st.button("✏️", key=f"edit_{idx}"):
                st.session_state.editing_goal = idx
            if st.button("🗑️", key=f"del_{idx}"):
                st.session_state.user_data['objectifs'].pop(idx)
                st.rerun()
    
    # Objectifs multiples
    st.subheader("🎯 Objectifs multiples")
    
    tab_poids, tab_mens, tab_perf = st.tabs(["Poids", "Mensurations", "Performance"])
    
    with tab_poids:
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Objectif poids (kg)", min_value=30, max_value=200, value=75)
        with col2:
            st.date_input("Date objectif poids")
    
    with tab_mens:
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Objectif tour de bras (cm)", value=40)
        with col2:
            st.number_input("Objectif tour de taille (cm)", value=80)

# Onglet Calendrier
elif menu == "📅 Calendrier":
    st.title("📅 Calendrier des séances")
    
    # Calendrier
    today = datetime.now().date()
    st.subheader(f"Aujourd'hui: {today.strftime('%d/%m/%Y')}")
    
    # Sélection de date
    selected_date = st.date_input("Sélectionnez une date", today)
    
    # Entrée de séance
    with st.form("session_form"):
        st.markdown(f"### Séance du {selected_date.strftime('%d/%m/%Y')}")
        
        duree = st.slider("Durée (minutes)", 15, 180, 60)
        programme = st.text_area("Programme de la séance", 
                               placeholder="Décrivez votre séance...")
        
        exercices = st.multiselect(
            "Exercices réalisés",
            ["Développé couché", "Développé incliné", "Squat", "Soulevé de terre", 
             "Rowing", "Développé militaire", "Curl", "Élévation latérale"],
            default=["Développé couché", "Squat"]
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
    import calendar
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
            default=["Développé couché", "Squat"]
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
                    line=dict(color=colors[idx % len(colors)], width=3)
                ))
            
            fig.update_layout(
                title="Évolution des charges",
                xaxis_title="Séances",
                yaxis_title="Poids (kg)",
                template='plotly_dark',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        # Carnet de séance en temps réel
        st.subheader("📝 Carnet de séance")
        
        exercice = st.selectbox("Exercice", list(exercices.keys()))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            series = st.number_input("Série", min_value=1, max_value=10, value=3)
        with col2:
            reps = st.number_input("Répétitions", min_value=1, max_value=50, value=10)
        with col3:
            poids = st.number_input("Poids (kg)", min_value=0, max_value=500, value=80)
        
        notes = st.text_area("Notes (sensations, forme, douleurs)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Ajouter la série"):
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
            if st.button("⏱️ Timer entre séries"):
                st.session_state.timer_active = True
    
    with tabs[2]:
        # Description technique des exercices
        st.subheader("🎥 Guide technique des exercices")
        
        exercice_detail = st.selectbox(
            "Sélectionnez un exercice",
            ["Développé couché", "Développé incliné", "Squat", "Soulevé de terre", 
             "Romanian Deadlift", "Rowing", "Développé militaire", "Élévation latérale", "Curl"]
        )
        
        if exercice_detail == "Développé couché":
            st.markdown("""
            ### Technique du Développé Couché
            
            **Position de départ :**
            - Allongé sur le banc, pieds au sol
            - Dos en légère cambrure naturelle
            - Omoplates rétractées
            
            **Prise :**
            - Largeur d'épaules + 10-15cm
            - Pouces autour de la barre
            - Poignets alignés
            
            **Exécution :**
            1. Descendre la barre au milieu de la poitrine
            2. Toucher légèrement le torse
            3. Pousser en ligne droite vers le haut
            4. Bloquer les coudes en haut
            
            **Angle des mains :** 45° par rapport au torse
            **Respiration :** Inspirer à la descente, expirer à la montée
            """)
        
        # Ajouter d'autres exercices ici...
    
    with tabs[3]:
        # Historique détaillé
        st.subheader("📋 Historique des entraînements")
        
        if 'entrainements' in st.session_state.user_data:
            for exo, sessions in st.session_state.user_data['entrainements'].items():
                with st.expander(f"{exo} ({len(sessions)} sessions)"):
                    for session in sessions[-5:]:  # 5 dernières sessions
                        st.write(f"**{session['date']}** - {session['series']}x{session['reps']} @ {session['poids']}kg")
                        if session['notes']:
                            st.caption(f"Notes: {session['notes']}")

# Onglet Repos
elif menu == "⏱️ Repos":
    st.title("⏱️ Gestion des temps de repos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Timer de repos
        st.subheader("⏱️ Timer de repos")
        
        minutes = st.number_input("Minutes", min_value=0, max_value=10, value=1)
        seconds = st.number_input("Secondes", min_value=0, max_value=59, value=30)
        
        total_seconds = minutes * 60 + seconds
        
        if 'timer_start' not in st.session_state:
            st.session_state.timer_start = None
            st.session_state.timer_running = False
        
        if st.button("▶️ Démarrer le timer") and total_seconds > 0:
            st.session_state.timer_start = time.time()
            st.session_state.timer_duration = total_seconds
            st.session_state.timer_running = True
        
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
                
                # Actualiser automatiquement
                time.sleep(0.1)
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
        <div style='border: 2px solid red; padding: 10px; border-radius: 10px; text-align: center;'>
            <h3>💪 Flappy Biceps</h3>
            <p>Espace pour faire un curl !</p>
            <div style='height: 200px; background: linear-gradient(180deg, #000033 0%, #000066 100%); 
                        border-radius: 5px; position: relative;'>
                <div style='position: absolute; top: 50%; left: 50px; width: 40px; height: 40px; 
                            background: url(https://img.icons8.com/color/96/muscle.png) center/contain no-repeat;'>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Démarrer le jeu"):
            st.info("Jeu en développement - Version complète bientôt disponible")

# Onglet Calculateurs
elif menu == "🧮 Calculateurs":
    st.title("🧮 Calculateurs")
    
    tabs = st.tabs(["🔥 Calories dépensées", "🍽️ Calories consommées", "🏋️‍♂️ 1RM", "📊 Macros"])
    
    with tabs[0]:
        st.subheader("🔥 Calculateur de calories dépensées")
        
        activite = st.selectbox(
            "Activité sportive",
            ["Musculation", "Course à pied", "Natation", "Cyclisme", "Basketball", 
             "Football", "Yoga", "HIIT", "CrossFit"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            duree = st.number_input("Durée (minutes)", min_value=1, max_value=300, value=60)
        with col2:
            intensite = st.select_slider("Intensité", ["Légère", "Modérée", "Intense"])
        
        poids_user = st.session_state.user_data['poids'][-1]['poids'] if st.session_state.user_data['poids'] else 70
        
        if st.button("Calculer"):
            # Facteurs MET approximatifs
            met_values = {
                "Musculation": {"Légère": 3.5, "Modérée": 5.0, "Intense": 6.0},
                "Course à pied": {"Légère": 8.0, "Modérée": 10.0, "Intense": 12.5},
                "Natation": {"Légère": 5.8, "Modérée": 8.0, "Intense": 10.0},
                "Basketball": {"Légère": 6.0, "Modérée": 8.0, "Intense": 10.0}
            }
            
            met = met_values.get(activite, {"Modérée": 5.0})[intensite]
            calories = met * poids_user * (duree / 60)
            
            st.success(f"**Calories dépensées : {calories:.0f} kcal**")
    
    with tabs[1]:
        st.subheader("🍽️ Calculateur de repas")
        
        repas = st.text_area("Description du repas", 
                           placeholder="Ex: 200g de poulet, 100g de riz, légumes...")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            proteines = st.number_input("Protéines (g)", min_value=0.0, value=30.0)
        with col2:
            glucides = st.number_input("Glucides (g)", min_value=0.0, value=40.0)
        with col3:
            lipides = st.number_input("Lipides (g)", min_value=0.0, value=20.0)
        with col4:
            kcal = st.number_input("Calories (kcal)", min_value=0.0, value=350.0)
        
        if st.button("Ajouter au journal"):
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
    
    with tabs[2]:
        st.subheader("🏋️‍♂️ Calculateur de 1RM (Rep Max)")
        
        exercice_1rm = st.selectbox(
            "Exercice",
            ["Développé couché", "Squat", "Soulevé de terre", "Développé militaire"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            poids = st.number_input("Poids soulevé (kg)", min_value=1.0, value=80.0)
        with col2:
            reps = st.number_input("Nombre de répétitions", min_value=1, max_value=12, value=5)
        
        # Formule de Brzycki
        if st.button("Calculer 1RM"):
            if reps == 1:
                rm1 = poids
            else:
                rm1 = poids / (1.0278 - 0.0278 * reps)
            
            st.metric("1RM estimé", f"{rm1:.1f} kg")
            
            # Suggestions d'entraînement
            st.info(f"""
            **Suggestions d'entraînement :**
            - 85% de 1RM : {rm1*0.85:.1f} kg (3-5 reps)
            - 75% de 1RM : {rm1*0.75:.1f} kg (8-10 reps)
            - 65% de 1RM : {rm1*0.65:.1f} kg (12-15 reps)
            """)

# Onglet Notes
elif menu == "📝 Notes":
    st.title("📝 Journal d'entraînement")
    
    tab_notes, tab_stats = st.tabs(["📝 Notes manuscrites", "📊 Statistiques"])
    
    with tab_notes:
        notes = st.text_area(
            "Vos notes d'entraînement",
            height=300,
            placeholder="Notez vos sensations, vos performances, vos douleurs, vos observations..."
        )
        
        if st.button("💾 Sauvegarder les notes"):
            st.session_state.user_data['notes'] = notes
            st.success("Notes sauvegardées !")
        
        if st.session_state.user_data.get('notes'):
            st.markdown("---")
            st.subheader("📄 Notes précédentes")
            st.write(st.session_state.user_data['notes'])
    
    with tab_stats:
        st.subheader("📊 Statistiques personnelles")
        
        if 'entrainements' in st.session_state.user_data:
            total_seances = sum(len(sessions) for sessions in st.session_state.user_data['entrainements'].values())
            st.metric("Séances totales", total_seances)
            
            # Graphique d'activité
            fig = go.Figure(data=[go.Bar(
                x=list(st.session_state.user_data['entrainements'].keys()),
                y=[len(sessions) for sessions in st.session_state.user_data['entrainements'].values()],
                marker_color='red'
            )])
            
            fig.update_layout(
                title="Séances par exercice",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Onglet Programmes
elif menu == "📊 Programmes":
    st.title("📊 Programmes d'entraînement")
    
    tabs = st.tabs(["🏁 Débutant", "💪 PPL 6 jours", "🔥 Amélioration PR", "🏠 Cardio Maison", "✏️ Personnalisé"])
    
    with tabs[0]:
        st.subheader("🏁 Programme Débutant - 5 jours")
        
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        
        for jour in jours:
            with st.expander(f"{jour}"):
                if jour == "Lundi":
                    st.markdown("""
                    **Pectoraux/Triceps**
                    - Développé couché: 3x8-12
                    - Développé incliné haltères: 3x10-12
                    - Écarté couché: 3x12-15
                    - Extension triceps: 3x10-12
                    - Dips: 3xMax
                    """)
                elif jour == "Mardi":
                    st.markdown("""
                    **Dos/Biceps**
                    - Tractions: 3xMax
                    - Rowing barre: 3x8-12
                    - Tirage vertical: 3x10-12
                    - Curl barre: 3x10-12
                    - Curl marteau: 3x12-15
                    """)
                # Ajouter les autres jours...
    
    with tabs[1]:
        st.subheader("💪 Programme PPL - 6 jours")
        
        st.markdown("""
        **Push (Lundi/Jeudi):**
        - Développé couché: 4x5-8
        - Développé militaire: 3x8-12
        - Développé incliné: 3x10-12
        - Élévations latérales: 4x12-15
        - Extension triceps: 3x10-15
        
        **Pull (Mardi/Vendredi):**
        - Soulevé de terre: 3x5
        - Tractions: 4xMax
        - Rowing barre: 3x8-12
        - Curl barre: 3x10-12
        - Face pull: 3x15-20
        
        **Legs (Mercredi/Samedi):**
        - Squat: 4x5-8
        - Presse à cuisses: 3x10-12
        - Leg curl: 3x12-15
        - Mollets: 4x15-20
        - Abdominaux: 3xMax
        """)
    
    with tabs[2]:
        st.subheader("🔥 Programme Amélioration PR au Bench")
        
        pr_objectif = st.number_input("PR objectif (kg)", min_value=50, max_value=300, value=100)
        
        st.markdown(f"""
        **Basé sur votre objectif de {pr_objectif}kg:**
        
        **Lundi:**
        - 4 série de 5 répétitions à {pr_objectif*0.75:.1f}kg (75%)
        - Bench haltère: 3 série de 6-10 répétitions
        - Triceps (au choix): 3 série de 10-12 répétitions
        
        **Mercredi:**
        - 3 série de 7 répétitions à {pr_objectif*0.65:.1f}kg (65%) - tempo 2s
        - Développé militaire: 3 série de 6-10 répétitions
        - Triceps: 3 série de 8-10 répétitions
        - Biceps: 3 série de 10-12 répétitions
        
        **Samedi:**
        - Single à {pr_objectif*0.8:.1f}kg (80%)
        - 3 série de 3 répétitions à {pr_objectif*0.75:.1f}kg (75%)
        
        **Progression:** +3% par semaine si réussi
        """)
        
        if st.button("Générer le programme personnalisé"):
            st.success(f"Programme généré pour objectif {pr_objectif}kg !")

# Onglet IA Coach
elif menu == "🤖 IA Coach":
    st.title("🤖 Coach IA Personnel")
    
    if not check_premium_access():
        st.warning("⚠️ Cette fonctionnalité nécessite l'accès premium")
        st.info("Débloquez toutes les fonctionnalités avec le code administrateur ou l'achat premium")
        return
    
    st.subheader("🎯 Analyse de vos habitudes")
    
    # Analyse des données utilisateur
    if st.session_state.user_data['poids']:
        dernier_poids = st.session_state.user_data['poids'][-1]['poids']
        premier_poids = st.session_state.user_data['poids'][0]['poids']
        evolution = dernier_poids - premier_poids
        
        st.markdown(f"""
        **📊 Analyse actuelle:**
        - Poids: {dernier_poids}kg ({evolution:+.1f}kg depuis le début)
        - Exercice préféré: {st.session_state.user_data['exercice_prefere']}
        - Objectifs en cours: {len(st.session_state.user_data['objectifs'])}
        """)
    
    # Conseils personnalisés
    st.subheader("💡 Conseils personnalisés")
    
    conseil_type = st.selectbox(
        "Type de conseil",
        ["Nutrition", "Entraînement", "Récupération", "Progression"]
    )
    
    if st.button("🔄 Obtenir des conseils"):
        with st.spinner("L'IA analyse vos données..."):
            time.sleep(2)
            
            if conseil_type == "Nutrition":
                st.success("""
                **🍎 Conseil Nutrition:**
                - Augmentez votre apport en protéines à 2g/kg pour optimiser la récupération
                - Consommez 500g de légumes par jour pour les micronutriments
                - Hydratation: 40ml/kg d'eau quotidiennement
                """)
            elif conseil_type == "Entraînement":
                st.success("""
                **💪 Conseil Entraînement:**
                - Variez vos angles de travail pour les pectoraux
                - Ajoutez 1 série dégressives à votre dernier exercice
                - Travaillez la mobilité scapulaire avant vos séances de développé
                """)

# Onglet Nutrition
elif menu == "🍎 Nutrition":
    st.title("🍎 Nutrition & Recettes")
    
    if not check_premium_access():
        st.warning("⚠️ Cette fonctionnalité nécessite l'accès premium")
        return
    
    tabs = st.tabs(["👨‍🍳 Chef IA", "📅 Tracker quotidien", "🛒 Liste de courses", "📊 Analyse macros"])
    
    with tabs[0]:
        st.subheader("👨‍🍳 Chef IA - Recettes personnalisées")
        
        col1, col2 = st.columns(2)
        with col1:
            calories = st.slider("Calories par repas", 300, 1000, 600)
            proteines = st.slider("Protéines (g)", 20, 80, 40)
        
        with col2:
            preferences = st.multiselect(
                "Préférences/Restrictions",
                ["Végétarien", "Sans gluten", "Sans lactose", "Paleo", "Keto"]
            )
            type_repas = st.selectbox("Type de repas", ["Petit-déjeuner", "Déjeuner", "Dîner", "Collation"])
        
        if st.button("🍳 Générer une recette"):
            with st.spinner("Le chef IA prépare votre recette..."):
                time.sleep(2)
                
                st.success(f"""
                **🍗 Recette pour {type_repas} ({calories}kcal, {proteines}g protéines)**
                
                **Poulet aux légumes rôtis:**
                - 200g de blanc de poulet
                - 150g de brocolis
                - 100g de patates douces
                - 30g d'amandes
                - Huile d'olive, épices
                
                **Préparation:**
                1. Préchauffer le four à 200°C
                2. Couper les légumes et le poulet
                3. Assaisonner et arroser d'huile d'olive
                4. Cuire 25-30 minutes
                5. Parsemer d'amandes concassées
                
                **Macros:** {proteines}g P / 45g G / 20g L
                """)
    
    with tabs[1]:
        st.subheader("📅 Tracker nutritionnel quotidien")
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kcal_jour = st.number_input("Calories aujourd'hui", value=1800)
        with col2:
            prots_jour = st.number_input("Protéines (g)", value=120)
        with col3:
            gluc_jour = st.number_input("Glucides (g)", value=200)
        with col4:
            lip_jour = st.number_input("Lipides (g)", value=60)
        
        # Graphique de la semaine
        jours = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
        calories_semaine = [1800, 1900, 1750, 1850, 1950, 1700, 1600]
        
        fig = go.Figure(data=[
            go.Bar(name='Calories', x=jours, y=calories_semaine, marker_color='red')
        ])
        
        fig.update_layout(
            title="Calories sur 7 jours",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        st.subheader("🛒 Liste de courses automatique")
        
        if st.button("🔄 Générer la liste de courses"):
            st.markdown("""
            **📝 Liste de courses hebdomadaire:**
            
            **Protéines:**
            - Poulet: 1kg
            - Œufs: 12
            - Thon: 4 boîtes
            - Yaourt grec: 1kg
            
            **Légumes:**
            - Brocolis: 1kg
            - Épinards: 500g
            - Patates douces: 2kg
            - Carottes: 1kg
            
            **Fruits:**
            - Bananes: 8
            - Pommes: 6
            - Baies surgelées: 500g
            
            **Autres:**
            - Riz basmati: 2kg
            - Flocons d'avoine: 1kg
            - Amandes: 500g
            """)

# Onglet Accès Premium
elif menu == "🔓 Accès Premium":
    st.title("🔓 Accès Premium")
    
    if check_premium_access():
        st.success("✅ Vous avez déjà accès à toutes les fonctionnalités premium !")
        
        st.markdown("""
        ### 🎉 Fonctionnalités Premium débloquées:
        
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
        """)
    else:
        st.warning("🔒 Fonctionnalités premium verrouillées")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 🚀 Passez à la version premium
            
            **Ce que vous obtenez:**
            - Coach IA personnel 24/7
            - Chef IA nutrition avec recettes illimitées
            - Programmes d'entraînement sur mesure
            - Analytics avancés
            - Support prioritaire
            - Mises à jour gratuites
            
            **Prix: 20€ - Paiement unique**
            """)
            
            if st.button("💳 Acheter maintenant - 20€"):
                st.info("Intégration de paiement à venir (Stripe, PayPal)")
        
        with col2:
            st.markdown("""
            ### 🔑 Code administrateur
            
            Entrez le code pour débloquer gratuitement:
            """)
            
            code_input = st.text_input("Code", type="password")
            
            if st.button("Déverrouiller avec code"):
                if code_input == "F12Berlinetta88170":
                    st.session_state.premium_unlocked = True
                    st.success("✅ Accès premium activé !")
                    st.rerun()
                else:
                    st.error("❌ Code incorrect")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>FitMaster Pro © 2024 - Application d'entraînement personnel</p>
    <p>Pour toute question: support@fitmaster.com</p>
</div>
""", unsafe_allow_html=True)

# Fonctions supplémentaires
def exporter_donnees():
    """Exporter les données utilisateur"""
    data_str = json.dumps(st.session_state.user_data, indent=2)
    b64 = base64.b64encode(data_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="fitmaster_data.json">📥 Exporter mes données</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

def importer_donnees():
    """Importer des données"""
    uploaded_file = st.sidebar.file_uploader("Importer données", type=['json'])
    if uploaded_file:
        data = json.load(uploaded_file)
        st.session_state.user_data.update(data)
        st.sidebar.success("Données importées !")

# Sidebar supplémentaire
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔧 Outils")
    
    if st.button("🔄 Actualiser les données"):
        st.rerun()
    
    exporter_donnees()
    
    st.markdown("---")
    st.markdown("### 📊 Statistiques rapides")
    
    if st.session_state.user_data['poids']:
        poids_actuel = st.session_state.user_data['poids'][-1]['poids']
        st.metric("Poids actuel", f"{poids_actuel} kg")
    
    if st.session_state.user_data.get('objectifs'):
        st.metric("Objectifs actifs", len(st.session_state.user_data['objectifs']))
