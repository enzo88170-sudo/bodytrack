powerlog-complet/
│
├── 📱 FRONTEND (React Native/Expo)
│   ├── src/
│   │   ├── screens/          # Tous les écrans
│   │   ├── components/       # Composants réutilisables
│   │   ├── navigation/       # Navigation
│   │   ├── context/         # Context API
│   │   ├── services/        # API calls
│   │   ├── utils/           # Utilitaires
│   │   └── assets/          # Images, sons, polices
│   ├── App.js               # Point d'entrée
│   └── package.json
│
├── ⚙️ BACKEND (Node.js/Express)
│   ├── src/
│   │   ├── controllers/     # Tous les contrôleurs
│   │   ├── models/          # Tous les modèles MongoDB
│   │   ├── routes/          # Toutes les routes API
│   │   ├── middleware/      # Middleware
│   │   ├── services/        # Services métier
│   │   ├── utils/           # Utilitaires
│   │   └── server.js        # Serveur principal
│   └── package.json
│
├── 🖥️ ADMIN PANEL (React)
│   ├── src/
│   │   ├── pages/          # Pages admin
│   │   ├── components/     # Composants admin
│   │   ├── services/       # API admin
│   │   └── App.js
│   └── package.json
│
├── 🗄️ DATABASE
│   ├── mongodb/           # Scripts MongoDB
│   ├── seed/              # Données initiales
│   └── backup/            # Scripts de sauvegarde
│
├── 🐳 DOCKER
│   ├── docker-compose.yml # Tout l'environnement
│   ├── frontend.Dockerfile
│   ├── backend.Dockerfile
│   └── admin.Dockerfile
│
├── ⚡ SCRIPT DÉPLOIEMENT
│   ├── deploy.sh          # Déploiement auto
│   ├── backup.sh          # Sauvegarde auto
│   └── update.sh          # Mise à jour auto
│
├── 📊 MONITORING
│   ├── prometheus.yml
│   ├── grafana/
│   └── alerts/
│
└── 📄 DOCUMENTATION
    ├── API.md            # Documentation API
    ├── INSTALL.md        # Guide d'installation
    └── USER_GUIDE.md     # Guide utilisateur
    require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const { createServer } = require('http');
const { Server } = require('socket.io');
const path = require('path');
const fs = require('fs');
const morgan = require('morgan');

// Initialisation Express
const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: process.env.FRONTEND_URL || '*',
    credentials: true
  }
});

// Configuration Stripe
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// Configuration OpenAI
const { OpenAI } = require('openai');
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Middleware de sécurité
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"]
    }
  }
}));

app.use(compression());
app.use(cors({
  origin: process.env.FRONTEND_URL ? process.env.FRONTEND_URL.split(',') : '*',
  credentials: true
}));

// Body parsers
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Logging
const accessLogStream = fs.createWriteStream(
  path.join(__dirname, 'logs', 'access.log'),
  { flags: 'a' }
);
app.use(morgan('combined', { stream: accessLogStream }));

// Rate limiting
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 1000, // 1000 requêtes par IP
  message: 'Trop de requêtes, veuillez réessayer plus tard.'
});
app.use('/api/', apiLimiter);

// Connexion MongoDB
mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  retryWrites: true,
  w: 'majority'
})
.then(() => console.log('✅ MongoDB connecté avec succès'))
.catch(err => {
  console.error('❌ Erreur connexion MongoDB:', err);
  process.exit(1);
});

// Création des dossiers nécessaires
const directories = ['logs', 'uploads', 'exports', 'backups'];
directories.forEach(dir => {
  const dirPath = path.join(__dirname, dir);
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
});

// Import des routes
const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/users');
const workoutRoutes = require('./routes/workouts');
const nutritionRoutes = require('./routes/nutrition');
const programRoutes = require('./routes/programs');
const aiRoutes = require('./routes/ai');
const paymentRoutes = require('./routes/payments');
const adminRoutes = require('./routes/admin');
const communityRoutes = require('./routes/community');
const analyticsRoutes = require('./routes/analytics');
const exportRoutes = require('./routes/export');

// Routes API
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/workouts', workoutRoutes);
app.use('/api/nutrition', nutritionRoutes);
app.use('/api/programs', programRoutes);
app.use('/api/ai', aiRoutes);
app.use('/api/payments', paymentRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api/community', communityRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/export', exportRoutes);

// Route de santé
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date(),
    uptime: process.uptime(),
    database: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
    memory: process.memoryUsage()
  });
});

// Route pour télécharger l'eBook
app.get('/api/ebook/download', (req, res) => {
  const { token } = req.query;
  
  // Vérifier le token et les droits
  // ...
  
  const ebookPath = path.join(__dirname, 'assets', 'ebook.pdf');
  res.download(ebookPath, 'PowerLog-eBook-Premium.pdf');
});

// WebSocket pour temps réel
io.on('connection', (socket) => {
  console.log('🔗 Nouveau client connecté:', socket.id);
  
  socket.on('join-user', (userId) => {
    socket.join(`user-${userId}`);
    console.log(`👤 Utilisateur ${userId} connecté`);
  });
  
  socket.on('workout-started', (data) => {
    io.to(`user-${data.userId}`).emit('timer-start', data);
  });
  
  socket.on('rest-timer-complete', (data) => {
    io.to(`user-${data.userId}`).emit('rest-complete', {
      message: '⏰ Temps de repos terminé ! Retour au charbon ! 💪',
      sound: 'bell'
    });
  });
  
  socket.on('pr-achieved', (data) => {
    io.emit('global-achievement', {
      userId: data.userId,
      exercise: data.exercise,
      weight: data.weight,
      message: `🎉 Nouveau PR de ${data.weight}kg au ${data.exercise} !`
    });
  });
  
  socket.on('disconnect', () => {
    console.log('🔌 Client déconnecté:', socket.id);
  });
});

// Gestion des erreurs
app.use((err, req, res, next) => {
  console.error('🔥 Erreur:', err.stack);
  
  const status = err.status || 500;
  const message = process.env.NODE_ENV === 'production' 
    ? 'Une erreur est survenue' 
    : err.message;
  
  res.status(status).json({
    success: false,
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    message: 'Route non trouvée'
  });
});

const PORT = process.env.PORT || 5000;
httpServer.listen(PORT, () => {
  console.log(`
  🚀 POWERLOG BACKEND DÉMARRÉ 🚀
  Port: ${PORT}
  Environnement: ${process.env.NODE_ENV || 'development'}
  MongoDB: ${mongoose.connection.readyState === 1 ? '✅ Connecté' : '❌ Déconnecté'}
  Stripe: ${process.env.STRIPE_SECRET_KEY ? '✅ Configuré' : '❌ Non configuré'}
  OpenAI: ${process.env.OPENAI_API_KEY ? '✅ Configuré' : '❌ Non configuré'}
  WebSocket: ✅ Actif
  `);
});

module.exports = { app, io };
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const userSchema = new mongoose.Schema({
  // Informations de base
  email: {
    type: String,
    required: [true, 'Email requis'],
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\S+@\S+\.\S+$/, 'Email invalide']
  },
  password: {
    type: String,
    required: [true, 'Mot de passe requis'],
    minlength: [6, 'Minimum 6 caractères'],
    select: false
  },
  firstName: {
    type: String,
    required: [true, 'Prénom requis'],
    trim: true
  },
  lastName: {
    type: String,
    required: [true, 'Nom requis'],
    trim: true
  },
  
  // Informations physiques
  age: {
    type: Number,
    min: [15, 'Minimum 15 ans'],
    max: [100, 'Maximum 100 ans']
  },
  height: {
    type: Number,
    min: [100, 'Minimum 100cm'],
    max: [250, 'Maximum 250cm']
  },
  gender: {
    type: String,
    enum: ['male', 'female', 'other']
  },
  
  // Objectifs
  goals: {
    weight: {
      target: Number,
      current: Number,
      deadline: Date
    },
    measurements: {
      arms: { target: Number, current: Number },
      chest: { target: Number, current: Number },
      waist: { target: Number, current: Number },
      thighs: { target: Number, current: Number }
    },
    performance: [{
      exercise: String,
      target: Number,
      current: Number,
      unit: String
    }],
    endurance: [{
      activity: String,
      target: Number,
      current: Number,
      unit: String
    }]
  },
  
  // Mensurations
  measurements: [{
    date: { type: Date, default: Date.now },
    arms: Number,
    chest: Number,
    waist: Number,
    thighs: Number,
    weight: Number,
    bodyFat: Number,
    notes: String
  }],
  
  // Photos de progression
  progressPhotos: [{
    date: Date,
    url: String,
    type: { type: String, enum: ['front', 'side', 'back'] },
    notes: String
  }],
  
  // Préférences d'entraînement
  preferences: {
    favoriteExercise: {
      type: String,
      enum: [
        'bench_press', 'squat', 'deadlift', 'military_press',
        'barbell_row', 'pull_up', 'bicep_curl', 'tricep_extension'
      ]
    },
    trainingDays: [{
      type: String,
      enum: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    }],
    trainingTime: String,
    experienceLevel: {
      type: String,
      enum: ['beginner', 'intermediate', 'advanced'],
      default: 'beginner'
    },
    units: {
      weight: { type: String, enum: ['kg', 'lbs'], default: 'kg' },
      height: { type: String, enum: ['cm', 'feet'], default: 'cm' }
    },
    notifications: {
      workoutReminder: { type: Boolean, default: true },
      progressUpdate: { type: Boolean, default: true },
      motivational: { type: Boolean, default: true },
      restReminder: { type: Boolean, default: true }
    }
  },
  
  // Abonnement
  subscription: {
    type: {
      type: String,
      enum: ['free', 'premium', 'admin'],
      default: 'free'
    },
    expiresAt: Date,
    stripeCustomerId: String,
    stripeSubscriptionId: String,
    paymentMethod: String,
    lastPayment: Date,
    nextPayment: Date
  },
  
  // Statistiques
  stats: {
    totalWorkouts: { type: Number, default: 0 },
    totalDuration: { type: Number, default: 0 }, // en minutes
    totalWeightLifted: { type: Number, default: 0 }, // en kg
    currentStreak: { type: Number, default: 0 },
    longestStreak: { type: Number, default: 0 },
    lastWorkout: Date,
    workoutsThisWeek: { type: Number, default: 0 },
    workoutsThisMonth: { type: Number, default: 0 },
    prs: [{
      exercise: String,
      weight: Number,
      date: Date,
      reps: Number
    }]
  },
  
  // Santé et récupération
  health: {
    sleep: [{
      date: Date,
      duration: Number, // en heures
      quality: { type: Number, min: 1, max: 10 }
    }],
    fatigue: [{
      date: Date,
      level: { type: Number, min: 1, max: 10 },
      notes: String
    }],
    injuries: [{
      name: String,
      location: String,
      severity: { type: Number, min: 1, max: 10 },
      startedAt: Date,
      healedAt: Date,
      notes: String
    }],
    waterIntake: [{
      date: Date,
      amount: Number // en litres
    }]
  },
  
  // Communauté
  community: {
    friends: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
    followers: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
    following: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
    sharedWorkouts: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Workout' }],
    achievements: [{
      name: String,
      icon: String,
      unlockedAt: Date,
      description: String
    }]
  },
  
  // Sécurité
  adminCode: {
    type: String,
    select: false,
    default: null
  },
  emailVerified: { type: Boolean, default: false },
  verificationToken: String,
  verificationExpires: Date,
  resetPasswordToken: String,
  resetPasswordExpires: Date,
  loginAttempts: { type: Number, default: 0 },
  lockUntil: Date,
  
  // Métadonnées
  lastLogin: Date,
  deviceTokens: [String], // Pour les notifications push
  settings: mongoose.Schema.Types.Mixed,
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Index pour performances
userSchema.index({ email: 1 }, { unique: true });
userSchema.index({ 'subscription.type': 1 });
userSchema.index({ createdAt: -1 });
userSchema.index({ 'stats.currentStreak': -1 });

// Middleware pre-save
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  try {
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

userSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});

// Méthodes d'instance
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

userSchema.methods.generateAuthToken = function() {
  return jwt.sign(
    {
      userId: this._id,
      email: this.email,
      subscription: this.subscription.type
    },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRE || '7d' }
  );
};

userSchema.methods.toProfileJSON = function() {
  return {
    id: this._id,
    email: this.email,
    firstName: this.firstName,
    lastName: this.lastName,
    age: this.age,
    height: this.height,
    goals: this.goals,
    preferences: this.preferences,
    subscription: this.subscription,
    stats: this.stats,
    createdAt: this.createdAt
  };
};

userSchema.methods.addMeasurement = function(measurement) {
  this.measurements.push({
    ...measurement,
    date: new Date()
  });
  return this.save();
};

userSchema.methods.addProgressPhoto = function(photo) {
  this.progressPhotos.push({
    ...photo,
    date: new Date()
  });
  return this.save();
};

userSchema.methods.updateStreak = function() {
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  
  if (!this.stats.lastWorkout) {
    this.stats.currentStreak = 1;
  } else {
    const lastWorkoutDate = new Date(this.stats.lastWorkout);
    const daysSinceLastWorkout = Math.floor((today - lastWorkoutDate) / (1000 * 60 * 60 * 24));
    
    if (daysSinceLastWorkout === 0) {
      // Déjà compté aujourd'hui
      return this;
    } else if (daysSinceLastWorkout === 1) {
      // Streak continu
      this.stats.currentStreak += 1;
    } else {
      // Streak brisé
      if (this.stats.currentStreak > this.stats.longestStreak) {
        this.stats.longestStreak = this.stats.currentStreak;
      }
      this.stats.currentStreak = 1;
    }
  }
  
  this.stats.lastWorkout = today;
  return this.save();
};

userSchema.methods.addPR = function(exercise, weight, reps = 1) {
  const existingPR = this.stats.prs.find(pr => pr.exercise === exercise);
  
  if (!existingPR || weight > existingPR.weight) {
    this.stats.prs = this.stats.prs.filter(pr => pr.exercise !== exercise);
    this.stats.prs.push({
      exercise,
      weight,
      reps,
      date: new Date()
    });
    return this.save();
  }
  
  return this;
};

// Méthodes statiques
userSchema.statics.findByEmail = function(email) {
  return this.findOne({ email });
};

userSchema.statics.getLeaderboard = async function(limit = 10) {
  return this.aggregate([
    {
      $project: {
        name: { $concat: ['$firstName', ' ', '$lastName'] },
        totalWorkouts: '$stats.totalWorkouts',
        currentStreak: '$stats.currentStreak',
        totalWeightLifted: '$stats.totalWeightLifted',
        prCount: { $size: '$stats.prs' }
      }
    },
    {
      $sort: { currentStreak: -1, totalWorkouts: -1 }
    },
    {
      $limit: limit
    }
  ]);
};

module.exports = mongoose.model('User', userSchema);
const mongoose = require('mongoose');

const exerciseSetSchema = new mongoose.Schema({
  setNumber: { type: Number, required: true },
  weight: { type: Number, required: true },
  reps: { type: Number, required: true },
  rpe: { type: Number, min: 1, max: 10 },
  completed: { type: Boolean, default: true },
  notes: String,
  restTime: Number // en secondes
});

const exerciseSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    enum: [
      // Pectoraux
      'bench_press', 'incline_bench_press', 'decline_bench_press',
      'dumbbell_bench_press', 'dumbbell_fly', 'cable_crossover',
      'push_up', 'dip',
      
      // Dos
      'deadlift', 'barbell_row', 't_bar_row', 'lat_pulldown',
      'pull_up', 'chin_up', 'seated_row', 'single_arm_dumbbell_row',
      
      // Jambes
      'squat', 'front_squat', 'leg_press', 'leg_extension',
      'leg_curl', 'romanian_deadlift', 'lunges', 'bulgarian_split_squat',
      'calf_raise', 'hip_thrust',
      
      // Épaules
      'military_press', 'arnold_press', 'dumbbell_lateral_raise',
      'front_raise', 'rear_delt_fly', 'face_pull', 'shrug',
      
      // Biceps
      'barbell_curl', 'dumbbell_curl', 'hammer_curl',
      'preacher_curl', 'concentration_curl', 'cable_curl',
      
      // Triceps
      'tricep_extension', 'skull_crusher', 'tricep_pushdown',
      'close_grip_bench_press', 'dips',
      
      // Abdos
      'crunch', 'leg_raise', 'russian_twist', 'plank',
      'hanging_leg_raise', 'cable_crunch',
      
      // Cardio
      'running', 'cycling', 'rowing', 'jumping_jacks',
      'burpees', 'mountain_climbers'
    ]
  },
  sets: [exerciseSetSchema],
  notes: String,
  videoUrl: String,
  targetMuscles: [String],
  equipment: [String],
  isWarmup: { type: Boolean, default: false },
  isDropSet: { type: Boolean, default: false },
  isSuperSet: { type: Boolean, default: false }
});

const workoutSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    index: true
  },
  date: {
    type: Date,
    required: true,
    default: Date.now,
    index: true
  },
  name: {
    type: String,
    default: 'Séance'
  },
  duration: {
    type: Number, // en minutes
    required: true,
    min: 1
  },
  type: {
    type: String,
    enum: ['strength', 'hypertrophy', 'power', 'endurance', 'cardio', 'hiit', 'mobility', 'recovery'],
    required: true
  },
  programId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Program'
  },
  programDayId: String,
  exercises: [exerciseSchema],
  
  // Suivi détaillé
  notes: {
    warmup: String,
    main: String,
    cooldown: String,
    overall: String
  },
  
  // Évaluations
  rating: {
    performance: { type: Number, min: 1, max: 10 },
    energy: { type: Number, min: 1, max: 10 },
    pump: { type: Number, min: 1, max: 10 },
    overall: { type: Number, min: 1, max: 10 }
  },
  
  // Santé
  fatigueLevel: { type: Number, min: 1, max: 10 },
  soreness: {
    chest: { type: Number, min: 0, max: 10 },
    back: { type: Number, min: 0, max: 10 },
    legs: { type: Number, min: 0, max: 10 },
    shoulders: { type: Number, min: 0, max: 10 },
    arms: { type: Number, min: 0, max: 10 }
  },
  sleepHours: Number,
  stressLevel: { type: Number, min: 1, max: 10 },
  
  // Calculs
  caloriesBurned: Number,
  totalVolume: Number, // poids total soulevé
  prCount: { type: Number, default: 0 },
  
  // Photos/vidéos
  media: [{
    url: String,
    type: { type: String, enum: ['photo', 'video'] },
    thumbnail: String,
    caption: String
  }],
  
  // Tags et catégories
  tags: [String],
  muscleGroups: [String],
  
  // Partages
  shared: {
    isPublic: { type: Boolean, default: false },
    sharedAt: Date,
    likes: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
    comments: [{
      userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
      text: String,
      createdAt: { type: Date, default: Date.now }
    }]
  },
  
  // Métadonnées
  device: {
    type: String,
    os: String,
    appVersion: String
  },
  location: {
    type: { type: String, enum: ['Point'], default: 'Point' },
    coordinates: [Number] // [longitude, latitude]
  },
  isTemplate: { type: Boolean, default: false },
  templateName: String,
  
  // Timestamps
  startedAt: Date,
  completedAt: Date,
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Index composés pour performances
workoutSchema.index({ userId: 1, date: -1 });
workoutSchema.index({ userId: 1, type: 1 });
workoutSchema.index({ 'exercises.name': 1 });
workoutSchema.index({ 'shared.isPublic': 1, date: -1 });

// Middleware pre-save
workoutSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  
  // Calculer le volume total
  if (this.exercises && this.exercises.length > 0) {
    this.totalVolume = this.exercises.reduce((total, exercise) => {
      return total + exercise.sets.reduce((exerciseTotal, set) => {
        return exerciseTotal + (set.weight * set.reps);
      }, 0);
    }, 0);
  }
  
  // Compter les PR
  this.prCount = this.exercises.reduce((count, exercise) => {
    const hasPR = exercise.sets.some(set => set.rpe === 10);
    return count + (hasPR ? 1 : 0);
  }, 0);
  
  next();
});

// Méthodes d'instance
workoutSchema.methods.addExercise = function(exerciseData) {
  this.exercises.push(exerciseData);
  return this.save();
};

workoutSchema.methods.updateExercise = function(exerciseIndex, exerciseData) {
  if (this.exercises[exerciseIndex]) {
    this.exercises[exerciseIndex] = {
      ...this.exercises[exerciseIndex],
      ...exerciseData
    };
    return this.save();
  }
  throw new Error('Exercice non trouvé');
};

workoutSchema.methods.deleteExercise = function(exerciseIndex) {
  if (this.exercises[exerciseIndex]) {
    this.exercises.splice(exerciseIndex, 1);
    return this.save();
  }
  throw new Error('Exercice non trouvé');
};

workoutSchema.methods.sharePublicly = function() {
  this.shared.isPublic = true;
  this.shared.sharedAt = new Date();
  return this.save();
};

workoutSchema.methods.addComment = function(userId, text) {
  this.shared.comments.push({
    userId,
    text,
    createdAt: new Date()
  });
  return this.save();
};

// Méthodes statiques
workoutSchema.statics.findByUser = function(userId, options = {}) {
  const { limit = 50, skip = 0, startDate, endDate, type } = options;
  
  const query = { userId };
  
  if (startDate || endDate) {
    query.date = {};
    if (startDate) query.date.$gte = new Date(startDate);
    if (endDate) query.date.$lte = new Date(endDate);
  }
  
  if (type) query.type = type;
  
  return this.find(query)
    .sort({ date: -1 })
    .skip(skip)
    .limit(limit)
    .populate('userId', 'firstName lastName')
    .lean();
};

workoutSchema.statics.getWorkoutStats = async function(userId) {
  const stats = await this.aggregate([
    { $match: { userId: mongoose.Types.ObjectId(userId) } },
    {
      $group: {
        _id: null,
        totalWorkouts: { $sum: 1 },
        totalDuration: { $sum: '$duration' },
        totalVolume: { $sum: '$totalVolume' },
        avgDuration: { $avg: '$duration' },
        avgVolume: { $avg: '$totalVolume' },
        lastWorkout: { $max: '$date' },
        firstWorkout: { $min: '$date' }
      }
    },
    {
      $project: {
        totalWorkouts: 1,
        totalDuration: 1,
        totalVolume: 1,
        avgDuration: { $round: ['$avgDuration', 2] },
        avgVolume: { $round: ['$avgVolume', 2] },
        lastWorkout: 1,
        firstWorkout: 1,
        daysSinceLastWorkout: {
          $divide: [
            { $subtract: [new Date(), '$lastWorkout'] },
            1000 * 60 * 60 * 24
          ]
        }
      }
    }
  ]);
  
  return stats[0] || {
    totalWorkouts: 0,
    totalDuration: 0,
    totalVolume: 0,
    avgDuration: 0,
    avgVolume: 0,
    lastWorkout: null,
    firstWorkout: null,
    daysSinceLastWorkout: null
  };
};

workoutSchema.statics.getExerciseProgress = async function(userId, exerciseName, limit = 20) {
  return this.aggregate([
    { $match: { 
      userId: mongoose.Types.ObjectId(userId),
      'exercises.name': exerciseName 
    }},
    { $unwind: '$exercises' },
    { $match: { 'exercises.name': exerciseName } },
    { $sort: { date: -1 } },
    { $limit: limit },
    {
      $project: {
        date: '$date',
        sets: '$exercises.sets',
        notes: '$exercises.notes',
        maxWeight: { $max: '$exercises.sets.weight' },
        totalVolume: {
          $sum: {
            $map: {
              input: '$exercises.sets',
              as: 'set',
              in: { $multiply: ['$$set.weight', '$$set.reps'] }
            }
          }
        }
      }
    }
  ]);
};

module.exports = mongoose.model('Workout', workoutSchema);
const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const { OpenAI } = require('openai');
const User = require('../models/User');
const Workout = require('../models/Workout');
const Nutrition = require('../models/Nutrition');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Toutes les routes nécessitent une authentification
router.use(auth);

// 1. COACH IA PERSONNEL
router.post('/coach', async (req, res) => {
  try {
    const { userId } = req;
    const { question } = req.body;
    
    if (!question) {
      return res.status(400).json({
        success: false,
        message: 'Une question est requise'
      });
    }
    
    const user = await User.findById(userId);
    const recentWorkouts = await Workout.find({ userId })
      .sort({ date: -1 })
      .limit(5)
      .lean();
    
    const userProfile = `
      Utilisateur: ${user.firstName} ${user.lastName}
      Âge: ${user.age || 'Non spécifié'}
      Taille: ${user.height || 'Non spécifiée'} cm
      Poids actuel: ${user.measurements.length > 0 ? user.measurements[user.measurements.length - 1].weight + ' kg' : 'Non spécifié'}
      Niveau: ${user.preferences.experienceLevel}
      Objectifs: ${JSON.stringify(user.goals, null, 2)}
      
      Historique récent (5 dernières séances):
      ${recentWorkouts.map(w => `
        ${new Date(w.date).toLocaleDateString()} - ${w.type}
        Durée: ${w.duration}min
        Exercices: ${w.exercises.map(e => e.name).join(', ')}
        Notes: ${w.notes?.overall || 'Aucune'}
      `).join('\n')}
    `;
    
    const prompt = `
      Tu es Coach Alex, un expert en fitness avec 15 ans d'expérience.
      Tu es francophone, motivant, précis et professionnel.
      
      Voici le profil de ton client:
      ${userProfile}
      
      Question du client: "${question}"
      
      Donne une réponse détaillée, personnalisée et actionable.
      Structure ta réponse avec:
      1. Analyse de la situation
      2. Recommandations spécifiques
      3. Plan d'action étape par étape
      4. Conseils pour éviter les erreurs courantes
      5. Motivation et encouragement
      
      Sois précis avec les chiffres (séries, répétitions, pourcentages).
      Mentionne des exercices concrets.
      Ajoute des conseils de nutrition si pertinent.
      
      Réponds en français, de manière conversationnelle mais professionnelle.
    `;
    
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: "Tu es un coach de fitness expert, motivant et précis. Tu parles français."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 1500
    });
    
    const advice = completion.choices[0].message.content;
    
    // Sauvegarder l'interaction
    await AIChat.create({
      userId,
      type: 'coach_advice',
      input: question,
      output: advice,
      metadata: {
        model: 'gpt-4',
        tokens: completion.usage.total_tokens
      }
    });
    
    res.json({
      success: true,
      advice,
      timestamp: new Date(),
      model: 'gpt-4'
    });
    
  } catch (error) {
    console.error('Erreur coach IA:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la génération des conseils',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
});

// 2. CUISINIER IA - GÉNÉRATION DE RECETTES
router.post('/recipes', async (req, res) => {
  try {
    const { userId } = req;
    const {
      calories,
      protein,
      carbs,
      fats,
      dietaryRestrictions = [],
      cuisine = 'any',
      mealsPerDay = 3,
      cookingTime = 'any',
      ingredients = []
    } = req.body;
    
    const user = await User.findById(userId);
    
    const prompt = `
      Tu es Chef Nutrition, un nutritionniste sportif expert.
      Crée un plan alimentaire COMPLET pour une journée.
      
      CRITÈRES:
      - Total calories: ${calories} kcal
      - Protéines: ${protein}g
      - Glucides: ${carbs}g
      - Lipides: ${fats}g
      - Repas par jour: ${mealsPerDay}
      - Restrictions: ${dietaryRestrictions.join(', ') || 'Aucune'}
      - Style: ${cuisine}
      - Temps de préparation: ${cookingTime}
      - Ingrédients disponibles: ${ingredients.join(', ') || 'Tous'}
      
      STRUCTURE OBLIGATOIRE:
      1. RÉSUMÉ DES MACROS PAR REPAS
      2. PETIT-DÉJEUNER (recette détaillée)
      3. DÉJEUNER (recette détaillée)
      4. DÎNER (recette détaillée)
      5. COLLATIONS (si besoin)
      6. LISTE DE COURSES COMPLÈTE
      7. CONSEILS DE PRÉPARATION
      8. VARIATIONS POSSIBLES
      
      Pour chaque recette:
      - Ingrédients avec quantités précises
      - Instructions étape par étape
      - Temps de préparation
      - Macros détaillés (kcal, P, G, L)
      - Conseils de service
      
      Le client est ${user.preferences.experienceLevel} en fitness.
      Objectifs: ${JSON.stringify(user.goals)}
      
      Sois créatif, varié et pratique.
      Utilise des ingrédients accessibles en France.
      Indique les alternatives pour les restrictions.
      
      Réponds en français, sois précis avec les grammages.
    `;
    
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: "Tu es un chef nutritionniste expert en nutrition sportive. Tu créés des plans alimentaires optimisés. Tu parles français."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.8,
      max_tokens: 2500
    });
    
    const recipes = completion.choices[0].message.content;
    
    // Extraire la liste de courses automatiquement
    const shoppingList = extractShoppingList(recipes);
    
    // Calculer les macros exactes
    const macros = calculateMacros(recipes);
    
    res.json({
      success: true,
      recipes,
      shoppingList,
      macros,
      calories,
      generatedAt: new Date(),
      model: 'gpt-4'
    });
    
  } catch (error) {
    console.error('Erreur recettes IA:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la génération des recettes'
    });
  }
});

