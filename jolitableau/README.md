# JoliTableau.com
## La galerie d'art en ligne 🎨

**JoliTableau** est une plateforme d'art en ligne complète et professionnelle conçue pour connecter artistes, galeries et collectionneurs du monde entier. Initialement optimisée pour le marché francophone (France, Belgique, Suisse, Québec, Afrique francophone), elle offre une expérience multilingue native (français, anglais, espagnol).

---

## 🌟 Fonctionnalités Principales

### 👤 Gestion des Utilisateurs
- **Profils personnalisés** : Artistes, Galeries, Collectionneurs
- **Authentification sécurisée** : Email-based avec Django Allauth
- **Vérification** : Badges vérifiés (SIRET, Maison des Artistes, CCI)
- **Conseil des Sages** : Conseil consultatif élitaire (max 20 membres)

### 🖼️ Œuvres d'Art
- **Portfolio complet** : Upload HD, vidéos 360°, modèles AR
- **Multi-langue** : Descriptions en français, anglais, espagnol
- **Provenance blockchain** : NFT d'authenticité non-spéculatif
- **Catégories** : Peinture, Sculpture, Photographie, Art numérique

### 🏛️ Galeries & Expositions
- **Galeries personnalisées** : Grille, carrousel, mosaïque
- **Expositions virtuelles** : Avec invitations privées
- **QR codes dynamiques** : Pour chaque œuvre, galerie, exposition
- **Visite AR** : Visualiser dans son salon via mobile

### 🌐 Domaines Personnalisés (White-Label)
- **Sous-domaine gratuit** : `nom.jolitableau.com`
- **Domaine personnalisé** : `artiste.com` (9,99€/mois après essai 30j)
- **Branding 100%** : Logo, couleurs, sans mention JoliTableau
- **SSL automatique** : Let's Encrypt

### 📧 Communication RGPD
- **Listes de diffusion privées** : Opt-in, anonymisées
- **WhatsApp Broadcast** : Via Twilio (0,05€/message ou forfait)
- **Templates pro** : Tracking ouvertures/clics
- **Double opt-in** : Conformité RGPD totale

### 💰 Marketplace & Paiements
- **Vente d'œuvres** : Prix fixe, enchères, prix sur demande
- **Paiements flexibles** : Stripe, Mollie, PayPal, Lydia
- **Escrow** : Paiement sécurisé
- **Commission** : 10% configurable par admin

### 🎯 Monétisation Premium
- Domaine personnalisé : **9,99€/mois**
- Boost visibilité : **4,99€/mois**
- WhatsApp broadcast : **0,05€/msg** ou forfait
- Listing foire partenaire : **49€/événement**
- Beta : **Tout gratuit ou prix symbolique**

### 🗳️ Conseil des Sages
- Vote hebdomadaire "Œuvre du Jour/Semaine"
- Curation thématique
- Dashboard privé : votes anonymes, chat, sondages
- Badge prestige : "Sage de l'Art"

### 📊 Analytics & Outils Pro
- Dashboards : vues, conversions, démographie
- SEO intégré
- Google Analytics, Meta Pixel
- Partenariats foires : Art Basel, FIAC

---

## 🏗️ Architecture Technique

### Stack
- **Backend** : Django 5.2, Python 3.11+
- **Database** : PostgreSQL (AWS RDS)
- **Cache/Queue** : Redis, Celery
- **Search** : Elasticsearch
- **Storage** : AWS S3 + CloudFront
- **Payments** : Stripe, Mollie
- **Messaging** : Twilio (WhatsApp)
- **Frontend** : Tailwind CSS, HTMX, WebSockets (Channels)

### Apps Django
```
jolitableau/
├── core/               # QR codes, domaines, multi-tenant, settings
├── users/              # Profils (artistes, galeries, collectionneurs)
├── artworks/           # Œuvres, provenance, catégories
├── galleries/          # Galeries, expositions virtuelles
├── community/          # Événements, forum
├── conseil/            # Conseil des Sages, votes
├── marketplace/        # Ventes, enchères, commandes
├── communications/     # Mailing lists, WhatsApp (Twilio)
├── payments/           # Transactions, abonnements, monétisation
├── verification/       # Badges, certifications
└── analytics/          # Dashboards, statistiques, tracking
```

---

## 🚀 Installation & Démarrage

### Prérequis
- Python 3.11+
- PostgreSQL 13+ (ou SQLite pour dev)
- Redis 6+ (optionnel pour dev)
- Elasticsearch 8+ (optionnel pour dev)

