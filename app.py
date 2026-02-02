import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import streamlit.components.v1 as components

# --- CONFIGURATION ---
st.set_page_config(page_title="BODYTRACK PRO", page_icon="💪", layout="wide")

# --- FONCTION POUR INTÉGRER CANVA ---
def afficher_canva(lien_embed, hauteur=600):
    components.html(
        f"""
        <iframe loading="lazy" 
            style="width: 100%; height: {hauteur}px; border: none; border-radius: 10px;" 
            src="{lien_embed}" 
            allowfullscreen="allowfullscreen" 
            allow="fullscreen">
        </iframe>
        """,
        height=hauteur,
    )

# --- STYLE CSS NOIR ET ROUGE ---
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    h1, h2, h3 { color: #dc2626; font-family: 'Bebas Neue', cursive; }
    .stButton>button { background-color: #dc2626; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- ACCÈS ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
# (Ici tu gardes ton système de code admin F12Berlinetta88170...)

# --- NAVIGATION ---
with st.sidebar:
    menu = st.radio("SÉCTIONS", ["📊 Profil", "💪 Entraînement", "📋 Programmes", "🍽️ Nutrition", "⏱️ Repos & Jeu"])

# ==========================================
# SECTION 1 : ENTRAÎNEMENT (TECHNIQUE)
# ==========================================
if menu == "💪 Entraînement":
    st.header("💪 GUIDE TECHNIQUE VISUEL")
    st.write("Voici tes fiches techniques professionnelles :")
    
    # REMPLACE LE LIEN CI-DESSOUS
     lien_nutri = "https://www.canva.com/design/DAG_QbeW4SU/jqXSEY7jaMUEBLxttSGZRQ/view?embed"
    afficher_canva(lien_technique, hauteur=800)

# ==========================================
# SECTION 2 : PROGRAMMES
# ==========================================
elif menu == "📋 Programmes":
    st.header("📋 TES PROGRAMMES DÉTAILLÉS")
    
    choix_prog = st.selectbox("Choisir le programme", ["PPL 6 Jours", "Débutant 5 Jours", "Spécial Bench"])
    
    if choix_prog == "PPL 6 Jours":
        # REMPLACE LE LIEN CI-DESSOUS
        lien_ppl = "https://www.canva.com/design/DA.../view?embed"
        afficher_canva(lien_ppl, hauteur=900)
        
    elif choix_prog == "Débutant 5 Jours":
        # REMPLACE LE LIEN CI-DESSOUS
        lien_deb = "https://www.canva.com/design/DA.../view?embed"
        afficher_canva(lien_deb, hauteur=900)

# ==========================================
# SECTION 3 : NUTRITION
# ==========================================
elif menu == "🍽️ Nutrition":
    st.header("🍽️ NUTRITION & MENUS")
    
    # REMPLACE LE LIEN CI-DESSOUS
    lien_nutri = https://www.canva.com/design/DAG_QbeW4SU/jqXSEY7jaMUEBLxttSGZRQ/view
    afficher_canva(lien_nutri, hauteur=700)

# (Tu peux garder tes autres onglets Repos, Profil, etc. comme avant)

# --- ACCÈS SÉCURISÉ ---
if not st.session_state['auth']:
    st.markdown("<h1 style='text-align: center;'>🔴 ACCÈS BODYTRACK PREMIUM</h1>", unsafe_allow_html=True)
    st.image("https://i.imgur.com/wlyusJ0.png", width=250)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>OFFRE EBOOK - 20€</h3><p>Accès complet à tous les outils et programmes à vie.</p></div>', unsafe_allow_html=True)
        if st.button("PAYER 20€ ET ACCÉDER"):
            st.session_state['auth'] = True
            st.rerun()
    with col2:
        code_input = st.text_input("Code Administrateur", type="password")
        if st.button("VALIDER CODE"):
            if code_input == "F12Berlinetta88170":
                st.session_state['auth'] = True
                st.rerun()
            else: st.error("Code incorrect")
    st.stop()

# --- NAVIGATION ---
with st.sidebar:
    st.image("https://i.imgur.com/wlyusJ0.png", width=120)
    menu = st.radio("SÉCTIONS", [
        "📊 Profil", "🎯 Objectifs", "📅 Calendrier", "💪 Entraînement", 
        "📋 Programmes", "🍽️ Nutrition", "⏱️ Repos & Jeu", "🤖 Coach IA", "📱 Installation"
    ])

# ==========================================
# 1. PROFIL
# ==========================================
if menu == "📊 Profil":
    st.header("📊 MON PROFIL & MENSURATIONS")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.text_input("Adresse Mail")
        st.number_input("Âge", 15, 80, 25)
        st.number_input("Taille (cm)", 120, 230, 175)
        st.selectbox("Exercice préféré", ["Bench", "Squat", "Deadlift", "Curl"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Suivi du Poids")
        new_p = st.number_input("Entrer poids (kg)", 40.0, 150.0, 75.0)
        if st.button("Ajouter Pesée"):
            now = datetime.now().strftime("%d/%m")
            new_row = pd.DataFrame({'Date': [now], 'Poids': [new_p]})
            st.session_state['poids_data'] = pd.concat([st.session_state['poids_data'], new_row])
        st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state['poids_data'].empty:
        fig = px.line(st.session_state['poids_data'], x='Date', y='Poids', title="Évolution", markers=True)
        fig.update_traces(line_color='#dc2626')
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 2. OBJECTIFS
# ==========================================
elif menu == "🎯 Objectifs":
    st.header("🎯 MES OBJECTIFS DE PERFORMANCE")
    col1, col2 = st.columns(2)
    with col1:
        nom_obj = st.text_input("Nom de l'objectif (ex: DC 100kg)")
        actuel = st.number_input("Valeur actuelle", 0, 500, 60)
        cible = st.number_input("Valeur cible", 1, 500, 100)
        percent = (actuel / cible) if cible > 0 else 0
        st.metric("Progression", f"{round(percent*100)}%")
        st.progress(min(percent, 1.0))
    with col2:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=actuel, gauge={'axis': {'range': [None, cible]}, 'bar': {'color': "#dc2626"}}, title={'text': nom_obj}))
        st.plotly_chart(fig)

# ==========================================
# 3. ENTRAÎNEMENT (TECHNIQUE & GRAPHIQUES)
# ==========================================
elif menu == "💪 Entraînement":
    st.header("💪 TECHNIQUE & ANALYSE")
    tab_tech, tab_stats = st.tabs(["📚 Guide Technique", "📈 Courbes par Exercice"])
    
    with tab_tech:
        exos = {
            "Développé Couché": "Allongé, omoplates serrées, pieds au sol. Angle des coudes 45°.",
            "Squat": "Pieds largeur épaules, dos droit, descente sous la parallèle.",
            "Soulevé de Terre": "Tibias contre la barre, dos plat, poussée jambes.",
            "Rowing": "Buste incliné, tirage vers le nombril, coudes serrés.",
            "Romanian Deadlift": "Légère flexion genoux, bascule hanches vers l'arrière.",
            "Élévation latérale": "Coudes légèrement fléchis, monter jusqu'aux épaules.",
            "Développé Militaire": "Gainage fort, pousser barre au dessus de la tête."
        }
        choix = st.selectbox("Exercice", list(exos.keys()))
        st.markdown(f'<div class="card"><h3>{choix}</h3><p>{exos[choix]}</p></div>', unsafe_allow_html=True)
        

    with tab_stats:
        st.subheader("Suivi de force par exercice")
        # Exemple dynamique
        ex_stat = st.selectbox("Sélectionner exercice pour voir la courbe", ["Bench", "Squat", "Deadlift"])
        st.info("Ajoutez vos données dans l'onglet Profil pour voir les courbes ici.")

# ==========================================
# 4. PROGRAMMES (CONTENU DÉTAILLÉ)
# ==========================================
elif menu == "📋 Programmes":
    st.header("📋 MES PROGRAMMES PROFESSIONNELS")
    p_choix = st.selectbox("Choisir un programme", ["Débutant 5 jours", "PPL 6 jours", "PR Bench (3j/sem)", "Cardio Maison"])
    
    if p_choix == "PR Bench (3j/sem)":
        pr_obj = st.number_input("PR Cible (kg)", 40, 300, 100)
        st.write(f"### Planning basé sur {pr_obj}kg")
        st.write(f"**Lundi:** 4x5 à {pr_obj*0.75}kg + Bench Haltères 3x10 + Triceps")
        st.write(f"**Mercredi:** 3x7 à {pr_obj*0.65}kg (Pause 2s poitrine) + Militaire + Biceps")
        st.write(f"**Samedi:** Single à {pr_obj*0.80}kg + 3x3 à {pr_obj*0.75}kg")
        st.success("Augmentez de +3% par semaine si réussi.")

    elif p_choix == "PPL 6 jours":
        st.write("**Lundi/Jeudi (Push):** DC 4x8, Militaire 3x10, Triceps 3x12")
        st.write("**Mardi/Vendredi (Pull):** Rowing 4x8, Tractions 3xMAX, Biceps 3x12")
        st.write("**Mercredi/Samedi (Legs):** Squat 4x8, RDL 3x10, Leg Press 3x12")

# ==========================================
# 5. NUTRITION
# ==========================================
elif menu == "🍽️ Nutrition":
    st.header("🍽️ NUTRITION & CUISINIER IA")
    tab_ia, tab_menu = st.tabs(["👨‍🍳 Cuisinier IA", "📋 Menus 2300kcal"])
    
    with tab_ia:
        envie = st.text_input("J'ai envie de... (ex: Poulet, rapide, italien)")
        if st.button("Générer Recette"):
            st.success(f"Recette IA : Bowl Muscu au {envie} - 650kcal, 45g Prot.")
            
    with tab_menu:
        st.subheader("3 Menus à 2300kcal")
        st.markdown("""
        **Menu 1 (Classique):** Matin: 3 oeufs + Avoine | Midi: Poulet/Riz/Brocolis | Soir: Saumon/Patate douce
        **Menu 2 (Rapide):** Matin: Shaker + Beurre cacahuète | Midi: Pâtes complètes/Thon | Soir: Omelette/Avocat
        **Menu 3 (Force):** Matin: Pancakes Protéinés | Midi: Steak 5%/Riz | Soir: Fromage Blanc/Amandes
        """)

# ==========================================
# 6. REPOS & JEU
# ==========================================
elif menu == "⏱️ Repos & Jeu":
    st.header("⏱️ REPOS & DIVERTISSEMENT")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Chronomètre")
        t = st.number_input("Secondes", 30, 300, 90)
        if st.button("START"):
            ph = st.empty()
            for i in range(t, -1, -1):
                ph.write(f"## ⏳ {i}s")
                time.sleep(1)
            st.error("🚀 TEMPS DE REPOS TERMINÉ, RETOUR AU CHARBON !")
    with c2:
        st.subheader("🎮 FLAPPY BICEPS")
        st.components.v1.html("""
            <canvas id='c' width='300' height='200' style='border:1px solid red; background: black;'></canvas>
            <script>
            var ctx=document.getElementById('c').getContext('2d'), y=100, v=0;
            function d(){ v+=0.1; y+=v; ctx.clearRect(0,0,300,200); ctx.fillStyle='white'; ctx.fillText('💪', 50, y);
            if(y>200) y=100, v=0; requestAnimationFrame(d); }
            window.onclick=()=>v=-3; d();
            </script>
        """, height=250)

# ==========================================
# 7. COACH IA
# ==========================================
elif menu == "🤖 Coach IA":
    st.header("🤖 MON ASSISTANT IA")
    st.info("L'IA analyse vos pesées et vos charges pour vous conseiller.")
    st.write("- Analyse : Votre progression est stable.")
    st.write("- Conseil : Dormez 1h de plus pour optimiser la récupération du PR Bench.")

# ==========================================
# 8. INSTALLATION
# ==========================================
elif menu == "📱 Installation":
    st.header("📱 INSTALLER SUR SMARTPHONE")
    st.write("**Sur iPhone :** Safari -> Partager -> 'Sur l'écran d'accueil'")
    st.write("**Sur Android :** Chrome -> 3 points -> 'Installer l'application'")