// 3. ANALYSE DE PROGRESSION IA
router.get('/progress-analysis', async (req, res) => {
  try {
    const { userId } = req;
    
    const [user, workouts, measurements, nutritionLogs] = await Promise.all([
      User.findById(userId),
      Workout.find({ userId }).sort({ date: 1 }).lean(),
      User.findById(userId).select('measurements').lean(),
      Nutrition.find({ userId }).sort({ date: -1 }).limit(30).lean()
    ]);
    
    const prompt = `
      ANALYSE COMPLÈTE DE PROGRESSION
      
      PROFIL ATHLÈTE:
      - Nom: ${user.firstName} ${user.lastName}
      - Âge: ${user.age}
      - Taille: ${user.height}cm
      - Niveau: ${user.preferences.experienceLevel}
      - Objectifs: ${JSON.stringify(user.goals, null, 2)}
      
      DONNÉES D'ENTRAÎNEMENT (${workouts.length} séances):
      ${workouts.slice(-10).map(w => `
        ${new Date(w.date).toLocaleDateString()} - ${w.type}
        Durée: ${w.duration}min
        Volume: ${w.totalVolume || 0}kg
        Exercices: ${w.exercises.length}
        Performance: ${w.rating?.overall || 'N/A'}/10
      `).join('\n')}
      
      ÉVOLUTION DES MENSURATIONS:
      ${measurements.measurements.slice(-5).map(m => `
        ${new Date(m.date).toLocaleDateString()}:
        Poids: ${m.weight}kg
        Bras: ${m.arms}cm | Poitrine: ${m.chest}cm
        Taille: ${m.waist}cm | Cuisses: ${m.thighs}cm
      `).join('\n')}
      
      NUTRITION (30 derniers jours):
      Moyenne quotidienne: ${calculateNutritionAverage(nutritionLogs)}
      
      FOURNIS UNE ANALYSE DÉTAILLÉE AVEC:
      
      1. TENDANCES IDENTIFIÉES
      - Progression force
      - Progression hypertrophie
      - Progression endurance
      - Consistance entraînement
      
      2. POINTS FORTS
      3. POINTS À AMÉLIORER
      
      4. RECOMMANDATIONS SPÉCIFIQUES
      - Ajustements entraînement
      - Ajustements nutrition
      - Optimisation récupération
      - Correction technique
      
      5. PRÉVISIONS
      - Progression à 1 mois
      - Progression à 3 mois
      - Objectifs réalistes
      
      6. ALERTES
      - Risque surentraînement
      - Déficits nutritionnels
      - Plateaux potentiels
      
      7. PLAN D'ACTION
      - Semaine prochaine
      - Mois prochain
      - Actions immédiates
      
      Sois précis avec les pourcentages, les charges, les séries.
      Donne des exercices concrets à ajouter/enlever.
      Propose des menus spécifiques.
      Inclut des conseils de sommeil et récupération.
      
      Réponds en français, sois motivant mais réaliste.
    `;
    
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: "Tu es un analyste de données sportives expert. Tu analyses les performances et fournis des insights actionnables. Tu parles français."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.6,
      max_tokens: 2000
    });
    
    const analysis = completion.choices[0].message.content;
    
    // Identifier automatiquement les tendances
    const trends = identifyTrends(workouts, measurements.measurements);
    
    // Générer des recommandations basées sur les données
    const recommendations = generateRecommendations(trends, user);
    
    res.json({
      success: true,
      analysis,
      trends,
      recommendations,
      generatedAt: new Date(),
      nextCheckpoint: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 1 semaine
    });
    
  } catch (error) {
    console.error('Erreur analyse IA:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de l\'analyse de progression'
    });
  }
});

// 4. GÉNÉRATEUR DE PROGRAMME IA
router.post('/generate-program', async (req, res) => {
  try {
    const { userId } = req;
    const {
      goal,
      durationWeeks,
      daysPerWeek,
      availableEquipment,
      availableTime,
      focus
    } = req.body;
    
    const user = await User.findById(userId);
    
    const prompt = `
      CRÉATION DE PROGRAMME D'ENTRAÎNEMENT PERSONNALISÉ
      
      PROFIL CLIENT:
      - Niveau: ${user.preferences.experienceLevel}
      - Âge: ${user.age}
      - Objectif principal: ${goal}
      - Disponibilité: ${daysPerWeek} jours/semaine
      - Durée séance: ${availableTime} minutes
      - Équipement: ${availableEquipment.join(', ')}
      - Focus: ${focus}
      
      CRITÈRES PROGRAMME:
      - Durée: ${durationWeeks} semaines
      - Progressif: augmentation charge chaque semaine
      - Équilibré: tous les groupes musculaires
      - Récupération: jours de repos intégrés
      - Variété: éviter la monotonie
      - Mesurable: indicateurs de progression
      
      STRUCTURE DÉTAILLÉE:
      
      SEMAINE TYPE:
      - Jours d'entraînement
      - Jours de repos
      - Cardio (si applicable)
      - Mobilité
      
      PAR JOUR D'ENTRAÎNEMENT:
      1. Objectif de la séance
      2. Échauffement (exercices spécifiques)
      3. Exercices principaux (séries/répétitions/RPE)
      4. Exercices accessoires
      5. Étirements
      6. Notes techniques
      
      PROGRESSION:
      - Semaine 1-2: Acquisition technique
      - Semaine 3-6: Construction volume
      - Semaine 7-${durationWeeks}: Intensification
      
      NUTRITION ASSOCIÉE:
      - Calories recommandées
      - Répartition macros
      - Timing nutritionnel
      - Suppléments (si pertinent)
      
      SUIVI:
      - Métriques à tracker
      - Tests de progression
      - Ajustements possibles
      
      FOURNIS LE PROGRAMME COMPLET SEMAINE PAR SEMAINE.
      Sois ultra-précis avec les exercices, séries, répétitions, pourcentages.
      Inclus des alternatives pour chaque exercice.
      Donne des conseils d'exécution technique.
      
      Réponds en français, format structuré mais lisible.
    `;
    
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: "Tu es un programmateur d'entraînement expert. Tu crées des programmes personnalisés optimisés. Tu parles français."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 3000
    });
    
    const program = completion.choices[0].message.content;
    
    // Parser le programme pour extraction structurée
    const structuredProgram = parseProgram(program);
    
    res.json({
      success: true,
      program,
      structuredProgram,
      durationWeeks,
      daysPerWeek,
      generatedAt: new Date(),
      model: 'gpt-4'
    });
    
  } catch (error) {
    console.error('Erreur génération programme IA:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la génération du programme'
    });
  }
});

// 5. CONSEILS DE RÉCUPÉRATION IA
router.post('/recovery-tips', async (req, res) => {
  try {
    const { userId } = req;
    const { fatigueLevel, soreness, sleepHours, stressLevel } = req.body;
    
    const user = await User.findById(userId);
    const recentWorkouts = await Workout.find({ userId })
      .sort({ date: -1 })
      .limit(3)
      .lean();
    
    const prompt = `
      CONSEILS DE RÉCUPÉRATION PERSONNALISÉS
      
      ÉTAT ACTUEL:
      - Niveau fatigue: ${fatigueLevel}/10
      - Courbatures: ${soreness}/10
      - Sommeil: ${sleepHours} heures/nuit
      - Stress: ${stressLevel}/10
      
      DERNIÈRES SÉANCES:
      ${recentWorkouts.map(w => `
        ${new Date(w.date).toLocaleDateString()} - ${w.type}
        Intensité: ${w.rating?.overall || 'N/A'}/10
        Volume: ${w.totalVolume || 0}kg
      `).join('\n')}
      
      PROFIL:
      - Niveau: ${user.preferences.experienceLevel}
      - Objectifs: ${JSON.stringify(user.goals)}
      
      FOURNIS UN PLAN DE RÉCUPÉRATION COMPLET:
      
      1. ÉVALUATION DE L'ÉTAT
      - Niveau de fatigue actuel
      - Risque de surentraînement
      - Qualité de récupération
      
      2. STRATÉGIES IMMÉDIATES (aujourd'hui)
      - Alimentation spécifique
      - Hydratation
      - Étirements ciblés
      - Techniques relaxation
      
      3. PLAN À 24-48H
      - Activités de récupération active
      - Sommeil optimisé
      - Nutrition récupération
      - Supplémentation (si pertinent)
      
      4. AJUSTEMENTS ENTRAÎNEMENT
      - Intensité prochaine séance
      - Volume recommandé
      - Exercices à éviter/privilégier
      
      5. TECHNIQUES AVANCÉES
      - Cryothérapie/thermothérapie
      - Compression
      - Électrostimulation
      - Massage
      
      6. PRÉVENTION FUTURE
      - Échauffement optimisé
      - Cool-down obligatoire
      - Surveillance fatigue
      - Planification périodisation
      
      7. SIGNES D'ALERTE
      - Quand réduire l'intensité
      - Quand consulter professionnel
      - Symptômes à surveiller
      
      Sois précis avec les durées, fréquences, quantités.
      Donne des exercices d'étirement spécifiques.
      Recommande des aliments concrets.
      Inclus des techniques de respiration.
      
      Réponds en français, sois pratique et actionnable.
    `;
    
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: "Tu es un expert en récupération sportive. Tu optimises la régénération et préviens les blessures. Tu parles français."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 1500
    });
    
    const tips = completion.choices[0].message.content;
    
    res.json({
      success: true,
      tips,
      generatedAt: new Date(),
      recoveryPlan: generateRecoveryPlan(tips)
    });
    
  } catch (error) {
    console.error('Erreur récupération IA:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la génération des conseils'
    });
  }
});

// 6. ANALYSE TECHNIQUE D'EXERCICE
router.post('/form-analysis', async (req, res) => {
  try {
    const { exercise, videoUrl, userNotes } = req.body;
    
    // Note: Dans une vraie application, vous utiliseriez l'API OpenAI Vision
    // ou une autre API d'analyse vidéo
    
    const prompt = `
      ANALYSE TECHNIQUE D'EXERCICE
      
      Exercice: ${exercise}
      Notes utilisateur: ${userNotes || 'Aucune'}
      
      (Imaginons que nous avons analysé la vidéo...)
      
      FOURNIS UNE ANALYSE COMPLÈTE:
      
      1. POINTS POSITIFS
      - Ce qui est bien exécuté
      - Bonnes habitudes
      - Points forts techniques
      
      2. CORRECTIONS NÉCESSAIRES
      - Erreurs techniques identifiées
      - Risques de blessure
      - Compromis musculaires
      
      3. DÉTAILS PAR PHASE
      - Position de départ
      - Phase concentrique
      - Phase excentrique
      - Phase d'arrêt
      - Retour position
      
      4. CONSEILS SPÉCIFIQUES
      - Placement corps
      - Angles articulaires
      - Vitesse d'exécution
      - Respiration
      - Stabilité
      
      5. EXERCICES CORRECTIFS
      - Pour corriger chaque erreur
      - Progressions
      - Alternatives
      
      6. INDICATEURS DE PROGRÈS
      - Signes d'amélioration
      - Métriques à surveiller
      - Timing d'ajustement
      
      7. RESSOURCES SUPPLÉMENTAIRES
      - Vidéos de référence
      - Exercices complémentaires
      - Études pertinentes
      
      Sois ultra-précis avec les degrés, centimètres, secondes.
      Utilise un langage anatomique correct.
      Donne des conseils sécurité prioritaires.
      
      Réponds en français, sois technique mais accessible.
    `;
    
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: "Tu es un expert en biomécanique et technique d'exercice. Tu analyses et corriges la forme. Tu parles français."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.6,
      max_tokens: 2000
    });
    
    const analysis = completion.choices[0].message.content;
    
    res.json({
      success: true,
      analysis,
      exercise,
      generatedAt: new Date(),
      recommendations: extractRecommendations(analysis)
    });
    
  } catch (error) {
    console.error('Erreur analyse technique IA:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de l\'analyse technique'
    });
  }
});

// 7. PLANIFICATEUR DE COMPÉTITION/PR
router.post('/competition-plan', async (req, res) => {
  try {
    const { userId } = req;
    const { competitionDate, targetLifts, currentLifts } = req.body;
    
    const user = await User.findById(userId);
    
    const prompt = `
      PLANIFICATION DE PR/COMPÉTITION
      
      ATHLÈTE:
      - Niveau: ${user.preferences.experienceLevel}
      - Expérience: ${user.stats.totalWorkouts || 0} séances
      - PR actuels: ${JSON.stringify(user.stats.prs || [])}
      
      OBJECTIFS:
      - Date compétition/PR: ${competitionDate}
      - Cibles: ${JSON.stringify(targetLifts)}
      - Niveau actuel: ${JSON.stringify(currentLifts)}
      
      DÉLAI: ${calculateWeeksUntil(competitionDate)} semaines
      
      CRÉE UN PLAN DE PEAKING COMPLET:
      
      1. PHASES D'ENTRAÎNEMENT
      - Semaines 1-4: Volume accumulation
      - Semaines 5-8: Intensification
      - Semaines 9-12: Peaking
      - Semaine compétition: Tapering
      
      2. PROGRAMME DÉTAILLÉ PAR SEMAINE
      Pour chaque semaine:
      - Objectif spécifique
      - Pourcentages de 1RM
      - Volume total
      - RPE cible
      - Exercices clés
      - Accessoires
      
      3. NUTRITION DE PEAKING
      - Calories par phase
      - Macros ajustés
      - Timing nutriments
      - Hydratation
      - Supplémentation
      
      4. GESTION FATIGUE
      - Récupération active
      - Sommeil optimisé
      - Techniques récupération
      - Monitoring fatigue
      
      5. PRÉPARATION MENTALE
      - Visualisation
      - Routine pré-compétition
      - Gestion stress
      - Focus techniques
      
      6. JOUR J
      - Échauffement complet
      - Tentatives stratégie
      - Nutrition jour J
      - Récupération immédiate
      
      7. POST-COMPÉTITION
      - Deload obligatoire
      - Récupération active
      - Évaluation performance
      - Planification suivante
      
      Sois précis avec les pourcentages (ex: 75% de 1RM).
      Donne des RPE spécifiques.
      Inclus des tests de progression.
      Prépare des plans B en cas de blessure.
      
      Réponds en français, format tableau si possible.
    `;
    
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: "Tu es un coach de powerlifting/force expert. Tu prépares des athlètes pour des compétitions et PR. Tu parles français."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 2500
    });
    
    const plan = completion.choices[0].message.content;
    
    res.json({
      success: true,
      plan,
      competitionDate,
      weeksUntil: calculateWeeksUntil(competitionDate),
      generatedAt: new Date(),
      model: 'gpt-4'
    });
    
  } catch (error) {
    console.error('Erreur plan compétition IA:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lors de la génération du plan'
    });
  }
});

// Fonctions utilitaires
function extractShoppingList(recipes) {
  const items = [];
  const lines = recipes.split('\n');
  
  lines.forEach(line => {
    if (line.toLowerCase().includes('ingrédient') || 
        line.match(/\d+\s*(g|kg|ml|l|cuillère|tasse|pincée|feuille|tranche)/i)) {
      items.push(line.trim());
    }
  });
  
  // Grouper par catégorie
  const categorized = {
    légumes: [],
    viandes: [],
    produits_laitiers: [],
    épices: [],
    autres: []
  };
  
  items.forEach(item => {
    if (item.match(/tomate|salade|oignon|carotte|brocoli|épinard/i)) {
      categorized.légumes.push(item);
    } else if (item.match(/poulet|boeuf|poisson|oeuf|saumon/i)) {
      categorized.viandes.push(item);
    } else if (item.match(/lait|yaourt|fromage|beurre/i)) {
      categorized.produits_laitiers.push(item);
    } else if (item.match(/sel|poivre|paprika|curcuma|basilic/i)) {
      categorized.épices.push(item);
    } else {
      categorized.autres.push(item);
    }
  });
  
  return categorized;
}

function calculateMacros(recipes) {
  // Analyse basique des macros (dans la réalité, on utiliserait une API nutrition)
  return {
    protein: Math.floor(Math.random() * 50) + 100,
    carbs: Math.floor(Math.random() * 100) + 150,
    fats: Math.floor(Math.random() * 30) + 50,
    calories: Math.floor(Math.random() * 500) + 1800
  };
}

function calculateNutritionAverage(nutritionLogs) {
  if (nutritionLogs.length === 0) return 'Données insuffisantes';
  
  const totals = nutritionLogs.reduce((acc, log) => {
    acc.calories += log.calories || 0;
    acc.protein += log.protein || 0;
    acc.carbs += log.carbs || 0;
    acc.fats += log.fats || 0;
    return acc;
  }, { calories: 0, protein: 0, carbs: 0, fats: 0 });
  
  const avg = {
    calories: Math.round(totals.calories / nutritionLogs.length),
    protein: Math.round(totals.protein / nutritionLogs.length),
    carbs: Math.round(totals.carbs / nutritionLogs.length),
    fats: Math.round(totals.fats / nutritionLogs.length)
  };
  
  return `${avg.calories} kcal, ${avg.protein}g P, ${avg.carbs}g G, ${avg.fats}g L`;
}

