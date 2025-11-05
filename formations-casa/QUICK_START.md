# 🚀 Quick Start - formations.casa

## Démarrage Rapide en 5 Minutes

### 1️⃣ Charger les Données en Français (IMPORTANT!)

```bash
cd formations-casa/backend
source venv/bin/activate
python manage.py create_initial_data
```

**✅ Cela créera:**
- 21 catégories (dont 6 sous-catégories tech)
- 9 types de formations
- **120 badges** en français
- 8 accomplissements
- 30 fonctionnalités

### 2️⃣ Lancer le Backend

```bash
# Créer un superuser si pas encore fait
python manage.py createsuperuser
# Username: admin
# Email: admin@formations.casa
# Password: (votre mot de passe)

# Lancer le serveur
python manage.py runserver
```

**Accès:**
- 🌐 API: http://localhost:8000/api/
- 👨‍💼 Admin: http://localhost:8000/admin/
- 📚 Docs: http://localhost:8000/api/docs/

### 3️⃣ Lancer le Frontend

**Terminal 2:**
```bash
cd formations-casa/frontend
npm install
cp .env.local.example .env.local
npm run dev
```

**Accès:**
- 🏠 Site: http://localhost:3000
- 🔐 Connexion: http://localhost:3000/login
- ✍️ Inscription: http://localhost:3000/register
- 📚 Formations: http://localhost:3000/formations
- 📊 Dashboard: http://localhost:3000/dashboard

## 🎯 Test de la Plateforme

### Test 1: S'inscrire comme Apprenant

1. Aller sur http://localhost:3000/register
2. Sélectionner "Apprenant"
3. Remplir le formulaire
4. Se connecter automatiquement
5. Accéder au dashboard

### Test 2: S'inscrire comme Formateur

1. Aller sur http://localhost:3000/register
2. Sélectionner "Formateur / Coach"
3. Remplir le formulaire
4. **Note:** Le compte nécessite une approbation admin

### Test 3: Approuver un Formateur

1. Se connecter à l'admin: http://localhost:8000/admin/
2. Aller dans "Accounts" > "Users"
3. Sélectionner l'utilisateur formateur
4. Cocher "Is approved"
5. Sauvegarder

### Test 4: Créer une Formation

1. Se connecter à l'admin en tant que formateur approuvé
2. Aller dans "Formations" > "Formations" > "Add Formation"
3. Remplir:
   - Titre: "Formation Python Débutant"
   - Catégorie: "Informatique et Technologie" > "Développement Web"
   - Prix: 2000 MAD
   - Date de début: (choisir une date future)
   - Mode: Présentiel/En ligne/Hybride
   - Status: "Published"
4. Ajouter des items de curriculum
5. Sauvegarder

### Test 5: Parcourir les Formations

1. Aller sur http://localhost:3000/formations
2. Rechercher des formations
3. Filtrer par catégorie/niveau
4. Cliquer sur une formation pour voir les détails

## 📊 Données Créées

### Catégories Populaires
- 💻 Informatique et Technologie
- 🗣️ Langues
- 💼 Business et Management
- 📱 Marketing et Communication
- 🎨 Design et Créativité
- Et 10 autres...

### Types de Formations
- Formation Courte
- Bootcamp
- Masterclass
- Cours du Soir
- Et 5 autres...

### 120 Badges (Exemples)

**Débutant:**
- 👶 Premier Pas (10 pts)
- 🔍 Explorateur (20 pts)
- ✅ Profil Complet (25 pts)

**Participation:**
- 🎓 Première Inscription (50 pts)
- 💪 Apprenant Actif (100 pts)
- 👑 Maître (500 pts)
- 💎 Légende (2000 pts)

**Spécial Maroc:**
- 🌙 Ramadan Studieux (100 pts)
- 🎊 Aïd Moubarak (150 pts)
- 🇲🇦 Fête du Trône (200 pts)
- 🎆 Fête de l'Indépendance (200 pts)

**Rare:**
- 🌟 Membre Fondateur (1000 pts) - RARE
- 💎 VIP (1000 pts) - RARE

## 🛠️ Fonctionnalités Disponibles

