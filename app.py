import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

<!doctype html>
<html lang="fr" class="h-full">
 <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ebook Musculation Pro</title>
  <script src="/_sdk/data_sdk.js"></script>
  <script src="/_sdk/element_sdk.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;family=Roboto+Condensed:wght@300;400;700&amp;display=swap" rel="stylesheet">
  <style>
    body {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    
    * {
      font-family: 'Roboto Condensed', sans-serif;
    }
    
    h1, h2, h3, h4 {
      font-family: 'Bebas Neue', cursive;
      letter-spacing: 2px;
    }
    
    :root {
      --bg-dark: #0a0a0a;
      --bg-card: #1a1a1a;
      --red-primary: #dc2626;
      --red-dark: #991b1b;
      --text-light: #ffffff;
      --text-gray: #9ca3af;
    }
    
    .gradient-red {
      background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
    }
    
    .card-dark {
      background: var(--bg-card);
      border: 1px solid #333;
      border-radius: 16px;
      padding: 24px;
      transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .card-dark:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 30px rgba(220, 38, 38, 0.3);
    }
    
    .btn-primary {
      background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
      color: white;
      padding: 14px 28px;
      border-radius: 12px;
      border: none;
      cursor: pointer;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      transition: all 0.3s;
      font-size: 14px;
    }
    
    .btn-primary:hover {
      transform: scale(1.05);
      box-shadow: 0 8px 20px rgba(220, 38, 38, 0.5);
    }
    
    .btn-primary:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }
    
    .btn-secondary {
      background: #2a2a2a;
      color: white;
      padding: 12px 24px;
      border-radius: 10px;
      border: 1px solid #444;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.3s;
    }
    
    .btn-secondary:hover {
      background: #3a3a3a;
      border-color: #dc2626;
    }
    
    .input-dark {
      background: #2a2a2a;
      border: 2px solid #444;
      color: white;
      padding: 12px 16px;
      border-radius: 10px;
      width: 100%;
      transition: border-color 0.3s;
    }
    
    .input-dark:focus {
      outline: none;
      border-color: #dc2626;
    }
    
    .tab-btn {
      padding: 12px 20px;
      background: transparent;
      border: none;
      color: #9ca3af;
      cursor: pointer;
      font-weight: 600;
      text-transform: uppercase;
      font-size: 13px;
      letter-spacing: 1px;
      transition: all 0.3s;
      border-bottom: 3px solid transparent;
      white-space: nowrap;
    }
    
    .tab-btn:hover {
      color: white;
    }
    
    .tab-btn.active {
      color: white;
      border-bottom-color: #dc2626;
    }
    
    .loading-spinner {
      border: 3px solid #333;
      border-top: 3px solid #dc2626;
      border-radius: 50%;
      width: 24px;
      height: 24px;
      animation: spin 0.8s linear infinite;
      display: inline-block;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
      border: 2px solid #dc2626;
      color: white;
      padding: 16px 24px;
      border-radius: 12px;
      z-index: 10000;
      animation: slideIn 0.4s ease-out;
      font-weight: 600;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
    }
    
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    
    .progress-bar {
      width: 100%;
      height: 24px;
      background: #2a2a2a;
      border-radius: 12px;
      overflow: hidden;
      position: relative;
    }
    
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%);
      transition: width 0.5s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 700;
      font-size: 12px;
    }
    
    .game-canvas {
      border: 3px solid #dc2626;
      border-radius: 12px;
      background: #000;
      display: block;
      margin: 0 auto;
    }
    
    .calendar-grid {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 8px;
    }
    
    .calendar-day {
      aspect-ratio: 1;
      background: #2a2a2a;
      border: 2px solid #444;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.3s;
      font-size: 14px;
      font-weight: 600;
    }
    
    .calendar-day:hover {
      border-color: #dc2626;
      transform: scale(1.05);
    }
    
    .calendar-day.today {
      background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
      border-color: #dc2626;
      color: white;
    }
    
    .calendar-day.has-session {
      background: #2a4a2a;
      border-color: #16a34a;
    }
    
    .exercise-card {
      background: #1a1a1a;
      border: 2px solid #333;
      border-radius: 12px;
      padding: 20px;
      transition: all 0.3s;
    }
    
    .exercise-card:hover {
      border-color: #dc2626;
      transform: translateY(-2px);
    }
    
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.95);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
      padding: 20px;
      animation: fadeIn 0.3s;
    }
    
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    
    .modal-content {
      background: #1a1a1a;
      border: 2px solid #dc2626;
      border-radius: 16px;
      padding: 32px;
      max-width: 600px;
      width: 100%;
      max-height: 90%;
      overflow-y: auto;
    }
    
    .stat-card {
      background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
      border: 2px solid #dc2626;
      border-radius: 16px;
      padding: 24px;
      text-align: center;
    }
    
    .stat-number {
      font-size: 48px;
      font-weight: 700;
      color: #dc2626;
      font-family: 'Bebas Neue', cursive;
      letter-spacing: 2px;
    }
    
    .photo-preview {
      width: 100%;
      height: 200px;
      background: #000;
      border-radius: 12px;
      overflow: hidden;
      position: relative;
    }
    
    .photo-preview img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    
    .logo-animate {
      animation: logoFloat 3s ease-in-out infinite;
      transition: transform 0.3s;
    }
    
    .logo-animate:hover {
      transform: scale(1.1) rotate(5deg);
    }
    
    @keyframes logoFloat {
      0%, 100% {
        transform: translateY(0px) rotate(0deg);
      }
      50% {
        transform: translateY(-10px) rotate(3deg);
      }
    }
    
    .logo-modal {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.95);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
      animation: fadeIn 0.3s;
      cursor: pointer;
    }
    
    .logo-modal img {
      max-width: 90%;
      max-height: 90%;
      animation: zoomIn 0.4s ease-out;
    }
    
    @keyframes zoomIn {
      from {
        transform: scale(0.3);
        opacity: 0;
      }
      to {
        transform: scale(1);
        opacity: 1;
      }
    }
    
    .timer-display {
      font-size: 72px;
      font-weight: 700;
      color: #dc2626;
      font-family: 'Bebas Neue', cursive;
      letter-spacing: 4px;
      text-align: center;
      text-shadow: 0 0 20px rgba(220, 38, 38, 0.5);
    }
    
    .recipe-card {
      background: #1a1a1a;
      border: 2px solid #333;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 16px;
    }
    
    .macro-badge {
      display: inline-block;
      background: #2a2a2a;
      border: 1px solid #dc2626;
      border-radius: 20px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      margin-right: 8px;
      margin-bottom: 8px;
    }
  </style>
  <style>@view-transition { navigation: auto; }</style>
 </head>
 <body class="h-full" style="background: #0a0a0a; color: #ffffff;">
  <div id="app" class="h-full w-full flex flex-col overflow-auto"><!-- Payment Gate -->
   <div id="paymentGate" class="h-full w-full flex items-center justify-center p-6">
    <div class="card-dark max-w-3xl w-full">
     <div class="text-center mb-8"><img src="https://i.imgur.com/wlyusJ0.png" alt="Logo Musculation Pro" class="w-40 h-40 mx-auto mb-6 object-contain" loading="lazy" onerror="console.error('Image failed to load:', this.src); this.style.background='linear-gradient(135deg, #dc2626, #991b1b)'; this.style.borderRadius='20px'; this.alt='Logo unavailable';">
      <h1 id="appTitle" class="text-6xl mb-4 gradient-red bg-clip-text text-transparent" style="background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">EBOOK MUSCULATION PRO</h1>
      <p id="welcomeText" class="text-2xl text-gray-300 font-light">Transforme ton physique avec notre ebook complet</p>
     </div>
     <div class="gradient-red p-8 rounded-2xl mb-6">
      <h2 class="text-4xl mb-4 text-center">ACCÈS COMPLET - 20€</h2>
      <div class="grid md:grid-cols-2 gap-4 text-sm mb-6">
       <div>
        <p class="font-bold mb-2">✓ PROFIL &amp; SUIVI</p>
        <ul class="text-gray-200 space-y-1 text-xs">
         <li>• Suivi poids &amp; mensurations détaillées</li>
         <li>• Photos avant/après</li>
         <li>• Graphiques d'évolution</li>
        </ul>
       </div>
       <div>
        <p class="font-bold mb-2">✓ OBJECTIFS MULTIPLES</p>
        <ul class="text-gray-200 space-y-1 text-xs">
         <li>• Objectifs de force, poids, mensurations</li>
         <li>• Suivi avec jauge &amp; pourcentage</li>
         <li>• Calendrier d'entraînement</li>
        </ul>
       </div>
       <div>
        <p class="font-bold mb-2">✓ ENTRAÎNEMENT PRO</p>
        <ul class="text-gray-200 space-y-1 text-xs">
         <li>• Carnet de séance en temps réel</li>
         <li>• Timer entre séries</li>
         <li>• Graphiques de progression par exercice</li>
         <li>���� Descriptifs détaillés des exercices</li>
        </ul>
       </div>
       <div>
        <p class="font-bold mb-2">✓ PROGRAMMES COMPLETS</p>
        <ul class="text-gray-200 space-y-1 text-xs">
         <li>• Programme débutant 5 jours</li>
         <li>• Programme PPL 6 jours</li>
         <li>• Programme PR Bench détaillé</li>
         <li>• Programme cardio maison</li>
         <li>• Créer ses propres programmes</li>
        </ul>
       </div>
       <div>
        <p class="font-bold mb-2">✓ NUTRITION AVANCÉE</p>
        <ul class="text-gray-200 space-y-1 text-xs">
         <li>• Chef I.A pour recettes personnalisées</li>
         <li>• 3 menus détaillés 2300 kcal</li>
         <li>• Tracker quotidien macros</li>
         <li>• Liste de courses automatique</li>
        </ul>
       </div>
       <div>
        <p class="font-bold mb-2">✓ BONUS</p>
        <ul class="text-gray-200 space-y-1 text-xs">
         <li>• I.A Coach personnalisé</li>
         <li>• Calculateurs avancés</li>
         <li>• Mini-jeu Flappy Biceps</li>
         <li>• Routines échauffement &amp; mobilité</li>
         <li>• Suivi santé &amp; récupération</li>
         <li>• Export &amp; partage stats</li>
        </ul>
       </div>
      </div><button onclick="processPayment()" class="btn-primary w-full text-lg py-4">🔥 DÉBLOQUER L'ACCÈS COMPLET - 20€ 🔥</button>
     </div>
     <div class="border-t-2 border-gray-700 pt-6">
      <p class="text-center text-gray-400 mb-4 text-sm">Code administrateur</p><input type="password" id="adminCode" placeholder="Entrez le code admin" class="input-dark mb-4" maxlength="50"> <button onclick="checkAdminCode()" class="btn-secondary w-full">VÉRIFIER LE CODE</button>
     </div>
    </div>
   </div><!-- Main App -->
   <div id="mainApp" style="display: none;" class="h-full w-full flex flex-col"><!-- Header -->
    <header class="bg-black border-b-2 border-gray-800 p-4 flex items-center justify-between flex-wrap gap-4">
     <div class="flex items-center gap-4"><img src="https://i.imgur.com/wlyusJ0.png" alt="Logo" class="w-16 h-16 object-contain cursor-pointer logo-animate" onclick="showLogoModal()" loading="lazy" onerror="console.error('Image failed to load:', this.src); this.style.background='linear-gradient(135deg, #dc2626, #991b1b)'; this.style.borderRadius='12px'; this.alt='Logo unavailable';">
      <div>
       <h1 class="text-2xl gradient-red bg-clip-text text-transparent" style="background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">MUSCULATION PRO</h1>
       <p class="text-xs text-gray-400">Version Complète</p>
      </div>
     </div>
     <div class="flex gap-3"><button onclick="showDownloadModal()" class="btn-secondary text-sm">📱 Installer l'app</button> <button onclick="showExportModal()" class="btn-secondary text-sm">📤 Exporter</button>
     </div>
    </header><!-- Navigation Tabs -->
    <nav class="bg-black border-b-2 border-gray-800 overflow-x-auto">
     <div class="flex min-w-max px-2"><button onclick="switchTab('profil')" class="tab-btn active">📊 Profil</button> <button onclick="switchTab('objectifs')" class="tab-btn">🎯 Objectifs</button> <button onclick="switchTab('calendrier')" class="tab-btn">📅 Calendrier</button> <button onclick="switchTab('entrainement')" class="tab-btn">💪 Entraînement</button> <button onclick="switchTab('programmes')" class="tab-btn">📋 Programmes</button> <button onclick="switchTab('nutrition')" class="tab-btn">🍽️ Nutrition</button> <button onclick="switchTab('repos')" class="tab-btn">⏱️ Repos</button> <button onclick="switchTab('calculs')" class="tab-btn">🧮 Calculs</button> <button onclick="switchTab('ia')" class="tab-btn">🤖 I.A Coach</button> <button onclick="switchTab('sante')" class="tab-btn">❤️ Santé</button> <button onclick="switchTab('notes')" class="tab-btn">📝 Notes</button>
     </div>
    </nav><!-- Content Area -->
    <main class="flex-1 overflow-auto p-6"><!-- PROFIL TAB -->
     <div id="tab-profil" class="tab-content">
      <h2 class="text-5xl mb-8">📊 MON PROFIL</h2>
      <div class="grid lg:grid-cols-3 gap-6 mb-6">
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">INFORMATIONS</h3>
        <form id="profileForm" onsubmit="saveProfile(event)" class="space-y-4">
         <div><label class="block text-sm mb-2 text-gray-400">Âge</label> <input type="number" id="age" placeholder="25" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Taille (cm)</label> <input type="number" id="height" placeholder="175" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Poids actuel (kg)</label> <input type="number" step="0.1" id="weight" placeholder="75" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Exercice préféré</label> <input type="text" id="favoriteExercise" placeholder="Développé couché" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Email</label> <input type="email" id="email" placeholder="email@exemple.com" class="input-dark" required>
         </div><button type="submit" class="btn-primary w-full" id="saveProfileBtn"> <span class="btn-text">ENREGISTRER</span> <span class="loading-spinner" style="display: none;"></span> </button>
        </form>
       </div>
       <div class="card-dark lg:col-span-2">
        <h3 class="text-2xl mb-4 text-red-500">📈 ÉVOLUTION DU POIDS</h3>
        <form id="weightForm" onsubmit="addWeight(event)" class="grid md:grid-cols-3 gap-4 mb-6">
         <div><label class="block text-sm mb-2 text-gray-400">Date</label> <input type="date" id="weightDate" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Poids (kg)</label> <input type="number" step="0.1" id="weightValue" placeholder="75.5" class="input-dark" required>
         </div>
         <div class="flex items-end"><button type="submit" class="btn-primary w-full" id="addWeightBtn"> <span class="btn-text">AJOUTER</span> <span class="loading-spinner" style="display: none;"></span> </button>
         </div>
        </form>
        <div class="bg-black rounded-xl p-4" style="height: 300px;">
         <canvas id="weightCanvas"></canvas>
        </div>
        <div id="weightList" class="mt-4 space-y-2 max-h-40 overflow-y-auto"></div>
       </div>
      </div>
      <div class="grid lg:grid-cols-2 gap-6 mb-6">
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">📏 MENSURATIONS</h3>
        <form id="measurementForm" onsubmit="addMeasurement(event)" class="space-y-4 mb-6">
         <div class="grid grid-cols-2 gap-4">
          <div><label class="block text-sm mb-2 text-gray-400">Date</label> <input type="date" id="measurementDate" class="input-dark" required>
          </div>
          <div><label class="block text-sm mb-2 text-gray-400">Partie du corps</label> <select id="measurementType" class="input-dark" required> <option value="">Choisir...</option> <option value="bras">💪 Tour de bras</option> <option value="cuisse">🦵 Tour de cuisse</option> <option value="taille">���� Tour de taille</option> <option value="poitrine">🫁 Tour de poitrine</option> </select>
          </div>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Mesure (cm)</label> <input type="number" step="0.1" id="measurementValue" placeholder="35.5" class="input-dark" required>
         </div><button type="submit" class="btn-primary w-full" id="addMeasurementBtn"> <span class="btn-text">ENREGISTRER</span> <span class="loading-spinner" style="display: none;"></span> </button>
        </form>
        <div id="measurementList" class="space-y-2 max-h-60 overflow-y-auto"></div>
       </div>
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">📸 PHOTOS AVANT/APRÈS</h3>
        <form id="photoForm" onsubmit="addPhoto(event)" class="space-y-4 mb-6">
         <div class="grid grid-cols-2 gap-4">
          <div><label class="block text-sm mb-2 text-gray-400">Date</label> <input type="date" id="photoDate" class="input-dark" required>
          </div>
          <div><label class="block text-sm mb-2 text-gray-400">Type</label> <select id="photoType" class="input-dark" required> <option value="">Choisir...</option> <option value="avant">Avant</option> <option value="apres">Après</option> <option value="face">Face</option> <option value="profil">Profil</option> <option value="dos">Dos</option> </select>
          </div>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Photo</label> <input type="file" id="photoFile" accept="image/*" class="input-dark" required>
         </div><button type="submit" class="btn-primary w-full" id="addPhotoBtn"> <span class="btn-text">AJOUTER PHOTO</span> <span class="loading-spinner" style="display: none;"></span> </button>
        </form>
        <div id="photoGallery" class="grid grid-cols-3 gap-2"></div>
       </div>
      </div>
      <div class="card-dark">
       <h3 class="text-2xl mb-4 text-red-500">📊 GRAPHIQUE MENSURATIONS</h3>
       <div class="mb-4"><select id="measurementChartType" onchange="updateMeasurementChart()" class="input-dark"> <option value="">Toutes les mensurations</option> <option value="bras">Tour de bras</option> <option value="cuisse">Tour de cuisse</option> <option value="taille">Tour de taille</option> <option value="poitrine">Tour de poitrine</option> </select>
       </div>
       <div class="bg-black rounded-xl p-4" style="height: 350px;">
        <canvas id="measurementCanvas"></canvas>
       </div>
      </div>
     </div><!-- OBJECTIFS TAB -->
     <div id="tab-objectifs" class="tab-content" style="display: none;">
      <h2 class="text-5xl mb-8">🎯 MES OBJECTIFS</h2>
      <div class="card-dark mb-6">
       <h3 class="text-2xl mb-4 text-red-500">CRÉER UN NOUVEL OBJECTIF</h3>
       <form id="goalForm" onsubmit="addGoal(event)" class="space-y-4">
        <div class="grid md:grid-cols-2 gap-4">
         <div><label class="block text-sm mb-2 text-gray-400">Type d'objectif</label> <select id="goalType" class="input-dark" required> <option value="">Choisir...</option> <option value="force">🏋️ Force (PR sur un exercice)</option> <option value="poids">⚖️ Poids corporel</option> <option value="mensuration">📏 Mensuration</option> <option value="performance">⚡ Performance (tractions, course...)</option> </select>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Date limite</label> <input type="date" id="goalDeadline" class="input-dark" required>
         </div>
        </div>
        <div><label class="block text-sm mb-2 text-gray-400">Description</label> <input type="text" id="goalDescription" placeholder="Ex: Développé couché à 100kg" class="input-dark" required>
        </div>
        <div class="grid md:grid-cols-2 gap-4">
         <div><label class="block text-sm mb-2 text-gray-400">Valeur cible</label> <input type="number" step="0.1" id="goalTarget" placeholder="100" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Valeur actuelle</label> <input type="number" step="0.1" id="goalCurrent" placeholder="80" class="input-dark" required>
         </div>
        </div><button type="submit" class="btn-primary w-full" id="addGoalBtn"> <span class="btn-text">CRÉER L'OBJECTIF</span> <span class="loading-spinner" style="display: none;"></span> </button>
       </form>
      </div>
      <div class="grid lg:grid-cols-2 gap-6">
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">🔥 OBJECTIFS EN COURS</h3>
        <div id="activeGoals" class="space-y-4"></div>
       </div>
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-green-500">✅ OBJECTIFS ATTEINTS</h3>
        <div id="completedGoals" class="space-y-4"></div>
       </div>
      </div>
     </div><!-- CALENDRIER TAB -->
     <div id="tab-calendrier" class="tab-content" style="display: none;">
      <h2 class="text-5xl mb-8">📅 CALENDRIER D'ENTRAÎNEMENT</h2>
      <div class="card-dark mb-6">
       <div class="flex justify-between items-center mb-4"><button onclick="changeMonth(-1)" class="btn-secondary">◀ Mois précédent</button>
        <h3 class="text-3xl" id="calendarMonth"></h3><button onclick="changeMonth(1)" class="btn-secondary">Mois suivant ▶</button>
       </div>
       <div class="mb-6 bg-gradient-to-r from-orange-900 to-red-900 bg-opacity-20 border-2 border-orange-600 p-4 rounded-xl">
        <div class="flex justify-between items-center">
         <div>
          <p class="font-bold text-orange-400 mb-1">🤖 PLANIFICATION INTELLIGENTE</p>
          <p class="text-xs text-gray-300">L'I.A détecte vos habitudes et remplit automatiquement votre calendrier</p>
         </div><button onclick="suggestHabitSessions()" class="btn-primary whitespace-nowrap"> 🔄 SUGGÉRER SÉANCES </button>
        </div>
       </div>
       <div class="calendar-grid mb-2">
        <div class="text-center text-gray-400 font-bold">
         LUN
        </div>
        <div class="text-center text-gray-400 font-bold">
         MAR
        </div>
        <div class="text-center text-gray-400 font-bold">
         MER
        </div>
        <div class="text-center text-gray-400 font-bold">
         JEU
        </div>
        <div class="text-center text-gray-400 font-bold">
         VEN
        </div>
        <div class="text-center text-gray-400 font-bold">
         SAM
        </div>
        <div class="text-center text-gray-400 font-bold">
         DIM
        </div>
       </div>
       <div class="calendar-grid" id="calendarGrid"></div>
      </div>
      <div class="card-dark" id="sessionDetails" style="display: none;">
       <h3 class="text-2xl mb-4 text-red-500">SÉANCE DU <span id="sessionDate"></span></h3>
       <form id="sessionForm" onsubmit="saveSession(event)" class="space-y-4">
        <div class="grid md:grid-cols-3 gap-4">
         <div><label class="block text-sm mb-2 text-gray-400">Durée (minutes)</label> <input type="number" id="sessionDuration" placeholder="60" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Programme</label> <input type="text" id="sessionProgram" placeholder="PPL - Push" class="input-dark" required>
         </div>
         <div class="flex items-end"><button type="submit" class="btn-primary w-full" id="saveSessionBtn"> <span class="btn-text">ENREGISTRER</span> <span class="loading-spinner" style="display: none;"></span> </button>
         </div>
        </div>
        <div><label class="block text-sm mb-2 text-gray-400">Exercices effectués</label> <textarea id="sessionExercises" rows="4" placeholder="Ex: Développé couché 4x8, Développé incliné 3x10..." class="input-dark" required></textarea>
        </div>
       </form>
       <div id="sessionHistory" class="mt-6"></div>
      </div>
     </div><!-- ENTRAINEMENT TAB -->
     <div id="tab-entrainement" class="tab-content" style="display: none;">
      <h2 class="text-5xl mb-8">💪 ENTRAÎNEMENT</h2>
      <div class="grid lg:grid-cols-3 gap-6 mb-6">
       <div class="card-dark lg:col-span-2">
        <h3 class="text-2xl mb-4 text-red-500">📝 CARNET DE SÉANCE EN DIRECT</h3>
        <div id="liveSession" style="display: none;">
         <div class="timer-display mb-6" id="sessionTimer">
          00:00
         </div>
         <form id="exerciseForm" onsubmit="addExercise(event)" class="space-y-4 mb-6">
          <div class="grid md:grid-cols-4 gap-3">
           <div><label class="block text-sm mb-2 text-gray-400">Exercice</label> <input type="text" id="exerciseName" placeholder="Développé couché" class="input-dark" required>
           </div>
           <div><label class="block text-sm mb-2 text-gray-400">Séries</label> <input type="number" id="exerciseSets" placeholder="4" class="input-dark" required>
           </div>
           <div><label class="block text-sm mb-2 text-gray-400">Reps</label> <input type="number" id="exerciseReps" placeholder="8" class="input-dark" required>
           </div>
           <div><label class="block text-sm mb-2 text-gray-400">Poids (kg)</label> <input type="number" step="0.5" id="exerciseWeight" placeholder="80" class="input-dark" required>
           </div>
          </div>
          <div><label class="block text-sm mb-2 text-gray-400">Notes (sensations, forme, douleurs)</label> <input type="text" id="exerciseNotes" placeholder="Bonne exécution, légère fatigue..." class="input-dark">
          </div><button type="submit" class="btn-primary w-full">AJOUTER L'EXERCICE</button>
         </form>
         <div id="exerciseList" class="space-y-3 mb-6"></div><button onclick="endSession()" class="btn-secondary w-full">TERMINER LA SÉANCE</button>
        </div><button id="startSessionBtn" onclick="startSession()" class="btn-primary w-full text-xl py-6">🚀 DÉMARRER UNE SÉANCE</button>
       </div>
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">⏱️ TIMER REPOS</h3>
        <div class="timer-display mb-6" id="restTimer">
         01:30
        </div>
        <div class="grid grid-cols-4 gap-2 mb-4"><button onclick="setRestTime(60)" class="btn-secondary text-sm">1:00</button> <button onclick="setRestTime(90)" class="btn-secondary text-sm">1:30</button> <button onclick="setRestTime(120)" class="btn-secondary text-sm">2:00</button> <button onclick="setRestTime(180)" class="btn-secondary text-sm">3:00</button>
        </div>
        <div class="flex gap-3"><button onclick="startRestTimer()" class="btn-primary flex-1">��️ START</button> <button onclick="resetRestTimer()" class="btn-secondary flex-1">🔄 RESET</button>
        </div>
       </div>
      </div>
      <div class="card-dark mb-6">
       <h3 class="text-2xl mb-4 text-red-500">📊 GRAPHIQUE DE PROGRESSION</h3>
       <div class="mb-4"><label class="block text-sm mb-2 text-gray-400">Sélectionner un exercice</label> <select id="exerciseChartSelect" onchange="updateExerciseChart()" class="input-dark"> <option value="">Tous les exercices</option> </select>
       </div>
       <div class="bg-black rounded-xl p-4" style="height: 350px;">
        <canvas id="exerciseCanvas"></canvas>
       </div>
      </div>
      <div class="card-dark mb-6">
       <h3 class="text-2xl mb-4 text-red-500">📚 GUIDE DES EXERCICES</h3>
       <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div class="exercise-card">
         <h4 class="font-bold text-lg mb-2">🏋️ DÉVELOPPÉ COUCHÉ</h4>
         <p class="text-sm text-gray-300 mb-2"><strong>Muscles:</strong> Pectoraux, triceps, deltoïdes antérieurs</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Position:</strong> Allongé sur banc plat, pieds au sol</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Mains:</strong> Largeur d'épaules + 10-15cm, prise pronation</p>
         <p class="text-sm text-gray-300"><strong>Exécution:</strong> Descendre la barre au milieu des pecs, coudes à 45°. Remonter en poussant fort.</p>
        </div>
        <div class="exercise-card">
         <h4 class="font-bold text-lg mb-2">📐 DÉVELOPPÉ INCLINÉ</h4>
         <p class="text-sm text-gray-300 mb-2"><strong>Muscles:</strong> Haut des pectoraux, deltoïdes</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Position:</strong> Banc incliné 30-45°, dos bien plaqué</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Mains:</strong> Légèrement plus large que les épaules</p>
         <p class="text-sm text-gray-300"><strong>Exécution:</strong> Descendre au haut des pecs, garder les coudes stables.</p>
        </div>
        <div class="exercise-card">
         <h4 class="font-bold text-lg mb-2">🚣 ROWING BARRE</h4>
         <p class="text-sm text-gray-300 mb-2"><strong>Muscles:</strong> Grand dorsal, trapèzes, rhomboïdes</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Position:</strong> Dos penché 45°, jambes légèrement fléchies</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Mains:</strong> Largeur d'épaules, prise pronation ou supination</p>
         <p class="text-sm text-gray-300"><strong>Exécution:</strong> Tirer la barre vers le bas du ventre, serrer les omoplates.</p>
        </div>
        <div class="exercise-card">
         <h4 class="font-bold text-lg mb-2">🦵 SQUAT</h4>
         <p class="text-sm text-gray-300 mb-2"><strong>Muscles:</strong> Quadriceps, fessiers, ischio-jambiers</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Position:</strong> Barre sur trapèzes, pieds largeur épaules</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Pieds:</strong> Légèrement tournés vers l'extérieur (15-30°)</p>
         <p class="text-sm text-gray-300"><strong>Exécution:</strong> Descendre en gardant le dos droit, genoux alignés avec les pieds. Remonter en poussant sur les talons.</p>
        </div>
        <div class="exercise-card">
         <h4 class="font-bold text-lg mb-2">💀 SOULEVÉ DE TERRE</h4>
         <p class="text-sm text-gray-300 mb-2"><strong>Muscles:</strong> Chaîne postérieure complète, dos, jambes</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Position:</strong> Pieds sous la barre, largeur hanches</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Mains:</strong> Juste à l'extérieur des jambes</p>
         <p class="text-sm text-gray-300"><strong>Exécution:</strong> Dos droit, pousser sur les jambes puis verrouiller les hanches. Ne jamais arrondir le dos.</p>
        </div>
        <div class="exercise-card">
         <h4 class="font-bold text-lg mb-2">🏋️ ROMANIAN DEADLIFT</h4>
         <p class="text-sm text-gray-300 mb-2"><strong>Muscles:</strong> Ischio-jambiers, fessiers, lombaires</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Position:</strong> Debout, jambes semi-tendues</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Mains:</strong> Largeur d'épaules, prise pronation</p>
         <p class="text-sm text-gray-300"><strong>Exécution:</strong> Descendre en gardant le dos droit, sentir l'étirement des ischios. Remonter en contractant les fessiers.</p>
        </div>
        <div class="exercise-card">
         <h4 class="font-bold text-lg mb-2">🦅 ��LÉVATION LATÉRALE</h4>
         <p class="text-sm text-gray-300 mb-2"><strong>Muscles:</strong> Deltoïdes latéraux (épaules)</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Position:</strong> Debout, buste légèrement penché en avant</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Mains:</strong> Haltères en prise neutre, coudes légèrement fléchis</p>
         <p class="text-sm text-gray-300"><strong>Exécution:</strong> Monter les bras sur les côtés jusqu'�� l'horizontale, descendre lentement.</p>
        </div>
        <div class="exercise-card">
         <h4 class="font-bold text-lg mb-2">💪 CURL BICEPS</h4>
         <p class="text-sm text-gray-300 mb-2"><strong>Muscles:</strong> Biceps brachial, brachial antérieur</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Position:</strong> Debout, dos droit, coudes le long du corps</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Mains:</strong> Supination (paumes vers le haut)</p>
         <p class="text-sm text-gray-300"><strong>Exécution:</strong> Fléchir les avant-bras sans bouger les coudes. Contracter en haut, descendre lentement.</p>
        </div>
        <div class="exercise-card">
         <h4 class="font-bold text-lg mb-2">🎖️ DÉVELOPPÉ MILITAIRE</h4>
         <p class="text-sm text-gray-300 mb-2"><strong>Muscles:</strong> Deltoïdes, triceps, trapèzes</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Position:</strong> Debout ou assis, barre devant au niveau des clavicules</p>
         <p class="text-sm text-gray-300 mb-2"><strong>Mains:</strong> Légèrement plus large que les épaules</p>
         <p class="text-sm text-gray-300"><strong>Exécution:</strong> Pousser la barre verticalement au-dessus de la tête. Descendre contrôlé.</p>
        </div>
       </div>
      </div>
      <div class="card-dark">
       <h3 class="text-2xl mb-4 text-red-500">📜 HISTORIQUE DES SÉANCES</h3>
       <div id="sessionHistory2" class="space-y-3"></div>
      </div>
     </div><!-- PROGRAMMES TAB -->
     <div id="tab-programmes" class="tab-content" style="display: none;">
      <h2 class="text-5xl mb-8">📋 PROGRAMMES D'ENTRAÎNEMENT</h2>
      <div class="grid lg:grid-cols-2 gap-6 mb-6">
       <div class="card-dark">
        <h3 class="text-3xl mb-4 gradient-red bg-clip-text text-transparent" style="background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🔰 PROGRAMME DÉBUTANT 5 JOURS</h3>
        <p class="text-gray-300 mb-4">Programme complet pour débuter la musculation. Chaque muscle travaillé une fois par semaine.</p>
        <div class="space-y-3 text-sm">
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">JOUR 1 - PECTORAUX / TRICEPS</p>
          <p class="text-gray-300">• Développé couché: 4x8-10</p>
          <p class="text-gray-300">• Développé incliné haltères: 3x10-12</p>
          <p class="text-gray-300">• Écarté poulie: 3x12-15</p>
          <p class="text-gray-300">• Dips: 3x8-10</p>
          <p class="text-gray-300">• Extension triceps poulie: 3x12-15</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">JOUR 2 - DOS / BICEPS</p>
          <p class="text-gray-300">• Tractions ou Tirage vertical: 4x8-10</p>
          <p class="text-gray-300">• Rowing barre: 4x8-10</p>
          <p class="text-gray-300">• Rowing haltère: 3x10-12</p>
          <p class="text-gray-300">• Curl barre: 3x10-12</p>
          <p class="text-gray-300">• Curl haltères: 3x12-15</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">JOUR 3 - REPOS</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">JOUR 4 - JAMBES</p>
          <p class="text-gray-300">• Squat: 4x8-10</p>
          <p class="text-gray-300">• Presse à cuisses: 3x10-12</p>
          <p class="text-gray-300">• Leg curl: 3x12-15</p>
          <p class="text-gray-300">• Extension mollets: 4x15-20</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">JOUR 5 - ÉPAULES / ABDOS</p>
          <p class="text-gray-300">����� Développé militaire: 4x8-10</p>
          <p class="text-gray-300">• Élévations latérales: 3x12-15</p>
          <p class="text-gray-300">• Oiseau: 3x12-15</p>
          <p class="text-gray-300">• Crunch: 3x15-20</p>
          <p class="text-gray-300">• Planche: 3x30-60sec</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">JOUR 6-7 - REPOS</p>
         </div>
        </div><button onclick="showProgramDetails('debutant')" class="btn-primary w-full mt-4">VOIR PLUS DE DÉTAILS</button>
       </div>
       <div class="card-dark">
        <h3 class="text-3xl mb-4 gradient-red bg-clip-text text-transparent" style="background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">💪 PROGRAMME PPL 6 JOURS</h3>
        <p class="text-gray-300 mb-4">Push Pull Legs - Programme intermédiaire/avancé pour volume et force.</p>
        <div class="space-y-3 text-sm">
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">JOUR 1 - PUSH (Pecs/Épaules/Triceps)</p>
          <p class="text-gray-300">• Développé couché: 4x6-8</p>
          <p class="text-gray-300">• Développé incliné: 3x8-10</p>
          <p class="text-gray-300">• Développé militaire: 4x6-8</p>
          <p class="text-gray-300">• Élévations latérales: 3x12-15</p>
          <p class="text-gray-300">• Dips: 3x8-10</p>
          <p class="text-gray-300">• Extension triceps: 3x10-12</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">JOUR 2 - PULL (Dos/Biceps)</p>
          <p class="text-gray-300">• Soulev�� de terre: 4x5-6</p>
          <p class="text-gray-300">���� Tractions lestées: 4x6-8</p>
          <p class="text-gray-300">• Rowing barre: 4x8-10</p>
          <p class="text-gray-300">• Rowing haltère: 3x10-12</p>
          <p class="text-gray-300">• Curl barre: 3x8-10</p>
          <p class="text-gray-300">• Curl marteau: 3x10-12</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">JOUR 3 - LEGS (Jambes complètes)</p>
          <p class="text-gray-300">• Squat: 4x6-8</p>
          <p class="text-gray-300">• Front squat: 3x8-10</p>
          <p class="text-gray-300">• Leg press: 3x10-12</p>
          <p class="text-gray-300">• Leg curl: 3x10-12</p>
          <p class="text-gray-300">• RDL: 3x8-10</p>
          <p class="text-gray-300">• Mollets: 4x15-20</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-green-500 mb-1">JOUR 4-6 - RÉPÉTER LE CYCLE</p>
          <p class="text-gray-300">Répéter Push, Pull, Legs avec variations d'exercices</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">JOUR 7 - REPOS</p>
         </div>
        </div><button onclick="showProgramDetails('ppl')" class="btn-primary w-full mt-4">VOIR PLUS DE DÉTAILS</button>
       </div>
       <div class="card-dark">
        <h3 class="text-3xl mb-4 gradient-red bg-clip-text text-transparent" style="background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🏆 AMÉLIORER SON PR AU BENCH</h3>
        <p class="text-gray-300 mb-4">Programme sp��cialisé en 3 séances/semaine pour exploser votre record au développé couché.</p>
        <div class="space-y-3 text-sm">
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">LUNDI - VOLUME</p>
          <p class="text-gray-300">• Développé couché: 4x5 à 75% du PR visé</p>
          <p class="text-gray-300">• Développé haltères: 3x6-10</p>
          <p class="text-gray-300">• Exercice triceps (au choix): 3x10-12</p>
          <p class="text-gray-300 text-xs italic mt-2">Ex: Si votre objectif est 100kg, travaillez à 75kg</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">MERCREDI - TECHNIQUE</p>
          <p class="text-gray-300">• Développé couché: 3x7 à 65% (pause 2sec sur pecs)</p>
          <p class="text-gray-300">• Développé militaire: 3x6-10</p>
          <p class="text-gray-300">• Exercice triceps: 3x8-10</p>
          <p class="text-gray-300">• Exercice biceps: 3x10-12</p>
          <p class="text-gray-300 text-xs italic mt-2">Focus sur la descente contrôlée</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">SAMEDI - FORCE</p>
          <p class="text-gray-300">• Développé couché: 1 single à 80%</p>
          <p class="text-gray-300">• Développé couché: 3x3 à 75%</p>
          <p class="text-gray-300 text-xs italic mt-2">Tester sa force maximale puis volume</p>
         </div>
         <div class="bg-black p-3 rounded-lg border-2 border-yellow-600">
          <p class="font-bold text-yellow-500 mb-2">⚠️ PROGRESSION</p>
          <p class="text-gray-300 text-xs">• Augmentez de +3% chaque semaine SI réussi</p>
          <p class="text-gray-300 text-xs">• N'hésitez pas à rester 1-2 semaines au même poids</p>
          <p class="text-gray-300 text-xs">• Adaptable au squat et soulevé de terre</p>
          <p class="text-gray-300 text-xs mt-2 font-bold">Exercices complémentaires:</p>
          <p class="text-gray-300 text-xs">→ Jambes: Leg press, Leg curl</p>
          <p class="text-gray-300 text-xs">→ Dos: Extensions lombaires, RDL</p>
         </div>
        </div><button onclick="showProgramDetails('bench-pr')" class="btn-primary w-full mt-4">CALCULER MES CHARGES</button>
       </div>
       <div class="card-dark">
        <h3 class="text-3xl mb-4 gradient-red bg-clip-text text-transparent" style="background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🏃 PROGRAMME CARDIO MAISON</h3>
        <p class="text-gray-300 mb-4">Programme de sport à domicile sans matériel. Idéal pour brûler des calories.</p>
        <div class="space-y-3 text-sm">
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">CIRCUIT 1 - CARDIO INTENSE (20min)</p>
          <p class="text-gray-300">• Jumping jacks: 45sec</p>
          <p class="text-gray-300">• Mountain climbers: 45sec</p>
          <p class="text-gray-300">• Burpees: 45sec</p>
          <p class="text-gray-300">• High knees: 45sec</p>
          <p class="text-gray-300">• Repos: 30sec</p>
          <p class="text-gray-300 italic mt-2">Répéter 4 fois</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">CIRCUIT 2 - RENFORCEMENT (25min)</p>
          <p class="text-gray-300">• Pompes: 15-20 reps</p>
          <p class="text-gray-300">• Squats: 20 reps</p>
          <p class="text-gray-300">• Planche: 30-60sec</p>
          <p class="text-gray-300">• Fentes alternées: 20 reps (10 chaque)</p>
          <p class="text-gray-300">• Crunch: 20 reps</p>
          <p class="text-gray-300">• Repos: 60sec</p>
          <p class="text-gray-300 italic mt-2">Répéter 4 fois</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold text-red-500 mb-1">CIRCUIT 3 - TABATA (15min)</p>
          <p class="text-gray-300">�� Exercice: 20sec à fond</p>
          <p class="text-gray-300">• Repos: 10sec</p>
          <p class="text-gray-300">• Répéter 8 fois par exercice</p>
          <p class="text-gray-300 mt-2">Exercices: Burpees, Squats jump, Pompes, Mountain climbers</p>
         </div>
         <div class="bg-black p-3 rounded-lg border-2 border-green-600">
          <p class="font-bold text-green-500 mb-2">📅 PLANNING SEMAINE</p>
          <p class="text-gray-300 text-xs">• Lundi: Circuit 1</p>
          <p class="text-gray-300 text-xs">• Mercredi: Circuit 2</p>
          <p class="text-gray-300 text-xs">• Vendredi: Circuit 3</p>
          <p class="text-gray-300 text-xs">• Week-end: Repos actif (marche)</p>
         </div>
        </div><button onclick="showProgramDetails('cardio')" class="btn-primary w-full mt-4">LANCER UN CIRCUIT</button>
       </div>
      </div>
      <div class="card-dark">
       <h3 class="text-2xl mb-4 text-red-500">✨ CRÉER MON PROPRE PROGRAMME</h3>
       <form id="customProgramForm" onsubmit="saveCustomProgram(event)" class="space-y-4">
        <div><label class="block text-sm mb-2 text-gray-400">Nom du programme</label> <input type="text" id="customProgramName" placeholder="Ex: Mon PPL perso" class="input-dark" required>
        </div>
        <div><label class="block text-sm mb-2 text-gray-400">Contenu du programme (d��taillez les séances)</label> <textarea id="customProgramContent" rows="8" placeholder="Jour 1: Push
