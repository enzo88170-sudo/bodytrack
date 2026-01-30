import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="BodyTrack Pro - Ebook Interactif", layout="wide")

# --- DESIGN CSS PERSONNALISÉ (NOIR & ROUGE) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111111; border-right: 2px solid #e60000; }
    h1, h2, h3 { color: #e60000 !important; font-family: 'Arial Black'; }
    .stButton>button { background: linear-gradient(90deg, #e60000, #8b0000); color: white; border: none; width: 100%; border-radius: 5px; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: white; border: 1px solid #e60000; }
    .metric-card { background-color: #1a1a1a; padding: 15px; border-radius: 10px; border-left: 5px solid #e60000; }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTÈME D'ACCÈS (CODE ADMIN CACHÉ) ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

def check_auth():
    st.sidebar.image("https://i.imgur.com/wlyusJ0.png", use_container_width=True)
    st.title("🔴 ACCÈS PREMIUM")
    st.write("Pour débloquer l'intégralité de l'ebook interactif (20€), veuillez procéder au paiement ou entrer un code.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Payer 20€ via Stripe"):
            st.session_state['auth'] = True
            st.rerun()
    with col2:
        code = st.text_input("Code Administrateur", type="password")
        # Le code caché demandé
        if code == "F12Berlinetta88170":
            st.session_state['auth'] = True
            st.rerun()

if not st.session_state['auth']:
    check_auth()
    st.stop()

# --- NAVIGATION ---
st.sidebar.title("MENU")
page = st.sidebar.radio("Navigation", [
    "👤 Profil & Mensurations", 
    "🎯 Objectifs & Jauge",
    "📈 Entraînement & Stats", 
    "📅 Calendrier & Séances",
    "💪 Programmes Spécialisés",
    "⏱️ Repos & Jeu",
    "🥗 Nutrition & IA Chef",
    "🤖 IA Coach",
    "🧮 Calculateurs & Notes",
    "📚 Contenu Éducatif"
])

# --- 1. PROFIL & MENSURATIONS ---
if page == "👤 Profil & Mensurations":
    st.header("👤 Mon Profil Sportif")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Adresse Mail")
        st.number_input("Âge", 14, 99)
        st.number_input("Taille (cm)", 100, 250)
        st.text_input("Exercice Préféré")
    with col2:
        st.subheader("Suivi de Poids")
        new_weight = st.number_input("Poids actuel (kg)", 30.0, 200.0)
        if st.button("Enregistrer le poids"):
            st.success("Poids enregistré !")
            
    st.markdown("---")
    st.subheader("📏 Mensurations (Bras, Cuisses, Taille)")
    st.image("https://via.placeholder.com/600x200/1a1a1a/e60000?text=Graphique+Evolution+Mensurations")

# --- 2. OBJECTIFS & JAUGE ---
elif page == "🎯 Objectifs & Jauge":
    st.header("🎯 Mes Objectifs")
    obj_name = st.text_input("Nom de l'objectif (ex: Bench 100kg)")
    val_actuelle = st.number_input("Valeur actuelle", 1)
    val_cible = st.number_input("Valeur cible", 1)
    
    progression = (val_actuelle / val_cible) * 100
    st.write(f"### Progression : {round(progression, 1)}%")
    st.progress(progression / 100)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = progression,
        title = {'text': "Objectif %"},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#e60000"}}
    ))
    st.plotly_chart(fig)

# --- 3. ENTRAÎNEMENT & STATS ---
elif page == "📈 Entraînement & Stats":
    st.header("📈 Suivi des Exercices")
    exo_liste = ["Développé couché", "Squat", "Soulevé de terre", "Rowing", "Développé militaire"]
    choix_exo = st.selectbox("Sélectionner l'exercice pour voir la courbe", exo_liste)
    
    # Simulation de graphique multi-courbes
    df_perf = pd.DataFrame({
        'Date': ['Semaine 1', 'Semaine 2', 'Semaine 3', 'Semaine 4'],
        choix_exo: [60, 62, 65, 67]
    })
    fig_perf = px.scatter(df_perf, x='Date', y=choix_exo, title=f"Evolution sur {choix_exo}", color_discrete_sequence=['#e60000'])
    fig_perf.update_traces(mode='lines+markers')
    st.plotly_chart(fig_perf)

    st.markdown("### 📖 Guide Technique")
    if choix_exo == "Développé couché":
        st.write("**Position :** Allongé, omoplates serrées. **Angle :** Coudes à 45°. **Mains :** Largeur moyenne.")

# --- 4. REPOS & JEU ---
elif page == "⏱️ Repos & Jeu":
    st.header("⏱️ Temps de Repos")
    t_repos = st.number_input("Régler le repos (secondes)", value=90)
    if st.button("Lancer le Chrono"):
        msg = st.empty()
        for i in range(t_repos, 0, -1):
            msg.metric("Repos restant", f"{i}s")
            time.sleep(1)
        st.error("🚀 TEMPS DE REPOS TERMINÉ, RETOUR AU CHARBON !")
        st.balloons()
    
    st.markdown("---")
    st.subheader("🎮 Mini-Jeu : Flappy Biceps")
    st.markdown("""
    <div style="background: black; height: 300px; border: 2px solid #e60000; display: flex; align-items: center; justify-content: center;">
        <p style="color: white;">[ ESPACE SPATIAL : Le Biceps doit éviter les planètes ]<br>Faites sauter le biceps avec 'Espace' (Simulation)</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. PROGRAMMES SPÉCIALISÉS ---
elif page == "💪 Programmes Spécialisés":
    st.header("💪 Mes Programmes")
    type_prog = st.selectbox("Choisir un programme", ["PR Bench 3j", "PPL 6 jours", "Débutant 5 jours", "Cardio Maison"])
    
    if type_prog == "PR Bench 3j":
        obj_pr = st.number_input("Objectif PR (kg)", value=100)
        st.markdown(f"""
        **Lundi :** 4x5 à {obj_pr * 0.75}kg (75%) + Bench Haltères + Triceps
        **Mercredi :** 3x7 à {obj_pr * 0.65}kg (Pause 2s) + Militaire + Triceps/Biceps
        **Samedi :** Single à {obj_pr * 0.80}kg + 3x3 à {obj_pr * 0.75}kg
        *Note : Augmentez de +3% par semaine si réussi.*
        """)

# --- 6. NUTRITION & IA ---
elif page == "🥗 Nutrition & IA Chef":
    st.header("🥗 Nutrition Avancée")
    st.subheader("👨‍🍳 Cuisinier IA")
    envie = st.text_input("De quoi as-tu envie ? (ex: Poulet, rapide, riche en prot)")
    if st.button("Générer Recette"):
        st.info("Recette IA : Poulet grillé au paprika, quinoa et avocat. (650 kcal, 45g Prot)")
    
    st.markdown("---")
    st.write("### Menu 2300 kcal (Exemple)")
    st.write("1. Matin : 3 oeufs, 80g avoine, 1 fruit. (600 kcal)")
    st.write("2. Midi : 150g Poulet, 100g Riz, Légumes, Huile olive. (850 kcal)")
    st.write("3. Soir : 150g Colin, 200g Patate douce, Salade. (850 kcal)")

# --- PIED DE PAGE & INSTALLATION ---
st.sidebar.markdown("---")
if st.sidebar.button("📲 Télécharger l'Application"):
    st.sidebar.info("""
    **Installation :**
    - **Android (Chrome) :** Menu (3 points) > Ajouter à l'écran d'accueil.
    - **iOS (Safari) :** Partager (flèche) > Sur l'écran d'accueil.
    """)