### 1. Cloner le dépôt
```bash
git clone https://github.com/votre-org/jolitableau.git
cd jolitableau
```

### 2. Installer les dépendances
```bash
pip install -r ../jolitableau-requirements.txt
```

### 3. Configuration
```bash
cp .env.example .env
# Éditer .env avec vos clés API
```

### 4. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer un superuser
```bash
python manage.py createsuperuser
```

### 6. Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

### 7. Lancer le serveur
```bash
python manage.py runserver
```

Accédez à : **http://localhost:8000**
Admin : **http://localhost:8000/admin**

---

## 🌍 Internationalisation (i18n)

Le projet supporte **3 langues** nativement :
- **Français** (défaut)
- Anglais
- Espagnol

### Générer les traductions
```bash
# Extraire les strings à traduire
python manage.py makemessages -l en
python manage.py makemessages -l es

# Compiler les traductions
python manage.py compilemessages
```

---

## 🔐 Sécurité

- **HTTPS forcé** en production
- **HSTS** activé
- **CSP** (Content Security Policy)
- **CSRF protection**
- **2FA** disponible pour paiements
- **Permissions objets** via Django Guardian
- **RGPD compliant** : double opt-in, anonymisation emails

---

## ☁️ Déploiement AWS

### Services requis
- **EC2 / ECS Fargate** : Django
- **RDS PostgreSQL** : Database
- **S3 + CloudFront** : Médias statiques
- **Route 53** : Domaines personnalisés
- **Certificate Manager** : SSL automatique
- **ElastiCache Redis** : Celery + Channels
- **CloudWatch + Sentry** : Monitoring

### Configuration Environnement
```bash
# Activer PostgreSQL
USE_POSTGRES=True
DB_HOST=your-rds-endpoint.amazonaws.com

# Activer S3
USE_S3=True
AWS_STORAGE_BUCKET_NAME=jolitableau-media
```

---

## 📦 Fonctionnalités Avancées

### QR Codes Dynamiques
Chaque œuvre, galerie, exposition génère automatiquement :
- QR code scannable → page dédiée
- Formats : PNG, SVG, PDF imprimable
- Analytics : nombre de scans, dernière date

### Multi-Tenant
Le middleware `MultiTenantMiddleware` détecte automatiquement :
- Sous-domaines : `picasso.jolitableau.com`
- Domaines personnalisés : `artiste.com` (CNAME)

### WhatsApp Broadcast
1. Artiste/galerie rédige message
2. Admin valide (anti-spam)
3. Envoi groupé via Twilio
4. Tracking : envoyés, délivrés, échecs
5. Facturation automatique

### Blockchain Provenance
- Hash de transaction enregistré
- NFT d'authenticité (non-spéculatif)
- Historique immuable

---

## 🧪 Tests

```bash
# Lancer les tests
pytest

# Coverage
pytest --cov=. --cov-report=html
```

---

## 📚 Documentation Admin

### Configurer les prix (Django Admin)
1. Accédez à **Site Settings**
2. Modifiez :
   - `domain_monthly_price` : Prix domaine (défaut 9,99€)
   - `boost_monthly_price` : Boost visibilité (défaut 4,99€)
   - `whatsapp_message_price` : WhatsApp (défaut 0,05€)
   - `commission_rate` : Taux commission (défaut 10%)

### Inviter au Conseil des Sages
1. Accédez à **Users > User Profile**
2. Cochez `is_sage`
3. L'utilisateur reçoit badge "Sage de l'Art"

### Approuver WhatsApp Broadcast
1. Accédez à **Communications > WhatsApp Broadcast**
2. Status : `PENDING_APPROVAL`
3. Bouton **Approve** ou **Reject**

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez :
1. Fork le projet
2. Créer une branche : `git checkout -b feature/ma-fonctionnalite`
3. Commit : `git commit -m "feat: ajouter fonctionnalité"`
4. Push : `git push origin feature/ma-fonctionnalite`
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet est sous licence propriétaire. Tous droits réservés © 2025 JoliTableau.

---

## 📞 Contact

- **Email** : contact@jolitableau.com
- **Support** : support@jolitableau.com
- **Site** : https://jolitableau.com

---

## 🎨 Slogan

> **« Une œuvre. Un QR. Un domaine. Une communauté. »**
> **Élégance. Expertise. Exclusivité. Éternité.**

---

**Démarrez en français. Dominez le monde de l'art.** 🌍🎨
