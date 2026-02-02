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

# 1. CONFIGURATION DE LA PAGE (Doit être la toute première ligne)
st.set_page_config(page_title="Ebook Musculation Pro", layout="wide", initial_sidebar_state="collapsed")

# 2. INJECTION DU DESIGN "PREMIUM" (Traduction de ton HTML/CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto+Condensed:wght@300;400;700&display=swap');

    /* Fond et Police Globale */
    .stApp {{
        background-color: #0a0a0a;
        color: #ffffff;
        font-family: 'Roboto Condensed', sans-serif;
    }}

    /* Titres Bebas Neue */
    h1, h2, h3, h4 {{
        font-family: 'Bebas Neue', cursive !important;
        letter-spacing: 2px;
        color: #dc2626;
    }}

    /* Barre latérale */
    [data-testid="stSidebar"] {{
        background-color: #1a1a1a;
        border-right: 2px solid #dc2626;
    }}

    /* Cartes Dark Style */
    .card-dark {{
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }}

    /* Boutons dégradé rouge */
    .stButton>button {{
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
    }}
    
    /* Animation Logo */
    .logo-animate {{
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 150px;
        transition: transform 0.3s;
    }}
    .logo-animate:hover {{
        transform: scale(1.1) rotate(5deg);
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. LOGIQUE D'ACCÈS (Code Admin Caché)
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

def check_access():
    st.markdown('<img src="https://i.imgur.com/wlyusJ0.png" class="logo-animate">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 4rem;'>EBOOK MUSCULATION PRO</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card-dark">
            <h3>ACCÈS COMPLET - 20€</h3>
            <p>✓ Programmes PPL, Débutant & PR Bench</p>
            <p>✓ Suivi Mensurations & Photos</p>
            <p>✓ I.A Coach & Nutrition Avancée</p>
            <p>✓ Mini-jeu Flappy Biceps</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("DÉBLOQUER VIA STRIPE"):
            st.session_state['auth'] = True
            st.rerun()

    with col2:
        st.markdown("<h3>ACCÈS ADMIN</h3>", unsafe_allow_html=True)
        admin_code = st.text_input("Code secret", type="password")
        if st.button("VÉRIFIER LE CODE"):
            if admin_code == "F12Berlinetta88170":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Code incorrect.")

if not st.session_state['auth']:
    check_access()
    st.stop()

# 4. APPLICATION PRINCIPALE (Tabs)
st.sidebar.image("https://i.imgur.com/wlyusJ0.png", width=100)
tabs = st.tabs(["📊 Profil", "🎯 Objectifs", "📅 Calendrier", "💪 Entraînement", "📋 Programmes", "🍽️ Nutrition", "⏱️ Repos", "🤖 I.A Coach"])

# --- TAB PROFIL ---
with tabs[0]:
    st.markdown("<h2 class='text-5xl'>📊 MON PROFIL</h2>", unsafe_allow_html=True)
    col_info, col_graph = st.columns([1, 2])
    
    with col_info:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        age = st.number_input("Âge", 14, 99)
        taille = st.number_input("Taille (cm)", 100, 230)
        poids = st.number_input("Poids actuel (kg)", 30.0, 200.0)
        st.button("ENREGISTRER")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_graph:
        st.markdown("### ÉVOLUTION DU POIDS")
        # Données de démo
        df = pd.DataFrame({'Date': ['01/01', '08/01', '15/01'], 'Poids': [75, 74.5, 74.2]})
        fig = px.line(df, x='Date', y='Poids', color_discrete_sequence=['#dc2626'])
        st.plotly_chart(fig, use_container_width=True)
with tabs[3]: # Onglet Entraînement
    st.markdown("<h2 class='text-5xl'>💪 GUIDE TECHNIQUE PRO</h2>", unsafe_allow_html=True)
    
    # Sélecteur stylé
    choix_guide = st.selectbox("Choisir un exercice pour voir la technique :", 
                              ["Développé couché", "Développé incliné", "Rowing Barre", "Squat", 
                               "Soulevé de terre", "Romanian Deadlift", "Élévations latérales", "Curl Biceps", "Développé Militaire"])

    st.markdown('<div class="card-dark">', unsafe_allow_html=True)
    
    if choix_guide == "Développé couché":
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### 🎯 Focus : Pectoraux, Triceps, Épaules")
            st.write("**Position :** Allongé, pieds ancrés au sol pour le 'Leg Drive'. Omoplates serrées (rétractées) pour protéger les épaules.")
            st.write("**Mains :** Largeur supérieure aux épaules. Poignets bien droits au-dessus des avant-bras.")
        with col2:
            st.write("**Angle :** Coudes à environ 45° du buste (ne pas les évaser à 90°).")
            st.write("**Exécution :** Descendre la barre au contact de la partie basse des pectoraux. Poussée explosive en expirant.")

    elif choix_guide == "Squat":
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### 🎯 Focus : Quadriceps, Fessiers, Lombaires")
            st.write("**Position :** Barre sur les trapèzes (High Bar) ou arrière des épaules (Low Bar). Pieds largeur d'épaules.")
            st.write("**Jambes :** Pieds légèrement ouverts (15-30°).")
        with col2:
            st.write("**Angle :** Garder le buste le plus droit possible. Les genoux doivent suivre l'axe des pieds.")
            st.write("**Exécution :** Descendre jusqu'à ce que les hanches soient sous les genoux. Pousser sur les talons.")

    elif choix_guide == "Soulevé de terre":
        st.markdown("#### 🎯 Focus : Chaîne postérieure (Dos, Ischios, Fessiers)")
        st.write("**Position :** Tibias à 2cm de la barre. Dos plat, poitrine sortie. Mains juste à l'extérieur des genoux.")
        st.write("**Exécution :** Tirer en gardant la barre collée aux jambes. Verrouillage des hanches en haut sans cambrer le dos en arrière.")

    elif choix_guide == "Romanian Deadlift":
        st.markdown("#### 🎯 Focus : Ischio-jambiers & Fessiers")
        st.write("**Différence :** On commence debout. On descend la barre en poussant les hanches au maximum vers l'arrière.")
        st.write("**Angle :** Jambes presque tendues (légère flexion). Arrêter la descente quand le dos commence à s'arrondir.")

    elif choix_guide == "Développé Militaire":
        st.markdown("#### 🎯 Focus : Épaules (Deltoïde antérieur) & Triceps")
        st.write("**Position :** Debout, gainage abdominal maximum. Barre repose sur le haut du torse.")
        st.write("**Exécution :** Pousser la barre verticalement. Passer la tête vers l'avant une fois la barre au-dessus du front.")

    elif choix_guide == "Rowing Barre":
        st.markdown("#### 🎯 Focus : Épaisseur du dos (Trapèzes, Grands dorsaux)")
        st.write("**Angle :** Buste penché à 45°. Dos parfaitement plat.")
        st.write("**Exécution :** Tirer la barre vers le nombril en ramenant les coudes vers l'arrière. Serrer les omoplates en fin de mouvement.")

    elif choix_guide == "Élévations latérales":
        st.markdown("#### 🎯 Focus : Largeur d'épaules (Deltoïde latéral)")
        st.write("**Position :** Haltères le long du corps. Légère inclinaison du buste vers l'avant.")
        st.write("**Angle :** Coudes légèrement fléchis. Monter les bras jusqu'à l'horizontale (pas plus haut).")

    elif choix_guide == "Curl Biceps":
        st.markdown("#### 🎯 Focus : Biceps Brachial")
        st.write("**Position :** Coudes collés au buste. Ne pas utiliser l'élan du dos.")
        st.write("**Exécution :** Rotation du poignet (supination) pour une contraction maximale en haut.")

    st.markdown('</div>', unsafe_allow_html=True)
# --- TAB REPOS & JEU ---
with tabs[6]:
    st.markdown("<h2>⏱️ TEMPS DE REPOS</h2>", unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown('<div class="card-dark">', unsafe_allow_html=True)
        sec = st.number_input("Secondes", value=90)
        if st.button("LANCER LE CHRONO"):
            progress_bar = st.progress(100)
            for i in range(sec, 0, -1):
                time.sleep(1)
                progress_bar.progress(int((i/sec)*100))
            st.error("🚀 TEMPS DE REPOS TERMINÉ, RETOUR AU CHARBON !")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_t2:
        with tabs[6]:         
            # L'onglet Repos
    st.markdown("<h2>⏱️ TEMPS DE REPOS</h2>", unsafe_allow_html=True)
    
    # ... (Garde ton code du chronomètre ici) ...

    st.markdown("---")
    st.markdown("### 🕹️ MINI-JEU : FLAPPY BICEPS (SPACE EDITION)")
    st.write("Cliquez dans le cadre ou appuyez sur une touche pour faire sauter le biceps !")

    # Injection du jeu via un composant HTML
    game_code = """
    <canvas id="flappyCanvas" width="400" height="500" style="border:2px solid #dc2626; border-radius:12px; display:block; margin:auto; background:#000;"></canvas>
    <script>
    const canvas = document.getElementById('flappyCanvas');
    const ctx = canvas.getContext('2d');
    
    let bird = { x: 50, y: 150, w: 40, h: 30, gravity: 0.6, lift: -10, velocity: 0 };
    let pipes = [];
    let frame = 0;
    let score = 0;
    let gameOver = false;

    function drawBird() {
        ctx.fillStyle = '#dc2626'; // Couleur rouge sport
        ctx.font = "30px Arial";
        ctx.fillText("💪", bird.x, bird.y); // Un biceps à la place de l'oiseau
    }

    function createPipe() {
        let gap = 120;
        let minH = 50;
        let h = Math.floor(Math.random() * (canvas.height - gap - minH*2)) + minH;
        pipes.push({ x: canvas.width, top: h, bottom: canvas.height - h - gap });
    }

    function update() {
        if (gameOver) return;
        bird.velocity += bird.gravity;
        bird.y += bird.velocity;
        
        if (frame % 90 === 0) createPipe();
        
        pipes.forEach((p, i) => {
            p.x -= 3;
            if (p.x + 50 < 0) { pipes.splice(i, 1); score++; }
            
            // Collision (Planètes/Poteaux)
            if (bird.x + 30 > p.x && bird.x < p.x + 50 && (bird.y < p.y.top || bird.y > canvas.height - p.y.bottom)) {
                // gameOver = true; // Désactivé pour la démo, réactiver pour du challenge
            }
        });
        
        if (bird.y > canvas.height || bird.y < 0) bird.y = 150;
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // Fond spatial
        ctx.fillStyle = "white";
        for(let i=0; i<10; i++) ctx.fillRect(Math.random()*400, Math.random()*500, 2, 2);
        
        drawBird();
        ctx.fillStyle = '#333'; // Planètes/Obstacles
        pipes.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x + 25, p.top - 20, 40, 0, Math.PI * 2); // Planète haut
            ctx.arc(p.x + 25, canvas.height - p.bottom + 20, 40, 0, Math.PI * 2); // Planète bas
            ctx.fill();
        });
        
        ctx.fillStyle = "white";
        ctx.fillText("Score: " + score, 10, 30);
        update();
        frame++;
        requestAnimationFrame(draw);
    }

    window.addEventListener('keydown', () => bird.velocity = bird.lift);
    canvas.addEventListener('mousedown', () => bird.velocity = bird.lift);
    draw();
    </script>
    """
    st.components.v1.html(game_code, height=550)fini
# --- TAB PROGRAMMES (PR BENCH) ---
with tabs[4]:
    st.markdown("<h2>📋 PROGRAMME PR BENCH</h2>", unsafe_allow_html=True)
    obj_pr = st.number_input("Objectif de PR Bench Press (kg)", value=100)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="card-dark">
            <h4>LUNDI (FORCE)</h4>
            <p>• Bench : 4x5 à <b>{obj_pr * 0.75}kg</b></p>
            <p>• Bench Haltère : 3x8</p>
            <p>• Triceps : 3x12</p>
        </div>
        """, unsafe_allow_html=True)
    # (Tu peux dupliquer pour Mercredi et Samedi)

# 5. BOUTON INSTALLATION
st.sidebar.markdown("---")
if st.sidebar.button("📱 INSTALLER L'APP"):
    st.sidebar.success("Chrome Android : Menu > Installer\niOS Safari : Partager > Écran d'accueil")