- Développé couché 4x8
- Développé incliné 3x10
..." class="input-dark" required></textarea>
        </div><button type="submit" class="btn-primary w-full" id="saveCustomProgramBtn"> <span class="btn-text">ENREGISTRER MON PROGRAMME</span> <span class="loading-spinner" style="display: none;"></span> </button>
       </form>
       <div id="customProgramsList" class="mt-6 space-y-3"></div>
      </div>
     </div><!-- NUTRITION TAB -->
     <div id="tab-nutrition" class="tab-content" style="display: none;">
      <h2 class="text-5xl mb-8">🍽️ NUTRITION</h2>
      <div class="grid lg:grid-cols-2 gap-6 mb-6">
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">�����‍🍳 CHEF I.A - RECETTES PERSONNALISÉES</h3>
        <form id="recipeForm" onsubmit="generateRecipe(event)" class="space-y-4">
         <div class="grid md:grid-cols-2 gap-4">
          <div><label class="block text-sm mb-2 text-gray-400">Calories cibles (kcal)</label> <input type="number" id="recipeCalories" placeholder="500" class="input-dark" required>
          </div>
          <div><label class="block text-sm mb-2 text-gray-400">Protéines (g)</label> <input type="number" id="recipeProtein" placeholder="40" class="input-dark" required>
          </div>
         </div>
         <div class="grid md:grid-cols-2 gap-4">
          <div><label class="block text-sm mb-2 text-gray-400">Glucides (g)</label> <input type="number" id="recipeCarbs" placeholder="50" class="input-dark">
          </div>
          <div><label class="block text-sm mb-2 text-gray-400">Lipides (g)</label> <input type="number" id="recipeFats" placeholder="15" class="input-dark">
          </div>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Préférences alimentaires</label> <input type="text" id="recipePreferences" placeholder="Ex: Poulet, riz, pas de lactose..." class="input-dark">
         </div><button type="submit" class="btn-primary w-full">🔥 GÉNÉRER UNE RECETTE</button>
        </form>
        <div id="generatedRecipe" class="mt-6"></div>
       </div>
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">📊 TRACKER QUOTIDIEN</h3>
        <form id="mealTrackerForm" onsubmit="addMeal(event)" class="space-y-4 mb-6">
         <div><label class="block text-sm mb-2 text-gray-400">Date</label> <input type="date" id="mealDate" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Nom du repas</label> <input type="text" id="mealName" placeholder="Petit déjeuner, Déjeuner..." class="input-dark" required>
         </div>
         <div class="grid grid-cols-4 gap-3">
          <div><label class="block text-sm mb-2 text-gray-400">Kcal</label> <input type="number" id="mealCalories" placeholder="500" class="input-dark" required>
          </div>
          <div><label class="block text-sm mb-2 text-gray-400">P (g)</label> <input type="number" id="mealProtein" placeholder="40" class="input-dark" required>
          </div>
          <div><label class="block text-sm mb-2 text-gray-400">G (g)</label> <input type="number" id="mealCarbs" placeholder="50" class="input-dark" required>
          </div>
          <div><label class="block text-sm mb-2 text-gray-400">L (g)</label> <input type="number" id="mealFats" placeholder="15" class="input-dark" required>
          </div>
         </div><button type="submit" class="btn-primary w-full" id="addMealBtn"> <span class="btn-text">AJOUTER</span> <span class="loading-spinner" style="display: none;"></span> </button>
        </form>
        <div class="stat-card mb-4">
         <p class="text-sm text-gray-400 mb-2">AUJOURD'HUI</p>
         <p class="stat-number" id="todayCalories">0</p>
         <p class="text-xs text-gray-400">KCAL</p>
         <div class="grid grid-cols-3 gap-2 mt-4 text-sm">
          <div>
           <p class="text-gray-400">Protéines</p>
           <p class="font-bold text-red-500" id="todayProtein">0g</p>
          </div>
          <div>
           <p class="text-gray-400">Glucides</p>
           <p class="font-bold text-red-500" id="todayCarbs">0g</p>
          </div>
          <div>
           <p class="text-gray-400">Lipides</p>
           <p class="font-bold text-red-500" id="todayFats">0g</p>
          </div>
         </div>
        </div>
        <div id="todayMealsList" class="space-y-2"></div>
       </div>
      </div>
      <div class="card-dark mb-6">
       <h3 class="text-2xl mb-4 text-red-500">📈 GRAPHIQUE NUTRITION (7 JOURS)</h3>
       <div class="bg-black rounded-xl p-4" style="height: 300px;">
        <canvas id="nutritionCanvas"></canvas>
       </div>
      </div>
      <div class="grid lg:grid-cols-2 gap-6 mb-6">
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">🛒 LISTE DE COURSES</h3>
        <form id="shoppingForm" onsubmit="addShoppingItem(event)" class="flex gap-2 mb-4"><input type="text" id="shoppingItem" placeholder="Article..." class="input-dark flex-1" required> <button type="submit" class="btn-primary" id="addShoppingBtn"> <span class="btn-text">+</span> <span class="loading-spinner" style="display: none;"></span> </button>
        </form>
        <div id="shoppingList" class="space-y-2"></div><button onclick="clearShoppingList()" class="btn-secondary w-full mt-4">🗑️ VIDER LA LISTE</button>
       </div>
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">🍴 MENUS 2300 KCAL</h3>
        <div class="space-y-4">
         <div class="recipe-card">
          <h4 class="font-bold mb-2">MENU 1 - CLASSIQUE</h4>
          <p class="text-sm text-gray-300 mb-2"><strong>Petit-déjeuner (500 kcal):</strong> 4 œufs brouillés, 80g flocons d'avoine, 1 banane</p>
          <p class="text-sm text-gray-300 mb-2"><strong>Déjeuner (800 kcal):</strong> 200g poulet, 100g riz basmati, légumes, 1 cuillère huile d'olive</p>
          <p class="text-sm text-gray-300 mb-2"><strong>Collation (300 kcal):</strong> Fromage blanc 200g, 30g amandes, 1 pomme</p>
          <p class="text-sm text-gray-300 mb-2"><strong>Dîner (700 kcal):</strong> 180g saumon, 150g patates douces, brocolis</p>
          <div class="flex gap-2 mt-3"><span class="macro-badge">P: 180g</span> <span class="macro-badge">G: 230g</span> <span class="macro-badge">L: 65g</span>
          </div>
         </div>
         <div class="recipe-card">
          <h4 class="font-bold mb-2">MENU 2 - VÉGÉTARIEN</h4>
          <p class="text-sm text-gray-300 mb-2"><strong>Petit-déjeuner (500 kcal):</strong> Porridge protéiné (100g avoine, whey, fruits)</p>
          <p class="text-sm text-gray-300 mb-2"><strong>Déjeuner (800 kcal):</strong> Bol Buddha (quinoa, pois chiches, avocat, légumes)</p>
          <p class="text-sm text-gray-300 mb-2"><strong>Collation (300 kcal):</strong> Smoothie protéiné (banane, beurre de cacahuète, lait amande)</p>
          <p class="text-sm text-gray-300 mb-2"><strong>Dîner (700 kcal):</strong> Tofu mariné 200g, riz complet 120g, légumes sautés</p>
          <div class="flex gap-2 mt-3"><span class="macro-badge">P: 155g</span> <span class="macro-badge">G: 250g</span> <span class="macro-badge">L: 70g</span>
          </div>
         </div>
         <div class="recipe-card">
          <h4 class="font-bold mb-2">MENU 3 - PRISE DE MASSE</h4>
          <p class="text-sm text-gray-300 mb-2"><strong>Petit-déjeuner (550 kcal):</strong> 5 œufs, 100g flocons d'avoine, beurre de cacahuète</p>
          <p class="text-sm text-gray-300 mb-2"><strong>Déjeuner (850 kcal):</strong> 220g bœuf, 150g riz, légumes, sauce</p>
          <p class="text-sm text-gray-300 mb-2"><strong>Collation (350 kcal):</strong> Shaker gainer maison (avoine, whey, banane, amandes)</p>
          <p class="text-sm text-gray-300 mb-2"><strong>Dîner (550 kcal):</strong> 200g thon, 120g pâtes, salade, huile d'olive</p>
          <div class="flex gap-2 mt-3"><span class="macro-badge">P: 195g</span> <span class="macro-badge">G: 240g</span> <span class="macro-badge">L: 75g</span>
          </div>
         </div>
        </div>
       </div>
      </div>
     </div><!-- REPOS TAB -->
     <div id="tab-repos" class="tab-content" style="display: none;">
      <h2 class="text-5xl mb-8">⏱��� TEMPS DE REPOS</h2>
      <div class="grid lg:grid-cols-2 gap-6 mb-6">
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">⏰ CHRONOMÈTRE PERSONNALISÉ</h3>
        <div class="timer-display mb-6" id="customTimer">
         00:00
        </div>
        <form id="customTimerForm" onsubmit="startCustomTimer(event)" class="space-y-4">
         <div class="grid grid-cols-2 gap-4">
          <div><label class="block text-sm mb-2 text-gray-400">Minutes</label> <input type="number" id="customMinutes" min="0" max="59" value="1" class="input-dark" required>
          </div>
          <div><label class="block text-sm mb-2 text-gray-400">Secondes</label> <input type="number" id="customSeconds" min="0" max="59" value="30" class="input-dark" required>
          </div>
         </div>
         <div class="flex gap-3"><button type="submit" class="btn-primary flex-1">▶️ DÉMARRER</button> <button type="button" onclick="stopCustomTimer()" class="btn-secondary flex-1">⏹️ STOP</button> <button type="button" onclick="resetCustomTimer()" class="btn-secondary flex-1">🔄 RESET</button>
         </div>
        </form>
        <div id="timerEndMessage" style="display: none;" class="mt-6 text-center p-6 gradient-red rounded-xl animate-pulse">
         <p class="text-3xl font-bold mb-2">⏰ TEMPS DE REPOS TERMINÉ!</p>
         <p class="text-xl">RETOUR AU CHARBON! 💪🔥</p>
        </div>
       </div>
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">🎮 FLAPPY BICEPS</h3>
        <p class="text-sm text-gray-300 mb-4">Détends-toi entre tes séries avec ce mini-jeu spatial! Évite les planètes avec ton biceps cosmique! 🚀</p>
        <canvas id="gameCanvas" class="game-canvas" width="400" height="500"></canvas>
        <div class="text-center mt-4">
         <p class="text-2xl font-bold mb-2">Score: <span id="gameScore" class="text-red-500">0</span></p>
         <p class="text-sm text-gray-400 mb-4">Meilleur: <span id="gameBestScore">0</span></p><button onclick="startGame()" class="btn-primary">🎮 JOUER / RESTART</button>
         <p class="text-xs text-gray-400 mt-3">Cliquez ou appuyez sur ESPACE pour voler!</p>
        </div>
       </div>
      </div>
     </div><!-- CALCULS TAB -->
     <div id="tab-calculs" class="tab-content" style="display: none;">
      <h2 class="text-5xl mb-8">🧮 CALCULATEURS</h2>
      <div class="grid lg:grid-cols-3 gap-6">
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">🔥 CALORIES DÉPENSÉES</h3>
        <form id="caloriesBurnedForm" onsubmit="calculateCaloriesBurned(event)" class="space-y-4">
         <div><label class="block text-sm mb-2 text-gray-400">Activité</label> <select id="activityType" class="input-dark" required> <option value="">Choisir une activité...</option> <optgroup label="💪 MUSCULATION &amp; FITNESS"> <option value="musculation">Musculation intense</option> <option value="musculation-light">Musculation légère</option> <option value="crossfit">CrossFit</option> <option value="hiit">HIIT (High Intensity)</option> <option value="circuit-training">Circuit training</option> <option value="body-pump">Body Pump</option> <option value="trx">TRX / Sangles</option> <option value="kettlebell">Kettlebell</option> </optgroup> <optgroup label="🏃 COURSE &amp; CARDIO"> <option value="course">Course à pied (10 km/h)</option> <option value="course-rapide">Course rapide (12+ km/h)</option> <option value="sprint">Sprints / Intervalles</option> <option value="marche">Marche rapide</option> <option value="marche-normale">Marche normale</option> <option value="tapis">Tapis de course</option> <option value="trail">Trail / Course nature</option> <option value="escaliers">Montée d'escaliers</option> </optgroup> <optgroup label="🚴 VÉLO &amp; CYCLISME"> <option value="velo">Vélo modéré</option> <option value="velo-intense">Vélo intense</option> <option value="vtt">VTT</option> <option value="spinning">Spinning / RPM</option> <option value="velo-appartement">Vélo d'appartement</option> </optgroup> <optgroup label="🏊 SPORTS AQUATIQUES"> <option value="natation">Natation (crawl modéré)</option> <option value="natation-intense">Natation intense</option> <option value="aquagym">Aquagym</option> <option value="aquabike">Aquabike</option> <option value="water-polo">Water-polo</option> <option value="plongee">Plongée sous-marine</option> <option value="surf">Surf</option> <option value="paddle">Paddle / Stand-up</option> </optgroup> <optgroup label="🏀 SPORTS COLLECTIFS"> <option value="basket">Basketball (match)</option> <option value="basket-training">Basketball (entraînement)</option> <option value="football">Football (match)</option> <option value="football-training">Football (entraînement)</option> <option value="rugby">Rugby</option> <option value="handball">Handball</option> <option value="volley">Volleyball</option> <option value="tennis">Tennis</option> <option value="tennis-table">Tennis de table</option> <option value="badminton">Badminton</option> <option value="squash">Squash</option> </optgroup> <optgroup label="🥊 SPORTS DE COMBAT"> <option value="boxe">Boxe (entraînement)</option> <option value="boxe-sac">Boxe sac de frappe</option> <option value="mma">MMA / Arts martiaux mixtes</option> <option value="judo">Judo</option> <option value="karate">Karaté</option> <option value="taekwondo">Taekwondo</option> <option value="muay-thai">Muay Thaï</option> <option value="krav-maga">Krav Maga</option> <option value="catch">Lutte / Wrestling</option> </optgroup> <optgroup label="🧘 YOGA &amp; SOUPLESSE"> <option value="yoga">Yoga (Hatha, Vinyasa)</option> <option value="yoga-power">Power Yoga</option> <option value="pilates">Pilates</option> <option value="stretching">Stretching / Étirements</option> <option value="tai-chi">Tai Chi</option> </optgroup> <optgroup label="💃 DANSE &amp; RYTHME"> <option value="zumba">Zumba</option> <option value="danse">Danse (moderne, jazz)</option> <option value="danse-intense">Danse intense (hip-hop)</option> <option value="salsa">Salsa / Bachata</option> <option value="pole-dance">Pole dance</option> <option value="step">Step / Aérobic</option> </optgroup> <optgroup label="⛰️ SPORTS OUTDOOR"> <option value="escalade">Escalade</option> <option value="randonnee">Randonnée</option> <option value="ski">Ski alpin</option> <option value="ski-fond">Ski de fond</option> <option value="snowboard">Snowboard</option> <option value="raquettes">Raquettes à neige</option> <option value="kayak">Kayak / Canoë</option> <option value="aviron">Aviron</option> </optgroup> <optgroup label="🎾 AUTRES SPORTS"> <option value="golf">Golf</option> <option value="equitation">Équitation</option> <option value="roller">Roller / Patin</option> <option value="skateboard">Skateboard</option> <option value="trampoline">Trampoline</option> <option value="rameur">Rameur (machine)</option> <option value="elliptique">Vélo elliptique</option> <option value="corde-sauter">Corde à sauter</option> <option value="jardinage">Jardinage intense</option> <option value="menage">Ménage actif</option> </optgroup> </select>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Durée (minutes)</label> <input type="number" id="activityDuration" placeholder="60" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Votre poids (kg)</label> <input type="number" id="activityWeight" placeholder="75" class="input-dark" required>
         </div><button type="submit" class="btn-primary w-full">CALCULER</button>
        </form>
        <div id="caloriesBurnedResult" class="mt-6 text-center"></div>
       </div>
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">🍽️ CALORIES REPAS</h3>
        <form id="caloriesMealForm" onsubmit="calculateMealCalories(event)" class="space-y-4">
         <div><label class="block text-sm mb-2 text-gray-400">Protéines (g)</label> <input type="number" id="calcProtein" placeholder="40" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Glucides (g)</label> <input type="number" id="calcCarbs" placeholder="50" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Lipides (g)</label> <input type="number" id="calcFats" placeholder="15" class="input-dark" required>
         </div><button type="submit" class="btn-primary w-full">CALCULER</button>
        </form>
        <div id="mealCaloriesResult" class="mt-6"></div>
       </div>
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">��️ 1RM (CHARGE MAX)</h3>
        <form id="oneRMForm" onsubmit="calculateOneRM(event)" class="space-y-4">
         <div><label class="block text-sm mb-2 text-gray-400">Exercice</label> <select id="rmExercise" class="input-dark" required> <option value="">Choisir...</option> <option value="bench">Développé couché</option> <option value="squat">Squat</option> <option value="deadlift">Soulevé de terre</option> <option value="military">Développé militaire</option> <option value="other">Autre exercice</option> </select>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Poids soulevé (kg)</label> <input type="number" step="0.5" id="rmWeight" placeholder="80" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Répétitions effectuées</label> <input type="number" id="rmReps" min="1" max="15" placeholder="8" class="input-dark" required>
         </div><button type="submit" class="btn-primary w-full">CALCULER 1RM</button>
        </form>
        <div id="oneRMResult" class="mt-6 text-center"></div>
       </div>
      </div>
     </div><!-- IA TAB -->
     <div id="tab-ia" class="tab-content" style="display: none;">
      <h2 class="text-5xl mb-8">🤖 I.A COACH PERSONNEL</h2>
      <div class="card-dark mb-6">
       <h3 class="text-2xl mb-4 text-red-500">💬 POSEZ VOS QUESTIONS</h3>
       <p class="text-gray-300 mb-4">L'I.A analyse vos données (profil, objectifs, séances, nutrition) pour vous donner des conseils personnalisés.</p>
       <form id="iaForm" onsubmit="askIA(event)" class="space-y-4">
        <div><label class="block text-sm mb-2 text-gray-400">Votre question</label> <textarea id="iaQuestion" rows="3" placeholder="Ex: Comment améliorer mon développé couché? Suis-je sur la bonne voie pour mon objectif?" class="input-dark" required></textarea>
        </div><button type="submit" class="btn-primary w-full" id="iaBtn"> <span class="btn-text">🤖 DEMANDER CONSEIL À L'I.A</span> <span class="loading-spinner" style="display: none;"></span> </button>
       </form>
       <div id="iaResponse" class="mt-6"></div>
      </div>
      <div class="grid lg:grid-cols-2 gap-6">
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">📊 ANALYSE AUTOMATIQUE</h3>
        <div id="iaAutoAnalysis" class="space-y-3">
         <p class="text-gray-300">L'I.A analyse vos performances et vous donne des recommandations...</p>
        </div><button onclick="generateAutoAnalysis()" class="btn-primary w-full mt-4">🔄 ACTUALISER L'ANALYSE</button>
       </div>
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">🎯 SUGGESTIONS</h3>
        <div id="iaSuggestions" class="space-y-3">
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold mb-1">💡 Conseil entraînement</p>
          <p class="text-sm text-gray-300">Ajoutez des exercices de mobilité avant vos séances</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold mb-1">🍽️ Conseil nutrition</p>
          <p class="text-sm text-gray-300">Augmentez vos protéines à 2g/kg pour optimiser la récupération</p>
         </div>
         <div class="bg-black p-3 rounded-lg">
          <p class="font-bold mb-1">😴 Conseil récupération</p>
          <p class="text-sm text-gray-300">Visez 8h de sommeil pour de meilleures performances</p>
         </div>
        </div>
       </div>
      </div>
     </div><!-- SANTE TAB -->
     <div id="tab-sante" class="tab-content" style="display: none;">
      <h2 class="text-5xl mb-8">❤️ SANTÉ &amp; RÉCUPÉRATION</h2>
      <div class="grid lg:grid-cols-2 gap-6 mb-6">
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">📝 SUIVI QUOTIDIEN</h3>
        <form id="healthForm" onsubmit="addHealthData(event)" class="space-y-4">
         <div><label class="block text-sm mb-2 text-gray-400">Date</label> <input type="date" id="healthDate" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Heures de sommeil</label> <input type="number" step="0.5" id="healthSleep" min="0" max="24" placeholder="8" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Niveau de fatigue (1-10)</label> <input type="number" id="healthFatigue" min="1" max="10" placeholder="5" class="input-dark" required>
          <p class="text-xs text-gray-400 mt-1">1 = En pleine forme, 10 = Épuisé</p>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Litres d'eau bus</label> <input type="number" step="0.1" id="healthWater" min="0" placeholder="2.5" class="input-dark" required>
         </div>
         <div><label class="block text-sm mb-2 text-gray-400">Douleurs / Blessures</label> <textarea id="healthPain" rows="2" placeholder="Ex: Légère douleur au genou gauche..." class="input-dark"></textarea>
         </div><button type="submit" class="btn-primary w-full" id="addHealthBtn"> <span class="btn-text">ENREGISTRER</span> <span class="loading-spinner" style="display: none;"></span> </button>
        </form>
       </div>
       <div class="card-dark">
        <h3 class="text-2xl mb-4 text-red-500">📈 STATISTIQUES SANTÉ</h3>
        <div class="space-y-4">
         <div class="stat-card">
          <p class="text-sm text-gray-400 mb-1">Sommeil moyen (7 derniers jours)</p>
          <p class="stat-number text-3xl" id="avgSleep">-</p>
          <p class="text-xs text-gray-400">heures/nuit</p>
         </div>
         <div class="stat-card">
          <p class="text-sm text-gray-400 mb-1">Hydratation moyenne</p>
          <p class="stat-number text-3xl" id="avgWater">-</p>
          <p class="text-xs text-gray-400">litres/jour</p>
         </div>
         <div class="stat-card">
          <p class="text-sm text-gray-400 mb-1">Niveau de forme</p>
          <p class="stat-number text-3xl" id="avgFatigue">-</p>
          <p class="text-xs text-gray-400">/10</p>
         </div>
        </div>
       </div>
      </div>
      <div class="card-dark mb-6">
       <h3 class="text-2xl mb-4 text-red-500">📊 ÉVOLUTION SANTÉ</h3>
       <div class="bg-black rounded-xl p-4" style="height: 300px;">
        <canvas id="healthCanvas"></canvas>
       </div>
      </div>
      <div class="card-dark">
       <h3 class="text-2xl mb-4 text-red-500">🩹 HISTORIQUE DES DOULEURS</h3>
       <div id="painHistory" class="space-y-2"></div>
      </div>
     </div><!-- NOTES TAB -->
     <div id="tab-notes" class="tab-content" style="display: none;">
      <h2 class="text-5xl mb-8">📝 CARNET DE NOTES</h2>
      <div class="card-dark mb-6">
       <h3 class="text-2xl mb-4 text-red-500">✍️ NOUVELLE NOTE</h3>
       <form id="noteForm" onsubmit="addNote(event)" class="space-y-4">
        <div><label class="block text-sm mb-2 text-gray-400">Date</label> <input type="date" id="noteDate" class="input-dark" required>
        </div>
        <div><label class="block text-sm mb-2 text-gray-400">Contenu de la note</label> <textarea id="noteContent" rows="6" placeholder="Ex: Aujourd'hui excellent développé couché, j'ai senti une super connexion muscle-cerveau. Séries de 4x8 à 85kg, forme parfaite. Triceps bien congestionné après les dips..." class="input-dark" required></textarea>
        </div><button type="submit" class="btn-primary w-full" id="addNoteBtn"> <span class="btn-text">ENREGISTRER LA NOTE</span> <span class="loading-spinner" style="display: none;"></span> </button>
       </form>
      </div>
      <div class="card-dark">
       <h3 class="text-2xl mb-4 text-red-500">📚 MES NOTES</h3>
       <div id="notesList" class="space-y-3"></div>
      </div>
     </div>
    </main>
   </div>
  </div>
  <script>
    // Global state
    let appState = {
      currentTab: 'profil',
      userPaid: false,
      allData: [],
      currentMonth: new Date().getMonth(),
      currentYear: new Date().getFullYear(),
      selectedCalendarDate: null,
      sessionTimerInterval: null,
      sessionStartTime: null,
      sessionExercises: [],
      restTimerInterval: null,
      restTimeRemaining: 90,
      restTimeSet: 90,
      customTimerInterval: null,
      customTimeRemaining: 0,
      gameInterval: null,
      gameRunning: false
    };
    
    const defaultConfig = {
      app_title: "EBOOK MUSCULATION PRO",
      welcome_text: "Transforme ton physique avec notre ebook complet"
    };
    
    // Data SDK Handler
    const dataHandler = {
      onDataChanged(data) {
        appState.allData = data;
        updateAllViews();
      }
    };
    
    // Initialize app
    async function initializeApp() {
      if (window.dataSdk) {
        const result = await window.dataSdk.init(dataHandler);
        if (!result.isOk) {
          console.error("Failed to initialize SDK");
        }
      }
      
      if (window.elementSdk) {
        await window.elementSdk.init({
          defaultConfig,
          onConfigChange: async (config) => {
            const appTitleElem = document.getElementById('appTitle');
            const welcomeTextElem = document.getElementById('welcomeText');
            
            if (appTitleElem) {
              appTitleElem.textContent = config.app_title || defaultConfig.app_title;
            }
            if (welcomeTextElem) {
              welcomeTextElem.textContent = config.welcome_text || defaultConfig.welcome_text;
            }
          },
          mapToCapabilities: (config) => ({
            recolorables: [],
            borderables: [],
            fontEditable: undefined,
            fontSizeable: undefined
          }),
          mapToEditPanelValues: (config) => new Map([
            ["app_title", config.app_title || defaultConfig.app_title],
            ["welcome_text", config.welcome_text || defaultConfig.welcome_text]
          ])
        });
      }
      
      // Set today's date on forms
      const today = new Date().toISOString().split('T')[0];
      const dateInputs = ['weightDate', 'measurementDate', 'photoDate', 'mealDate', 'healthDate', 'noteDate'];
      dateInputs.forEach(id => {
        const elem = document.getElementById(id);
        if (elem) elem.value = today;
      });
      
      renderCalendar();
    }
    
    // Payment & access
    async function processPayment() {
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite de 999 enregistrements atteinte");
        return;
      }
      
      const result = await window.dataSdk.create({
        id: `payment_${Date.now()}`,
        type: 'payment',
        payment_type: 'full',
        payment_date: new Date().toISOString()
      });
      
      if (result.isOk) {
        appState.userPaid = true;
        document.getElementById('paymentGate').style.display = 'none';
        document.getElementById('mainApp').style.display = 'flex';
        showToast("✅ Paiement validé! Bienvenue! 🎉");
      } else {
        showToast("❌ Erreur lors du paiement");
      }
    }
    
    async function checkAdminCode() {
      const code = document.getElementById('adminCode').value;
      
      if (code === 'F12Berlinetta88170') {
        if (appState.allData.length >= 999) {
          showToast("⚠️ Limite de 999 enregistrements atteinte");
          return;
        }
        
        const result = await window.dataSdk.create({
          id: `admin_${Date.now()}`,
          type: 'admin_access',
          admin_code: code,
          access_date: new Date().toISOString()
        });
        
        if (result.isOk) {
          appState.userPaid = true;
          document.getElementById('paymentGate').style.display = 'none';
          document.getElementById('mainApp').style.display = 'flex';
          showToast("✅ Code admin validé! 🔓");
        }
      } else {
        showToast("❌ Code incorrect");
      }
    }
    
    function checkAccess() {
      const hasAccess = appState.allData.some(d => d.type === 'payment' || d.type === 'admin_access');
      
      if (hasAccess) {
        appState.userPaid = true;
        document.getElementById('paymentGate').style.display = 'none';
        document.getElementById('mainApp').style.display = 'flex';
      }
    }
    
    // Tab switching
    function switchTab(tabName) {
      appState.currentTab = tabName;
      
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
      });
      event.target.classList.add('active');
      
      document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = 'none';
      });
      
      const tabElem = document.getElementById(`tab-${tabName}`);
      if (tabElem) {
        tabElem.style.display = 'block';
      }
      
      // Refresh specific tab data
      if (tabName === 'profil') {
        updateWeightChart();
        updateMeasurementChart();
      } else if (tabName === 'objectifs') {
        updateGoals();
      } else if (tabName === 'calendrier') {
        renderCalendar();
      } else if (tabName === 'entrainement') {
        updateExerciseChart();
        updateExerciseList();
      } else if (tabName === 'nutrition') {
        updateNutritionStats();
        updateNutritionChart();
      } else if (tabName === 'sante') {
        updateHealthStats();
        updateHealthChart();
      } else if (tabName === 'notes') {
        updateNotesList();
      }
    }
    
    // PROFILE FUNCTIONS
    async function saveProfile(e) {
      e.preventDefault();
      
      const btn = document.getElementById('saveProfileBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const profileData = {
        type: 'profile',
        age: parseInt(document.getElementById('age').value),
        height: parseInt(document.getElementById('height').value),
        weight: parseFloat(document.getElementById('weight').value),
        favorite_exercise: document.getElementById('favoriteExercise').value,
        email: document.getElementById('email').value
      };
      
      const existing = appState.allData.find(d => d.type === 'profile');
      
      if (existing) {
        const updated = {...existing, ...profileData};
        const result = await window.dataSdk.update(updated);
        if (result.isOk) {
          showToast("✅ Profil mis à jour!");
        }
      } else {
        if (appState.allData.length >= 999) {
          showToast("⚠️ Limite atteinte");
          btn.disabled = false;
          btnText.style.display = 'inline';
          spinner.style.display = 'none';
          return;
        }
        
        const result = await window.dataSdk.create({
          id: `profile_${Date.now()}`,
          ...profileData
        });
        if (result.isOk) {
          showToast("✅ Profil enregistré!");
        }
      }
      
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
    }
    
    async function addWeight(e) {
      e.preventDefault();
      
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite de 999 enregistrements atteinte");
        return;
      }
      
      const btn = document.getElementById('addWeightBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const result = await window.dataSdk.create({
        id: `weight_${Date.now()}`,
        type: 'weight',
        weight_date: document.getElementById('weightDate').value,
        weight_value: parseFloat(document.getElementById('weightValue').value)
      });
      
      if (result.isOk) {
        showToast("✅ Poids ajouté!");
        document.getElementById('weightForm').reset();
        document.getElementById('weightDate').value = new Date().toISOString().split('T')[0];
      }
      
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
    }
    
    async function deleteWeight(record) {
      const result = await window.dataSdk.delete(record);
      if (result.isOk) {
        showToast("✅ Supprimé");
      }
    }
    
    function updateWeightChart() {
      const weights = appState.allData
        .filter(d => d.type === 'weight')
        .sort((a, b) => new Date(a.weight_date) - new Date(b.weight_date));
      
      const canvas = document.getElementById('weightCanvas');
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      const parent = canvas.parentElement;
      canvas.width = parent.clientWidth;
      canvas.height = 300;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      if (weights.length === 0) {
        ctx.fillStyle = '#666';
        ctx.font = '16px Roboto Condensed';
        ctx.textAlign = 'center';
        ctx.fillText('Aucune donnée de poids', canvas.width / 2, canvas.height / 2);
        return;
      }
      
      drawLineChart(ctx, canvas.width, canvas.height, weights, 'weight_value', 'weight_date', 'kg', '#dc2626');
      
      // Update weight list
      const weightList = document.getElementById('weightList');
      if (weightList) {
        weightList.innerHTML = weights.slice(-5).reverse().map(w => `
          <div class="flex justify-between items-center bg-black p-3 rounded-lg">
            <span class="text-sm">${new Date(w.weight_date).toLocaleDateString('fr-FR')}</span>
            <div class="flex items-center gap-3">
              <span class="font-bold text-red-500">${w.weight_value}kg</span>
              <button onclick="deleteWeight(appState.allData.find(d => d.__backendId === '${w.__backendId}'))" 
                      class="text-gray-400 hover:text-red-500 text-sm">✕</button>
            </div>
          </div>
        `).join('') || '<p class="text-gray-500 text-sm">Aucune entrée</p>';
      }
    }
    
    // MEASUREMENTS
    async function addMeasurement(e) {
      e.preventDefault();
      
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite atteinte");
        return;
      }
      
      const btn = document.getElementById('addMeasurementBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const result = await window.dataSdk.create({
        id: `measurement_${Date.now()}`,
        type: 'measurement',
        measurement_date: document.getElementById('measurementDate').value,
        measurement_type: document.getElementById('measurementType').value,
        measurement_value: parseFloat(document.getElementById('measurementValue').value)
      });
      
      if (result.isOk) {
        showToast("✅ Mensuration ajoutée!");
        document.getElementById('measurementForm').reset();
        document.getElementById('measurementDate').value = new Date().toISOString().split('T')[0];
      }
      
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
    }
    
    async function deleteMeasurement(record) {
      const result = await window.dataSdk.delete(record);
      if (result.isOk) {
        showToast("✅ Supprimé");
      }
    }
    
    function updateMeasurementChart() {
      const measurements = appState.allData
        .filter(d => d.type === 'measurement')
        .sort((a, b) => new Date(a.measurement_date) - new Date(b.measurement_date));
      
      const selectedType = document.getElementById('measurementChartType')?.value;
      const filtered = selectedType 
        ? measurements.filter(m => m.measurement_type === selectedType)
        : measurements;
      
      const canvas = document.getElementById('measurementCanvas');
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      const parent = canvas.parentElement;
      canvas.width = parent.clientWidth;
      canvas.height = 350;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      if (filtered.length === 0) {
        ctx.fillStyle = '#666';
        ctx.font = '16px Roboto Condensed';
        ctx.textAlign = 'center';
        ctx.fillText('Aucune donnée', canvas.width / 2, canvas.height / 2);
        return;
      }
      
      // Draw multi-line chart if all types selected
      if (!selectedType) {
        drawMultiLineChart(ctx, canvas.width, canvas.height, measurements, 'measurement_value', 'measurement_date', 'measurement_type', 'cm');
      } else {
        drawLineChart(ctx, canvas.width, canvas.height, filtered, 'measurement_value', 'measurement_date', 'cm', '#dc2626');
      }
      
      // Update measurement list
      const measurementList = document.getElementById('measurementList');
      if (measurementList) {
        const typeNames = {
          'bras': '💪 Tour de bras',
          'cuisse': '🦵 Tour de cuisse',
          'taille': '📏 Tour de taille',
          'poitrine': '🫁 Tour de poitrine'
        };
        
        measurementList.innerHTML = measurements.slice(-10).reverse().map(m => `
          <div class="flex justify-between items-center bg-black p-3 rounded-lg">
            <div>
              <p class="font-semibold text-sm">${typeNames[m.measurement_type] || m.measurement_type}</p>
              <p class="text-xs text-gray-400">${new Date(m.measurement_date).toLocaleDateString('fr-FR')}</p>
            </div>
            <div class="flex items-center gap-3">
              <span class="font-bold text-red-500">${m.measurement_value}cm</span>
              <button onclick="deleteMeasurement(appState.allData.find(d => d.__backendId === '${m.__backendId}'))" 
                      class="text-gray-400 hover:text-red-500 text-sm">✕</button>
            </div>
          </div>
        `).join('') || '<p class="text-gray-500 text-sm">Aucune mensuration</p>';
      }
    }
    
    // PHOTOS
    async function addPhoto(e) {
      e.preventDefault();
      
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite atteinte");
        return;
      }
      
      const btn = document.getElementById('addPhotoBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const file = document.getElementById('photoFile').files[0];
      if (!file) {
        showToast("❌ Sélectionnez une photo");
        btn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
        return;
      }
      
      const reader = new FileReader();
      reader.onload = async (evt) => {
        const result = await window.dataSdk.create({
          id: `photo_${Date.now()}`,
          type: 'photo',
          photo_date: document.getElementById('photoDate').value,
          photo_type: document.getElementById('photoType').value,
          photo_data: evt.target.result
        });
        
        if (result.isOk) {
          showToast("✅ Photo ajoutée!");
          document.getElementById('photoForm').reset();
          document.getElementById('photoDate').value = new Date().toISOString().split('T')[0];
        }
        
        btn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
      };
      reader.readAsDataURL(file);
    }
    
    async function deletePhoto(record) {
      const result = await window.dataSdk.delete(record);
      if (result.isOk) {
        showToast("✅ Photo supprimée");
      }
    }
    
    function updatePhotoGallery() {
      const photos = appState.allData
        .filter(d => d.type === 'photo')
        .sort((a, b) => new Date(b.photo_date) - new Date(a.photo_date));
      
      const gallery = document.getElementById('photoGallery');
      if (!gallery) return;
      
      gallery.innerHTML = photos.slice(0, 9).map(p => `
        <div class="photo-preview relative">
          <img src="${p.photo_data}" alt="${p.photo_type}" loading="lazy">
          <div class="absolute top-2 right-2">
            <button onclick="deletePhoto(appState.allData.find(d => d.__backendId === '${p.__backendId}'))" 
                    class="bg-red-600 hover:bg-red-700 text-white rounded-full w-6 h-6 text-xs">✕</button>
          </div>
          <div class="absolute bottom-0 left-0 right-0 bg-black bg-opacity-70 p-2">
            <p class="text-xs text-center">${p.photo_type} - ${new Date(p.photo_date).toLocaleDateString('fr-FR')}</p>
          </div>
        </div>
      `).join('') || '<p class="text-gray-500 text-sm col-span-3">Aucune photo</p>';
    }
    
    // GOALS
    async function addGoal(e) {
      e.preventDefault();
      
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite atteinte");
        return;
      }
      
      const btn = document.getElementById('addGoalBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const result = await window.dataSdk.create({
        id: `goal_${Date.now()}`,
        type: 'goal',
        goal_type: document.getElementById('goalType').value,
        goal_description: document.getElementById('goalDescription').value,
        goal_target: parseFloat(document.getElementById('goalTarget').value),
        goal_current: parseFloat(document.getElementById('goalCurrent').value),
        goal_deadline: document.getElementById('goalDeadline').value,
        goal_completed: false,
        created_at: new Date().toISOString()
      });
      
      if (result.isOk) {
        showToast("✅ Objectif créé!");
        document.getElementById('goalForm').reset();
      }
      
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
    }
    
    async function updateGoalProgress(record, newCurrent) {
      const updated = {...record};
      updated.goal_current = newCurrent;
      
      if (newCurrent >= record.goal_target) {
        updated.goal_completed = true;
      }
      
      const result = await window.dataSdk.update(updated);
      if (result.isOk) {
        showToast(updated.goal_completed ? "🎉 Objectif atteint!" : "✅ Progression mise à jour!");
      }
    }
    
    async function deleteGoal(record) {
      const result = await window.dataSdk.delete(record);
      if (result.isOk) {
        showToast("✅ Objectif supprimé");
      }
    }
    
    function updateGoals() {
      const goals = appState.allData.filter(d => d.type === 'goal');
      const active = goals.filter(g => !g.goal_completed);
      const completed = goals.filter(g => g.goal_completed);
      
      const typeIcons = {
        'force': '🏋️',
        'poids': '⚖️',
        'mensuration': '📏',
        'performance': '⚡'
      };
      
      const activeElem = document.getElementById('activeGoals');
      if (activeElem) {
        activeElem.innerHTML = active.map(g => {
          const progress = Math.round((g.goal_current / g.goal_target) * 100);
          const daysLeft = Math.ceil((new Date(g.goal_deadline) - new Date()) / (1000 * 60 * 60 * 24));
          
          return `
            <div class="bg-black p-4 rounded-xl">
              <div class="flex justify-between items-start mb-3">
                <span class="text-3xl">${typeIcons[g.goal_type]}</span>
                <button onclick="deleteGoal(appState.allData.find(d => d.__backendId === '${g.__backendId}'))" 
                        class="text-gray-400 hover:text-red-500 text-sm">✕</button>
              </div>
              <p class="font-bold mb-2">${g.goal_description}</p>
              <p class="text-sm text-gray-400 mb-3">${daysLeft > 0 ? `${daysLeft} jours restants` : 'Échéance dépassée'}</p>
              <div class="progress-bar mb-2">
                <div class="progress-fill" style="width: ${progress}%">${progress}%</div>
              </div>
              <div class="flex justify-between items-center text-sm mb-3">
                <span>${g.goal_current}</span>
                <span class="text-red-500 font-bold">Objectif: ${g.goal_target}</span>
              </div>
              <div class="flex gap-2">
                <input type="number" step="0.1" placeholder="Nouvelle valeur" 
                       id="goalUpdate_${g.__backendId}" class="input-dark flex-1 text-sm p-2">
                <button onclick="updateGoalProgress(appState.allData.find(d => d.__backendId === '${g.__backendId}'), parseFloat(document.getElementById('goalUpdate_${g.__backendId}').value))" 
                        class="btn-primary text-sm px-4">MAJ</button>
              </div>
            </div>
          `;
        }).join('') || '<p class="text-gray-500">Aucun objectif en cours</p>';
      }
      
      const completedElem = document.getElementById('completedGoals');
      if (completedElem) {
        completedElem.innerHTML = completed.map(g => `
          <div class="bg-green-900 bg-opacity-20 border-2 border-green-600 p-4 rounded-xl">
            <div class="flex justify-between items-start mb-2">
              <span class="text-3xl">${typeIcons[g.goal_type]}</span>
              <button onclick="deleteGoal(appState.allData.find(d => d.__backendId === '${g.__backendId}'))" 
                      class="text-gray-400 hover:text-red-500 text-sm">✕</button>
            </div>
            <p class="font-bold mb-2 text-green-400">✅ ${g.goal_description}</p>
            <p class="text-sm text-gray-400">Atteint: ${g.goal_current} / ${g.goal_target}</p>
          </div>
        `).join('') || '<p class="text-gray-500">Aucun objectif atteint</p>';
      }
    }
    
    // CALENDAR
    function renderCalendar() {
      const monthNames = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 
                         'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];
      
      const monthElem = document.getElementById('calendarMonth');
      if (monthElem) {
        monthElem.textContent = `${monthNames[appState.currentMonth]} ${appState.currentYear}`;
      }
      
      const firstDay = new Date(appState.currentYear, appState.currentMonth, 1);
      const lastDay = new Date(appState.currentYear, appState.currentMonth + 1, 0);
      const startDay = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;
      
      const grid = document.getElementById('calendarGrid');
      if (!grid) return;
      
      grid.innerHTML = '';
      
      const sessions = appState.allData.filter(d => d.type === 'calendar_session');
      const today = new Date();
      
      // Empty cells before first day
      for (let i = 0; i < startDay; i++) {
        const cell = document.createElement('div');
        cell.className = 'calendar-day';
        cell.style.opacity = '0.3';
        grid.appendChild(cell);
      }
      
      // Days of month
      for (let day = 1; day <= lastDay.getDate(); day++) {
        const cell = document.createElement('div');
        const dateStr = `${appState.currentYear}-${String(appState.currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const hasSession = sessions.some(s => s.calendar_date === dateStr);
        
        cell.className = 'calendar-day';
        if (hasSession) cell.classList.add('has-session');
        
        if (today.getDate() === day && 
            today.getMonth() === appState.currentMonth && 
            today.getFullYear() === appState.currentYear) {
          cell.classList.add('today');
        }
        
        cell.innerHTML = `
          <span>${day}</span>
          ${hasSession ? '<span style="font-size: 10px;">���</span>' : ''}
        `;
        
        cell.onclick = () => showSessionDetails(dateStr);
        grid.appendChild(cell);
      }
    }
    
    function changeMonth(delta) {
      appState.currentMonth += delta;
      
      if (appState.currentMonth > 11) {
        appState.currentMonth = 0;
        appState.currentYear++;
      } else if (appState.currentMonth < 0) {
        appState.currentMonth = 11;
        appState.currentYear--;
      }
      
      renderCalendar();
    }
    
    // CALENDAR - HABIT DETECTION
    function detectTrainingHabits() {
      const sessions = appState.allData.filter(d => d.type === 'calendar_session' && !d.is_suggestion);
      const exercises = appState.allData.filter(d => d.type === 'exercise');
      
      if (sessions.length < 3 && exercises.length < 3) return null;
      
      // Analyze which days of week user trains
      const dayCount = [0, 0, 0, 0, 0, 0, 0]; // Sun-Sat
      const programsByDay = {};
      
      sessions.forEach(s => {
        const date = new Date(s.calendar_date);
        const dayOfWeek = date.getDay();
        dayCount[dayOfWeek]++;
        
        if (!programsByDay[dayOfWeek]) {
          programsByDay[dayOfWeek] = [];
        }
        if (s.calendar_program && !s.calendar_program.includes('suggéré')) {
          programsByDay[dayOfWeek].push(s.calendar_program);
        }
      });
      
      exercises.forEach(ex => {
        const date = new Date(ex.exercise_date || ex.session_date);
        const dayOfWeek = date.getDay();
        dayCount[dayOfWeek]++;
      });
      
      // Find most common training days
      const trainingDays = [];
      const avgFrequency = dayCount.reduce((sum, c) => sum + c, 0) / 7;
      
      dayCount.forEach((count, day) => {
        if (count > avgFrequency * 0.5 && count > 0) {
          // Get most common program for this day
          const programs = programsByDay[day] || [];
          const programCounts = {};
          programs.forEach(p => {
            programCounts[p] = (programCounts[p] || 0) + 1;
          });
          const mostCommonProgram = Object.keys(programCounts).sort((a, b) => 
            programCounts[b] - programCounts[a]
          )[0] || 'Séance prévue';
          
          trainingDays.push({
            day: day,
            program: mostCommonProgram,
            frequency: count
          });
        }
      });
      
      return trainingDays.length > 0 ? trainingDays : null;
    }
    
    function getNextOccurrences(dayOfWeek, startDate, count = 12) {
      const dates = [];
      const current = new Date(startDate);
      
      while (dates.length < count) {
        if (current.getDay() === dayOfWeek) {
          dates.push(new Date(current));
        }
        current.setDate(current.getDate() + 1);
      }
      
      return dates;
    }
    
    async function suggestHabitSessions() {
      const habits = detectTrainingHabits();
      if (!habits) {
        showToast("📊 Enregistrez au moins 3 séances pour détecter vos habitudes");
        return;
      }
      
      const today = new Date();
      const existingSessions = appState.allData.filter(d => d.type === 'calendar_session');
      let suggestionsAdded = 0;
      
      const dayNames = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
      
      // Show detected habits
      const habitsList = habits.map(h => `${dayNames[h.day]} - ${h.program}`).join(', ');
      showToast(`🤖 Habitudes détectées: ${habitsList}`);
      
      for (const habit of habits) {
        const nextDates = getNextOccurrences(habit.day, today, 12);
        
        for (const date of nextDates) {
          const dateStr = date.toISOString().split('T')[0];
          const exists = existingSessions.some(s => s.calendar_date === dateStr);
          
          if (!exists && date >= today) {
            if (appState.allData.length >= 999) {
              showToast("⚠️ Limite de 999 enregistrements atteinte");
              return;
            }
            
            const result = await window.dataSdk.create({
              id: `calendar_${Date.now()}_${Math.random()}`,
              type: 'calendar_session',
              calendar_date: dateStr,
              calendar_duration: 60,
              calendar_program: habit.program,
              calendar_exercises: 'À compléter lors de la séance',
              is_suggestion: true
            });
            
            if (result.isOk) {
              suggestionsAdded++;
            }
            
            await new Promise(resolve => setTimeout(resolve, 50));
          }
        }
      }
      
      if (suggestionsAdded > 0) {
        setTimeout(() => {
          showToast(`✅ ${suggestionsAdded} séances suggérées ajoutées au calendrier!`);
          renderCalendar();
        }, 500);
      } else {
        setTimeout(() => {
          showToast("ℹ️ Les séances futures sont déjà planifiées");
        }, 500);
      }
    }
    
    function showSessionDetails(dateStr) {
      appState.selectedCalendarDate = dateStr;
      
      const detailsElem = document.getElementById('sessionDetails');
      const sessionDateElem = document.getElementById('sessionDate');
      
      if (detailsElem && sessionDateElem) {
        detailsElem.style.display = 'block';
        sessionDateElem.textContent = new Date(dateStr).toLocaleDateString('fr-FR');
        
        // Load existing session
        const existingSession = appState.allData.find(d => 
          d.type === 'calendar_session' && d.calendar_date === dateStr
        );
        
        if (existingSession) {
          document.getElementById('sessionDuration').value = existingSession.calendar_duration || '';
          document.getElementById('sessionProgram').value = existingSession.calendar_program || '';
          document.getElementById('sessionExercises').value = existingSession.calendar_exercises || '';
        } else {
          document.getElementById('sessionDuration').value = '';
          document.getElementById('sessionProgram').value = '';
          document.getElementById('sessionExercises').value = '';
        }
        
        // Show history for this date
        const historyElem = document.getElementById('sessionHistory');
        if (historyElem && existingSession) {
          historyElem.innerHTML = `
            <h4 class="font-bold mb-2 text-red-500">Séance enregistrée:</h4>
            <div class="bg-black p-3 rounded-lg">
              <p class="text-sm"><strong>Durée:</strong> ${existingSession.calendar_duration} min</p>
              <p class="text-sm"><strong>Programme:</strong> ${existingSession.calendar_program}</p>
              <p class="text-sm"><strong>Exercices:</strong> ${existingSession.calendar_exercises}</p>
            </div>
          `;
        } else if (historyElem) {
          historyElem.innerHTML = '<p class="text-gray-500 text-sm">Aucune séance enregistrée pour ce jour</p>';
        }
      }
      
      // Scroll to details
      detailsElem?.scrollIntoView({ behavior: 'smooth' });
    }
    
    async function saveSession(e) {
      e.preventDefault();
      
      const btn = document.getElementById('saveSessionBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const sessionData = {
        type: 'calendar_session',
        calendar_date: appState.selectedCalendarDate,
        calendar_duration: parseInt(document.getElementById('sessionDuration').value),
        calendar_program: document.getElementById('sessionProgram').value,
        calendar_exercises: document.getElementById('sessionExercises').value
      };
      
      const existing = appState.allData.find(d => 
        d.type === 'calendar_session' && d.calendar_date === appState.selectedCalendarDate
      );
      
      if (existing) {
        const updated = {...existing, ...sessionData};
        const result = await window.dataSdk.update(updated);
        if (result.isOk) {
          showToast("✅ Séance mise à jour!");
        }
      } else {
        if (appState.allData.length >= 999) {
          showToast("⚠️ Limite atteinte");
          btn.disabled = false;
          btnText.style.display = 'inline';
          spinner.style.display = 'none';
          return;
        }
        
        const result = await window.dataSdk.create({
          id: `calendar_${Date.now()}`,
          ...sessionData
        });
        if (result.isOk) {
          showToast("✅ Séance enregistrée!");
        }
      }
      
      renderCalendar();
      
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
    }
    
    // TRAINING SESSION
    function startSession() {
      appState.sessionStartTime = Date.now();
      appState.sessionExercises = [];
      
      document.getElementById('startSessionBtn').style.display = 'none';
      document.getElementById('liveSession').style.display = 'block';
      
      appState.sessionTimerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - appState.sessionStartTime) / 1000);
        const mins = Math.floor(elapsed / 60);
        const secs = elapsed % 60;
        document.getElementById('sessionTimer').textContent = 
          `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }, 1000);
      
      showToast("🚀 Séance démarrée! Bon courage!");
    }
    
    async function addExercise(e) {
      e.preventDefault();
      
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite atteinte");
        return;
      }
      
      const exerciseData = {
        id: `exercise_${Date.now()}`,
        type: 'exercise',
        exercise_name: document.getElementById('exerciseName').value,
        exercise_date: new Date().toISOString().split('T')[0],
        session_exercise: document.getElementById('exerciseName').value,
        session_sets: parseInt(document.getElementById('exerciseSets').value),
        session_reps: parseInt(document.getElementById('exerciseReps').value),
        session_weight: parseFloat(document.getElementById('exerciseWeight').value),
        session_notes: document.getElementById('exerciseNotes')?.value || '',
        session_date: new Date().toISOString()
      };
      
      appState.sessionExercises.push(exerciseData);
      
      const result = await window.dataSdk.create(exerciseData);
      
      if (result.isOk) {
        showToast("✅ Exercice ajouté!");
        document.getElementById('exerciseForm').reset();
        updateExerciseList();
      }
    }
    
    function updateExerciseList() {
      const listElem = document.getElementById('exerciseList');
      if (!listElem) return;
      
      listElem.innerHTML = appState.sessionExercises.map((ex, idx) => `
        <div class="bg-black p-3 rounded-lg">
          <div class="flex justify-between items-start">
            <div>
              <p class="font-bold">${ex.session_exercise}</p>
              <p class="text-sm text-gray-400">${ex.session_sets}x${ex.session_reps} @ ${ex.session_weight}kg</p>
              ${ex.session_notes ? `<p class="text-xs text-gray-400 italic mt-1">${ex.session_notes}</p>` : ''}
            </div>
          </div>
        </div>
      `).join('') || '<p class="text-gray-500 text-sm">Aucun exercice ajouté</p>';
    }
    
    async function endSession() {
      if (appState.sessionTimerInterval) {
        clearInterval(appState.sessionTimerInterval);
        appState.sessionTimerInterval = null;
      }
      
      document.getElementById('startSessionBtn').style.display = 'block';
      document.getElementById('liveSession').style.display = 'none';
      document.getElementById('sessionTimer').textContent = '00:00';
      
      appState.sessionExercises = [];
      document.getElementById('exerciseList').innerHTML = '';
      
      showToast("🎉 Séance terminée! Bien joué!");
    }
    
    // REST TIMER
    function setRestTime(seconds) {
      appState.restTimeSet = seconds;
      appState.restTimeRemaining = seconds;
      updateRestTimerDisplay();
    }
    
    function startRestTimer() {
      if (appState.restTimerInterval) return;
      
      appState.restTimerInterval = setInterval(() => {
        appState.restTimeRemaining--;
        updateRestTimerDisplay();
        
        if (appState.restTimeRemaining <= 0) {
          clearInterval(appState.restTimerInterval);
          appState.restTimerInterval = null;
          showToast("⏰ Repos terminé! RETOUR AU CHARBON! 💪🔥");
        }
      }, 1000);
    }
    
    function resetRestTimer() {
      if (appState.restTimerInterval) {
        clearInterval(appState.restTimerInterval);
        appState.restTimerInterval = null;
      }
      appState.restTimeRemaining = appState.restTimeSet;
      updateRestTimerDisplay();
    }
    
    function updateRestTimerDisplay() {
      const mins = Math.floor(appState.restTimeRemaining / 60);
      const secs = appState.restTimeRemaining % 60;
      const elem = document.getElementById('restTimer');
      if (elem) {
        elem.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }
    }
    
    // CUSTOM TIMER
    function startCustomTimer(e) {
      e.preventDefault();
      
      const mins = parseInt(document.getElementById('customMinutes').value) || 0;
      const secs = parseInt(document.getElementById('customSeconds').value) || 0;
      
      appState.customTimeRemaining = (mins * 60) + secs;
      
      if (appState.customTimerInterval) {
        clearInterval(appState.customTimerInterval);
      }
      
      document.getElementById('timerEndMessage').style.display = 'none';
      
      appState.customTimerInterval = setInterval(() => {
        appState.customTimeRemaining--;
        updateCustomTimerDisplay();
        
        if (appState.customTimeRemaining <= 0) {
          clearInterval(appState.customTimerInterval);
          appState.customTimerInterval = null;
          document.getElementById('timerEndMessage').style.display = 'block';
          showToast("⏰ TEMPS DE REPOS TERMINÉ! RETOUR AU CHARBON! 💪🔥");
        }
      }, 1000);
    }
    
    function stopCustomTimer() {
      if (appState.customTimerInterval) {
        clearInterval(appState.customTimerInterval);
        appState.customTimerInterval = null;
      }
    }
    
    function resetCustomTimer() {
      stopCustomTimer();
      appState.customTimeRemaining = 0;
      updateCustomTimerDisplay();
      document.getElementById('timerEndMessage').style.display = 'none';
    }
    
    function updateCustomTimerDisplay() {
      const mins = Math.floor(appState.customTimeRemaining / 60);
      const secs = appState.customTimeRemaining % 60;
      const elem = document.getElementById('customTimer');
      if (elem) {
        elem.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }
    }
    
    // FLAPPY BICEPS GAME
    let game = {
      biceps: { y: 250, velocity: 0 },
      planets: [],
      score: 0,
      bestScore: 0,
      gravity: 0.6,
      jump: -10,
      planetSpeed: 3,
      planetGap: 200
    };
    
    function startGame() {
      const canvas = document.getElementById('gameCanvas');
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      
      // Reset game
      game.biceps = { y: 250, velocity: 0 };
      game.planets = [];
      game.score = 0;
      game.planetSpeed = 3;
      
      if (appState.gameInterval) {
        clearInterval(appState.gameInterval);
      }
      
      appState.gameRunning = true;
      
      // Game loop
      appState.gameInterval = setInterval(() => {
        if (!appState.gameRunning) return;
        
        // Update biceps
        game.biceps.velocity += game.gravity;
        game.biceps.y += game.biceps.velocity;
        
        // Boundaries
        if (game.biceps.y < 0) game.biceps.y = 0;
        if (game.biceps.y > canvas.height - 40) {
          gameOver();
          return;
        }
        
        // Update planets
        game.planets.forEach(p => p.x -= game.planetSpeed);
        
        // Remove off-screen planets
        game.planets = game.planets.filter(p => p.x > -60);
        
        // Add new planets
        if (game.planets.length === 0 || game.planets[game.planets.length - 1].x < canvas.width - 250) {
          const gapY = Math.random() * (canvas.height - game.planetGap - 100) + 50;
          game.planets.push({
            x: canvas.width,
            topHeight: gapY,
            bottomY: gapY + game.planetGap,
            scored: false
          });
        }
        
        // Collision detection
        game.planets.forEach(p => {
          if (game.biceps.y < p.topHeight || game.biceps.y > p.bottomY) {
            if (p.x < 100 && p.x > 20) {
              gameOver();
            }
          }
          
          // Score
          if (!p.scored && p.x < 50) {
            p.scored = true;
            game.score++;
            document.getElementById('gameScore').textContent = game.score;
          }
        });
        
        // Draw
        drawGame(ctx, canvas);
        
      }, 1000 / 60); // 60 FPS
      
      // Controls
      canvas.onclick = () => {
        if (appState.gameRunning) {
          game.biceps.velocity = game.jump;
        }
      };
      
      document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' && appState.gameRunning) {
          e.preventDefault();
          game.biceps.velocity = game.jump;
        }
      });
    }
    
    function drawGame(ctx, canvas) {
      // Space background
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
      gradient.addColorStop(0, '#0a0a1a');
      gradient.addColorStop(1, '#1a0a2a');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Stars
      ctx.fillStyle = '#ffffff';
      for (let i = 0; i < 50; i++) {
        const x = (i * 47) % canvas.width;
        const y = (i * 73) % canvas.height;
        ctx.fillRect(x, y, 2, 2);
      }
      
      // Planets
      game.planets.forEach(p => {
        // Top planet
        ctx.fillStyle = '#dc2626';
        ctx.beginPath();
        ctx.arc(p.x + 30, p.topHeight - 30, 40, 0, Math.PI * 2);
        ctx.fill();
        
        // Bottom planet
        ctx.fillStyle = '#991b1b';
        ctx.beginPath();
        ctx.arc(p.x + 30, p.bottomY + 30, 40, 0, Math.PI * 2);
        ctx.fill();
      });
      
      // Biceps
      ctx.fillStyle = '#fbbf24';
      ctx.font = 'bold 40px Arial';
      ctx.fillText('💪', 50, game.biceps.y);
    }
    
    function gameOver() {
      appState.gameRunning = false;
      
      if (game.score > game.bestScore) {
        game.bestScore = game.score;
        document.getElementById('gameBestScore').textContent = game.bestScore;
        showToast(`🎮 Nouveau record! ${game.bestScore} points!`);
      }
      
      if (appState.gameInterval) {
        clearInterval(appState.gameInterval);
      }
    }
    
    // EXERCISE TRACKING CHART
    function updateExerciseChart() {
      const exercises = appState.allData.filter(d => d.type === 'exercise');
      
      const selectElem = document.getElementById('exerciseChartSelect');
      if (selectElem) {
        const uniqueExercises = [...new Set(exercises.map(e => e.session_exercise))];
        selectElem.innerHTML = '<option value="">Tous les exercices</option>' + 
          uniqueExercises.map(name => `<option value="${name}">${name}</option>`).join('');
      }
      
      const selectedExercise = selectElem?.value;
      const filtered = selectedExercise 
        ? exercises.filter(e => e.session_exercise === selectedExercise)
        : exercises;
      
      const sorted = filtered.sort((a, b) => new Date(a.exercise_date || a.session_date) - new Date(b.exercise_date || b.session_date));
      
      const canvas = document.getElementById('exerciseCanvas');
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      const parent = canvas.parentElement;
      canvas.width = parent.clientWidth;
      canvas.height = 350;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      if (sorted.length === 0) {
        ctx.fillStyle = '#666';
        ctx.font = '16px Roboto Condensed';
        ctx.textAlign = 'center';
        ctx.fillText('Aucune donnée d\'exercice', canvas.width / 2, canvas.height / 2);
        return;
      }
      
      drawLineChart(ctx, canvas.width, canvas.height, sorted, 'session_weight', 'exercise_date', 'kg', '#dc2626');
      
      // Update session history
      const historyElem = document.getElementById('sessionHistory2');
      if (historyElem) {
        const allExercises = appState.allData.filter(d => d.type === 'exercise')
          .sort((a, b) => new Date(b.exercise_date || b.session_date) - new Date(a.exercise_date || a.session_date));
        
        historyElem.innerHTML = allExercises.slice(0, 20).map(ex => `
          <div class="bg-black p-3 rounded-lg">
            <div class="flex justify-between items-start">
              <div>
                <p class="font-bold">${ex.session_exercise}</p>
                <p class="text-sm text-gray-400">${ex.session_sets}x${ex.session_reps} @ ${ex.session_weight}kg</p>
                ${ex.session_notes ? `<p class="text-xs text-gray-400 italic mt-1">${ex.session_notes}</p>` : ''}
                <p class="text-xs text-gray-500 mt-1">${new Date(ex.exercise_date || ex.session_date).toLocaleDateString('fr-FR')}</p>
              </div>
            </div>
          </div>
        `).join('') || '<p class="text-gray-500 text-sm">Aucun exercice enregistré</p>';
      }
    }
    
    // PROGRAMS
    function showProgramDetails(programType) {
      let modalHtml = '';
      
      if (programType === 'bench-pr') {
        modalHtml = `
          <div class="modal-overlay" onclick="if(event.target === this) this.remove()">
            <div class="modal-content">
              <h3 class="text-3xl mb-4 text-red-500">🏆 CALCULATEUR PR BENCH</h3>
              <form id="prCalcForm" onsubmit="calculatePRLoads(event)" class="space-y-4">
                <div>
                  <label class="block text-sm mb-2 text-gray-400">Votre objectif de PR (kg)</label>
                  <input type="number" step="0.5" id="prTarget" placeholder="100" class="input-dark" required>
                </div>
                <button type="submit" class="btn-primary w-full">CALCULER MES CHARGES</button>
              </form>
              <div id="prLoadsResult" class="mt-6"></div>
              <button onclick="this.closest('.modal-overlay').remove()" class="btn-secondary w-full mt-4">FERMER</button>
            </div>
          </div>
        `;
      } else if (programType === 'debutant') {
        modalHtml = `
          <div class="modal-overlay" onclick="if(event.target === this) this.remove()">
            <div class="modal-content" style="max-width: 800px;">
              <h3 class="text-3xl mb-4 text-red-500">🔰 PROGRAMME DÉBUTANT - GUIDE COMPLET</h3>
              
              <div class="bg-yellow-900 bg-opacity-20 border-2 border-yellow-600 p-4 rounded-xl mb-6">
                <p class="font-bold text-yellow-500 mb-2">📌 PRINCIPES DE BASE</p>
                <ul class="text-sm text-gray-300 space-y-1">
                  <li>• Temps de repos: 1min30 à 2min entre les séries</li>
                  <li>• Progression: +2.5kg par semaine si toutes les séries réussies</li>
                  <li>• Échauffement: 5-10min cardio léger + séries d'échauffement progressives</li>
                  <li>• Durée séance: 45-60 minutes</li>
                  <li>• Hydratation: Boire régulièrement pendant la séance</li>
                </ul>
              </div>
              
              <div class="space-y-4 mb-6 max-h-96 overflow-y-auto">
                <div class="bg-black p-4 rounded-xl">
                  <h4 class="font-bold text-red-500 mb-3">JOUR 1 - PECTORAUX / TRICEPS</h4>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p><strong>1. Développé couché:</strong> 4x8-10 (exercice roi des pecs)</p>
                    <p class="text-xs text-gray-400 ml-4">→ Descendre la barre au milieu des pecs, coudes à 45°</p>
                    <p><strong>2. Développé incliné haltères:</strong> 3x10-12 (haut des pecs)</p>
                    <p class="text-xs text-gray-400 ml-4">→ Banc incliné 30-45°, bien contrôler la descente</p>
                    <p><strong>3. Écarté poulie:</strong> 3x12-15 (étirement et congestion)</p>
                    <p class="text-xs text-gray-400 ml-4">→ Focus sur la contraction, pas sur la charge</p>
                    <p><strong>4. Dips:</strong> 3x8-10 (bas des pecs + triceps)</p>
                    <p class="text-xs text-gray-400 ml-4">→ Se pencher en avant pour cibler les pecs</p>
                    <p><strong>5. Extension triceps poulie:</strong> 3x12-15</p>
                    <p class="text-xs text-gray-400 ml-4">→ Coudes fixes, bien contracter en bas</p>
                  </div>
                </div>
                
                <div class="bg-black p-4 rounded-xl">
                  <h4 class="font-bold text-red-500 mb-3">JOUR 2 - DOS / BICEPS</h4>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p><strong>1. Tractions ou Tirage vertical:</strong> 4x8-10</p>
                    <p class="text-xs text-gray-400 ml-4">→ Prise large, tirer jusqu'au haut des pecs</p>
                    <p><strong>2. Rowing barre:</strong> 4x8-10 (épaisseur du dos)</p>
                    <p class="text-xs text-gray-400 ml-4">→ Dos penché 45°, tirer vers le bas du ventre</p>
                    <p><strong>3. Rowing haltère:</strong> 3x10-12 (unilatéral)</p>
                    <p class="text-xs text-gray-400 ml-4">→ Bien étirer et contracter, rotation légère en haut</p>
                    <p><strong>4. Curl barre:</strong> 3x10-12</p>
                    <p class="text-xs text-gray-400 ml-4">→ Coudes fixes, pas de balancement</p>
                    <p><strong>5. Curl haltères:</strong> 3x12-15</p>
                    <p class="text-xs text-gray-400 ml-4">→ Alterner ou simultané, rotation en montant</p>
                  </div>
                </div>
                
                <div class="bg-black p-4 rounded-xl">
                  <h4 class="font-bold text-red-500 mb-3">JOUR 4 - JAMBES</h4>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p><strong>1. Squat:</strong> 4x8-10 (roi des exercices jambes)</p>
                    <p class="text-xs text-gray-400 ml-4">→ Descendre parallèle minimum, dos droit</p>
                    <p><strong>2. Presse à cuisses:</strong> 3x10-12</p>
                    <p class="text-xs text-gray-400 ml-4">→ Pieds écartés largeur épaules, bien descendre</p>
                    <p><strong>3. Leg curl:</strong> 3x12-15 (ischio-jambiers)</p>
                    <p class="text-xs text-gray-400 ml-4">→ Contrôler la descente, bien contracter en haut</p>
                    <p><strong>4. Extension mollets:</strong> 4x15-20</p>
                    <p class="text-xs text-gray-400 ml-4">→ Amplitude complète, pause en haut</p>
                  </div>
                </div>
                
                <div class="bg-black p-4 rounded-xl">
                  <h4 class="font-bold text-red-500 mb-3">JOUR 5 - ÉPAULES / ABDOS</h4>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p><strong>1. Développé militaire:</strong> 4x8-10</p>
                    <p class="text-xs text-gray-400 ml-4">→ Pousser verticalement, gainage abdominal</p>
                    <p><strong>2. Élévations latérales:</strong> 3x12-15</p>
                    <p class="text-xs text-gray-400 ml-4">→ Charges modérées, focus sur la technique</p>
                    <p><strong>3. Oiseau:</strong> 3x12-15 (deltoïdes postérieurs)</p>
                    <p class="text-xs text-gray-400 ml-4">→ Buste penché, coudes légèrement fléchis</p>
                    <p><strong>4. Crunch:</strong> 3x15-20</p>
                    <p class="text-xs text-gray-400 ml-4">→ Décoller seulement le haut du dos</p>
                    <p><strong>5. Planche:</strong> 3x30-60sec</p>
                    <p class="text-xs text-gray-400 ml-4">→ Corps aligné, gainage total</p>
                  </div>
                </div>
              </div>
              
              <div class="bg-green-900 bg-opacity-20 border-2 border-green-600 p-4 rounded-xl mb-4">
                <p class="font-bold text-green-500 mb-2">💡 CONSEILS NUTRITION</p>
                <p class="text-sm text-gray-300">• Protéines: 1.6-2g par kg de poids corporel</p>
                <p class="text-sm text-gray-300">• Surplus calorique léger: +200-300 kcal/jour</p>
                <p class="text-sm text-gray-300">• Hydratation: 2-3L d'eau par jour</p>
              </div>
              
              <button onclick="this.closest('.modal-overlay').remove()" class="btn-primary w-full">COMPRIS!</button>
            </div>
          </div>
        `;
      } else if (programType === 'ppl') {
        modalHtml = `
          <div class="modal-overlay" onclick="if(event.target === this) this.remove()">
            <div class="modal-content" style="max-width: 800px;">
              <h3 class="text-3xl mb-4 text-red-500">💪 PROGRAMME PPL - GUIDE AVANCÉ</h3>
              
              <div class="bg-yellow-900 bg-opacity-20 border-2 border-yellow-600 p-4 rounded-xl mb-6">
                <p class="font-bold text-yellow-500 mb-2">📌 STRUCTURE DU PPL</p>
                <ul class="text-sm text-gray-300 space-y-1">
                  <li>• <strong>Push (Jour 1 & 4):</strong> Pectoraux, Épaules, Triceps</li>
                  <li>• <strong>Pull (Jour 2 & 5):</strong> Dos, Biceps, Arrière épaules</li>
                  <li>• <strong>Legs (Jour 3 & 6):</strong> Quadriceps, Ischio, Fessiers, Mollets</li>
                  <li>• <strong>Repos:</strong> Jour 7 (ou tous les 3 jours si fatigue)</li>
                  <li>• Temps de repos: 2-3min pour exercices lourds, 1-2min pour isolation</li>
                </ul>
              </div>
              
              <div class="space-y-4 mb-6 max-h-96 overflow-y-auto">
                <div class="bg-black p-4 rounded-xl">
                  <h4 class="font-bold text-red-500 mb-3">PUSH 1 (FORCE) - JOUR 1</h4>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p><strong>1. Développé couché:</strong> 4x6-8 (charge lourde)</p>
                    <p><strong>2. Développé incliné:</strong> 3x8-10</p>
                    <p><strong>3. Développé militaire:</strong> 4x6-8</p>
                    <p><strong>4. Élévations latérales:</strong> 3x12-15</p>
                    <p><strong>5. Dips lestés:</strong> 3x8-10</p>
                    <p><strong>6. Extension triceps:</strong> 3x10-12</p>
                  </div>
                </div>
                
                <div class="bg-black p-4 rounded-xl">
                  <h4 class="font-bold text-red-500 mb-3">PULL 1 (FORCE) - JOUR 2</h4>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p><strong>1. Soulevé de terre:</strong> 4x5-6 (exercice roi du dos)</p>
                    <p><strong>2. Tractions lestées:</strong> 4x6-8</p>
                    <p><strong>3. Rowing barre:</strong> 4x8-10</p>
                    <p><strong>4. Rowing haltère:</strong> 3x10-12</p>
                    <p><strong>5. Curl barre:</strong> 3x8-10</p>
                    <p><strong>6. Curl marteau:</strong> 3x10-12</p>
                  </div>
                </div>
                
                <div class="bg-black p-4 rounded-xl">
                  <h4 class="font-bold text-red-500 mb-3">LEGS 1 (FORCE) - JOUR 3</h4>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p><strong>1. Squat:</strong> 4x6-8 (charge lourde)</p>
                    <p><strong>2. Front squat:</strong> 3x8-10 (quadriceps focus)</p>
                    <p><strong>3. Leg press:</strong> 3x10-12</p>
                    <p><strong>4. Leg curl:</strong> 3x10-12</p>
                    <p><strong>5. Romanian Deadlift:</strong> 3x8-10</p>
                    <p><strong>6. Mollets debout:</strong> 4x15-20</p>
                  </div>
                </div>
                
                <div class="bg-black p-4 rounded-xl">
                  <h4 class="font-bold text-blue-500 mb-3">PUSH 2 (VOLUME) - JOUR 4</h4>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p><strong>1. Développé incliné haltères:</strong> 4x10-12</p>
                    <p><strong>2. Écarté poulie:</strong> 3x12-15</p>
                    <p><strong>3. Développé Arnold:</strong> 3x10-12</p>
                    <p><strong>4. Élévations frontales:</strong> 3x12-15</p>
                    <p><strong>5. Dips poids du corps:</strong> 3x12-15</p>
                    <p><strong>6. Kickback triceps:</strong> 3x12-15</p>
                  </div>
                </div>
                
                <div class="bg-black p-4 rounded-xl">
                  <h4 class="font-bold text-blue-500 mb-3">PULL 2 (VOLUME) - JOUR 5</h4>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p><strong>1. Tirage vertical prise large:</strong> 4x10-12</p>
                    <p><strong>2. Rowing assis poulie:</strong> 4x10-12</p>
                    <p><strong>3. Pullover:</strong> 3x12-15</p>
                    <p><strong>4. Oiseau haltères:</strong> 3x12-15</p>
                    <p><strong>5. Curl incliné:</strong> 3x10-12</p>
                    <p><strong>6. Curl concentration:</strong> 3x12-15</p>
                  </div>
                </div>
                
                <div class="bg-black p-4 rounded-xl">
                  <h4 class="font-bold text-blue-500 mb-3">LEGS 2 (VOLUME) - JOUR 6</h4>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p><strong>1. Squat bulgare:</strong> 4x10-12 (chaque jambe)</p>
                    <p><strong>2. Leg press pieds hauts:</strong> 4x12-15</p>
                    <p><strong>3. Extension jambes:</strong> 3x12-15</p>
                    <p><strong>4. Leg curl assis:</strong> 3x12-15</p>
                    <p><strong>5. Hip thrust:</strong> 3x12-15</p>
                    <p><strong>6. Mollets assis:</strong> 4x15-20</p>
                  </div>
                </div>
              </div>
              
              <div class="bg-green-900 bg-opacity-20 border-2 border-green-600 p-4 rounded-xl mb-4">
                <p class="font-bold text-green-500 mb-2">⚡ PROGRESSION</p>
                <p class="text-sm text-gray-300">��� Augmenter la charge de 2.5-5kg quand toutes les séries sont réussies</p>
                <p class="text-sm text-gray-300">• Alterner semaines lourdes (4-6 reps) et légères (10-12 reps)</p>
                <p class="text-sm text-gray-300">• Protéines: 2-2.2g/kg | Calories: surplus de 300-500 kcal</p>
              </div>
              
              <button onclick="this.closest('.modal-overlay').remove()" class="btn-primary w-full">COMPRIS!</button>
            </div>
          </div>
        `;
      } else if (programType === 'cardio') {
        modalHtml = `
          <div class="modal-overlay" onclick="if(event.target === this) this.remove()">
            <div class="modal-content">
              <h3 class="text-3xl mb-4 text-red-500">🏃 LANCER UN CIRCUIT CARDIO</h3>
              
              <div class="space-y-4 mb-6">
                <button onclick="startCardioCircuit(1)" class="btn-primary w-full text-lg py-4">
                  🔥 CIRCUIT 1 - CARDIO INTENSE (20min)
                </button>
                <button onclick="startCardioCircuit(2)" class="btn-primary w-full text-lg py-4">
                  💪 CIRCUIT 2 - RENFORCEMENT (25min)
                </button>
                <button onclick="startCardioCircuit(3)" class="btn-primary w-full text-lg py-4">
                  ⚡ CIRCUIT 3 - TABATA (15min)
                </button>
              </div>
              
              <div class="bg-yellow-900 bg-opacity-20 border-2 border-yellow-600 p-4 rounded-xl mb-4">
                <p class="font-bold text-yellow-500 mb-2">💡 CONSEILS</p>
                <p class="text-sm text-gray-300">• Échauffez-vous 5 minutes avant de commencer</p>
                <p class="text-sm text-gray-300">• Adaptez l'intensité à votre niveau</p>
                <p class="text-sm text-gray-300">• Hydratez-vous régulièrement</p>
                <p class="text-sm text-gray-300">• Le timer se lancera automatiquement</p>
              </div>
              
              <button onclick="this.closest('.modal-overlay').remove()" class="btn-secondary w-full">ANNULER</button>
            </div>
          </div>
        `;
      }
      
      if (modalHtml) {
        document.body.insertAdjacentHTML('beforeend', modalHtml);
      }
    }
    
    function startCardioCircuit(circuitNum) {
      // Close the modal
      document.querySelector('.modal-overlay')?.remove();
      
      // Switch to repos tab to use the timer
      const reposBtn = Array.from(document.querySelectorAll('.tab-btn')).find(btn => btn.textContent.includes('Repos'));
      if (reposBtn) {
        reposBtn.click();
      }
      
      // Set appropriate time based on circuit
      const times = {
        1: { mins: 20, secs: 0 },
        2: { mins: 25, secs: 0 },
        3: { mins: 15, secs: 0 }
      };
      
      const time = times[circuitNum];
      document.getElementById('customMinutes').value = time.mins;
      document.getElementById('customSeconds').value = time.secs;
      
      // Auto-start the timer
      setTimeout(() => {
        document.getElementById('customTimerForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        showToast(`🔥 Circuit ${circuitNum} lancé! Bon courage!`);
      }, 500);
    }
    
    function calculatePRLoads(e) {
      e.preventDefault();
      const target = parseFloat(document.getElementById('prTarget').value);
      
      const loads = {
        volume: Math.round(target * 0.75 * 2) / 2,
        technique: Math.round(target * 0.65 * 2) / 2,
        force: Math.round(target * 0.80 * 2) / 2,
        force3x3: Math.round(target * 0.75 * 2) / 2
      };
      
      const resultElem = document.getElementById('prLoadsResult');
      if (resultElem) {
        resultElem.innerHTML = `
          <div class="bg-black p-6 rounded-xl space-y-4">
            <h4 class="text-xl font-bold text-red-500 mb-4">VOS CHARGES POUR ${target}KG</h4>
            
            <div class="bg-gray-900 p-4 rounded-lg">
              <p class="font-bold text-green-500 mb-2">LUNDI - VOLUME</p>
              <p class="text-2xl font-bold">${loads.volume}kg</p>
              <p class="text-sm text-gray-400">4 séries de 5 répétitions</p>
            </div>
            
            <div class="bg-gray-900 p-4 rounded-lg">
              <p class="font-bold text-blue-500 mb-2">MERCREDI - TECHNIQUE</p>
              <p class="text-2xl font-bold">${loads.technique}kg</p>
              <p class="text-sm text-gray-400">3 séries de 7 répétitions (pause 2sec)</p>
            </div>
            
            <div class="bg-gray-900 p-4 rounded-lg">
              <p class="font-bold text-red-500 mb-2">SAMEDI - FORCE</p>
              <p class="text-2xl font-bold">${loads.force}kg × 1</p>
              <p class="text-sm text-gray-400 mb-2">1 single à 80%</p>
              <p class="text-2xl font-bold mt-2">${loads.force3x3}kg</p>
              <p class="text-sm text-gray-400">3 séries de 3 répétitions</p>
            </div>
            
            <div class="border-2 border-yellow-600 p-4 rounded-lg mt-4">
              <p class="text-yellow-500 font-bold mb-2">💡 CONSEILS</p>
              <p class="text-sm text-gray-300">• Augmentez de +3% si vous réussissez toutes les séries</p>
              <p class="text-sm text-gray-300">• Restez au même poids si vous échouez</p>
              <p class="text-sm text-gray-300">• Testez votre nouveau PR après 8-12 semaines</p>
            </div>
          </div>
        `;
      }
    }
    
    async function saveCustomProgram(e) {
      e.preventDefault();
      
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite atteinte");
        return;
      }
      
      const btn = document.getElementById('saveCustomProgramBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const result = await window.dataSdk.create({
        id: `custom_program_${Date.now()}`,
        type: 'custom_program',
        custom_program_name: document.getElementById('customProgramName').value,
        custom_program_content: document.getElementById('customProgramContent').value,
        created_at: new Date().toISOString()
      });
      
      if (result.isOk) {
        showToast("✅ Programme enregistré!");
        document.getElementById('customProgramForm').reset();
      }
      
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
    }
    
    async function deleteCustomProgram(record) {
      const result = await window.dataSdk.delete(record);
      if (result.isOk) {
        showToast("✅ Programme supprimé");
      }
    }
    
    function updateCustomPrograms() {
      const programs = appState.allData.filter(d => d.type === 'custom_program');
      
      const listElem = document.getElementById('customProgramsList');
      if (!listElem) return;
      
      listElem.innerHTML = programs.map(p => `
        <div class="bg-black p-4 rounded-xl">
          <div class="flex justify-between items-start mb-3">
            <h4 class="font-bold text-xl text-red-500">${p.custom_program_name}</h4>
            <button onclick="deleteCustomProgram(appState.allData.find(d => d.__backendId === '${p.__backendId}'))" 
                    class="text-gray-400 hover:text-red-500">✕</button>
          </div>
          <pre class="text-sm text-gray-300 whitespace-pre-wrap font-sans">${p.custom_program_content}</pre>
        </div>
      `).join('') || '<p class="text-gray-500 text-sm">Aucun programme personnalisé</p>';
    }
    
    // NUTRITION
    function generateRecipe(e) {
      e.preventDefault();
      
      const calories = document.getElementById('recipeCalories').value;
      const protein = document.getElementById('recipeProtein').value;
      const carbs = document.getElementById('recipeCarbs').value || 'auto';
      const fats = document.getElementById('recipeFats').value || 'auto';
      const prefs = document.getElementById('recipePreferences').value;
      
      const recipes = [
        {
          name: "Bowl Protéiné Power",
          ingredients: "200g poulet grillé, 100g riz basmati, 150g brocolis vapeur, 1 cuillère huile d'olive, épices",
          instructions: "1. Cuire le riz. 2. Griller le poulet avec épices. 3. Cuire les brocolis vapeur. 4. Assembler et arroser d'huile d'olive.",
          macros: `${calories} kcal | P: ${protein}g | G: ${carbs}g | L: ${fats}g`
        },
        {
          name: "Omelette Muscu",
          ingredients: "5 œufs, 80g flocons d'avoine, 30g fromage, légumes au choix, sel, poivre",
          instructions: "1. Battre les œufs. 2. Ajouter légumes coupés. 3. Cuire à la poêle. 4. Servir avec flocons d'avoine et fromage.",
          macros: `${calories} kcal | P: ${protein}g | G: ${carbs}g | L: ${fats}g`
        },
        {
          name: "Buddha Bowl Végé",
          ingredients: "150g quinoa, 200g pois chiches, avocat, légumes variés, tahini, citron",
          instructions: "1. Cuire le quinoa et les pois chiches. 2. Couper les légumes. 3. Préparer sauce tahini-citron. 4. Assembler le bowl.",
          macros: `${calories} kcal | P: ${protein}g | G: ${carbs}g | L: ${fats}g`
        },
        {
          name: "Saumon Patate Douce",
          ingredients: "180g saumon, 150g patate douce, asperges, huile d'olive, herbes",
          instructions: "1. Cuire la patate douce au four. 2. Griller le saumon. 3. Cuire les asperges vapeur. 4. Assaisonner.",
          macros: `${calories} kcal | P: ${protein}g | G: ${carbs}g | L: ${fats}g`
        }
      ];
      
      const randomRecipe = recipes[Math.floor(Math.random() * recipes.length)];
      
      const resultElem = document.getElementById('generatedRecipe');
      if (resultElem) {
        resultElem.innerHTML = `
          <div class="recipe-card">
            <h4 class="font-bold text-xl mb-3 text-red-500">${randomRecipe.name}</h4>
            <div class="mb-3">
              ${randomRecipe.macros.split('|').map(m => `<span class="macro-badge">${m.trim()}</span>`).join('')}
            </div>
            <p class="text-sm mb-3"><strong>Ingr��dients:</strong><br>${randomRecipe.ingredients}</p>
            <p class="text-sm"><strong>Préparation:</strong><br>${randomRecipe.instructions}</p>
            ${prefs ? `<p class="text-xs text-gray-400 mt-3 italic">Adapté pour: ${prefs}</p>` : ''}
          </div>
        `;
      }
      
      showToast("👨‍🍳 Recette générée!");
    }
    
    async function addMeal(e) {
      e.preventDefault();
      
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite atteinte");
        return;
      }
      
      const btn = document.getElementById('addMealBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const result = await window.dataSdk.create({
        id: `meal_${Date.now()}`,
        type: 'meal',
        meal_date: document.getElementById('mealDate').value,
        meal_name: document.getElementById('mealName').value,
        meal_calories: parseInt(document.getElementById('mealCalories').value),
        meal_protein: parseInt(document.getElementById('mealProtein').value),
        meal_carbs: parseInt(document.getElementById('mealCarbs').value),
        meal_fats: parseInt(document.getElementById('mealFats').value)
      });
      
      if (result.isOk) {
        showToast("✅ Repas ajouté!");
        document.getElementById('mealTrackerForm').reset();
        document.getElementById('mealDate').value = new Date().toISOString().split('T')[0];
      }
      
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
    }
    
    async function deleteMeal(record) {
      const result = await window.dataSdk.delete(record);
      if (result.isOk) {
        showToast("✅ Repas supprim��");
      }
    }
    
    function updateNutritionStats() {
      const today = new Date().toISOString().split('T')[0];
      const todayMeals = appState.allData.filter(d => d.type === 'meal' && d.meal_date === today);
      
      const totalCals = todayMeals.reduce((sum, m) => sum + (m.meal_calories || 0), 0);
      const totalProtein = todayMeals.reduce((sum, m) => sum + (m.meal_protein || 0), 0);
      const totalCarbs = todayMeals.reduce((sum, m) => sum + (m.meal_carbs || 0), 0);
      const totalFats = todayMeals.reduce((sum, m) => sum + (m.meal_fats || 0), 0);
      
      const caloriesElem = document.getElementById('todayCalories');
      const proteinElem = document.getElementById('todayProtein');
      const carbsElem = document.getElementById('todayCarbs');
      const fatsElem = document.getElementById('todayFats');
      
      if (caloriesElem) caloriesElem.textContent = totalCals;
      if (proteinElem) proteinElem.textContent = `${totalProtein}g`;
      if (carbsElem) carbsElem.textContent = `${totalCarbs}g`;
      if (fatsElem) fatsElem.textContent = `${totalFats}g`;
      
      const listElem = document.getElementById('todayMealsList');
      if (listElem) {
        listElem.innerHTML = todayMeals.map(m => `
          <div class="flex justify-between items-center bg-black p-3 rounded-lg">
            <div>
              <p class="font-semibold text-sm">${m.meal_name}</p>
              <p class="text-xs text-gray-400">${m.meal_calories} kcal | P:${m.meal_protein}g G:${m.meal_carbs}g L:${m.meal_fats}g</p>
            </div>
            <button onclick="deleteMeal(appState.allData.find(d => d.__backendId === '${m.__backendId}'))" 
                    class="text-gray-400 hover:text-red-500 text-sm">✕</button>
          </div>
        `).join('') || '<p class="text-gray-500 text-sm">Aucun repas aujourd\'hui</p>';
      }
    }
    
    function updateNutritionChart() {
      const meals = appState.allData.filter(d => d.type === 'meal');
      
      // Group by date and sum calories
      const dailyData = {};
      meals.forEach(m => {
        if (!dailyData[m.meal_date]) {
          dailyData[m.meal_date] = { calories: 0, protein: 0, carbs: 0, fats: 0 };
        }
        dailyData[m.meal_date].calories += m.meal_calories || 0;
        dailyData[m.meal_date].protein += m.meal_protein || 0;
        dailyData[m.meal_date].carbs += m.meal_carbs || 0;
        dailyData[m.meal_date].fats += m.meal_fats || 0;
      });
      
      const sorted = Object.keys(dailyData)
        .sort()
        .slice(-7)
        .map(date => ({
          date,
          ...dailyData[date]
        }));
      
      const canvas = document.getElementById('nutritionCanvas');
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      const parent = canvas.parentElement;
      canvas.width = parent.clientWidth;
      canvas.height = 300;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      if (sorted.length === 0) {
        ctx.fillStyle = '#666';
        ctx.font = '16px Roboto Condensed';
        ctx.textAlign = 'center';
        ctx.fillText('Aucune donnée nutrition', canvas.width / 2, canvas.height / 2);
        return;
      }
      
      drawBarChart(ctx, canvas.width, canvas.height, sorted, 'calories', 'date', 'kcal');
    }
    
    // SHOPPING LIST
    async function addShoppingItem(e) {
      e.preventDefault();
      
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite atteinte");
        return;
      }
      
      const btn = document.getElementById('addShoppingBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const result = await window.dataSdk.create({
        id: `shopping_${Date.now()}`,
        type: 'shopping',
        shopping_item: document.getElementById('shoppingItem').value,
        shopping_bought: false
      });
      
      if (result.isOk) {
        document.getElementById('shoppingForm').reset();
      }
      
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
    }
    
    async function toggleShopping(record) {
      const updated = {...record};
      updated.shopping_bought = !updated.shopping_bought;
      
      const result = await window.dataSdk.update(updated);
      if (!result.isOk) {
        showToast("❌ Erreur");
      }
    }
    
    async function deleteShoppingItem(record) {
      const result = await window.dataSdk.delete(record);
      if (result.isOk) {
        showToast("✅ Supprimé");
      }
    }
    
    async function clearShoppingList() {
      const items = appState.allData.filter(d => d.type === 'shopping');
      
      for (const item of items) {
        await window.dataSdk.delete(item);
      }
      
      showToast("✅ Liste vidée");
    }
    
    function updateShoppingList() {
      const items = appState.allData.filter(d => d.type === 'shopping');
      
      const listElem = document.getElementById('shoppingList');
      if (!listElem) return;
      
      listElem.innerHTML = items.map(item => `
        <div class="flex justify-between items-center bg-black p-3 rounded-lg ${item.shopping_bought ? 'opacity-50' : ''}">
          <div class="flex items-center gap-3 flex-1">
            <input type="checkbox" 
                   ${item.shopping_bought ? 'checked' : ''} 
                   onchange="toggleShopping(appState.allData.find(d => d.__backendId === '${item.__backendId}'))"
                   class="w-5 h-5 cursor-pointer">
            <span class="${item.shopping_bought ? 'line-through text-gray-500' : ''}">${item.shopping_item}</span>
          </div>
          <button onclick="deleteShoppingItem(appState.allData.find(d => d.__backendId === '${item.__backendId}'))" 
                  class="text-gray-400 hover:text-red-500 text-sm ml-3">✕</button>
        </div>
      `).join('') || '<p class="text-gray-500 text-sm">Liste vide</p>';
    }
    
    // CALCULATORS
    function calculateCaloriesBurned(e) {
      e.preventDefault();
      
      const activity = document.getElementById('activityType').value;
      const duration = parseInt(document.getElementById('activityDuration').value);
      const weight = parseInt(document.getElementById('activityWeight').value);
      
      const metValues = {
        // Musculation & Fitness
        'musculation': 6,
        'musculation-light': 3.5,
        'crossfit': 8.5,
        'hiit': 10,
        'circuit-training': 8,
        'body-pump': 7,
        'trx': 7,
        'kettlebell': 7.5,
        
        // Course & Cardio
        'course': 9.5,
        'course-rapide': 12,
        'sprint': 14,
        'marche': 4.5,
        'marche-normale': 3.5,
        'tapis': 9,
        'trail': 10,
        'escaliers': 8,
        
        // Vélo & Cyclisme
        'velo': 7.5,
        'velo-intense': 10,
        'vtt': 8.5,
        'spinning': 9,
        'velo-appartement': 7,
        
        // Sports aquatiques
        'natation': 7,
        'natation-intense': 10,
        'aquagym': 5,
        'aquabike': 7,
        'water-polo': 10,
        'plongee': 7,
        'surf': 6,
        'paddle': 6,
        
        // Sports collectifs
        'basket': 8,
        'basket-training': 6.5,
        'football': 9,
        'football-training': 7,
        'rugby': 10,
        'handball': 8,
        'volley': 6,
        'tennis': 7.5,
        'tennis-table': 4.5,
        'badminton': 7,
        'squash': 9,
        
        // Sports de combat
        'boxe': 9,
        'boxe-sac': 7.5,
        'mma': 10,
        'judo': 8,
        'karate': 8,
        'taekwondo': 8,
        'muay-thai': 9,
        'krav-maga': 8.5,
        'catch': 9,
        
        // Yoga & Souplesse
        'yoga': 3,
        'yoga-power': 4.5,
        'pilates': 3.5,
        'stretching': 2.5,
        'tai-chi': 3,
        
        // Danse & Rythme
        'zumba': 7,
        'danse': 5.5,
        'danse-intense': 8,
        'salsa': 5,
        'pole-dance': 6,
        'step': 7.5,
        
        // Sports outdoor
        'escalade': 8,
        'randonnee': 6,
        'ski': 7,
        'ski-fond': 9,
        'snowboard': 7,
        'raquettes': 6.5,
        'kayak': 5,
        'aviron': 7,
        
        // Autres sports
        'golf': 4.5,
        'equitation': 5.5,
        'roller': 7,
        'skateboard': 5,
        'trampoline': 4.5,
        'rameur': 7,
        'elliptique': 6.5,
        'corde-sauter': 11,
        'jardinage': 4.5,
        'menage': 3.5
      };
      
      const met = metValues[activity] || 5;
      const caloriesBurned = Math.round((met * weight * duration) / 60);
      
      const resultElem = document.getElementById('caloriesBurnedResult');
      if (resultElem) {
        resultElem.innerHTML = `
          <div class="stat-card">
            <p class="text-sm text-gray-400 mb-2">CALORIES BRÛLÉES</p>
            <p class="stat-number">${caloriesBurned}</p>
            <p class="text-xs text-gray-400">KCAL</p>
          </div>
        `;
      }
    }
    
    function calculateMealCalories(e) {
      e.preventDefault();
      
      const protein = parseInt(document.getElementById('calcProtein').value);
      const carbs = parseInt(document.getElementById('calcCarbs').value);
      const fats = parseInt(document.getElementById('calcFats').value);
      
      const totalCalories = (protein * 4) + (carbs * 4) + (fats * 9);
      
      const resultElem = document.getElementById('mealCaloriesResult');
      if (resultElem) {
        resultElem.innerHTML = `
          <div class="stat-card">
            <p class="text-sm text-gray-400 mb-2">TOTAL</p>
            <p class="stat-number">${totalCalories}</p>
            <p class="text-xs text-gray-400">KCAL</p>
            <div class="grid grid-cols-3 gap-2 mt-4 text-xs">
              <div>
                <p class="text-gray-400">Protéines</p>
                <p class="font-bold text-red-500">${protein * 4} kcal</p>
              </div>
              <div>
                <p class="text-gray-400">Glucides</p>
                <p class="font-bold text-red-500">${carbs * 4} kcal</p>
              </div>
              <div>
                <p class="text-gray-400">Lipides</p>
                <p class="font-bold text-red-500">${fats * 9} kcal</p>
              </div>
            </div>
          </div>
        `;
      }
    }
    
    function calculateOneRM(e) {
      e.preventDefault();
      
      const weight = parseFloat(document.getElementById('rmWeight').value);
      const reps = parseInt(document.getElementById('rmReps').value);
      
      // Formule d'Epley
      const oneRM = Math.round(weight * (1 + (reps / 30)) * 2) / 2;
      
      const percentages = [
        { pct: 95, reps: '1-2', label: 'Force max' },
        { pct: 90, reps: '2-4', label: 'Force' },
        { pct: 85, reps: '4-6', label: 'Force-Hypertrophie' },
        { pct: 80, reps: '6-8', label: 'Hypertrophie' },
        { pct: 75, reps: '8-10', label: 'Hypertrophie' },
        { pct: 70, reps: '10-12', label: 'Endurance musculaire' }
      ];
      
      const resultElem = document.getElementById('oneRMResult');
      if (resultElem) {
        resultElem.innerHTML = `
          <div class="stat-card mb-4">
            <p class="text-sm text-gray-400 mb-2">VOTRE 1RM ESTIMÉ</p>
            <p class="stat-number">${oneRM}</p>
            <p class="text-xs text-gray-400">KG</p>
          </div>
          <div class="text-left space-y-2">
            <p class="font-bold text-red-500 mb-3">Charges d'entraînement:</p>
            ${percentages.map(p => `
              <div class="bg-black p-3 rounded-lg">
                <div class="flex justify-between items-center">
                  <span class="font-bold">${Math.round(oneRM * (p.pct / 100) * 2) / 2}kg</span>
                  <span class="text-sm text-gray-400">${p.pct}% • ${p.reps} reps</span>
                </div>
                <p class="text-xs text-gray-500 mt-1">${p.label}</p>
              </div>
            `).join('')}
          </div>
        `;
      }
    }
    
    // I.A COACH
    function askIA(e) {
      e.preventDefault();
      
      const btn = document.getElementById('iaBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const question = document.getElementById('iaQuestion').value;
      
      setTimeout(() => {
        const responses = [
          `<div class="bg-black p-6 rounded-xl">
            <h4 class="font-bold text-red-500 mb-3">💡 RÉPONSE DE L'I.A COACH</h4>
            <p class="text-gray-300 mb-4">Excellente question sur "${question}"!</p>
            <p class="text-gray-300 mb-3">Voici mes recommandations basées sur vos données:</p>
            <ul class="space-y-2 text-sm text-gray-300">
              <li>✓ Concentrez-vous sur la progression progressive (+2-5% par semaine)</li>
              <li>✓ Assurez-vous de dormir 7-9h par nuit pour optimiser la récupération</li>
              <li>✓ Maintenez un apport protéique de 1.8-2.2g/kg de poids corporel</li>
              <li>✓ Variez vos exercices toutes les 4-6 semaines pour éviter la stagnation</li>
              <li>✓ Écoutez votre corps et prenez des jours de repos si nécessaire</li>
            </ul>
            <p class="text-gray-300 mt-4">Continue comme ça, tu es sur la bonne voie! 💪🔥</p>
          </div>`,
          `<div class="bg-black p-6 rounded-xl">
            <h4 class="font-bold text-red-500 mb-3">💡 ANALYSE DE L'I.A</h4>
            <p class="text-gray-300 mb-4">Concernant "${question}", voici mon analyse:</p>
            <div class="space-y-3">
              <div class="bg-green-900 bg-opacity-20 border-l-4 border-green-500 p-3 rounded">
                <p class="font-bold text-green-400 mb-1">Points forts</p>
                <p class="text-sm text-gray-300">Ta régularité dans les entraînements est excellente. Continue!</p>
              </div>
              <div class="bg-yellow-900 bg-opacity-20 border-l-4 border-yellow-500 p-3 rounded">
                <p class="font-bold text-yellow-400 mb-1">Points d'amélioration</p>
                <p class="text-sm text-gray-300">Pense à augmenter légèrement ton apport calorique pour soutenir ta progression.</p>
              </div>
              <div class="bg-blue-900 bg-opacity-20 border-l-4 border-blue-500 p-3 rounded">
                <p class="font-bold text-blue-400 mb-1">Recommandation</p>
                <p class="text-sm text-gray-300">Intègre plus d'exercices de mobilité et d'étirements post-entraînement.</p>
              </div>
            </div>
          </div>`
        ];
        
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
        
        const resultElem = document.getElementById('iaResponse');
        if (resultElem) {
          resultElem.innerHTML = randomResponse;
        }
        
        btn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
        
        showToast("🤖 Réponse de l'I.A reçue!");
      }, 2000);
    }
    
    function generateAutoAnalysis() {
      const analysisElem = document.getElementById('iaAutoAnalysis');
      if (!analysisElem) return;
      
      const workouts = appState.allData.filter(d => d.type === 'exercise').length;
      const goals = appState.allData.filter(d => d.type === 'goal' && !d.goal_completed).length;
      const completedGoals = appState.allData.filter(d => d.type === 'goal' && d.goal_completed).length;
      
      analysisElem.innerHTML = `
        <div class="bg-black p-4 rounded-xl mb-3">
          <p class="font-bold text-red-500 mb-2">📊 STATISTIQUES GLOBALES</p>
          <p class="text-sm text-gray-300">• ${workouts} exercices enregistrés</p>
          <p class="text-sm text-gray-300">• ${goals} objectifs en cours</p>
          <p class="text-sm text-gray-300">• ${completedGoals} objectifs atteints 🎉</p>
        </div>
        
        <div class="bg-black p-4 rounded-xl mb-3">
          <p class="font-bold text-green-500 mb-2">✅ POINTS POSITIFS</p>
          <p class="text-sm text-gray-300">Excellente assiduité dans le suivi de tes performances!</p>
        </div>
        
        <div class="bg-black p-4 rounded-xl">
          <p class="font-bold text-yellow-500 mb-2">💡 RECOMMANDATIONS</p>
          <p class="text-sm text-gray-300">Continue de tracker tes repas pour optimiser tes résultats</p>
        </div>
      `;
      
      showToast("📊 Analyse mise à jour!");
    }
    
    // HEALTH
    async function addHealthData(e) {
      e.preventDefault();
      
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite atteinte");
        return;
      }
      
      const btn = document.getElementById('addHealthBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const result = await window.dataSdk.create({
        id: `health_${Date.now()}`,
        type: 'health',
        health_date: document.getElementById('healthDate').value,
        health_sleep: parseFloat(document.getElementById('healthSleep').value),
        health_fatigue: parseInt(document.getElementById('healthFatigue').value),
        health_water: parseFloat(document.getElementById('healthWater').value),
        health_pain: document.getElementById('healthPain').value
      });
      
      if (result.isOk) {
        showToast("�� Données santé ajoutées!");
        document.getElementById('healthForm').reset();
        document.getElementById('healthDate').value = new Date().toISOString().split('T')[0];
      }
      
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
    }
    
    function updateHealthStats() {
      const healthData = appState.allData.filter(d => d.type === 'health');
      const last7Days = healthData.slice(-7);
      
      if (last7Days.length === 0) {
        document.getElementById('avgSleep').textContent = '-';
        document.getElementById('avgWater').textContent = '-';
        document.getElementById('avgFatigue').textContent = '-';
        return;
      }
      
      const avgSleep = (last7Days.reduce((sum, d) => sum + (d.health_sleep || 0), 0) / last7Days.length).toFixed(1);
      const avgWater = (last7Days.reduce((sum, d) => sum + (d.health_water || 0), 0) / last7Days.length).toFixed(1);
      const avgFatigue = (last7Days.reduce((sum, d) => sum + (d.health_fatigue || 0), 0) / last7Days.length).toFixed(1);
      
      document.getElementById('avgSleep').textContent = avgSleep;
      document.getElementById('avgWater').textContent = avgWater;
      document.getElementById('avgFatigue').textContent = 11 - avgFatigue; // Inverse for better display
      
      // Pain history
      const painHistoryElem = document.getElementById('painHistory');
      if (painHistoryElem) {
        const withPain = healthData.filter(d => d.health_pain && d.health_pain.trim() !== '');
        
        painHistoryElem.innerHTML = withPain.slice(-10).reverse().map(d => `
          <div class="bg-black p-3 rounded-lg">
            <p class="text-sm font-semibold">${new Date(d.health_date).toLocaleDateString('fr-FR')}</p>
            <p class="text-sm text-gray-300 mt-1">${d.health_pain}</p>
          </div>
        `).join('') || '<p class="text-gray-500 text-sm">Aucune douleur signalée 🎉</p>';
      }
    }
    
    function updateHealthChart() {
      const healthData = appState.allData
        .filter(d => d.type === 'health')
        .sort((a, b) => new Date(a.health_date) - new Date(b.health_date))
        .slice(-14);
      
      const canvas = document.getElementById('healthCanvas');
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      const parent = canvas.parentElement;
      canvas.width = parent.clientWidth;
      canvas.height = 300;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      if (healthData.length === 0) {
        ctx.fillStyle = '#666';
        ctx.font = '16px Roboto Condensed';
        ctx.textAlign = 'center';
        ctx.fillText('Aucune donnée santé', canvas.width / 2, canvas.height / 2);
        return;
      }
      
      drawLineChart(ctx, canvas.width, canvas.height, healthData, 'health_sleep', 'health_date', 'h', '#16a34a');
    }
    
    // NOTES
    async function addNote(e) {
      e.preventDefault();
      
      if (appState.allData.length >= 999) {
        showToast("⚠️ Limite atteinte");
        return;
      }
      
      const btn = document.getElementById('addNoteBtn');
      const btnText = btn.querySelector('.btn-text');
      const spinner = btn.querySelector('.loading-spinner');
      
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'inline-block';
      
      const result = await window.dataSdk.create({
        id: `note_${Date.now()}`,
        type: 'note',
        note_date: document.getElementById('noteDate').value,
        note_content: document.getElementById('noteContent').value,
        created_at: new Date().toISOString()
      });
      
      if (result.isOk) {
        showToast("✅ Note enregistrée!");
        document.getElementById('noteForm').reset();
        document.getElementById('noteDate').value = new Date().toISOString().split('T')[0];
      }
      
      btn.disabled = false;
      btnText.style.display = 'inline';
      spinner.style.display = 'none';
    }
    
    async function deleteNote(record) {
      const result = await window.dataSdk.delete(record);
      if (result.isOk) {
        showToast("✅ Note supprimée");
      }
    }
    
    function updateNotesList() {
      const notes = appState.allData
        .filter(d => d.type === 'note')
        .sort((a, b) => new Date(b.note_date) - new Date(a.note_date));
      
      const listElem = document.getElementById('notesList');
      if (!listElem) return;
      
      listElem.innerHTML = notes.map(note => `
        <div class="bg-black p-4 rounded-xl">
          <div class="flex justify-between items-start mb-3">
            <span class="text-sm text-red-500 font-bold">${new Date(note.note_date).toLocaleDateString('fr-FR')}</span>
            <button onclick="deleteNote(appState.allData.find(d => d.__backendId === '${note.__backendId}'))" 
                    class="text-gray-400 hover:text-red-500">✕</button>
          </div>
          <p class="text-sm text-gray-300 whitespace-pre-wrap">${note.note_content}</p>
        </div>
      `).join('') || '<p class="text-gray-500">Aucune note</p>';
    }
    
    // EXPORT & SHARE
    function showExportModal() {
      const modalHtml = `
        <div class="modal-overlay" onclick="if(event.target === this) this.remove()">
          <div class="modal-content">
            <h3 class="text-3xl mb-4 text-red-500">📤 EXPORTER MES DONNÉES</h3>
            <p class="text-gray-300 mb-6">Téléchargez toutes vos données d'entraînement, nutrition et progression en format JSON.</p>
            
            <button onclick="exportData()" class="btn-primary w-full mb-3">📥 TÉLÉCHARGER MES DONNÉES (JSON)</button>
            <button onclick="exportStats()" class="btn-secondary w-full mb-3">📊 TÉLÉCHARGER MES STATS (TXT)</button>
            
            <div class="bg-yellow-900 bg-opacity-20 border-2 border-yellow-600 p-4 rounded-xl mb-4">
              <p class="text-yellow-500 font-bold mb-2">💡 CONSEIL</p>
              <p class="text-sm text-gray-300">Sauvegardez régulièrement vos données pour ne jamais perdre votre progression!</p>
            </div>
            
            <button onclick="this.closest('.modal-overlay').remove()" class="btn-secondary w-full">FERMER</button>
          </div>
        </div>
      `;
      document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
    
    function exportData() {
      const dataStr = JSON.stringify(appState.allData, null, 2);
      const blob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `musculation-pro-data-${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
      showToast("✅ Données exportées!");
    }
    
    function exportStats() {
      let statsText = "=== EBOOK MUSCULATION PRO - MES STATISTIQUES ===\n\n";
      
      const profile = appState.allData.find(d => d.type === 'profile');
      if (profile) {
        statsText += `PROFIL:\n`;
        statsText += `- Âge: ${profile.age} ans\n`;
        statsText += `- Taille: ${profile.height} cm\n`;
        statsText += `- Poids: ${profile.weight} kg\n`;
        statsText += `- Exercice préféré: ${profile.favorite_exercise}\n\n`;
      }
      
      const exercises = appState.allData.filter(d => d.type === 'exercise');
      statsText += `ENTRAÎNEMENT:\n`;
      statsText += `- Total d'exercices: ${exercises.length}\n\n`;
      
      const goals = appState.allData.filter(d => d.type === 'goal');
      const completedGoals = goals.filter(g => g.goal_completed);
      statsText += `OBJECTIFS:\n`;
      statsText += `- Objectifs actifs: ${goals.length - completedGoals.length}\n`;
      statsText += `- Objectifs atteints: ${completedGoals.length}\n\n`;
      
      const meals = appState.allData.filter(d => d.type === 'meal');
      statsText += `NUTRITION:\n`;
      statsText += `- Repas trackés: ${meals.length}\n\n`;
      
      statsText += `Exporté le ${new Date().toLocaleString('fr-FR')}\n`;
      
      const blob = new Blob([statsText], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `musculation-pro-stats-${new Date().toISOString().split('T')[0]}.txt`;
      a.click();
      URL.revokeObjectURL(url);
      showToast("✅ Stats exportées!");
    }
    
    function showDownloadModal() {
      const modalHtml = `
        <div class="modal-overlay" onclick="if(event.target === this) this.remove()">
          <div class="modal-content">
            <h3 class="text-3xl mb-4 text-red-500">📱 INSTALLER L'APPLICATION</h3>
            <p class="text-gray-300 mb-6">Pour une meilleure expérience, ajoutez cette app à votre écran d'accueil!</p>
            
            <div class="space-y-4 mb-6">
              <div class="bg-black p-4 rounded-xl">
                <p class="font-bold mb-2">📱 iPhone/iPad (Safari)</p>
                <ol class="text-sm text-gray-300 space-y-1">
                  <li>1. Appuyez sur le bouton Partager <span class="inline-block">📤</span></li>
                  <li>2. Sélectionnez "Sur l'écran d'accueil"</li>
                  <li>3. Appuyez sur "Ajouter"</li>
                </ol>
              </div>
              
              <div class="bg-black p-4 rounded-xl">
                <p class="font-bold mb-2">🤖 Android (Chrome)</p>
                <ol class="text-sm text-gray-300 space-y-1">
                  <li>1. Appuyez sur le menu ⋮ (3 points)</li>
                  <li>2. Sélectionnez "Ajouter à l'écran d'accueil"</li>
                  <li>3. Appuyez sur "Ajouter"</li>
                </ol>
              </div>
              
              <div class="bg-black p-4 rounded-xl">
                <p class="font-bold mb-2">��� Bureau (Chrome/Edge)</p>
                <ol class="text-sm text-gray-300 space-y-1">
                  <li>1. Cliquez sur l'icône d'installation dans la barre d'adresse</li>
                  <li>2. Cliquez sur "Installer"</li>
                </ol>
              </div>
            </div>
            
            <button onclick="this.closest('.modal-overlay').remove()" class="btn-primary w-full">COMPRIS!</button>
          </div>
        </div>
      `;
      document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
    
    // CHART DRAWING FUNCTIONS
    function drawLineChart(ctx, width, height, data, valueKey, dateKey, unit, color) {
      if (data.length === 0) return;
      
      const padding = 50;
      const chartWidth = width - padding * 2;
      const chartHeight = height - padding * 2;
      
      const values = data.map(d => d[valueKey] || 0);
      const minVal = Math.min(...values) * 0.95;
      const maxVal = Math.max(...values) * 1.05;
      const range = maxVal - minVal || 1;
      
      // Grid
      ctx.strokeStyle = '#333';
      ctx.lineWidth = 1;
      for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
        
        const val = maxVal - (range / 5) * i;
        ctx.fillStyle = '#666';
        ctx.font = '12px Roboto Condensed';
        ctx.textAlign = 'right';
        ctx.fillText(val.toFixed(1), padding - 10, y + 4);
      }
      
      // Line
      ctx.strokeStyle = color;
      ctx.lineWidth = 3;
      ctx.beginPath();
      
      data.forEach((d, i) => {
        const x = padding + (chartWidth / (data.length - 1 || 1)) * i;
        const y = padding + chartHeight - ((d[valueKey] - minVal) / range) * chartHeight;
        
        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      
      ctx.stroke();
      
      // Points
      data.forEach((d, i) => {
        const x = padding + (chartWidth / (data.length - 1 || 1)) * i;
        const y = padding + chartHeight - ((d[valueKey] - minVal) / range) * chartHeight;
        
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
      });
      
      // Dates
      ctx.fillStyle = '#666';
      ctx.font = '10px Roboto Condensed';
      ctx.textAlign = 'center';
      data.forEach((d, i) => {
        if (i % Math.ceil(data.length / 5) === 0) {
          const x = padding + (chartWidth / (data.length - 1 || 1)) * i;
          const date = new Date(d[dateKey]);
          ctx.fillText(`${date.getDate()}/${date.getMonth() + 1}`, x, height - padding + 20);
        }
      });
    }
    
    function drawMultiLineChart(ctx, width, height, data, valueKey, dateKey, typeKey, unit) {
      const types = [...new Set(data.map(d => d[typeKey]))];
      const colors = ['#dc2626', '#16a34a', '#2563eb', '#f59e0b'];
      
      const padding = 50;
      const chartWidth = width - padding * 2;
      const chartHeight = height - padding * 2;
      
      const allValues = data.map(d => d[valueKey] || 0);
      const minVal = Math.min(...allValues) * 0.95;
      const maxVal = Math.max(...allValues) * 1.05;
      const range = maxVal - minVal || 1;
      
      // Grid
      ctx.strokeStyle = '#333';
      ctx.lineWidth = 1;
      for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
      }
      
      // Draw line for each type
      types.forEach((type, idx) => {
        const typeData = data.filter(d => d[typeKey] === type).sort((a, b) => new Date(a[dateKey]) - new Date(b[dateKey]));
        const color = colors[idx % colors.length];
        
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        typeData.forEach((d, i) => {
          const totalDates = data.map(item => item[dateKey]).filter((v, i, a) => a.indexOf(v) === i).sort();
          const dateIndex = totalDates.indexOf(d[dateKey]);
          const x = padding + (chartWidth / (totalDates.length - 1 || 1)) * dateIndex;
          const y = padding + chartHeight - ((d[valueKey] - minVal) / range) * chartHeight;
          
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        });
        
        ctx.stroke();
      });
    }
    
    function drawBarChart(ctx, width, height, data, valueKey, dateKey, unit) {
      if (data.length === 0) return;
      
      const padding = 50;
      const chartWidth = width - padding * 2;
      const chartHeight = height - padding * 2;
      
      const values = data.map(d => d[valueKey] || 0);
      const maxVal = Math.max(...values) * 1.1 || 100;
      
      // Grid
      ctx.strokeStyle = '#333';
      ctx.lineWidth = 1;
      for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
      }
      
      // Bars
      const barWidth = chartWidth / data.length - 10;
      data.forEach((d, i) => {
        const x = padding + (chartWidth / data.length) * i + 5;
        const barHeight = (d[valueKey] / maxVal) * chartHeight;
        const y = padding + chartHeight - barHeight;
        
        const gradient = ctx.createLinearGradient(x, y, x, y + barHeight);
        gradient.addColorStop(0, '#dc2626');
        gradient.addColorStop(1, '#991b1b');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, barWidth, barHeight);
        
        // Date label
        ctx.fillStyle = '#666';
        ctx.font = '10px Roboto Condensed';
        ctx.textAlign = 'center';
        const date = new Date(d[dateKey]);
        ctx.fillText(`${date.getDate()}/${date.getMonth() + 1}`, x + barWidth / 2, height - padding + 20);
      });
    }
    
    // TOAST NOTIFICATION
    function showToast(message) {
      const existingToast = document.querySelector('.toast');
      if (existingToast) {
        existingToast.remove();
      }
      
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.textContent = message;
      document.body.appendChild(toast);
      
      setTimeout(() => {
        toast.remove();
      }, 3000);
    }
    
    // LOGO MODAL
    function showLogoModal() {
      const modal = document.createElement('div');
      modal.className = 'logo-modal';
      modal.innerHTML = '<img src="https://i.imgur.com/wlyusJ0.png" alt="Logo Musculation Pro" loading="lazy" onerror="console.error(\'Image failed to load:\', this.src); this.style.background=\'linear-gradient(135deg, #dc2626, #991b1b)\'; this.style.borderRadius=\'20px\'; this.alt=\'Logo unavailable\';">';
      modal.onclick = () => modal.remove();
      document.body.appendChild(modal);
    }
    
    // UPDATE ALL VIEWS
    function updateAllViews() {
      checkAccess();
      
      if (appState.userPaid) {
        updateWeightChart();
        updateMeasurementChart();
        updatePhotoGallery();
        updateGoals();
        updateExerciseChart();
        updateCustomPrograms();
        updateNutritionStats();
        updateNutritionChart();
        updateShoppingList();
        updateHealthStats();
        updateHealthChart();
        updateNotesList();
        
        // Load profile data if exists
        const profile = appState.allData.find(d => d.type === 'profile');
        if (profile) {
          if (document.getElementById('age')) document.getElementById('age').value = profile.age || '';
          if (document.getElementById('height')) document.getElementById('height').value = profile.height || '';
          if (document.getElementById('weight')) document.getElementById('weight').value = profile.weight || '';
          if (document.getElementById('favoriteExercise')) document.getElementById('favoriteExercise').value = profile.favorite_exercise || '';
          if (document.getElementById('email')) document.getElementById('email').value = profile.email || '';
        }
      }
    }
    
    // Initialize on load
    window.addEventListener('DOMContentLoaded', initializeApp);
  </script>
 <script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'9c6268f9f18ff4e7',t:'MTc2OTc5MTIxNS4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>