### Pour les Apprenants
- ✅ Parcourir les formations
- ✅ S'inscrire aux formations
- ✅ Voir son dashboard
- ✅ Gagner des badges et points
- ⏳ Voir ses badges (à venir)
- ⏳ Laisser des avis (à venir)

### Pour les Formateurs
- ✅ Créer des formations (via admin)
- ✅ Gérer le curriculum
- ⏳ Voir les inscriptions (à venir)
- ⏳ Gérer les paiements (à venir)
- ⏳ Dashboard formateur complet (à venir)

### Pour les Centres
- ✅ Créer un centre (via admin)
- ✅ Ajouter des salles
- ✅ Définir les disponibilités
- ⏳ Dashboard centre (à venir)

### Pour les Admins
- ✅ Tout gérer via l'admin Django
- ✅ Approuver utilisateurs
- ✅ Gérer les catégories
- ✅ Créer des badges
- ✅ Configurer les fonctionnalités

## 🎨 Interface

### Pages Disponibles
- 🏠 Page d'accueil avec hero section
- 🔐 Connexion
- ✍️ Inscription (avec choix de rôle)
- 📚 Liste des formations (avec recherche et filtres)
- 📖 Détail d'une formation (avec curriculum)
- 📊 Dashboard (adapté par rôle)

### Composants
- Navbar avec état d'authentification
- Cartes de formations
- Formulaires stylés
- Messages d'erreur et de succès

## 🇲🇦 Spécificités Maroc

### Langue
- ✅ 100% en français
- ⏳ Support arabe à venir
- ⏳ Support anglais à venir

### Localisation
- ✅ Fuseau horaire: Africa/Casablanca
- ✅ Devise: MAD
- ✅ Format de date: DD/MM/YYYY
- ✅ Événements marocains dans les badges

### Paiement
- ✅ Support RIB (Relevé d'Identité Bancaire)
- ✅ Virement bancaire
- ✅ Upload de preuve de paiement
- ✅ Réconciliation manuelle

## 🐛 Dépannage

### Le backend ne démarre pas
```bash
# Vérifier que le venv est activé
source venv/bin/activate

# Réinstaller les dépendances
pip install -r requirements.txt

# Refaire les migrations
python manage.py makemigrations
python manage.py migrate
```

### Le frontend ne démarre pas
```bash
# Supprimer node_modules et réinstaller
rm -rf node_modules package-lock.json
npm install

# Vérifier le fichier .env.local
cat .env.local
# Devrait contenir: NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Les données ne sont pas chargées
```bash
# Relancer la commande de création des données
python manage.py create_initial_data

# Vérifier dans l'admin
# Aller sur http://localhost:8000/admin/
# Formations > Categories (devrait voir 15 catégories)
# Gamification > Badges (devrait voir 120 badges)
```

### Erreur CORS
```bash
# Vérifier que CORS est configuré dans backend/config/settings.py
# CORS_ALLOWED_ORIGINS devrait inclure http://localhost:3000
```

## 📚 Documentation

- **README.md** - Vue d'ensemble complète
- **SETUP.md** - Guide de configuration détaillé
- **FRENCH_DATA_SUMMARY.md** - Détails sur toutes les données en français
- **PROJECT_SUMMARY.md** - Résumé du projet

## 🎯 Prochaines Étapes Recommandées

1. **Créer des formations de test** via l'admin
2. **Tester le flux d'inscription** complet
3. **Implémenter le système de réservation**
4. **Ajouter les dashboards spécifiques** (coach, centre)
5. **Implémenter l'attribution automatique des badges**
6. **Ajouter les notifications par email**

## 💡 Conseils

- **Utilisez l'admin Django** pour gérer tout le contenu
- **Tous les badges sont en français** et adaptés au Maroc
- **Les fonctionnalités sont à 0 crédits** - Vous pouvez les modifier dans l'admin
- **Approuvez les formateurs** manuellement via l'admin
- **Les formations** peuvent être créées via l'admin ou l'API

## 🆘 Support

Questions? Consultez:
1. Les fichiers README.md et SETUP.md
2. La documentation API: http://localhost:8000/api/docs/
3. L'admin Django: http://localhost:8000/admin/

---

**Plateforme:** formations.casa
**Version:** 1.0
**Date:** 2025-11-05
**Marché:** Casablanca, Maroc 🇲🇦