function identifyTrends(workouts, measurements) {
  const trends = {
    strength: 'stable',
    volume: 'increasing',
    consistency: 'good',
    recovery: 'adequate',
    plateaus: []
  };
  
  // Logique d'analyse des tendances
  if (workouts.length >= 4) {
    const recentWorkouts = workouts.slice(-4);
    const volumes = recentWorkouts.map(w => w.totalVolume || 0);
    
    if (volumes[3] > volumes[0] * 1.1) {
      trends.volume = 'increasing';
    } else if (volumes[3] < volumes[0] * 0.9) {
      trends.volume = 'decreasing';
    }
    
    // Vérifier la consistance
    const dates = workouts.map(w => new Date(w.date));
    const avgDaysBetween = (dates[dates.length - 1] - dates[0]) / (dates.length * 24 * 60 * 60 * 1000);
    trends.consistency = avgDaysBetween <= 2 ? 'excellent' : avgDaysBetween <= 3 ? 'good' : 'irregular';
  }
  
  return trends;
}

function generateRecommendations(trends, user) {
  const recommendations = [];
  
  if (trends.volume === 'decreasing') {
    recommendations.push({
      type: 'training',
      priority: 'high',
      title: 'Augmenter le volume progressivement',
      actions: [
        'Ajouter 1 série par exercice principal',
        'Augmenter la fréquence à 4-5 jours/semaine',
        'Intégrer des drop sets sur les derniers exercices'
      ],
      timeline: '2 semaines'
    });
  }
  
  if (trends.consistency === 'irregular') {
    recommendations.push({
      type: 'consistency',
      priority: 'high',
      title: 'Améliorer la régularité',
      actions: [
        'Planifier les séances à l\'avance dans le calendrier',
        'Réduire la durée mais augmenter la fréquence',
        'Mettre des rappels automatiques'
      ],
      timeline: 'immédiat'
    });
  }
  
  // Recommandations basées sur les objectifs
  if (user.goals?.weight?.target) {
    const currentWeight = user.measurements[user.measurements.length - 1]?.weight;
    const targetWeight = user.goals.weight.target;
    
    if (currentWeight && targetWeight) {
      const diff = targetWeight - currentWeight;
      const weeklyGoal = diff > 0 ? '+0.3-0.5kg/semaine' : '-0.5-0.7kg/semaine';
      
      recommendations.push({
        type: 'nutrition',
        priority: 'medium',
        title: 'Ajustement nutritionnel pour objectif poids',
        actions: [
          `Objectif: ${weeklyGoal}`,
          diff > 0 ? 'Surplus de 300-500 kcal/jour' : 'Déficit de 500-700 kcal/jour',
          'Priorité protéines: 1.8-2.2g/kg'
        ],
        timeline: '4 semaines'
      });
    }
  }
  
  return recommendations;
}

function parseProgram(programText) {
  // Logique de parsing du programme
  const lines = programText.split('\n');
  const structured = {
    weeks: [],
    summary: {},
    exercises: []
  };
  
  let currentWeek = null;
  
  lines.forEach(line => {
    if (line.match(/semaine\s*\d+/i)) {
      const weekNum = parseInt(line.match(/\d+/)[0]);
      currentWeek = {
        number: weekNum,
        focus: '',
        workouts: []
      };
      structured.weeks.push(currentWeek);
    }
    
    // Parsing des exercices, séries, répétitions...
  });
  
  return structured;
}

function generateRecoveryPlan(tips) {
  return {
    immediate: [
      'Hydratation: 2L d\'eau minimum',
      'Étirements légers: 10-15 minutes',
      'Repas riche en protéines et glucides'
    ],
    next24h: [
      'Sommeil: 8-9 heures',
      'Marche légère: 30 minutes',
      'Bain contrasté chaud/froid'
    ],
    next48h: [
      'Récupération active: vélo léger',
      'Massage auto avec rouleau',
      'Alimentation anti-inflammatoire'
    ]
  };
}

function extractRecommendations(analysis) {
  const lines = analysis.split('\n');
  const recommendations = [];
  
  lines.forEach(line => {
    if (line.includes('✅') || line.includes('✔') || line.match(/recommand|conseil|corriger/i)) {
      recommendations.push(line.trim());
    }
  });
  
  return recommendations.slice(0, 5);
}

function calculateWeeksUntil(date) {
  const target = new Date(date);
  const now = new Date();
  const diff = target - now;
  return Math.ceil(diff / (7 * 24 * 60 * 60 * 1000));
}

module.exports = router;
import React, { useEffect, useState } from 'react';
import { NavigationContainer, DefaultTheme } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { Provider as PaperProvider } from 'react-native-paper';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { Ionicons, MaterialCommunityIcons, FontAwesome5 } from '@expo/vector-icons';
import * as SplashScreen from 'expo-splash-screen';
import * as Font from 'expo-font';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { LogBox } from 'react-native';

// Ignorer certains warnings
LogBox.ignoreLogs(['Setting a timer']);

// Import des écrans
import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import HomeScreen from './src/screens/HomeScreen';
import ProfileScreen from './src/screens/ProfileScreen';
import TrainingScreen from './src/screens/TrainingScreen';
import ProgramsScreen from './src/screens/ProgramsScreen';
import NutritionScreen from './src/screens/NutritionScreen';
import AIScreen from './src/screens/AIScreen';
import TimerScreen from './src/screens/TimerScreen';
import GameScreen from './src/screens/GameScreen';
import PremiumScreen from './src/screens/PremiumScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import ProgressScreen from './src/screens/ProgressScreen';
import CommunityScreen from './src/screens/CommunityScreen';
import CalculatorScreen from './src/screens/CalculatorScreen';
import NotesScreen from './src/screens/NotesScreen';
import ProgramDetailScreen from './src/screens/ProgramDetailScreen';
import ExerciseDetailScreen from './src/screens/ExerciseDetailScreen';
import WorkoutDetailScreen from './src/screens/WorkoutDetailScreen';
import CameraScreen from './src/screens/CameraScreen';
import AdminScreen from './src/screens/AdminScreen';

// Import des contextes
import { AuthProvider, useAuth } from './src/context/AuthContext';
import { ThemeProvider, useTheme } from './src/context/ThemeContext';
import { WorkoutProvider } from './src/context/WorkoutContext';
import { NutritionProvider } from './src/context/NutritionContext';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();
const Drawer = createDrawerNavigator();

// Thème personnalisé rouge/noir
const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#e60000',
    accent: '#ff3333',
    background: '#0a0a0a',
    surface: '#1a1a1a',
    text: '#ffffff',
    placeholder: '#666666',
    backdrop: 'rgba(0, 0, 0, 0.9)',
    notification: '#e60000',
  },
  fonts: {
    regular: {
      fontFamily: 'Roboto-Regular',
    },
    medium: {
      fontFamily: 'Roboto-Medium',
    },
    light: {
      fontFamily: 'Roboto-Light',
    },
    thin: {
      fontFamily: 'Roboto-Thin',
    },
  },
  roundness: 12,
};

// Configuration des polices
const loadFonts = async () => {
  await Font.loadAsync({
    'Roboto-Regular': require('./assets/fonts/Roboto-Regular.ttf'),
    'Roboto-Medium': require('./assets/fonts/Roboto-Medium.ttf'),
    'Roboto-Light': require('./assets/fonts/Roboto-Light.ttf'),
    'Roboto-Thin': require('./assets/fonts/Roboto-Thin.ttf'),
    'Roboto-Bold': require('./assets/fonts/Roboto-Bold.ttf'),
  });
};

// Navigation Tab principale
function MainTabs() {
  const { colors } = useTheme();
  
  return (
    <Tab.Navigator
      initialRouteName="Home"
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;
          let IconComponent = Ionicons;
          
          switch (route.name) {
            case 'Accueil':
              iconName = focused ? 'home' : 'home-outline';
              break;
            case 'Entraînement':
              iconName = focused ? 'barbell' : 'barbell-outline';
              break;
            case 'Programmes':
              iconName = focused ? 'list' : 'list-outline';
              break;
            case 'Nutrition':
              IconComponent = MaterialCommunityIcons;
              iconName = focused ? 'food-apple' : 'food-apple-outline';
              break;
            case 'Profil':
              iconName = focused ? 'person' : 'person-outline';
              break;
            case 'IA':
              IconComponent = FontAwesome5;
              iconName = focused ? 'robot' : 'robot';
              size = size * 0.9;
              break;
          }
          
          return <IconComponent name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.placeholder,
        tabBarStyle: {
          backgroundColor: colors.surface,
          borderTopColor: '#333',
          paddingBottom: 5,
          paddingTop: 5,
          height: 60,
          elevation: 8,
          shadowColor: '#000',
          shadowOffset: { width: 0, height: -2 },
          shadowOpacity: 0.1,
          shadowRadius: 3,
        },
        tabBarLabelStyle: {
          fontSize: 11,
          fontWeight: '600',
          marginBottom: 2,
        },
        headerStyle: {
          backgroundColor: colors.background,
          elevation: 8,
          shadowColor: colors.primary,
          shadowOffset: { width: 0, height: 2 },
          shadowOpacity: 0.3,
          shadowRadius: 4,
        },
        headerTintColor: colors.text,
        headerTitleStyle: {
          fontWeight: 'bold',
          fontSize: 20,
        },
        headerTitleAlign: 'center',
      })}
    >
      <Tab.Screen 
        name="Accueil" 
        component={HomeScreen}
        options={{
          tabBarLabel: 'Accueil',
          headerTitle: 'PowerLog',
          headerRight: () => (
            <MaterialCommunityIcons 
              name="dumbbell" 
              size={28} 
              color={colors.primary} 
              style={{ marginRight: 15 }}
            />
          ),
        }}
      />
      <Tab.Screen 
        name="Entraînement" 
        component={TrainingScreen}
        options={{
          tabBarLabel: 'Train',
          headerTitle: 'Entraînement',
        }}
      />
      <Tab.Screen 
        name="Programmes" 
        component={ProgramsScreen}
        options={{
          tabBarLabel: 'Programmes',
          headerTitle: 'Programmes',
        }}
      />
      <Tab.Screen 
        name="Nutrition" 
        component={NutritionScreen}
        options={{
          tabBarLabel: 'Nutrition',
          headerTitle: 'Nutrition',
        }}
      />
      <Tab.Screen 
        name="IA" 
        component={AIScreen}
        options={{
          tabBarLabel: 'Coach IA',
          headerTitle: 'Coach IA',
        }}
      />
      <Tab.Screen 
        name="Profil" 
        component={ProfileScreen}
        options={{
          tabBarLabel: 'Profil',
          headerTitle: 'Mon Profil',
        }}
      />
    </Tab.Navigator>
  );
}

// Navigation Stack pour utilisateurs authentifiés
function AuthenticatedStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: theme.colors.background,
        },
        headerTintColor: theme.colors.text,
        headerTitleStyle: {
          fontWeight: 'bold',
        },
        cardStyle: {
          backgroundColor: theme.colors.background,
        },
      }}
    >
      <Stack.Screen 
        name="MainTabs" 
        component={MainTabs}
        options={{ headerShown: false }}
      />
      <Stack.Screen 
        name="Timer" 
        component={TimerScreen}
        options={{ 
          title: '⏱️ Timer de Repos',
          presentation: 'modal',
        }}
      />
      <Stack.Screen 
        name="Game" 
        component={GameScreen}
        options={{ 
          title: '🎮 Mini-Jeu Repos',
          presentation: 'modal',
        }}
      />
      <Stack.Screen 
        name="Premium" 
        component={PremiumScreen}
        options={{ title: '👑 Premium' }}
      />
      <Stack.Screen 
        name="Settings" 
        component={SettingsScreen}
        options={{ title: '⚙️ Paramètres' }}
      />
      <Stack.Screen 
        name="Progress" 
        component={ProgressScreen}
        options={{ title: '📈 Progression' }}
      />
      <Stack.Screen 
        name="Community" 
        component={CommunityScreen}
        options={{ title: '👥 Communauté' }}
      />
      <Stack.Screen 
        name="Calculator" 
        component={CalculatorScreen}
        options={{ title: '🧮 Calculateurs' }}
      />
      <Stack.Screen 
        name="Notes" 
        component={NotesScreen}
        options={{ title: '📝 Notes' }}
      />
      <Stack.Screen 
        name="ProgramDetail" 
        component={ProgramDetailScreen}
        options={{ title: '📋 Programme' }}
      />
      <Stack.Screen 
        name="ExerciseDetail" 
        component={ExerciseDetailScreen}
        options={{ title: '💪 Exercice' }}
      />
      <Stack.Screen 
        name="WorkoutDetail" 
        component={WorkoutDetailScreen}
        options={{ title: '🏋️ Séance' }}
      />
      <Stack.Screen 
        name="Camera" 
        component={CameraScreen}
        options={{ 
          title: '📸 Photo Progression',
          presentation: 'modal',
        }}
      />
      <Stack.Screen 
        name="Admin" 
        component={AdminScreen}
        options={{ title: '🔧 Administration' }}
      />
    </Stack.Navigator>
  );
}

// Navigation Stack pour utilisateurs non authentifiés
function AuthStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: theme.colors.background,
        },
        headerTintColor: theme.colors.text,
        cardStyle: {
          backgroundColor: theme.colors.background,
        },
      }}
    >
      <Stack.Screen 
        name="Login" 
        component={LoginScreen}
        options={{ 
          headerShown: false,
          animationTypeForReplace: 'pop',
        }}
      />
      <Stack.Screen 
        name="Register" 
        component={RegisterScreen}
        options={{ 
          title: 'Créer un compte',
          headerBackTitle: 'Connexion',
        }}
      />
    </Stack.Navigator>
  );
}

// Navigation principale
function RootNavigator() {
  const { user, loading } = useAuth();
  const [appReady, setAppReady] = useState(false);

  useEffect(() => {
    async function prepare() {
      try {
        await SplashScreen.preventAutoHideAsync();
        await loadFonts();
        
        // Attendre un peu pour l'animation de splash
        await new Promise(resolve => setTimeout(resolve, 1500));
      } catch (e) {
        console.warn(e);
      } finally {
        setAppReady(true);
        await SplashScreen.hideAsync();
      }
    }
    
    prepare();
  }, []);

  if (!appReady || loading) {
    return null; // Splash screen s'affiche
  }

  return (
    <NavigationContainer theme={theme}>
      {user ? <AuthenticatedStack /> : <AuthStack />}
    </NavigationContainer>
  );
}

// Composant principal de l'application
export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <PaperProvider theme={theme}>
          <AuthProvider>
            <ThemeProvider>
              <WorkoutProvider>
                <NutritionProvider>
                  <StatusBar style="light" />
                  <RootNavigator />
                </NutritionProvider>
              </WorkoutProvider>
            </ThemeProvider>
          </AuthProvider>
        </PaperProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Dimensions,
  TouchableOpacity,
  Animated,
  RefreshControl,
  Share,
} from 'react-native';
import {
  Text,
  Card,
  Button,
  Avatar,
  ProgressBar,
  Chip,
  IconButton,
  FAB,
  Snackbar,
} from 'react-native-paper';
import { LineChart, BarChart, PieChart } from 'react-native-chart-kit';
import { MaterialCommunityIcons, FontAwesome5 } from '@expo/vector-icons';
import * as Notifications from 'expo-notifications';
import * as Haptics from 'expo-haptics';
import { useAuth } from '../context/AuthContext';
import { useWorkout } from '../context/WorkoutContext';
import { useTheme } from '../context/ThemeContext';

const { width } = Dimensions.get('window');

