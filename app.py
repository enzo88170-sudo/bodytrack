import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# ==========================================
# 0. INITIALISATION (PERSISTANCE DES DONNÉES)
# ==========================================
# Gérer l'état de la session pour simuler une base de données simple
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
if 'historique_poids' not in st.session_state:
    st.session_state['historique_poids'] = {'Date': [], 'Poids': []}
if 'poids_actuel_user' not in st.session_state:
    st.session_state['poids_actuel_user'] = 75.0 # Valeur par défaut
if 'taille_user' not in st.session_state:
    st.session_state['taille_user'] = 175
if 'age_user' not in st.session_state:
    st.session_state['age_user'] = 25

# ==========================================
# 1. CONFIGURATION & DESIGN (CSS)
# ==========================================
st.set_page_config(
    page_title="Ebook Musculation Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto+Condensed:wght@300;400;700&display=swap');
    
    /* Fond global */
    .stApp { background-color: #0a0a0a; color: #ffffff; font-family: 'Roboto Condensed', sans-serif; }
    
    /* Titres style Musculation */
    h1, h2, h3, h4 { 
        font-family: 'Bebas Neue', cursive !important; 
        letter-spacing: 2px; 
        color: #dc2626; 
        text-transform: uppercase;
    }

    /* Cartes sombres style Canva */
    .card-dark {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        transition: transform 0.2s ease-in-out; /* Effet hover */
    }
    .card-dark:hover {
        transform: translateY(-5px); /* Légère élévation au survol */
        border-color: #dc2626;
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
        width: 100%; /* S'étend sur toute la largeur de sa colonne */
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(220, 38, 38, 0.6);
    }

    /* Input text et number */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 10px;
    }
    .stSelectbox>div>div>div { /* Selectbox style */
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #333;
        border-radius: 8px;
    }
    .stSelectbox>div>div>div>span {
        color: white; /* Couleur du texte sélectionné */
    }


    /* Cacher les éléments Streamlit par défaut */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LOGIQUE D'ACCÈS
# ==========================================
def login_screen():
    st.markdown("<h1 style='text-align: center; font-size: 4rem;'>MUSCULATION PRO</h1>", unsafe_allow_html=True)
    st.image("https://i.imgur.com/wlyusJ0.png", width=250, use_column_width=False, output_format="PNG") # Logo centré
    
    col1, col2 = st.columns([1.2, 1]) # Colonnes pour l'offre et l'admin
    
    with col1:
        st.markdown("""
        <div class="card-dark">
            <h2 style='color: white;'>ACCÈS COMPLET - 20€</h2>
            <p>✅ Programmes PPL (6j) & Débutant (5j) détaillés</p>
            <p>✅ IA Coach & Cuisinier Personnel (recettes sur mesure)</p>
            <p>✅ Suivi de Poids & Mensurations (graphiques)</p>
            <p>✅ Guide Technique des exercices avec vidéos</p>
            <p>✅ Accès à vie & Mises à jour incluses</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("DÉBLOQUER VIA STRIPE"):
            st.session_state['auth'] = True # Placeholder pour la connexion Stripe
            st.rerun()

    with col2:
        st.markdown("<div class='card-dark'>", unsafe_allow_html=True)
        st.subheader("CONNEXION ADMIN")
        code = st.text_input("Entrez votre code secret", type="password")
        if st.button("VÉRIFIER LE CODE"):
            if code == "F12Berlinetta88170": # Ton code secret
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Code invalide. Contactez le support.")
        st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state['auth']:
    login_screen()
    st.stop()

# ==========================================
# 3. APPLICATION PRINCIPALE (NAVIGATION PAR ONGLET)
# ==========================================
tabs = st.tabs(["📊 PROFIL", "🎯 OBJECTIFS", "💪 ENTRAÎNEMENT", "📋 PROGRAMMES", "🍽️ NUTRITION", "⏱️ REPOS", "🤖 IA COACH"])

# --- TAB 1 : PROFIL & SUIVI ---
with tabs[0]:
    st.markdown("<h2>📊 MON PROFIL & SUIVI D'ÉVOLUTION</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.subheader("Mes Informations Personnelles")
        
        # Date de la pesée
        today = datetime.now().date()
        date_pesee = st.date_input("Date de la pesée", value=today)
        
        # Champs modifiables, liés à session_state pour la persistance
        poids_input = st.number_input(
            "Poids actuel (kg)", 
            min_value=40.0, max_value=200.0, 
            value=float(st.session_state['poids_actuel_user']), 
            step=0.1, key="poids_profile_input"
        )
        taille_input = st.number_input(
            "Taille (cm)", 
            min_value=100, max_value=230, 
            value=st.session_state['taille_user'], 
            step=1, key="taille_profile_input"
        )
        age_input = st.number_input(
            "Âge", 
            min_value=15, max_value=80, 
            value=st.session_state['age_user'], 
            step=1, key="age_profile_input"
        )

        if st.button("ENREGISTRER MES INFOS & PESÉE"):
            st.session_state['poids_actuel_user'] = poids_input
            st.session_state['taille_user'] = taille_input
            st.session_state['age_user'] = age_input
            
            # Ajouter à l'historique de poids
            st.session_state['historique_poids']['Date'].append(str(date_pesee))
            st.session_state['historique_poids']['Poids'].append(poids_input)
            st.success("Données mises à jour et pesée enregistrée !")
            st.rerun() # Pour rafraîchir le graphique
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.subheader("Évolution du Poids")
        if st.session_state['historique_poids']['Poids']:
            df_poids = pd.DataFrame(st.session_state['historique_poids'])
            # S'assurer que les dates sont triées si elles sont ajoutées dans le désordre
            df_poids['Date'] = pd.to_datetime(df_poids['Date'])
            df_poids = df_poids.sort_values(by='Date').reset_index(drop=True)
            df_poids['Date'] = df_poids['Date'].dt.strftime('%d/%m/%Y') # Format d'affichage
            
            fig = px.line(df_poids, x='Date', y='Poids', title="COURBE DE POIDS", 
                          color_discrete_sequence=['#dc2626'], markers=True)
            fig.update_layout(xaxis_title="Date", yaxis_title="Poids (kg)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Enregistrez votre première pesée pour voir le graphique d'évolution.")

# --- TAB 2 : OBJECTIFS ---
with tabs[1]:
    st.markdown("<h2>🎯 MES OBJECTIFS</h2>", unsafe_allow_html=True)
    st.info("Fixez-vous des objectifs SMART (Spécifiques, Mesurables, Atteignables, Réalistes, Temporellement définis).")
    
    col_obj1, col_obj2 = st.columns(2)
    with col_obj1:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.subheader("Objectif de Force")
        obj_force = st.text_input("Ex: Atteindre 100kg au Développé Couché", "100kg au DC d'ici 3 mois")
        st.progress(75) # Exemple de progression
        st.write("Progression actuelle: 75%")
        st.button("Mettre à jour l'objectif force")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_obj2:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.subheader("Objectif Corporel")
        obj_corporel = st.text_input("Ex: Perdre 5kg de graisse d'ici 2 mois", "Perdre 5kg de graisse")
        st.progress(40) # Exemple de progression
        st.write("Progression actuelle: 40%")
        st.button("Mettre à jour l'objectif corporel")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 3 : ENTRAÎNEMENT (FICHES TECHNIQUES AVEC VIDÉOS) ---
with tabs[2]:
    st.markdown("<h2>💪 GUIDE TECHNIQUE DES EXERCICES</h2>", unsafe_allow_html=True)
    st.write("Apprenez la bonne exécution pour maximiser vos gains et éviter les blessures.")
    
    exo_selectionne = st.selectbox(
        "Sélectionner un exercice :", 
        ["Développé Couché", "Squat Barre", "Soulevé de Terre", "Rowing Barre", 
         "Développé Militaire", "Élévations Latérales", "Curl Biceps", "Extension Triceps à la Poulie"]
    )
    
    st.markdown('<div class="card-dark">', unsafe_allow_html=True)
    if exo_selectionne == "Développé Couché":
        st.markdown("<h3>🏋️ DÉVELOPPÉ COUCHÉ</h3>")
        st.video("https://www.youtube.com/watch?v=gG-u_XzT3OQ") # Vidéo de démonstration
        st.write("**Muscles ciblés :** Pectoraux (grand, petit), Triceps, Deltoïdes antérieurs.")
        st.write("**Placement :** Allongé sur le banc, pieds à plat au sol. Cambrure naturelle du bas du dos. Omoplates serrées et rétractées (poitrine sortie). Barre au niveau des yeux.")
        st.write("**Prise :** Ligerement plus large que les épaules, poignets cassés pour éviter la barre au cou.")
        st.write("**Exécution :** Descendre la barre de manière contrôlée jusqu'au milieu de la poitrine. Pousser explosivement en gardant les coudes à environ 45° du buste. Expirer à la poussée.")
    
    elif exo_selectionne == "Squat Barre":
        st.markdown("<h3>🦵 SQUAT BARRE (ROY DES EXERCICES)</h3>")
        st.video("https://www.youtube.com/watch?v=ULT9C93f0bQ")
        st.write("**Muscles ciblés :** Quadriceps, Fessiers, Ischio-jambiers, Lombaires, Abdos (gainage).")
        st.write("**Placement :** Barre sur les trapèzes (high bar) ou l'arrière des épaules (low bar). Pieds largeur d'épaules, pointes légèrement ouvertes (15-30°).")
        st.write("**Exécution :** Descendre en poussant les hanches vers l'arrière comme pour s'asseoir. Genoux dans l'axe des pieds. Descendre au moins jusqu'à ce que les hanches soient en dessous des genoux (parallèle). Pousser fort sur les talons pour remonter. Garder le dos droit et gainé tout le long.")
        
    elif exo_selectionne == "Soulevé de Terre":
        st.markdown("<h3>💥 SOULEVÉ DE TERRE (DEADLIFT)</h3>")
        st.video("https://www.youtube.com/watch?v=VL5B099Fv34")
        st.write("**Muscles ciblés :** Chaîne postérieure complète (Dos, Lombaires, Fessiers, Ischio-jambiers, Trapèzes).")
        st.write("**Placement :** Barre proche des tibias. Pieds sous la barre, mains juste à l'extérieur des genoux. Dos droit, poitrine sortie, épaules en arrière. Les hanches plus hautes que les genoux mais plus basses que les épaules.")
        st.write("**Exécution :** Commencer la poussée avec les jambes, puis redresser le buste. Garder la barre collée aux jambes. Verrouiller les hanches en haut (pas d'hyperextension du dos). Redescendre de manière contrôlée en inversant le mouvement.")

    elif exo_selectionne == "Rowing Barre":
        st.markdown("<h3>🛶 ROWING BARRE</h3>")
        st.video("https://www.youtube.com/watch?v=0kF_H1Nl1a0")
        st.write("**Muscles ciblés :** Grand dorsal, Trapèzes, Rhomboïdes, Biceps.")
        st.write("**Placement :** Buste penché à environ 45° (voire plus si confort). Dos droit et gainé. Genoux légèrement fléchis. Prise des mains un peu plus large que les épaules.")
        st.write("**Exécution :** Tirer la barre vers le nombril en ramenant les coudes vers l'arrière du corps. Se concentrer sur la contraction des omoplates. Contrôler la phase excentrique (descente de la barre).")

    elif exo_selectionne == "Développé Militaire":
        st.markdown("<h3>🎯 DÉVELOPPÉ MILITAIRE (OVERHEAD PRESS)</h3>")
        st.video("https://www.youtube.com/watch?v=F3QYdE_t-cQ")
        st.write("**Muscles ciblés :** Deltoïdes (épaules, surtout antérieurs et moyens), Triceps, Trapèzes.")
        st.write("**Placement :** Debout, pieds largeur d'épaules, gainage abdominal fort. Barre posée sur le haut de la poitrine, coudes sous la barre. Prise un peu plus large que les épaules.")
        st.write("**Exécution :** Pousser la barre verticalement au-dessus de la tête. Une fois la barre au-dessus du front, passer la tête légèrement vers l'avant pour aligner la barre avec le corps. Redescendre en contrôlant la charge.")

    elif exo_selectionne == "Élévations Latérales":
        st.markdown("<h3>↔️ ÉLÉVATIONS LATÉRALES</h3>")
        st.video("https://www.youtube.com/watch?v=r0Yd20Xh0_8")
        st.write("**Muscles ciblés :** Deltoïde moyen (pour la largeur des épaules).")
        st.write("**Placement :** Debout, buste légèrement penché en avant. Coudes très légèrement fléchis. Haltères le long du corps ou légèrement devant.")
        st.write("**Exécution :** Monter les haltères latéralement jusqu'à ce que les bras soient parallèles au sol (pas plus haut pour ne pas solliciter les trapèzes supérieurs). Concentrer sur le mouvement du coude. Contrôler la descente.")

    elif exo_selectionne == "Curl Biceps":
        st.markdown("<h3>💪 CURL BICEPS</h3>")
        st.video("https://www.youtube.com/watch?v=tI9w_l7wTf8")
        st.write("**Muscles ciblés :** Biceps brachial.")
        st.write("**Placement :** Debout ou assis, coudes collés au buste. Dos droit, épaules stables.")
        st.write("**Exécution :** Ramener les haltères/la barre vers les épaules en contractant fort le biceps. Contrôler la descente. Éviter de balancer le buste pour tricher.")

    elif exo_selectionne == "Extension Triceps à la Poulie":
        st.markdown("<h3>🔺 EXTENSION TRICEPS POULIE</h3>")
        st.video("https://www.youtube.com/watch?v=BqB3g3yW1mE")
        st.write("**Muscles ciblés :** Triceps brachial.")
        st.write("**Placement :** Debout face à la poulie haute. Coudes près du corps, avant-bras parallèles au sol. Petite flexion des genoux.")
        st.write("**Exécution :** Descendre la barre (ou corde) jusqu'à extension complète des bras, en contractant le triceps. Garder les coudes fixes. Remonter lentement et contrôler la phase excentrique.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 4 : PROGRAMMES D'ENTRAÎNEMENT ---
with tabs[3]:
    st.markdown("<h2>📋 MES PROGRAMMES D'ENTRAÎNEMENT</h2>", unsafe_allow_html=True)
    st.write("Choisissez le programme qui correspond le mieux à votre niveau et votre disponibilité.")
    
    choix_prog = st.selectbox("Sélectionner un programme :", ["PPL - 6 jours (Avancé)", "Upper/Lower - 4 jours (Intermédiaire)", "Full Body - 3 jours (Débutant)"])
    
    st.markdown('<div class="card-dark">', unsafe_allow_html=True)
    if choix_prog == "PPL - 6 jours (Avancé)":
        st.markdown("<h3>🚀 PUSH / PULL / LEGS - 6 JOURS</h3>")
        st.info("Ce programme est idéal pour les personnes ayant déjà une bonne base et souhaitant maximiser l'hypertrophie. Il se base sur un cycle de 3 jours répété.")
        st.markdown("---")
        
        col_ppl1, col_ppl2, col_ppl3 = st.columns(3)
        with col_ppl1:
            st.markdown('<h4>JOUR 1 & 4 : PUSH (Pectoraux, Épaules, Triceps)</h4>'
                        '<ul>'
                        '<li>Développé Couché Barre : 4 séries de 8-12 répétitions</li>'
                        '<li>Développé Incliné Haltères : 3 séries de 10-15 répétitions</li>'
                        '<li>Écartés Poulies : 3 séries de 15-20 répétitions</li>'
                        '<li>Développé Militaire Haltères : 3 séries de 10-15 répétitions</li>'
                        '<li>Élévations Latérales : 3 séries de 15-20 répétitions</li>'
                        '<li>Extensions Triceps Poulie : 4 séries de 12-15 répétitions</li>'
                        '</ul>', unsafe_allow_html=True)
        with col_ppl2:
            st.markdown('<h4>JOUR 2 & 5 : PULL (Dos, Biceps, Arrière-Épaule)</h4>'
                        '<ul>'
                        '<li>Tractions ou Tirage Poitrine : 4 séries de 8-12 répétitions</li>'
                        '<li>Rowing Barre (Prise pronation) : 4 séries de 8-12 répétitions</li>'
                        '<li>Tirage Vertical Prise Serrée : 3 séries de 10-15 répétitions</li>'
                        '<li>Facepull : 3 séries de 15-20 répétitions</li>'
                        '<li>Curl Barre EZ : 4 séries de 10-15 répétitions</li>'
                        '<li>Curl Marteau Haltères : 3 séries de 12-15 répétitions</li>'
                        '</ul>', unsafe_allow_html=True)
        with col_ppl3:
            st.markdown('<h4>JOUR 3 & 6 : LEGS (Jambes & Abdos)</h4>'
                        '<ul>'
                        '<li>Squat Barre : 4 séries de 8-12 répétitions</li>'
                        '<li>Presse à Cuisses : 3 séries de 10-15 répétitions</li>'
                        '<li>Leg Extension : 3 séries de 15-20 répétitions</li>'
                        '<li>Leg Curl : 3 séries de 15-20 répétitions</li>'
                        '<li>Mollets Debout : 4 séries de 15-20 répétitions</li>'
                        '<li>Gainage Planche : 3 séries de 60 secondes</li>'
                        '</ul>', unsafe_allow_html=True)
        st.markdown("---")
        st.write("**Repos :** Jour 7 (ou selon votre cycle).")

    elif choix_prog == "Upper/Lower - 4 jours (Intermédiaire)":
        st.markdown("<h3>📈 UPPER / LOWER - 4 JOURS</h3>")
        st.info("Un bon compromis pour progresser avec une fréquence d'entraînement équilibrée.")
        st.markdown("---")
        col_ul1, col_ul2 = st.columns(2)
        with col_ul1:
            st.markdown('<h4>JOUR 1 & 3 : UPPER BODY (Haut du Corps)</h4>'
                        '<ul>'
                        '<li>Développé Couché : 3 séries de 8-12 répétitions</li>'
                        '<li>Rowing Barre : 3 séries de 8-12 répétitions</li>'
                        '<li>Développé Militaire : 3 séries de 10-15 répétitions</li>'
                        '<li>Tractions ou Tirage Vertical : 3 séries de 8-12 répétitions</li>'
                        '<li>Extensions Triceps : 3 séries de 12-15 répétitions</li>'
                        '<li>Curl Biceps : 3 séries de 12-15 répétitions</li>'
                        '</ul>', unsafe_allow_html=True)
        with col_ul2:
            st.markdown('<h4>JOUR 2 & 4 : LOWER BODY (Bas du Corps)</h4>'
                        '<ul>'
                        '<li>Squat Barre : 3 séries de 8-12 répétitions</li>'
                        '<li>Soulevé de Terre Roumain : 3 séries de 10-15 répétitions</li>'
                        '<li>Leg Press : 3 séries de 10-15 répétitions</li>'
                        '<li>Leg Extension : 3 séries de 15-20 répétitions</li>'
                        '<li>Leg Curl : 3 séries de 15-20 répétitions</li>'
                        '<li>Mollets assis : 3 séries de 15-20 répétitions</li>'
                        '</ul>', unsafe_allow_html=True)
        st.markdown("---")
        st.write("**Repos :** Jour 5, 6, 7.")

    elif choix_prog == "Full Body - 3 jours (Débutant)":
        st.markdown("<h3>🌱 FULL BODY - 3 JOURS</h3>")
        st.info("Excellent pour les débutants, il permet d'apprendre les mouvements de base et de développer une bonne base musculaire rapidement.")
        st.markdown("---")
        st.markdown('<h4>Séance A :</h4>'
                    '<ul>'
                    '<li>Squat Barre : 3 séries de 10-12 répétitions</li>'
                    '<li>Développé Couché : 3 séries de 10-12 répétitions</li>'
                    '<li>Rowing Buste Penché : 3 séries de 10-12 répétitions</li>'
                    '<li>Développé Militaire Haltères : 2 séries de 12-15 répétitions</li>'
                    '<li>Gainage Planche : 3 séries de 30-60 secondes</li>'
                    '</ul>', unsafe_allow_html=True)
        st.markdown('<h4>Séance B :</h4>'
                    '<ul>'
                    '<li>Soulevé de Terre : 3 séries de 6-8 répétitions</li>'
                    '<li>Presse à Cuisses : 3 séries de 10-15 répétitions</li>'
                    '<li>Tirage Vertical : 3 séries de 10-12 répétitions</li>'
                    '<li>Développé Couché Haltères : 3 séries de 10-12 répétitions</li>'
                    '<li>Élévations Latérales : 2 séries de 15-20 répétitions</li>'
                    '</ul>', unsafe_allow_html=True)
        st.markdown("---")
        st.write("**Fréquence :** 3 séances par semaine (ex: Lundi, Mercredi, Vendredi) avec un jour de repos entre chaque séance.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 5 : NUTRITION (Cuisinier IA + Menus) ---
with tabs[4]:
    st.markdown("<h2>🍽️ NUTRITION & CUISINIER IA</h2>", unsafe_allow_html=True)
    st.write("Optimisez votre alimentation pour vos objectifs. L'IA vous aide à créer des repas équilibrés.")
    
    col_cuisinier, col_menus = st.columns(2)
    
    with col_cuisinier:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.subheader("👨‍🍳 CUISINIER IA PERSONNEL")
        st.write("Dites-moi ce que vous avez dans le frigo et je vous suggère une recette ! (Ex: 'poulet, riz, courgettes')")
        ingredients = st.text_input("Ingrédients disponibles :", "Poulet, patate douce, brocolis")
        
        if st.button("GÉNÉRER RECETTE SUR MESURE"):
            if "poulet" in ingredients.lower() and "riz" in ingredients.lower() and "brocolis" in ingredients.lower():
                st.success("**Recette suggérée :** Bowl protéiné : Poulet grillé mariné, riz basmati et brocolis vapeur. Assaisonnez d'un filet d'huile d'olive et d'épices. (~550 kcal)")
            elif "oeufs" in ingredients.lower() and "pain" in ingredients.lower() and "avocat" in ingredients.lower():
                st.success("**Recette suggérée :** Toast avocat-œuf : Pain complet toasté, écrasé d'avocat et œuf poché ou brouillé. (~400 kcal)")
            elif "saumon" in ingredients.lower() and "quinoa" in ingredients.lower():
                st.success("**Recette suggérée :** Pavé de saumon au four, accompagné de quinoa et d'une poêlée de légumes de saison. (~600 kcal)")
            else:
                st.info("**Recette suggérée :** Essayez un 'Stir-fry' de bœuf (ou tofu) avec des légumes variés et des nouilles complètes. (~650 kcal)")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_menus:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        st.subheader("📋 MENUS TYPE (2300 KCAL / JOUR)")
        menu_type = st.selectbox("Sélectionnez votre type de menu :", ["Musculation Classique", "Végétarien / Vegan", "Rapide / Étudiant"])
        
        if menu_type == "Musculation Classique":
            st.markdown("<h4>PETIT DÉJEUNER (~500 kcal)</h4>"
                        "<p>• 3 œufs brouillés ou en omelette<br>"
                        "• 80g de flocons d'avoine avec 200ml de lait demi-écrémé<br>"
                        "• 1 banane</p>"
                        "<h4>DÉJEUNER (~900 kcal)</h4>"
                        "<p>• 180g de poulet (cuit)<br>"
                        "• 150g de riz basmati (cuit)<br>"
                        "• Grosses portions de légumes verts (brocolis, haricots verts)<br>"
                        "• 1 cuillère à soupe d'huile d'olive</p>"
                        "<h4>DÎNER (~900 kcal)</h4>"
                        "<p>• 180g de poisson blanc (cabillaud, colin) ou steak haché 5%<br>"
                        "• 300g de patate douce (cuite)<br>"
                        "• Salade verte avec vinaigrette légère</p>", unsafe_allow_html=True)
        elif menu_type == "Végétarien / Vegan":
            st.markdown("<h4>PETIT DÉJEUNER (~500 kcal)</h4>"
                        "<p>• Smoothie (protéine végétale, lait végétal, fruits rouges, graines de chia)<br>"
                        "• 60g de granola sans sucre ajouté</p>"
                        "<h4>DÉJEUNER (~900 kcal)</h4>"
                        "<p>• 200g de lentilles ou pois chiches<br>"
                        "• 150g de quinoa<br>"
                        "• Wok de légumes variés avec sauce soja légère</p>"
                        "<h4>DÎNER (~900 kcal)</h4>"
                        "<p>• Omelette ou Tofu brouillé (150g)<br>"
                        "• Grande salade composée (crudités,