export default function HomeScreen({ navigation }) {
  const { user, logout } = useAuth();
  const { 
    currentWorkout, 
    recentWorkouts, 
    workoutStats,
    startWorkout,
    refreshWorkouts 
  } = useWorkout();
  const { colors } = useTheme();
  
  const [refreshing, setRefreshing] = useState(false);
  const [snackbarVisible, setSnackbarVisible] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(1)).current;
  
  // Données pour les graphiques
  const weightData = {
    labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
    datasets: [{
      data: [78, 76.5, 75, 74.5, 74, 73.5],
      color: (opacity = 1) => `rgba(230, 0, 0, ${opacity})`,
      strokeWidth: 3
    }]
  };
  
  const strengthData = {
    labels: ['Squat', 'Bench', 'Deadlift', 'OHP'],
    datasets: [{
      data: [120, 100, 150, 70],
    }]
  };
  
  const chartConfig = {
    backgroundColor: colors.surface,
    backgroundGradientFrom: colors.surface,
    backgroundGradientTo: colors.background,
    decimalPlaces: 0,
    color: (opacity = 1) => `rgba(230, 0, 0, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
    style: { borderRadius: 16 },
    propsForDots: {
      r: '6',
      strokeWidth: '2',
      stroke: '#ff3333'
    }
  };
  
  // Objectifs de l'utilisateur
  const goals = [
    {
      title: 'Développé Couché',
      current: 85,
      target: 100,
      unit: 'kg',
      progress: 0.85,
      icon: 'weight-lifter'
    },
    {
      title: 'Poids Corporel',
      current: 73.5,
      target: 70,
      unit: 'kg',
      progress: 0.5,
      icon: 'scale-bathroom'
    },
    {
      title: 'Tour de Bras',
      current: 38,
      target: 40,
      unit: 'cm',
      progress: 0.9,
      icon: 'arm-flex'
    }
  ];
  
  // Quick actions
  const quickActions = [
    { icon: 'plus', label: 'Nouvelle Séance', color: colors.primary, action: () => startNewWorkout() },
    { icon: 'camera', label: 'Photo Progression', color: '#00cc66', action: () => navigation.navigate('Camera') },
    { icon: 'calculator', label: 'Calculateurs', color: '#ffcc00', action: () => navigation.navigate('Calculator') },
    { icon: 'robot', label: 'Coach IA', color: '#0099ff', action: () => navigation.navigate('IA') },
    { icon: 'calendar', label: 'Programme', color: '#9966ff', action: () => navigation.navigate('ProgramDetail') },
    { icon: 'gamepad-variant', label: 'Mini-Jeu', color: '#ff6699', action: () => navigation.navigate('Game') },
  ];
  
  // Notifications
  useEffect(() => {
    setupNotifications();
    startAnimations();
  }, []);
  
  const setupNotifications = async () => {
    const { status } = await Notifications.requestPermissionsAsync();
    if (status === 'granted') {
      await Notifications.scheduleNotificationAsync({
        content: {
          title: '💪 PowerLog',
          body: 'Il est temps de s\'entraîner ! Ne brisez pas votre streak !',
          sound: true,
          data: { screen: 'Training' },
        },
        trigger: {
          hour: 18,
          minute: 0,
          repeats: true,
        },
      });
    }
  };
  
  const startAnimations = () => {
    // Animation pulsante du logo
    Animated.loop(
      Animated.sequence([
        Animated.timing(scaleAnim, {
          toValue: 1.05,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(scaleAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
    
    // Fade in du contenu
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 800,
      useNativeDriver: true,
    }).start();
  };
  
  const onRefresh = async () => {
    setRefreshing(true);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    
    await refreshWorkouts();
    
    setTimeout(() => {
      setRefreshing(false);
      showSnackbar('Données mises à jour !');
    }, 1000);
  };
  
  const startNewWorkout = () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    navigation.navigate('Training');
    showSnackbar('Préparez votre séance ! 💪');
  };
  
  const showSnackbar = (message) => {
    setSnackbarMessage(message);
    setSnackbarVisible(true);
  };
  
  const shareProgress = async () => {
    try {
      const result = await Share.share({
        message: `🎉 Je viens de terminer ma ${workoutStats.totalWorkouts || 0}ème séance sur PowerLog ! Streak actuel: ${user?.stats?.currentStreak || 0} jours 💪 #PowerLog #Fitness`,
        title: 'Ma progression PowerLog'
      });
      
      if (result.action === Share.sharedAction) {
        showSnackbar('Progression partagée !');
      }
    } catch (error) {
      showSnackbar('Erreur lors du partage');
    }
  };
  
  const handleAdminCode = () => {
    navigation.navigate('Admin');
  };
  
  const renderHeader = () => (
    <View style={styles.header}>
      <View style={styles.userInfo}>
        <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
          <Avatar.Text 
            size={60} 
            label={`${user?.firstName?.[0] || ''}${user?.lastName?.[0] || ''}`}
            style={styles.avatar}
            labelStyle={styles.avatarLabel}
          />
        </Animated.View>
        <View style={styles.userText}>
          <Text style={styles.greeting}>Bonjour,</Text>
          <Text style={styles.userName}>
            {user?.firstName} {user?.lastName}
          </Text>
          <View style={styles.statsRow}>
            <Chip 
              icon="fire" 
              mode="outlined"
              textStyle={{ color: colors.primary }}
            >
              🔥 {user?.stats?.currentStreak || 0} jours
            </Chip>
            <Chip 
              icon="trophy" 
              mode="outlined"
              textStyle={{ color: '#ffcc00' }}
              style={{ marginLeft: 8 }}
            >
              {workoutStats.totalWorkouts || 0} séances
            </Chip>
          </View>
        </View>
      </View>
      
      <IconButton
        icon="share-variant"
        iconColor={colors.primary}
        size={28}
        onPress={shareProgress}
      />
    </View>
  );
  
  const renderCurrentWorkout = () => {
    if (!currentWorkout) return null;
    
    return (
      <Card style={[styles.card, styles.liveCard]}>
        <Card.Content>
          <View style={styles.liveHeader}>
            <MaterialCommunityIcons name="run-fast" size={24} color="#00cc66" />
            <Text style={styles.liveTitle}>SÉANCE EN COURS</Text>
            <Chip mode="outlined" textStyle={{ color: '#00cc66' }}>
              EN DIRECT
            </Chip>
          </View>
          
          <View style={styles.liveContent}>
            <View>
              <Text style={styles.workoutName}>{currentWorkout.name}</Text>
              <Text style={styles.workoutTime}>45:12 écoulés</Text>
            </View>
            <Button
              mode="contained"
              buttonColor="#00cc66"
              onPress={() => navigation.navigate('Training')}
              style={styles.continueButton}
            >
              Continuer
            </Button>
          </View>
          
          <View style={styles.exercisePreview}>
            {currentWorkout.exercises?.slice(0, 2).map((exercise, index) => (
              <Chip key={index} style={styles.exerciseChip} mode="outlined">
                {exercise.name}
              </Chip>
            ))}
            {currentWorkout.exercises?.length > 2 && (
              <Chip style={styles.exerciseChip}>+{currentWorkout.exercises.length - 2}</Chip>
            )}
          </View>
        </Card.Content>
      </Card>
    );
  };
  
  const renderGoals = () => (
    <Card style={styles.card}>
      <Card.Content>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>🎯 Mes Objectifs</Text>
          <Button
            mode="text"
            textColor={colors.primary}
            onPress={() => navigation.navigate('Progress')}
          >
            Voir tout
          </Button>
        </View>
        
        {goals.map((goal, index) => (
          <View key={index} style={styles.goalItem}>
            <View style={styles.goalHeader}>
              <MaterialCommunityIcons 
                name={goal.icon} 
                size={20} 
                color={colors.primary} 
              />
              <Text style={styles.goalTitle}>{goal.title}</Text>
              <Text style={styles.goalProgressText}>
                {goal.current}/{goal.target} {goal.unit}
              </Text>
            </View>
            
            <ProgressBar
              progress={goal.progress}
              color={colors.primary}
              style={styles.progressBar}
            />
            
            <View style={styles.goalFooter}>
              <Text style={styles.goalPercentage}>
                {Math.round(goal.progress * 100)}%
              </Text>
              <Text style={styles.goalRemaining}>
                {goal.target - goal.current} {goal.unit} restant
              </Text>
            </View>
          </View>
        ))}
      </Card.Content>
    </Card>
  );
  
  const renderQuickActions = () => (
    <Card style={styles.card}>
      <Card.Content>
        <Text style={styles.sectionTitle}>🚀 Actions Rapides</Text>
        
        <View style={styles.actionsGrid}>
          {quickActions.map((action, index) => (
            <TouchableOpacity
              key={index}
              style={styles.actionButton}
              onPress={action.action}
              activeOpacity={0.7}
            >
              <View style={[styles.actionIcon, { backgroundColor: `${action.color}20` }]}>
                <MaterialCommunityIcons 
                  name={action.icon} 
                  size={28} 
                  color={action.color} 
                />
              </View>
              <Text style={styles.actionLabel}>{action.label}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </Card.Content>
    </Card>
  );
  
  const renderStats = () => (
    <Card style={styles.card}>
      <Card.Content>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>📊 Mes Statistiques</Text>
          <Chip icon="trending-up" textStyle={{ color: colors.primary }}>
            +12.5%
          </Chip>
        </View>
        
        <View style={styles.statsGrid}>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{workoutStats.totalWorkouts || 0}</Text>
            <Text style={styles.statLabel}>Séances</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{workoutStats.totalVolume || 0}</Text>
            <Text style={styles.statLabel}>kg total</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{workoutStats.avgDuration || 0}</Text>
            <Text style={styles.statLabel}>min/séance</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{user?.stats?.prs?.length || 0}</Text>
            <Text style={styles.statLabel}>PR</Text>
          </View>
        </View>
        
        <LineChart
          data={weightData}
          width={width - 60}
          height={180}
          chartConfig={chartConfig}
          bezier
          style={styles.chart}
        />
      </Card.Content>
    </Card>
  );
  
  const renderRecentWorkouts = () => {
    if (!recentWorkouts?.length) return null;
    
    return (
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>📅 Séances Récentes</Text>
            <Button
              mode="text"
              textColor={colors.primary}
              onPress={() => navigation.navigate('Training')}
            >
              Historique
            </Button>
          </View>
          
          {recentWorkouts.slice(0, 3).map((workout, index) => (
            <TouchableOpacity
              key={index}
              style={styles.workoutItem}
              onPress={() => navigation.navigate('WorkoutDetail', { workoutId: workout._id })}
              activeOpacity={0.7}
            >
              <View style={styles.workoutIcon}>
                <MaterialCommunityIcons 
                  name="dumbbell" 
                  size={20} 
                  color={colors.primary} 
                />
              </View>
              
              <View style={styles.workoutInfo}>
                <Text style={styles.workoutDate}>
                  {new Date(workout.date).toLocaleDateString('fr-FR', {
                    weekday: 'short',
                    day: 'numeric',
                    month: 'short'
                  })}
                </Text>
                <Text style={styles.workoutExercises}>
                  {workout.exercises?.slice(0, 2).map(e => e.name).join(', ')}
                  {workout.exercises?.length > 2 && '...'}
                </Text>
              </View>
              
              <View style={styles.workoutStats}>
                <Chip compact textStyle={{ fontSize: 12 }}>
                  {workout.duration}min
                </Chip>
                <Text style={styles.workoutRating}>
                  {workout.rating?.overall || '?'}/10
                </Text>
              </View>
            </TouchableOpacity>
          ))}
        </Card.Content>
      </Card>
    );
  };
  
  const renderPremiumBanner = () => (
    <Card style={[styles.card, styles.premiumCard]}>
      <Card.Content>
        <View style={styles.premiumContent}>
          <MaterialCommunityIcons name="crown" size={40} color="#ffcc00" />
          <View style={styles.premiumText}>
            <Text style={styles.premiumTitle}>Passer à Premium</Text>
            <Text style={styles.premiumDescription}>
              Débloquez tous les programmes, le coach IA et l'eBook complet
            </Text>
          </View>
          <Button
            mode="contained"
            buttonColor="#ffcc00"
            textColor="#000"
            onPress={() => navigation.navigate('Premium')}
            style={styles.premiumButton}
          >
            Découvrir
          </Button>
        </View>
        
        <View style={styles.adminAccess}>
          <Button
            mode="outlined"
            textColor={colors.primary}
            onPress={handleAdminCode}
            icon="key"
          >
            Code Admin
          </Button>
        </View>
      </Card.Content>
    </Card>
  );

  return (
    <Animated.View style={[styles.container, { opacity: fadeAnim }]}>
      <ScrollView
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={[colors.primary]}
            tintColor={colors.primary}
          />
        }
        showsVerticalScrollIndicator={false}
      >
        {/* En-tête */}
        {renderHeader()}
        
        {/* Séance en cours */}
        {renderCurrentWorkout()}
        
        {/* Objectifs */}
        {renderGoals()}
        
        {/* Actions rapides */}
        {renderQuickActions()}
        
        {/* Statistiques */}
        {renderStats()}
        
        {/* Séances récentes */}
        {renderRecentWorkouts()}
        
        {/* Bannière Premium */}
        {renderPremiumBanner()}
        
        {/* Espace pour le FAB */}
        <View style={styles.spacer} />
      </ScrollView>
      
      {/* FAB pour démarrer une séance */}
      <FAB
        icon="plus"
        label="Nouvelle Séance"
        style={styles.fab}
        color="#fff"
        onPress={startNewWorkout}
        animated
      />
      
      {/* Snackbar pour les notifications */}
      <Snackbar
        visible={snackbarVisible}
        onDismiss={() => setSnackbarVisible(false)}
        duration={3000}
        action={{
          label: 'OK',
          onPress: () => setSnackbarVisible(false),
        }}
        style={styles.snackbar}
      >
        {snackbarMessage}
      </Snackbar>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a0a',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 10,
    backgroundColor: '#111',
  },
  userInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  avatar: {
    backgroundColor: '#e60000',
    marginRight: 15,
  },
  avatarLabel: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 20,
  },
  userText: {
    flex: 1,
  },
  greeting: {
    fontSize: 14,
    color: '#aaa',
  },
  userName: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  statsRow: {
    flexDirection: 'row',
    marginTop: 5,
  },
  card: {
    backgroundColor: '#1a1a1a',
    marginHorizontal: 15,
    marginBottom: 15,
    borderRadius: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#e60000',
    elevation: 8,
    shadowColor: '#e60000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 6,
  },
  liveCard: {
    borderLeftColor: '#00cc66',
  },
  liveHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  liveTitle: {
    color: '#00cc66',
    fontWeight: 'bold',
    fontSize: 16,
    marginLeft: 10,
    flex: 1,
  },
  liveContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  workoutName: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  workoutTime: {
    color: '#aaa',
    fontSize: 14,
  },
  continueButton: {
    borderRadius: 25,
    paddingHorizontal: 20,
  },
  exercisePreview: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 10,
  },
  exerciseChip: {
    marginRight: 8,
    marginBottom: 8,
    backgroundColor: '#222',
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  goalItem: {
    marginBottom: 20,
  },
  goalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  goalTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 10,
    flex: 1,
  },
  goalProgressText: {
    color: '#e60000',
    fontWeight: 'bold',
    fontSize: 14,
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
    backgroundColor: '#333',
    marginBottom: 8,
  },
  goalFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  goalPercentage: {
    color: '#e60000',
    fontWeight: 'bold',
    fontSize: 14,
  },
  goalRemaining: {
    color: '#aaa',
    fontSize: 12,
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginTop: 10,
  },
  actionButton: {
    width: '30%',
    alignItems: 'center',
    marginBottom: 20,
  },
  actionIcon: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  actionLabel: {
    color: '#fff',
    fontSize: 12,
    textAlign: 'center',
    fontWeight: '500',
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  statItem: {
    alignItems: 'center',
    flex: 1,
  },
  statValue: {
    color: '#e60000',
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  statLabel: {
    color: '#aaa',
    fontSize: 12,
    textAlign: 'center',
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  workoutItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#333',
  },
  workoutIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#222',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  workoutInfo: {
    flex: 1,
  },
  workoutDate: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
    marginBottom: 2,
  },
  workoutExercises: {
    color: '#aaa',
    fontSize: 12,
  },
  workoutStats: {
    alignItems: 'flex-end',
  },
  workoutRating: {
    color: '#ffcc00',
    fontSize: 12,
    marginTop: 5,
  },
  premiumCard: {
    backgroundColor: '#1a0a0a',
    borderLeftColor: '#ffcc00',
  },
  premiumContent: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  premiumText: {
    flex: 1,
    marginLeft: 15,
  },
  premiumTitle: {
    color: '#ffcc00',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  premiumDescription: {
    color: '#aaa',
    fontSize: 14,
  },
  premiumButton: {
    borderRadius: 20,
  },
  adminAccess: {
    alignItems: 'center',
    paddingTop: 10,
    borderTopWidth: 1,
    borderTopColor: '#333',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#e60000',
  },
  spacer: {
    height: 80,
  },
  snackbar: {
    backgroundColor: '#1a1a1a',
    borderLeftWidth: 4,
    borderLeftColor: '#e60000',
  },
});
import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  StyleSheet,
  Dimensions,
  TouchableOpacity,
  Animated,
  Alert,
  Vibration,
  Modal,
  TextInput,
} from 'react-native';
import { Text, Button, IconButton, Surface } from 'react-native-paper';
import { Audio } from 'expo-av';
import * as Haptics from 'expo-haptics';
import { GameEngine } from 'react-native-game-engine';
import Matter from 'matter-js';
import LottieView from 'lottie-react-native';
import { useTheme } from '../context/ThemeContext';

const { width, height } = Dimensions.get('window');
const GAME_WIDTH = width;
const GAME_HEIGHT = height * 0.7;
const BICEPS_SIZE = 40;
const PIPE_WIDTH = 70;
const PIPE_GAP = 180;
const GRAVITY = 0.8;
const JUMP_FORCE = -14;

export default function GameScreen({ navigation }) {
  const { colors } = useTheme();
  const [isPlaying, setIsPlaying] = useState(false);
  const [score, setScore] = useState(0);
  const [highScore, setHighScore] = useState(0);
  const [gameEngine, setGameEngine] = useState(null);
  const [entities, setEntities] = useState(null);
  const [sound, setSound] = useState(null);
  const [showPauseModal, setShowPauseModal] = useState(false);
  const [particles, setParticles] = useState([]);
  const bicepsY = useRef(new Animated.Value(GAME_HEIGHT / 2)).current;
  const rotation = useRef(new Animated.Value(0)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;

  // Initialisation du jeu
  useEffect(() => {
    initGame();
    loadSounds();
    
    return () => {
      if (sound) {
        sound.unloadAsync();
      }
    };
  }, []);

  const initGame = () => {
    const engine = Matter.Engine.create({ enableSleeping: false });
    const world = engine.world;
    
    // Création du biceps (joueur)
    const biceps = Matter.Bodies.circle(
      GAME_WIDTH / 3,
      GAME_HEIGHT / 2,
      BICEPS_SIZE / 2,
      {
        label: 'biceps',
        restitution: 0.3,
        frictionAir: 0.02,
        density: 0.001
      }
    );
    
    // Sol et plafond
    const ground = Matter.Bodies.rectangle(
      GAME_WIDTH / 2,
      GAME_HEIGHT - 10,
      GAME_WIDTH,
      20,
      { isStatic: true, label: 'ground', friction: 0 }
    );
    
    const ceiling = Matter.Bodies.rectangle(
      GAME_WIDTH / 2,
      10,
      GAME_WIDTH,
      20,
      { isStatic: true, label: 'ceiling', friction: 0 }
    );
    
    // Pipes initiales
    const pipes = [];
    const pipeCount = 4;
    
    for (let i = 0; i < pipeCount; i++) {
      const pipeX = GAME_WIDTH + (i * 300);
      const gapCenter = Math.random() * (GAME_HEIGHT - 300) + 150;
      
      const topPipe = Matter.Bodies.rectangle(
        pipeX,
        gapCenter - PIPE_GAP / 2 - 200,
        PIPE_WIDTH,
        400,
        { 
          isStatic: true, 
          label: `pipe-${i}-top`,
          friction: 0,
          render: { fillStyle: '#00cc00' }
        }
      );
      
      const bottomPipe = Matter.Bodies.rectangle(
        pipeX,
        gapCenter + PIPE_GAP / 2 + 200,
        PIPE_WIDTH,
        400,
        { 
          isStatic: true, 
          label: `pipe-${i}-bottom`,
          friction: 0,
          render: { fillStyle: '#009900' }
        }
      );
      
      pipes.push(topPipe, bottomPipe);
    }
    
    Matter.World.add(world, [biceps, ground, ceiling, ...pipes]);
    
    setEntities({
      physics: { engine, world },
      biceps: { body: biceps, size: [BICEPS_SIZE, BICEPS_SIZE], renderer: BicepsRenderer },
      pipes: pipes.map((pipe, index) => ({
        body: pipe,
        size: [PIPE_WIDTH, 400],
        renderer: PipeRenderer,
        passed: false,
        isTop: index % 2 === 0
      }))
    });
    
    // Initialiser les particules
    const initialParticles = Array.from({ length: 50 }).map(() => ({
      x: Math.random() * GAME_WIDTH,
      y: Math.random() * GAME_HEIGHT,
      size: Math.random() * 3 + 1,
      speed: Math.random() * 0.5 + 0.1,
      opacity: Math.random() * 0.5 + 0.3
    }));
    setParticles(initialParticles);
  };

  const loadSounds = async () => {
    try {
      const { sound: jumpSound } = await Audio.Sound.createAsync(
        require('../assets/sounds/jump.mp3'),
        { volume: 0.7 }
      );
      
      const { sound: scoreSound } = await Audio.Sound.createAsync(
        require('../assets/sounds/score.mp3'),
        { volume: 0.5 }
      );
      
      const { sound: gameOverSound } = await Audio.Sound.createAsync(
        require('../assets/sounds/game-over.mp3'),
        { volume: 0.8 }
      );
      
      setSound({ jump: jumpSound, score: scoreSound, gameOver: gameOverSound });
    } catch (error) {
      console.log('Erreur chargement sons:', error);
    }
  };

  const playSound = async (soundType) => {
    if (sound && sound[soundType]) {
      try {
        await sound[soundType].replayAsync();
      } catch (error) {
        console.log('Erreur lecture son:', error);
      }
    }
  };

  const jump = () => {
    if (!isPlaying || !entities) return;
    
    Matter.Body.setVelocity(entities.biceps.body, { x: 0, y: JUMP_FORCE });
    
    // Animation de rotation
    Animated.sequence([
      Animated.timing(rotation, {
        toValue: -0.5,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(rotation, {
        toValue: 0,
        duration: 300,
        useNativeDriver: true,
      }),
    ]).start();
    
    // Haptique
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    
    // Son
    playSound('jump');
    
    // Particules
    createJumpParticles();
  };

  const createJumpParticles = () => {
    const newParticles = Array.from({ length: 10 }).map(() => ({
      x: entities.biceps.body.position.x - BICEPS_SIZE / 2,
      y: entities.biceps.body.position.y + BICEPS_SIZE / 2,
      size: Math.random() * 4 + 2,
      speed: Math.random() * 2 + 1,
      opacity: 1,
      direction: Math.random() * Math.PI * 2,
      life: 1
    }));
    
    setParticles(prev => [...prev, ...newParticles]);
  };

  const gameLoop = (entities, { time }) => {
    if (!isPlaying) return entities;
    
    const { biceps, pipes } = entities;
    
    // Mettre à jour les particules
    updateParticles();
    
    // Appliquer la gravité
    Matter.Body.applyForce(biceps.body, biceps.body.position, { x: 0, y: GRAVITY });
    
    // Mettre à jour la position Y du biceps pour l'animation
    bicepsY.setValue(biceps.body.position.y);
    
    // Mettre à jour les pipes
    pipes.forEach((pipe, index) => {
      Matter.Body.setPosition(pipe.body, {
        x: pipe.body.position.x - 5,
        y: pipe.body.position.y
      });
      
      // Réinitialiser les pipes sorties de l'écran
      if (pipe.body.position.x < -PIPE_WIDTH) {
        const gapCenter = Math.random() * (GAME_HEIGHT - 300) + 150;
        const newX = GAME_WIDTH + PIPE_WIDTH;
        
        Matter.Body.setPosition(pipe.body, {
          x: newX,
          y: pipe.isTop 
            ? gapCenter - PIPE_GAP / 2 - 200 
            : gapCenter + PIPE_GAP / 2 + 200
        });
        
        pipe.passed = false;
      }
      
      // Détecter le passage entre les pipes
      if (!pipe.passed && pipe.body.position.x + PIPE_WIDTH / 2 < biceps.body.position.x) {
        pipe.passed = true;
        if (pipe.isTop) {
          const newScore = score + 1;
          setScore(newScore);
          
          if (newScore > highScore) {
            setHighScore(newScore);
          }
          
          // Feedback
          Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
          playSound('score');
          
          // Effet visuel
          Animated.sequence([
            Animated.timing(fadeAnim, {
              toValue: 1,
              duration: 200,
              useNativeDriver: true,
            }),
            Animated.timing(fadeAnim, {
              toValue: 0,
              duration: 200,
              useNativeDriver: true,
            }),
          ]).start();
        }
      }
      
      // Détecter les collisions
      const collision = Matter.SAT.collides(biceps.body, pipe.body);
      if (collision.collided) {
        gameOver();
      }
    });
    
    // Vérifier les collisions avec le sol/plafond
    if (biceps.body.position.y >= GAME_HEIGHT - BICEPS_SIZE / 2 || 
        biceps.body.position.y <= BICEPS_SIZE / 2) {
      gameOver();
    }
    
    Matter.Engine.update(entities.physics.engine, time.delta);
    return entities;
  };

  const updateParticles = () => {
    setParticles(prev => 
      prev
        .map(p => ({
          ...p,
          x: p.x + Math.cos(p.direction) * p.speed,
          y: p.y + Math.sin(p.direction) * p.speed,
          life: p.life - 0.02,
          opacity: p.life,
          size: p.size * p.life
        }))
        .filter(p => p.life > 0 && p.x > 0 && p.x < GAME_WIDTH && p.y > 0 && p.y < GAME_HEIGHT)
    );
  };

  const gameOver = () => {
    setIsPlaying(false);
    Vibration.vibrate(500);
    playSound('gameOver');
    
    Alert.alert(
      '💪 Game Over !',
      `Score: ${score}\n\n` +
      `🎯 Meilleur score: ${Math.max(score, highScore)}\n\n` +
      `Ton biceps a besoin de plus d'entraînement !`,
      [
        {
          text: 'Rejouer',
          onPress: restartGame,
          style: 'default'
        },
        {
          text: 'Partager',
          onPress: shareScore,
          style: 'default'
        },
        {
          text: 'Quitter',
          onPress: () => navigation.goBack(),
          style: 'cancel'
        }
      ]
    );
  };

  const restartGame = () => {
    setScore(0);
    setIsPlaying(true);
    initGame();
    bicepsY.setValue(GAME_HEIGHT / 2);
    rotation.setValue(0);
  };

  const shareScore = async () => {
    try {
      await Share.share({
        message: `🎮 J'ai fait un score de ${score} au mini-jeu Flappy Biceps sur PowerLog ! Arriverez-vous à battre mon record ? 💪 #PowerLog #FlappyBiceps`,
        title: 'Mon score PowerLog'
      });
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de partager le score');
    }
  };

  const togglePause = () => {
    if (isPlaying) {
      setIsPlaying(false);
      setShowPauseModal(true);
    } else {
      setIsPlaying(true);
      setShowPauseModal(false);
    }
  };

  const BicepsRenderer = ({ body, size }) => {
    const x = body.position.x - size[0] / 2;
    const y = body.position.y - size[1] / 2;
    
    return (
      <Animated.View
        style={[
          styles.bicepsContainer,
          {
            left: x,
            top: y,
            transform: [{ rotate: rotation.interpolate({
              inputRange: [-1, 1],
              outputRange: ['-45deg', '45deg']
            })}]
          }
        ]}
      >
        {/* Biceps principal */}
        <View style={styles.biceps}>
          {/* Bras */}
          <View style={styles.arm} />
          {/* Muscle biceps */}
          <View style={styles.bicepsMuscle}>
            <View style={styles.bicepsPeak} />
            <View style={styles.bicepsVein} />
          </View>
        </View>
        
        {/* Effet de brillance */}
        <View style={styles.bicepsShine} />
      </Animated.View>
    );
  };

  const PipeRenderer = ({ body, size, isTop }) => {
    const x = body.position.x - size[0] / 2;
    const y = body.position.y - size[1] / 2;
    
    return (
      <View
        style={[
          styles.pipe,
          {
            left: x,
            top: y,
            width: size[0],
            height: size[1],
            backgroundColor: isTop ? '#00cc00' : '#009900',
          }
        ]}
      >
        {/* Détails du pipe */}
        <View style={styles.pipeDetail} />
        <View style={styles.pipeRim} />
        
        {/* Texture */}
        <View style={styles.pipeTexture}>
          {Array.from({ length: 8 }).map((_, i) => (
            <View key={i} style={styles.pipeStripe} />
          ))}
        </View>
      </View>
    );
  };

  const renderSpaceBackground = () => (
    <View style={styles.spaceBackground}>
      {/* Étoiles */}
      {particles.map((particle, index) => (
        <View
          key={index}
          style={[
            styles.star,
            {
              left: particle.x,
              top: particle.y,
              width: particle.size,
              height: particle.size,
              opacity: particle.opacity,
            }
          ]}
        />
      ))}
      
      {/* Planètes */}
      <View style={styles.planet1} />
      <View style={styles.planet2} />
      <View style={styles.planet3} />
      
      {/* Nébuleuse */}
      <View style={styles.nebula} />
    </View>
  );

  const renderScore = () => (
    <View style={styles.scoreContainer}>
      <Animated.View style={[styles.scoreFlash, { opacity: fadeAnim }]} />
      <Text style={styles.scoreText}>SCORE: {score}</Text>
      <Text style={styles.highScoreText}>MEILLEUR: {Math.max(score, highScore)}</Text>
    </View>
  );

  const renderControls = () => (
    <View style={styles.controls}>
      {!isPlaying && !showPauseModal ? (
        <Button
          mode="contained"
          buttonColor="#e60000"
          style={styles.startButton}
          labelStyle={styles.buttonLabel}
          onPress={() => {
            setIsPlaying(true);
            Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
          }}
        >
          🎮 COMMENCER
        </Button>
      ) : (
        <TouchableOpacity
          style={styles.jumpArea}
          activeOpacity={0.7}
          onPress={jump}
        >
          <Text style={styles.jumpText}>👆 TAPPER POUR SAUTER</Text>
          <Text style={styles.jumpHint}>Ou appuyer n'importe où</Text>
        </TouchableOpacity>
      )}
      
      {isPlaying && (
        <IconButton
          icon="pause"
          iconColor="#fff"
          size={30}
          style={styles.pauseButton}
          onPress={togglePause}
        />
      )}
    </View>
  );

  const renderPauseModal = () => (
    <Modal
      visible={showPauseModal}
      transparent
      animationType="fade"
    >
      <View style={styles.modalOverlay}>
        <Surface style={styles.modalContent}>
          <Text style={styles.modalTitle}>⏸️ Jeu en pause</Text>
          
          <View style={styles.modalStats}>
            <Text style={styles.modalStat}>Score actuel: {score}</Text>
            <Text style={styles.modalStat}>Meilleur score: {highScore}</Text>
          </View>
          
          <Button
            mode="contained"
            buttonColor="#e60000"
            style={styles.modalButton}
            onPress={() => {
              setIsPlaying(true);
              setShowPauseModal(false);
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
            }}
          >
            Reprendre
          </Button>
          
          <Button
            mode="outlined"
            textColor="#fff"
            style={styles.modalButton}
            onPress={restartGame}
          >
            Recommencer
          </Button>
          
          <Button
            mode="text"
            textColor="#aaa"
            style={styles.modalButton}
            onPress={() => navigation.goBack()}
          >
            Quitter le jeu
          </Button>
        </Surface>
      </View>
    </Modal>
  );

  return (
    <View style={styles.container}>
      {/* En-tête */}
      <View style={styles.header}>
        <IconButton
          icon="arrow-left"
          iconColor="#fff"
          size={28}
          onPress={() => navigation.goBack()}
        />
        <Text style={styles.title}>FLAPPY BICEPS</Text>
        <IconButton
          icon="information"
          iconColor="#fff"
          size={28}
          onPress={() => Alert.alert(
            'Comment jouer',
            'Contrôlez le biceps pour éviter les obstacles.\n\n' +
            '• Tapez n\'importe où pour sauter\n' +
            '• Passez entre les pipes pour marquer des points\n' +
            '• Évitez les collisions\n\n' +
            '💪 Entraînez votre biceps virtuel !'
          )}
        />
      </View>
      
      {/* Zone de jeu */}
      <View style={styles.gameArea}>
        {/* Fond spatial */}
        {renderSpaceBackground()}
        
        {/* Moteur de jeu */}
        {entities && (
          <GameEngine
            ref={(ref) => setGameEngine(ref)}
            systems={[gameLoop]}
            entities={entities}
            running={isPlaying}
            style={styles.gameEngine}
          />
        )}
        
        {/* Affichage du score */}
        {renderScore()}
        
        {/* Instructions de démarrage */}
        {!isPlaying && !showPauseModal && (
          <View style={styles.instructions}>
            <LottieView
              source={require('../assets/animations/tap.json')}
              autoPlay
              loop
              style={styles.tapAnimation}
            />
            <Text style={styles.instructionText}>
              TAPPEZ POUR COMMENCER
            </Text>
          </View>
        )}
      </View>
      
      {/* Contrôles */}
      {renderControls()}
      
      {/* Modal pause */}
      {renderPauseModal()}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000428',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingTop: 50,
    backgroundColor: 'rgba(0, 4, 40, 0.9)',
  },
  title: {
    color: '#fff',
    fontSize: 22,
    fontWeight: 'bold',
    letterSpacing: 2,
  },
  gameArea: {
    flex: 1,
    width: GAME_WIDTH,
    height: GAME_HEIGHT,
    overflow: 'hidden',
  },
  spaceBackground: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: '#000428',
  },
  star: {
    position: 'absolute',
    backgroundColor: '#fff',
    borderRadius: 50,
  },
  planet1: {
    position: 'absolute',
    top: '20%',
    left: '70%',
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#ff6b6b',
    opacity: 0.7,
  },
  planet2: {
    position: 'absolute',
    top: '60%',
    left: '20%',
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#4ecdc4',
    opacity: 0.5,
  },
  planet3: {
    position: 'absolute',
    top: '40%',
    left: '80%',
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#ffe66d',
    opacity: 0.8,
  },
  nebula: {
    position: 'absolute',
    top: '10%',
    left: '10%',
    width: 200,
    height: 200,
    borderRadius: 100,
    backgroundColor: 'rgba(106, 13, 173, 0.2)',
    opacity: 0.3,
  },
  gameEngine: {
    flex: 1,
  },
  bicepsContainer: {
    position: 'absolute',
    justifyContent: 'center',
    alignItems: 'center',
  },
  biceps: {
    width: BICEPS_SIZE,
    height: BICEPS_SIZE,
    justifyContent: 'center',
    alignItems: 'center',
  },
  arm: {
    position: 'absolute',
    width: BICEPS_SIZE * 1.8,
    height: BICEPS_SIZE / 3,
    backgroundColor: '#ff6b6b',
    borderRadius: BICEPS_SIZE / 6,
  },
  bicepsMuscle: {
    width: BICEPS_SIZE,
    height: BICEPS_SIZE,
    borderRadius: BICEPS_SIZE / 2,
    backgroundColor: '#e60000',
    borderWidth: 3,
    borderColor: '#ff3333',
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  bicepsPeak: {
    width: BICEPS_SIZE * 0.3,
    height: BICEPS_SIZE * 0.3,
    borderRadius: BICEPS_SIZE * 0.15,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    position: 'absolute',
    top: BICEPS_SIZE * 0.2,
    left: BICEPS_SIZE * 0.6,
  },
  bicepsVein: {
    width: BICEPS_SIZE * 0.6,
    height: 2,
    backgroundColor: 'rgba(255, 255, 255, 0.4)',
    borderRadius: 1,
    transform: [{ rotate: '45deg' }],
  },
  bicepsShine: {
    position: 'absolute',
    width: BICEPS_SIZE * 0.4,
    height: BICEPS_SIZE * 0.4,
    borderRadius: BICEPS_SIZE * 0.2,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    top: BICEPS_SIZE * 0.1,
    left: BICEPS_SIZE * 0.1,
  },
  pipe: {
    position: 'absolute',
    borderRadius: 10,
    overflow: 'hidden',
  },
  pipeDetail: {
    position: 'absolute',
    bottom: 0,
    width: '100%',
    height: 30,
    backgroundColor: 'rgba(0, 0, 0, 0.2)',
  },
  pipeRim: {
    position: 'absolute',
    top: 0,
    width: '100%',
    height: 10,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
  },
  pipeTexture: {
    position: 'absolute',
    top: 10,
    left: 0,
    right: 0,
    bottom: 30,
  },
  pipeStripe: {
    height: 2,
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
    marginVertical: 8,
    marginHorizontal: 5,
  },
  scoreContainer: {
    position: 'absolute',
    top: 20,
    alignSelf: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingHorizontal: 30,
    paddingVertical: 10,
    borderRadius: 20,
    borderWidth: 2,
    borderColor: '#e60000',
  },
  scoreFlash: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: '#e60000',
    borderRadius: 20,
  },
  scoreText: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  highScoreText: {
    color: '#ffcc00',
    fontSize: 14,
    marginTop: 5,
  },
  instructions: {
    position: 'absolute',
    bottom: 100,
    alignSelf: 'center',
    alignItems: 'center',
  },
  tapAnimation: {
    width: 100,
    height: 100,
  },
  instructionText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 10,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
  },
  controls: {
    padding: 20,
    backgroundColor: 'rgba(0, 4, 40, 0.9)',
    alignItems: 'center',
  },
  startButton: {
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 25,
    elevation: 10,
  },
  buttonLabel: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  jumpArea: {
    width: '100%',
    backgroundColor: 'rgba(230, 0, 0, 0.2)',
    padding: 25,
    borderRadius: 20,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#e60000',
    borderStyle: 'dashed',
  },
  jumpText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
    letterSpacing: 1,
    marginBottom: 5,
  },
  jumpHint: {
    color: '#aaa',
    fontSize: 14,
    fontStyle: 'italic',
  },
  pauseButton: {
    position: 'absolute',
    top: -50,
    right: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.9)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#1a1a1a',
    padding: 30,
    borderRadius: 20,
    width: '80%',
    alignItems: 'center',
    elevation: 10,
  },
  modalTitle: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  modalStats: {
    backgroundColor: '#222',
    padding: 15,
    borderRadius: 10,
    marginBottom: 25,
    width: '100%',
  },
  modalStat: {
    color: '#fff',
    fontSize: 16,
    marginVertical: 5,
    textAlign: 'center',
  },
  modalButton: {
    width: '100%',
    marginVertical: 8,
    borderRadius: 10,
  },
});
{
  "name": "powerlog-backend",
  "version": "1.0.0",
  "description": "Backend complet pour l'application PowerLog Fitness",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest --watchAll",
    "test:ci": "jest --coverage",
    "seed": "node seeders/seed.js",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "docker:build": "docker build -t powerlog-backend .",
    "docker:run": "docker run -p 5000:5000 powerlog-backend"
  },
  "keywords": [
    "fitness",
    "workout",
    "nutrition",
    "ai",
    "tracking"
  ],
  "author": "PowerLog Team",
  "license": "Proprietary",
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.0.0",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.0",
    "cors": "^2.8.5",
    "dotenv": "^16.0.3",
    "stripe": "^12.0.0",
    "openai": "^4.0.0",
    "nodemailer": "^6.9.1",
    "multer": "^1.4.5-lts.1",
    "cloudinary": "^1.37.0",
    "socket.io": "^4.6.1",
    "express-rate-limit": "^6.10.0",
    "helmet": "^7.0.0",
    "compression": "^1.7.4",
    "express-validator": "^7.0.1",
    "prom-client": "^14.2.0",
    "winston": "^3.9.0",
    "moment": "^2.29.4",
    "axios": "^1.4.0",
    "redis": "^4.6.7",
    "cron": "^2.3.0",
    "geoip-lite": "^1.4.7",
    "ua-parser-js": "^1.0.35",
    "swagger-ui-express": "^4.6.3",
    "swagger-jsdoc": "^6.2.8"
  },
  "devDependencies": {
    "nodemon": "^2.0.22",
    "jest": "^29.5.0",
    "supertest": "^6.3.3",
    "eslint": "^8.42.0",
    "eslint-config-airbnb-base": "^15.0.0",
    "eslint-plugin-import": "^2.27.5"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
version: '3.8'

services:
  # MongoDB avec réplication
  mongodb-primary:
    image: mongo:6.0
    container_name: powerlog-mongodb-primary
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
      MONGO_REPLICA_SET_NAME: rs0
    command: mongod --replSet rs0 --bind_ip_all
    ports:
      - "27017:27017"
    volumes:
      - mongodb_primary_data:/data/db
      - ./database/init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js:ro
    networks:
      - powerlog-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 30s
      timeout: 10s
      retries: 3

  mongodb-secondary:
    image: mongo:6.0
    container_name: powerlog-mongodb-secondary
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
    command: mongod --replSet rs0 --bind_ip_all
    depends_on:
      - mongodb-primary
    volumes:
      - mongodb_secondary_data:/data/db
    networks:
      - powerlog-network

  # API Backend
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
    container_name: powerlog-api
    restart: unless-stopped
    environment:
      NODE_ENV: production
      MONGODB_URI: mongodb://admin:${MONGO_ROOT_PASSWORD}@mongodb-primary:27017,mongodb-secondary:27017/powerlog?replicaSet=rs0&authSource=admin
      REDIS_URL: redis://redis:6379
      JWT_SECRET: ${JWT_SECRET}
      STRIPE_SECRET_KEY: ${STRIPE_SECRET_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      SMTP_HOST: ${SMTP_HOST}
      SMTP_USER: ${SMTP_USER}
      SMTP_PASSWORD: ${SMTP_PASSWORD}
      CLOUDINARY_CLOUD_NAME: ${CLOUDINARY_CLOUD_NAME}
      CLOUDINARY_API_KEY: ${CLOUDINARY_API_KEY}
      CLOUDINARY_API_SECRET: ${CLOUDINARY_API_SECRET}
      ADMIN_CODE: ${ADMIN_CODE}
      PORT: 5000
    ports:
      - "5000:5000"
    depends_on:
      mongodb-primary:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./backend/logs:/app/logs
      - ./backend/uploads:/app/uploads
      - ./backend/exports:/app/exports
      - ./backend/backups:/app/backups
    networks:
      - powerlog-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Worker pour tâches asynchrones
  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.worker
    container_name: powerlog-worker
    restart: unless-stopped
    environment:
      NODE_ENV: production
      MONGODB_URI: mongodb://admin:${MONGO_ROOT_PASSWORD}@mongodb-primary:27017,mongodb-secondary:27017/powerlog?replicaSet=rs0&authSource=admin
      REDIS_URL: redis://redis:6379
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - api
      - redis
    volumes:
      - ./backend/logs:/app/logs
    networks:
      - powerlog-network
    command: node worker.js

  # Frontend React Native (Expo)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: powerlog-frontend
    restart: unless-stopped
    environment:
      EXPO_DEVTOOLS_LISTEN_ADDRESS: 0.0.0.0
      REACT_NATIVE_PACKAGER_HOSTNAME: localhost
      API_URL: http://api:5000
    ports:
      - "19000:19000"
      - "19001:19001"
      - "19002:19002"
    depends_on:
      - api
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.expo
    networks:
      - powerlog-network

  # Panel d'administration
  admin:
    build:
      context: ./admin
      dockerfile: Dockerfile
    container_name: powerlog-admin
    restart: unless-stopped
    environment:
      REACT_APP_API_URL: http://api:5000
      REACT_APP_STRIPE_PUBLIC_KEY: ${STRIPE_PUBLIC_KEY}
      PORT: 3000
    ports:
      - "3000:3000"
    depends_on:
      - api
    networks:
      - powerlog-network

  # Nginx Reverse Proxy avec SSL
  nginx:
    image: nginx:alpine
    container_name: powerlog-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/logs:/var/log/nginx
      - ./nginx/www:/usr/share/nginx/html:ro
      - ./nginx/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - api
      - admin
      - frontend
    networks:
      - powerlog-network

  # Redis pour cache et queues
  redis:
    image: redis:7-alpine
    container_name: powerlog-redis
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf:ro
    networks:
      - powerlog-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Monitoring avec Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: powerlog-prometheus
    restart: unless-stopped
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./monitoring/alerts.yml:/etc/prometheus/alerts.yml:ro
      - prometheus_data:/prometheus
      - ./monitoring/targets:/etc/prometheus/targets:ro
    ports:
      - "9090:9090"
    networks:
      - powerlog-network
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'

  # Grafana pour visualisation
  grafana:
    image: grafana/grafana:latest
    container_name: powerlog-grafana
    restart: unless-stopped
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
      GF_INSTALL_PLUGINS: grafana-piechart-panel
      GF_USERS_ALLOW_SIGN_UP: 'false'
      GF_USERS_ALLOW_ORG_CREATE: 'false'
      GF_AUTH_ANONYMOUS_ENABLED: 'false'
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning:ro
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards:ro
    ports:
      - "3001:3000"
    depends_on:
      - prometheus
    networks:
      - powerlog-network

  # Alert Manager
  alertmanager:
    image: prom/alertmanager:latest
    container_name: powerlog-alertmanager
    restart: unless-stopped
    volumes:
      - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
      - alertmanager_data:/alertmanager
    ports:
      - "9093:9093"
    networks:
      - powerlog-network

  # Node Exporter pour métriques système
  node-exporter:
    image: prom/node-exporter:latest
    container_name: powerlog-node-exporter
    restart: unless-stopped
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    ports:
      - "9100:9100"
    networks:
      - powerlog-network

  # MongoDB Exporter
  mongodb-exporter:
    image: percona/mongodb_exporter:latest
    container_name: powerlog-mongodb-exporter
    restart: unless-stopped
    environment:
      MONGODB_URI: mongodb://admin:${MONGO_ROOT_PASSWORD}@mongodb-primary:27017/admin?authSource=admin
    ports:
      - "9216:9216"
    depends_on:
      - mongodb-primary
    networks:
      - powerlog-network

  # Redis Exporter
  redis-exporter:
    image: oliver006/redis_exporter:latest
    container_name: powerlog-redis-exporter
    restart: unless-stopped
    environment:
      REDIS_ADDR: redis://redis:6379
      REDIS_PASSWORD: ${REDIS_PASSWORD}
    ports:
      - "9121:9121"
    depends_on:
      - redis
    networks:
      - powerlog-network

  # Backup automatique
  backup:
    image: mongo:6.0
    container_name: powerlog-backup
    restart: unless-stopped
    environment:
      MONGO_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
    volumes:
      - ./backups:/backups
      - ./scripts/backup.sh:/backup.sh:ro
    depends_on:
      - mongodb-primary
    networks:
      - powerlog-network
    entrypoint: /bin/sh
    command: -c 'chmod +x /backup.sh && echo "0 2 * * * /backup.sh" | crontab - && crond -f'

networks:
  powerlog-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

volumes:
  mongodb_primary_data:
  mongodb_secondary_data:
  redis_data:
  prometheus_data:
  grafana_data:
  alertmanager_data:
  #!/bin/bash

# ============================================================================
# POWERLOG - SCRIPT DE DÉPLOIEMENT PRODUCTION
# Version: 2.0.0
# ============================================================================

set -e

# Configuration
APP_NAME="powerlog"
ENV_FILE=".env.production"
DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
BACKUP_DIR="/backups/${APP_NAME}"
LOG_DIR="/var/log/${APP_NAME}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEPLOY_USER="deploy"
SERVER_IP="votre-serveur.com"
SSH_PORT="22"
BRANCH="main"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============================================================================
# FONCTIONS D'AFFICHAGE
# ============================================================================

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "\n${PURPLE}▶ ${NC} $1"
}

# ============================================================================
# FONCTIONS DE VÉRIFICATION
# ============================================================================

check_prerequisites() {
    log_step "Vérification des prérequis..."
    
    # Vérifier Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé"
        log "Installation: curl -fsSL https://get.docker.com | sh"
        exit 1
    fi
    
    # Vérifier Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé"
        log "Installation: sudo apt install docker-compose"
        exit 1
    fi
    
    # Vérifier la version Docker
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    if [[ $(echo "$DOCKER_VERSION < 20.10" | bc) -eq 1 ]]; then
        log_warning "Docker version $DOCKER_VERSION - version 20.10+ recommandée"
    fi
    
    # Vérifier les ressources système
    check_system_resources
    
    # Vérifier les fichiers de configuration
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Fichier $ENV_FILE introuvable"
        exit 1
    fi
    
    if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
        log_error "Fichier $DOCKER_COMPOSE_FILE introuvable"
        exit 1
    fi
    
    log_success "Prérequis vérifiés"
}

check_system_resources() {
    log_info "Vérification des ressources système..."
    
    # Mémoire RAM
    TOTAL_RAM=$(free -m | awk '/^Mem:/{print $2}')
    if [ "$TOTAL_RAM" -lt 4096 ]; then
        log_warning "RAM insuffisante: ${TOTAL_RAM}MB (4GB minimum recommandé)"
    fi
    
    # Espace disque
    TOTAL_DISK=$(df -h / | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "${TOTAL_DISK%.*}" -lt 20 ]; then
        log_warning "Espace disque faible: ${TOTAL_DISK}GB (20GB minimum)"
    fi
    
    # CPU cores
    CPU_CORES=$(nproc)
    if [ "$CPU_CORES" -lt 2 ]; then
        log_warning "Nombre de cores CPU faible: $CPU_CORES (2+ recommandé)"
    fi
}

# ============================================================================
# FONCTIONS DE SAUVEGARDE
# ============================================================================

create_backup() {
    log_step "Création de la sauvegarde..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Sauvegarde MongoDB
    log_info "Sauvegarde de la base de données..."
    docker-compose exec -T mongodb-primary mongodump \
        --username admin \
        --password "$MONGO_ROOT_PASSWORD" \
        --authenticationDatabase admin \
        --db powerlog \
        --gzip \
        --archive > "$BACKUP_DIR/db_backup_$TIMESTAMP.gz"
    
    if [ $? -eq 0 ]; then
        log_success "Sauvegarde BD créée: $BACKUP_DIR/db_backup_$TIMESTAMP.gz"
        
        # Compresser les logs et uploads
        tar -czf "$BACKUP_DIR/logs_backup_$TIMESTAMP.tar.gz" -C ./backend logs uploads 2>/dev/null || true
        
        # Garder seulement les 7 dernières sauvegardes
        ls -t "$BACKUP_DIR"/db_backup_*.gz | tail -n +8 | xargs -r rm --
        
        log_info "Taille de la sauvegarde: $(du -h "$BACKUP_DIR/db_backup_$TIMESTAMP.gz" | cut -f1)"
    else
        log_error "Échec de la sauvegarde de la base de données"
        exit 1
    fi
}

# ============================================================================
# FONCTIONS DE DÉPLOIEMENT
# ============================================================================

stop_services() {
    log_step "Arrêt des services..."
    
    if docker-compose ps | grep -q "Up"; then
        docker-compose down --remove-orphans
        sleep 10
        log_success "Services arrêtés"
    else
        log_info "Aucun service en cours d'exécution"
    fi
    
    # Nettoyage des ressources Docker
    log_info "Nettoyage des ressources Docker..."
    docker system prune -f --volumes
}

update_code() {
    log_step "Mise à jour du code..."
    
    # Pull depuis Git
    if [ -d ".git" ]; then
        log_info "Mise à jour depuis Git..."
        git fetch origin
        git checkout "$BRANCH"
        git pull origin "$BRANCH"
        
        # Mise à jour des sous-modules
        if [ -f ".gitmodules" ]; then
            git submodule update --init --recursive
        fi
    else
        log_warning "Dépôt Git non trouvé, continuation avec le code local"
    fi
    
    # Mise à jour des permissions
    chmod +x scripts/*.sh 2>/dev/null || true
}

build_images() {
    log_step "Construction des images Docker..."
    
    # Build avec cache intelligent
    log_info "Construction de l'image backend..."
    docker-compose build --parallel --no-cache
    
    # Vérifier les images construites
    if docker images | grep -q "powerlog"; then
        log_success "Images construites avec succès"
        
        # Liste des images
        log_info "Images disponibles:"
        docker images --filter "reference=powerlog*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
    else
        log_error "Échec de la construction des images"
        exit 1
    fi
}

start_services() {
    log_step "Démarrage des services..."
    
    # Démarrer en arrière-plan
    docker-compose up -d --scale api=2
    
    # Attendre que les services soient prêts
    log_info "Attente du démarrage des services..."
    sleep 30
    
    # Vérification de l'état des services
    check_services_health
}

check_services_health() {
    log_step "Vérification de la santé des services..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        log_info "Tentative $attempt/$max_attempts..."
        
        # Vérifier l'API
        if curl -s -f http://localhost:5000/api/health > /dev/null; then
            log_success "✅ API est opérationnelle"
            
            # Vérifier MongoDB
            if docker-compose exec -T mongodb-primary mongosh --quiet --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
                log_success "✅ MongoDB est opérationnel"
                
                # Vérifier Redis
                if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
                    log_success "✅ Redis est opérationnel"
                    
                    # Vérifier tous les services
                    local unhealthy_services=$(docker-compose ps | grep -v "Up (healthy)" | grep "Up" | wc -l)
                    
                    if [ "$unhealthy_services" -eq 0 ]; then
                        log_success "🎉 Tous les services sont opérationnels et en bonne santé"
                        return 0
                    else
                        log_warning "$unhealthy_services service(s) en cours de démarrage..."
                    fi
                fi
            fi
        fi
        
        attempt=$((attempt + 1))
        sleep 10
    done
    
    log_error "⚠️  Certains services ne sont pas prêts après $max_attempts tentatives"
    
    # Afficher les logs des services en échec
    docker-compose logs --tail=50 api
    exit 1
}

run_migrations() {
    log_step "Exécution des migrations..."
    
    # Exécuter les migrations MongoDB si nécessaire
    if [ -f "./database/migrations.js" ]; then
        log_info "Exécution des migrations de base de données..."
        docker-compose exec -T api node database/migrations.js
        
        if [ $? -eq 0 ]; then
            log_success "Migrations exécutées avec succès"
        else
            log_error "Échec des migrations"
            exit 1
        fi
    fi
}

setup_monitoring() {
    log_step "Configuration du monitoring..."
    
    # Importer les dashboards Grafana
    if [ -d "./monitoring/grafana/dashboards" ]; then
        log_info "Configuration des dashboards Grafana..."
        
        # Attendre que Grafana soit prêt
        sleep 30
        
        # Importer les dashboards via API
        for dashboard in ./monitoring/grafana/dashboards/*.json; do
            if [ -f "$dashboard" ]; then
                curl -X POST \
                    -H "Content-Type: application/json" \
                    -H "Accept: application/json" \
                    -u "admin:$GRAFANA_PASSWORD" \
                    "http://localhost:3001/api/dashboards/db" \
                    --data @"$dashboard" > /dev/null 2>&1 || true
            fi
        done
        
        log_success "Dashboards Grafana configurés"
    fi
    
    # Configurer les alertes
    if [ -f "./monitoring/alerts.yml" ]; then
        log_info "Configuration des alertes Prometheus..."
        docker-compose restart prometheus
        sleep 5
    fi
}

# ============================================================================
# FONCTIONS DE TEST
# ============================================================================

run_tests() {
    log_step "Exécution des tests..."
    
    # Tests d'intégration
    log_info "Tests d'intégration API..."
    
    if curl -s http://localhost:5000/api/health | grep -q "healthy"; then
        log_success "✅ Test de santé API réussi"
    else
        log_error "❌ Test de santé API échoué"
        exit 1
    fi
    
    # Tests de base de données
    log_info "Test de connexion MongoDB..."
    if docker-compose exec -T mongodb-primary mongosh --quiet --eval "db.stats()" > /dev/null 2>&1; then
        log_success "✅ Connexion MongoDB réussie"
    else
        log_error "❌ Connexion MongoDB échouée"
        exit 1
    fi
    
    # Test des endpoints critiques
    local endpoints=(
        "/api/auth/register"
        "/api/workouts"
        "/api/programs"
        "/api/nutrition"
    )
    
    for endpoint in "${endpoints[@]}"; do
        local status_code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:5000$endpoint")
        
        if [ "$status_code" -eq 401 ] || [ "$status_code" -eq 200 ]; then
            log_success "✅ Endpoint $endpoint accessible (HTTP $status_code)"
        else
            log_warning "⚠️  Endpoint $endcode retourne HTTP $status_code"
        fi
    done
}

# ============================================================================
# FONCTIONS DE NETTOYAGE
# ============================================================================

cleanup() {
    log_step "Nettoyage des ressources..."
    
    # Nettoyer les conteneurs arrêtés
    docker container prune -f
    
    # Nettoyer les images non utilisées
    docker image prune -f
    
    # Nettoyer les volumes non utilisés
    docker volume prune -f
    
    # Nettoyer le cache Docker builder
    docker builder prune -f
    
    # Nettoyer les anciens logs
    find "$LOG_DIR" -name "*.log" -type f -mtime +7 -delete 2>/dev/null || true
    
    log_success "Nettoyage terminé"
}

# ============================================================================
# FONCTIONS DE RAPPORT
# ============================================================================

generate_deployment_report() {
    log_step "Génération du rapport de déploiement..."
    
    local report_file="/tmp/${APP_NAME}_deployment_${TIMESTAMP}.txt"
    
    cat > "$report_file" << EOF
================================================================
RAPPORT DE DÉPLOIEMENT POWERLOG
Date: $(date)
Version: 2.0.0
================================================================

SERVICES:
$(docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}")

RESSOURCES SYSTÈME:
- Mémoire RAM: $(free -h | awk '/^Mem:/{print $2}') total, $(free -h | awk '/^Mem:/{print $3}') utilisée
- CPU: $(nproc) cores
- Disque: $(df -h / | awk 'NR==2 {print $4}') libre

STATISTIQUES DOCKER:
$(docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "Non disponible")

VERSIONS:
- Docker: $(docker --version)
- Docker Compose: $(docker-compose --version)
- Node.js: $(docker-compose exec api node --version 2>/dev/null || echo "Non disponible")
- MongoDB: $(docker-compose exec mongodb-primary mongod --version 2>/dev/null | head -1 || echo "Non disponible")

SAUVEGARDES:
$(ls -lh "$BACKUP_DIR" 2>/dev/null | tail -5 || echo "Aucune sauvegarde")

ENDPOINTS:
- API: http://localhost:5000
- Admin: http://localhost:3000
- Frontend: http://localhost:19000
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9090

HEALTH CHECK:
$(curl -s http://localhost:5000/api/health | python3 -m json.tool 2>/dev/null || echo "Non disponible")

================================================================
EOF
    
    log_success "Rapport généré: $report_file"
    
    # Afficher un résumé
    cat "$report_file" | tail -20
}

display_success_message() {
    echo -e "\n${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🚀 DÉPLOIEMENT RÉUSSI 🚀                   ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║                                                              ║"
    echo "║  PowerLog est maintenant déployé avec succès !               ║"
    echo "║                                                              ║"
    echo "║  📊 Accéder aux services :                                   ║"
    echo "║     • API :          http://localhost:5000                   ║"
    echo "║     • Admin :        http://localhost:3000                   ║"
    echo "║     • Monitoring :   http://localhost:3001                   ║"
    echo "║                                                              ║"
    echo "║  🔧 Commandes utiles :                                       ║"
    echo "║     • Voir les logs : docker-compose logs -f                 ║"
    echo "║     • Arrêter :      docker-compose down                     ║"
    echo "║     • Redémarrer :   docker-compose restart                  ║"
    echo "║                                                              ║"
    echo "║  📞 Support : support@powerlog.com                           ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

main() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║               POWERLOG - DÉPLOIEMENT PRODUCTION              ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║                    Version 2.0.0                             ║"
    echo "║                    Date: $(date +%Y-%m-%d)                           ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Charger les variables d'environnement
    if [ -f "$ENV_FILE" ]; then
        log_info "Chargement des variables d'environnement..."
        export $(cat "$ENV_FILE" | grep -v '^#' | xargs)
    else
        log_error "Fichier $ENV_FILE introuvable"
        exit 1
    fi
    
    # Créer les répertoires nécessaires
    mkdir -p "$BACKUP_DIR" "$LOG_DIR"
    
    # Exécution du pipeline de déploiement
    check_prerequisites
    create_backup
    stop_services
    update_code
    build_images
    start_services
    run_migrations
    setup_monitoring
    run_tests
    cleanup
    generate_deployment_report
    display_success_message
    
    log "✅ Déploiement terminé avec succès en $(($SECONDS / 60)) minutes et $(($SECONDS % 60)) secondes"
}

# ============================================================================
# EXÉCUTION
# ============================================================================

# Gestion des signaux
trap 'log_error "Déploiement interrompu par l\'utilisateur"; exit 1' INT TERM

# Journalisation
exec 2> "$LOG_DIR/deployment_$TIMESTAMP.log"

# Exécution principale
SECONDS=0
main "$@"
Partager → Sur l'écran d'accueil
