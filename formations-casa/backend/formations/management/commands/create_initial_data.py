from django.core.management.base import BaseCommand
from django.utils.text import slugify
from formations.models import Category, FormationType
from gamification.models import Badge, Achievement
from features.models import Feature


class Command(BaseCommand):
    help = 'Crée les données initiales en français pour le marché marocain'

    def handle(self, *args, **kwargs):
        self.stdout.write('Création des données initiales en français...\n')

        # Create Categories
        self.create_categories()

        # Create Formation Types
        self.create_formation_types()

        # Create Badges (100+)
        self.create_badges()

        # Create Achievements
        self.create_achievements()

        # Create Features
        self.create_features()

        self.stdout.write(self.style.SUCCESS('\n✅ Données initiales créées avec succès!'))

    def create_categories(self):
        self.stdout.write('\n📁 Création des catégories...')

        categories = [
            {
                'name': 'Informatique et Technologie',
                'description': 'Formations en développement web, mobile, cybersécurité, intelligence artificielle',
                'icon': '💻'
            },
            {
                'name': 'Langues',
                'description': 'Apprentissage des langues : Français, Anglais, Espagnol, Arabe, Allemand',
                'icon': '🗣️'
            },
            {
                'name': 'Business et Management',
                'description': 'Gestion d\'entreprise, leadership, stratégie, entrepreneuriat',
                'icon': '💼'
            },
            {
                'name': 'Marketing et Communication',
                'description': 'Marketing digital, réseaux sociaux, branding, communication d\'entreprise',
                'icon': '📱'
            },
            {
                'name': 'Finance et Comptabilité',
                'description': 'Comptabilité, analyse financière, fiscalité, audit',
                'icon': '💰'
            },
            {
                'name': 'Design et Créativité',
                'description': 'Design graphique, UX/UI, photographie, vidéo, architecture',
                'icon': '🎨'
            },
            {
                'name': 'Développement Personnel',
                'description': 'Confiance en soi, prise de parole, gestion du temps, intelligence émotionnelle',
                'icon': '🌟'
            },
            {
                'name': 'Ressources Humaines',
                'description': 'Recrutement, gestion des talents, droit du travail, paie',
                'icon': '👥'
            },
            {
                'name': 'Santé et Bien-être',
                'description': 'Yoga, nutrition, méditation, coaching sportif, premiers secours',
                'icon': '🧘'
            },
            {
                'name': 'Artisanat et Métiers',
                'description': 'Cuisine, pâtisserie, couture, menuiserie, électricité, plomberie',
                'icon': '🔨'
            },
            {
                'name': 'Commerce et Vente',
                'description': 'Techniques de vente, négociation, relation client, commerce international',
                'icon': '🛍️'
            },
            {
                'name': 'Juridique',
                'description': 'Droit des affaires, droit du travail, droit immobilier, conformité',
                'icon': '⚖️'
            },
            {
                'name': 'Immobilier',
                'description': 'Gestion immobilière, promotion immobilière, estimation, investissement',
                'icon': '🏠'
            },
            {
                'name': 'Transport et Logistique',
                'description': 'Supply chain, douanes, transport international, gestion des stocks',
                'icon': '🚚'
            },
            {
                'name': 'Tourisme et Hôtellerie',
                'description': 'Accueil, restauration, gestion hôtelière, guide touristique',
                'icon': '🏨'
            },
        ]

        # Create subcategories for Informatique
        tech_subcats = [
            {'name': 'Développement Web', 'parent': 'Informatique et Technologie', 'icon': '🌐'},
            {'name': 'Développement Mobile', 'parent': 'Informatique et Technologie', 'icon': '📱'},
            {'name': 'Data Science et IA', 'parent': 'Informatique et Technologie', 'icon': '🤖'},
            {'name': 'Cybersécurité', 'parent': 'Informatique et Technologie', 'icon': '🔒'},
            {'name': 'Cloud Computing', 'parent': 'Informatique et Technologie', 'icon': '☁️'},
            {'name': 'DevOps', 'parent': 'Informatique et Technologie', 'icon': '⚙️'},
        ]

        for cat_data in categories:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ {cat.name}')

        # Create subcategories
        for subcat in tech_subcats:
            parent = Category.objects.get(name=subcat['parent'])
            cat, created = Category.objects.get_or_create(
                name=subcat['name'],
                defaults={
                    'slug': slugify(subcat['name']),
                    'description': '',
                    'icon': subcat['icon'],
                    'parent': parent,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'    ↳ {cat.name}')

    def create_formation_types(self):
        self.stdout.write('\n📚 Création des types de formations...')

        types = [
            {'name': 'Formation Courte', 'description': 'Formation intensive de quelques jours'},
            {'name': 'Formation Longue', 'description': 'Formation approfondie sur plusieurs semaines/mois'},
            {'name': 'Atelier Pratique', 'description': 'Session pratique axée sur la mise en application'},
            {'name': 'Bootcamp', 'description': 'Formation intensive et immersive'},
            {'name': 'Séminaire', 'description': 'Conférence et présentation sur un sujet spécifique'},
            {'name': 'Certification', 'description': 'Formation menant à une certification reconnue'},
            {'name': 'Masterclass', 'description': 'Formation avancée avec un expert'},
            {'name': 'Cours du Soir', 'description': 'Formation en soirée pour les professionnels'},
            {'name': 'Formation Continue', 'description': 'Formation pour le développement professionnel continu'},
        ]

        for type_data in types:
            ftype, created = FormationType.objects.get_or_create(
                name=type_data['name'],
                defaults={'description': type_data['description']}
            )
            if created:
                self.stdout.write(f'  ✓ {ftype.name}')

    def create_badges(self):
        self.stdout.write('\n🏆 Création des badges (100+)...')

        badges = [
            # BEGINNER BADGES (20)
            {'name': 'Premier Pas', 'category': 'beginner', 'description': 'Inscription sur la plateforme', 'icon': '👶', 'points': 10},
            {'name': 'Explorateur', 'category': 'beginner', 'description': 'Consulter 10 formations', 'icon': '🔍', 'points': 20},
            {'name': 'Curieux', 'category': 'beginner', 'description': 'Parcourir 5 catégories différentes', 'icon': '🤔', 'points': 15},
            {'name': 'Profil Complet', 'category': 'beginner', 'description': 'Compléter 100% de votre profil', 'icon': '✅', 'points': 25},
            {'name': 'Photo de Profil', 'category': 'beginner', 'description': 'Ajouter une photo de profil', 'icon': '📸', 'points': 10},
            {'name': 'Bienvenue', 'category': 'beginner', 'description': 'Première connexion', 'icon': '👋', 'points': 5},
            {'name': 'Découvreur', 'category': 'beginner', 'description': 'Visiter 3 centres de formation', 'icon': '🗺️', 'points': 15},
            {'name': 'Chercheur', 'category': 'beginner', 'description': 'Utiliser la fonction recherche', 'icon': '🔎', 'points': 10},
            {'name': 'Favori', 'category': 'beginner', 'description': 'Ajouter une formation en favori', 'icon': '⭐', 'points': 10},
            {'name': 'Planificateur', 'category': 'beginner', 'description': 'Consulter le calendrier', 'icon': '📅', 'points': 10},
            {'name': 'Informé', 'category': 'beginner', 'description': 'Lire 3 articles de blog', 'icon': '📰', 'points': 15},
            {'name': 'Connecté', 'category': 'beginner', 'description': 'Se connecter 7 jours consécutifs', 'icon': '🔗', 'points': 30},
            {'name': 'Matinal', 'category': 'beginner', 'description': 'Se connecter avant 8h', 'icon': '🌅', 'points': 10},
            {'name': 'Nocturne', 'category': 'beginner', 'description': 'Se connecter après 22h', 'icon': '🌙', 'points': 10},
            {'name': 'Week-end Warrior', 'category': 'beginner', 'description': 'Consulter des formations le week-end', 'icon': '🏖️', 'points': 15},
            {'name': 'Mobile User', 'category': 'beginner', 'description': 'Se connecter depuis un mobile', 'icon': '📱', 'points': 10},
            {'name': 'Partage', 'category': 'beginner', 'description': 'Partager une formation sur les réseaux sociaux', 'icon': '🔄', 'points': 20},
            {'name': 'Recommandation', 'category': 'beginner', 'description': 'Recommander la plateforme à un ami', 'icon': '🤝', 'points': 25},
            {'name': 'Newsletter', 'category': 'beginner', 'description': 'S\'inscrire à la newsletter', 'icon': '📧', 'points': 15},
            {'name': 'Explorateur Pro', 'category': 'beginner', 'description': 'Consulter le profil de 10 formateurs', 'icon': '👔', 'points': 20},

            # PARTICIPATION BADGES (25)
            {'name': 'Première Inscription', 'category': 'participation', 'description': 'S\'inscrire à sa première formation', 'icon': '🎓', 'points': 50},
            {'name': 'Apprenant Actif', 'category': 'participation', 'description': 'Participer à 5 formations', 'icon': '📚', 'points': 100},
            {'name': 'Étudiant Dévoué', 'category': 'participation', 'description': 'Compléter 10 formations', 'icon': '🎯', 'points': 200},
            {'name': 'Maître', 'category': 'participation', 'description': 'Compléter 25 formations', 'icon': '🏅', 'points': 500},
            {'name': 'Expert', 'category': 'participation', 'description': 'Compléter 50 formations', 'icon': '👑', 'points': 1000},
            {'name': 'Légende', 'category': 'participation', 'description': 'Compléter 100 formations', 'icon': '💎', 'points': 2000},
            {'name': 'Présence Parfaite', 'category': 'participation', 'description': '100% de présence à une formation', 'icon': '✨', 'points': 75},
            {'name': 'Jamais en Retard', 'category': 'participation', 'description': 'Arriver à l\'heure à 10 sessions', 'icon': '⏰', 'points': 50},
            {'name': 'Assidu', 'category': 'participation', 'description': '100% présence sur 3 formations', 'icon': '💪', 'points': 150},
            {'name': 'Marathon', 'category': 'participation', 'description': 'Suivre une formation de plus de 40h', 'icon': '🏃', 'points': 100},
            {'name': 'Sprint', 'category': 'participation', 'description': 'Compléter une formation en moins de 7 jours', 'icon': '⚡', 'points': 75},
            {'name': 'Week-end Intensif', 'category': 'participation', 'description': 'Suivre une formation le week-end', 'icon': '📖', 'points': 50},
            {'name': 'Formation du Soir', 'category': 'participation', 'description': 'Suivre 5 formations en soirée', 'icon': '🌆', 'points': 60},
            {'name': 'En Ligne', 'category': 'participation', 'description': 'Compléter 5 formations à distance', 'icon': '💻', 'points': 75},
            {'name': 'En Présentiel', 'category': 'participation', 'description': 'Compléter 5 formations en présentiel', 'icon': '🏢', 'points': 75},
            {'name': 'Hybride', 'category': 'participation', 'description': 'Suivre une formation hybride', 'icon': '🔀', 'points': 50},
            {'name': 'Multi-centres', 'category': 'participation', 'description': 'Suivre des formations dans 3 centres différents', 'icon': '🏛️', 'points': 100},
            {'name': 'Casablanca Explorer', 'category': 'participation', 'description': 'Visiter 5 centres à Casablanca', 'icon': '🌆', 'points': 80},
            {'name': 'Apprenant Rapide', 'category': 'participation', 'description': 'Terminer une formation avec mention excellent', 'icon': '🚀', 'points': 150},
            {'name': 'Régularité', 'category': 'participation', 'description': 'Suivre au moins 1 formation par mois pendant 6 mois', 'icon': '📊', 'points': 200},
            {'name': 'Année Productive', 'category': 'participation', 'description': 'Compléter 12 formations en un an', 'icon': '🗓️', 'points': 300},
            {'name': 'Été Studieux', 'category': 'participation', 'description': 'Suivre 3 formations pendant l\'été', 'icon': '☀️', 'points': 75},
            {'name': 'Rentrée Active', 'category': 'participation', 'description': 'S\'inscrire à 3 formations en septembre', 'icon': '🍂', 'points': 75},
            {'name': 'Fin d\'Année', 'category': 'participation', 'description': 'Compléter 5 formations avant la fin d\'année', 'icon': '🎄', 'points': 100},
            {'name': 'Ramadan Studieux', 'category': 'participation', 'description': 'Suivre une formation pendant le Ramadan', 'icon': '🌙', 'points': 100},

            # ACHIEVEMENT BADGES (25)
            {'name': 'Lève-tôt', 'category': 'achievement', 'description': 'S\'inscrire dans les 24h du lancement', 'icon': '🐦', 'points': 100},
            {'name': 'Perfectionniste', 'category': 'achievement', 'description': 'Obtenir 100% dans 5 formations', 'icon': '💯', 'points': 200},
            {'name': 'Excellence', 'category': 'achievement', 'description': 'Moyenne générale supérieure à 90%', 'icon': '🌟', 'points': 250},
            {'name': 'Sans Échec', 'category': 'achievement', 'description': 'Réussir 20 formations d\'affilée', 'icon': '🎭', 'points': 300},
            {'name': 'Premier de la Classe', 'category': 'achievement', 'description': 'Être dans le top 3 d\'une formation', 'icon': '🥇', 'points': 150},
            {'name': 'Leader', 'category': 'achievement', 'description': 'Être 1er au classement mensuel', 'icon': '👑', 'points': 400},
            {'name': 'Podium', 'category': 'achievement', 'description': 'Être dans le top 10 au classement général', 'icon': '🏆', 'points': 350},
            {'name': 'Montée Rapide', 'category': 'achievement', 'description': 'Gagner 1000 points en un mois', 'icon': '📈', 'points': 150},
            {'name': 'Millionnaire', 'category': 'achievement', 'description': 'Atteindre 10000 points', 'icon': '💰', 'points': 500},
            {'name': 'Collectionneur', 'category': 'achievement', 'description': 'Obtenir 50 badges différents', 'icon': '🎖️', 'points': 300},
            {'name': 'Niveau 10', 'category': 'achievement', 'description': 'Atteindre le niveau 10', 'icon': '🔟', 'points': 200},
            {'name': 'Niveau 25', 'category': 'achievement', 'description': 'Atteindre le niveau 25', 'icon': '2️⃣5️⃣', 'points': 500},
            {'name': 'Paiement Rapide', 'category': 'achievement', 'description': 'Payer dans les 24h après inscription', 'icon': '💳', 'points': 50},
            {'name': 'Fidèle', 'category': 'achievement', 'description': 'Utiliser la plateforme pendant 1 an', 'icon': '🎂', 'points': 400},
            {'name': 'Ancien', 'category': 'achievement', 'description': 'Membre depuis 2 ans', 'icon': '🏛️', 'points': 800},
            {'name': 'Vétéran', 'category': 'achievement', 'description': 'Membre depuis 5 ans', 'icon': '⚡', 'points': 2000},
            {'name': 'Certificat d\'Or', 'category': 'achievement', 'description': 'Obtenir 10 certifications', 'icon': '📜', 'points': 500},
            {'name': 'Débloqueur', 'category': 'achievement', 'description': 'Débloquer tous les badges d\'une catégorie', 'icon': '🔓', 'points': 250},
            {'name': 'Challenge Accepté', 'category': 'achievement', 'description': 'Compléter un défi spécial', 'icon': '🎯', 'points': 200},
            {'name': 'Record Personnel', 'category': 'achievement', 'description': 'Battre son meilleur score', 'icon': '📊', 'points': 100},
            {'name': 'Série Gagnante', 'category': 'achievement', 'description': '10 formations consécutives réussies', 'icon': '🔥', 'points': 200},
            {'name': 'Investissement', 'category': 'achievement', 'description': 'Dépenser plus de 10000 MAD en formations', 'icon': '💎', 'points': 300},
            {'name': 'Tout Payé', 'category': 'achievement', 'description': 'Payer 20 formations à temps', 'icon': '✅', 'points': 150},
            {'name': 'Booké', 'category': 'achievement', 'description': 'Avoir 3 formations réservées en même temps', 'icon': '📅', 'points': 100},
            {'name': 'Planificateur Pro', 'category': 'achievement', 'description': 'Planifier 6 mois de formations à l\'avance', 'icon': '📋', 'points': 200},

            # SOCIAL BADGES (15)
            {'name': 'Premier Avis', 'category': 'social', 'description': 'Laisser un premier avis', 'icon': '💬', 'points': 25},
            {'name': 'Critique', 'category': 'social', 'description': 'Laisser 10 avis', 'icon': '📝', 'points': 75},
            {'name': 'Influenceur', 'category': 'social', 'description': 'Avoir 50 avis utiles', 'icon': '⭐', 'points': 150},
            {'name': 'Leader d\'Opinion', 'category': 'social', 'description': '100 avis publiés', 'icon': '🎤', 'points': 300},
            {'name': 'Constructif', 'category': 'social', 'description': 'Laisser un avis détaillé de plus de 200 mots', 'icon': '✍️', 'points': 50},
            {'name': 'Ambassadeur', 'category': 'social', 'description': 'Parrainer 5 amis', 'icon': '🤝', 'points': 200},
            {'name': 'Recruteur', 'category': 'social', 'description': 'Parrainer 10 personnes', 'icon': '👥', 'points': 400},
            {'name': 'Réseau', 'category': 'social', 'description': 'Se connecter avec 20 autres apprenants', 'icon': '🌐', 'points': 100},
            {'name': 'Populaire', 'category': 'social', 'description': 'Avoir 50 followers', 'icon': '👏', 'points': 150},
            {'name': 'Célébrité', 'category': 'social', 'description': 'Avoir 100 followers', 'icon': '🌟', 'points': 300},
            {'name': 'Contributeur', 'category': 'social', 'description': 'Aider 10 autres utilisateurs dans les forums', 'icon': '🆘', 'points': 100},
            {'name': 'Mentor', 'category': 'social', 'description': 'Guider un nouvel utilisateur', 'icon': '🧙', 'points': 150},
            {'name': 'Social Butterfly', 'category': 'social', 'description': 'Interagir avec 30 utilisateurs différents', 'icon': '🦋', 'points': 120},
            {'name': 'Photographe', 'category': 'social', 'description': 'Partager 10 photos de formations', 'icon': '📷', 'points': 75},
            {'name': 'Viral', 'category': 'social', 'description': 'Avoir un post partagé 100 fois', 'icon': '🔥', 'points': 250},

            # EXPERT BADGES (20)
            {'name': 'Spécialiste Tech', 'category': 'expert', 'description': 'Compléter toutes les formations Tech', 'icon': '💻', 'points': 500},
            {'name': 'Expert Langues', 'category': 'expert', 'description': 'Maîtriser 3 langues via la plateforme', 'icon': '🗣️', 'points': 600},
            {'name': 'Pro du Business', 'category': 'expert', 'description': 'Compléter 15 formations business', 'icon': '💼', 'points': 400},
            {'name': 'Maître Marketing', 'category': 'expert', 'description': 'Expert en marketing digital', 'icon': '📱', 'points': 450},
            {'name': 'Génie Financier', 'category': 'expert', 'description': 'Compléter toutes les formations finance', 'icon': '💰', 'points': 500},
            {'name': 'Designer Pro', 'category': 'expert', 'description': 'Maîtriser tous les outils de design', 'icon': '🎨', 'points': 450},
            {'name': 'Développeur Full Stack', 'category': 'expert', 'description': 'Maîtriser front-end et back-end', 'icon': '⚙️', 'points': 600},
            {'name': 'Data Scientist', 'category': 'expert', 'description': 'Expert en data science et IA', 'icon': '🤖', 'points': 700},
            {'name': 'Polyvalent', 'category': 'expert', 'description': 'Compléter des formations dans 10 catégories', 'icon': '🎭', 'points': 800},
            {'name': 'Renaissance', 'category': 'expert', 'description': 'Maîtriser 5 domaines différents', 'icon': '🎨', 'points': 1000},
            {'name': 'Certifié Pro', 'category': 'expert', 'description': 'Obtenir 5 certifications professionnelles', 'icon': '📜', 'points': 500},
            {'name': 'Expert Reconnu', 'category': 'expert', 'description': 'Avoir une moyenne de 95% sur 20 formations', 'icon': '🏆', 'points': 600},
            {'name': 'Maître Formateur', 'category': 'expert', 'description': 'Suivre une formation de formateurs', 'icon': '👨‍🏫', 'points': 400},
            {'name': 'Bilingue', 'category': 'expert', 'description': 'Suivre des formations en 2 langues', 'icon': '🌍', 'points': 200},
            {'name': 'Trilingue', 'category': 'expert', 'description': 'Suivre des formations en 3 langues', 'icon': '🌎', 'points': 400},
            {'name': 'Casablanca Expert', 'category': 'expert', 'description': 'Connaître tous les centres de Casablanca', 'icon': '🏙️', 'points': 300},
            {'name': 'Connaissance Approfondie', 'category': 'expert', 'description': 'Passer plus de 500h en formation', 'icon': '⏳', 'points': 1000},
            {'name': 'Investisseur Formation', 'category': 'expert', 'description': 'Investir 50000 MAD dans sa formation', 'icon': '💎', 'points': 800},
            {'name': 'Formation Express', 'category': 'expert', 'description': 'Compléter 5 formations en 1 mois', 'icon': '⚡', 'points': 400},
            {'name': 'Élite', 'category': 'expert', 'description': 'Atteindre le top 1% des utilisateurs', 'icon': '👑', 'points': 2000},

            # SPECIAL EVENT BADGES (15)
            {'name': 'Membre Fondateur', 'category': 'special', 'description': 'Parmi les 100 premiers inscrits', 'icon': '🌟', 'points': 1000, 'is_rare': True},
            {'name': 'Beta Testeur', 'category': 'special', 'description': 'Participant à la phase beta', 'icon': '🧪', 'points': 500, 'is_rare': True},
            {'name': 'Jour du Lancement', 'category': 'special', 'description': 'Inscrit le jour du lancement', 'icon': '🚀', 'points': 200, 'is_rare': True},
            {'name': 'Anniversaire 1 an', 'category': 'special', 'description': 'Présent au 1er anniversaire', 'icon': '🎂', 'points': 300},
            {'name': 'Nouvel An 2025', 'category': 'special', 'description': 'Formation terminée pendant les fêtes 2025', 'icon': '🎉', 'points': 150},
            {'name': 'Ramadan 2025', 'category': 'special', 'description': 'Formation suivie pendant Ramadan', 'icon': '🌙', 'points': 200},
            {'name': 'Aïd Moubarak', 'category': 'special', 'description': 'Actif pendant l\'Aïd', 'icon': '🎊', 'points': 150},
            {'name': 'Fête du Trône', 'category': 'special', 'description': 'Formation le jour de la Fête du Trône', 'icon': '🇲🇦', 'points': 200},
            {'name': 'Fête de l\'Indépendance', 'category': 'special', 'description': 'Actif le 18 novembre', 'icon': '🎆', 'points': 200},
            {'name': 'Black Friday', 'category': 'special', 'description': 'S\'inscrire pendant le Black Friday', 'icon': '🛍️', 'points': 150},
            {'name': 'Cyber Monday', 'category': 'special', 'description': 'Formation achetée pendant Cyber Monday', 'icon': '💻', 'points': 150},
            {'name': 'Soldes d\'Été', 'category': 'special', 'description': 'Profiter des soldes d\'été', 'icon': '☀️', 'points': 100},
            {'name': 'Rentrée 2025', 'category': 'special', 'description': 'Inscription en septembre 2025', 'icon': '🎒', 'points': 150},
            {'name': 'VIP', 'category': 'special', 'description': 'Badge VIP spécial', 'icon': '💎', 'points': 1000, 'is_rare': True},
            {'name': 'Champion', 'category': 'special', 'description': 'Gagner un concours spécial', 'icon': '🏆', 'points': 500, 'is_rare': True},
        ]

        for badge_data in badges:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults={
                    'slug': slugify(badge_data['name']),
                    'description': badge_data['description'],
                    'category': badge_data['category'],
                    'icon': badge_data['icon'],
                    'points_reward': badge_data['points'],
                    'is_rare': badge_data.get('is_rare', False),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ {badge.name} ({badge.get_category_display()}) - {badge.points_reward} pts')

    def create_achievements(self):
        self.stdout.write('\n🎯 Création des accomplissements...')

        achievements = [
            {'name': 'Première Inscription', 'trigger': 'first_formation', 'description': 'Vous vous êtes inscrit à votre première formation', 'icon': '🎓', 'points': 50},
            {'name': 'Formation Terminée', 'trigger': 'first_completion', 'description': 'Vous avez terminé votre première formation avec succès', 'icon': '✅', 'points': 100},
            {'name': 'Premier Avis', 'trigger': 'first_review', 'description': 'Vous avez laissé votre premier avis', 'icon': '⭐', 'points': 30},
            {'name': 'Formation Créée', 'trigger': 'create_formation', 'description': 'Vous avez créé votre première formation en tant que formateur', 'icon': '👨‍🏫', 'points': 100},
            {'name': 'Profil 100%', 'trigger': 'complete_profile', 'description': 'Votre profil est complet à 100%', 'icon': '💯', 'points': 50},
            {'name': 'Partage Social', 'trigger': 'social_share', 'description': 'Vous avez partagé une formation sur les réseaux sociaux', 'icon': '📱', 'points': 25},
            {'name': 'Série de 7 jours', 'trigger': 'streak', 'description': 'Vous vous êtes connecté 7 jours consécutifs', 'icon': '🔥', 'points': 75},
            {'name': 'Parrainage', 'trigger': 'referral', 'description': 'Vous avez parrainé un ami avec succès', 'icon': '🤝', 'points': 100},
        ]

        for ach_data in achievements:
            achievement, created = Achievement.objects.get_or_create(
                name=ach_data['name'],
                defaults={
                    'slug': slugify(ach_data['name']),
                    'description': ach_data['description'],
                    'icon': ach_data['icon'],
                    'trigger_type': ach_data['trigger'],
                    'points': ach_data['points'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ {achievement.name} - {achievement.points} pts')

    def create_features(self):
        self.stdout.write('\n⚙️ Création des fonctionnalités...')

        features = [
            # Formation features
            {'name': 'Mise en Avant de Formation', 'type': 'formation', 'description': 'Mettre votre formation en avant sur la page d\'accueil', 'cost': 0, 'coach': True, 'user': False},
            {'name': 'Formation Sponsorisée', 'type': 'formation', 'description': 'Sponsoriser votre formation en haut des résultats de recherche', 'cost': 0, 'coach': True, 'user': False},
            {'name': 'Badge Formation Populaire', 'type': 'formation', 'description': 'Afficher un badge "Populaire" sur votre formation', 'cost': 0, 'coach': True, 'user': False},
            {'name': 'Vidéo Promotionnelle', 'type': 'formation', 'description': 'Ajouter une vidéo promotionnelle à votre formation', 'cost': 0, 'coach': True, 'user': False},
            {'name': 'Galerie Photos Étendue', 'type': 'formation', 'description': 'Jusqu\'à 20 photos au lieu de 5', 'cost': 0, 'coach': True, 'center': True},

            # Marketing features
            {'name': 'Email Marketing', 'type': 'marketing', 'description': 'Envoyer des emails promotionnels à votre audience', 'cost': 0, 'coach': True, 'center': True},
            {'name': 'SMS Marketing', 'type': 'marketing', 'description': 'Campagne SMS aux prospects', 'cost': 0, 'coach': True, 'center': True},
            {'name': 'Réseaux Sociaux Auto', 'type': 'marketing', 'description': 'Publication automatique sur les réseaux sociaux', 'cost': 0, 'coach': True, 'center': True},
            {'name': 'Newsletter Dédiée', 'type': 'marketing', 'description': 'Apparaître dans la newsletter hebdomadaire', 'cost': 0, 'coach': True, 'center': True},
            {'name': 'Bannière Publicitaire', 'type': 'marketing', 'description': 'Bannière publicitaire sur le site', 'cost': 0, 'coach': True, 'center': True},

            # Analytics features
            {'name': 'Statistiques Avancées', 'type': 'analytics', 'description': 'Accès aux statistiques détaillées de vos formations', 'cost': 0, 'coach': True, 'center': True},
            {'name': 'Rapport Mensuel', 'type': 'analytics', 'description': 'Rapport mensuel automatique', 'cost': 0, 'coach': True, 'center': True},
            {'name': 'Export de Données', 'type': 'analytics', 'description': 'Exporter vos données en Excel/CSV', 'cost': 0, 'coach': True, 'center': True},
            {'name': 'Tableau de Bord Pro', 'type': 'analytics', 'description': 'Tableau de bord professionnel avec graphiques', 'cost': 0, 'coach': True, 'center': True},
            {'name': 'Analyse de Concurrence', 'type': 'analytics', 'description': 'Comparer vos performances avec la concurrence', 'cost': 0, 'coach': True, 'center': True},

            # Training center features
            {'name': 'Gestion Multi-salles', 'type': 'center', 'description': 'Gérer plusieurs salles simultanément', 'cost': 0, 'coach': False, 'center': True},
            {'name': 'Calendrier Intelligent', 'type': 'center', 'description': 'Calendrier intelligent avec suggestions', 'cost': 0, 'coach': False, 'center': True},
            {'name': 'Réservation Instantanée', 'type': 'center', 'description': 'Les formateurs peuvent réserver instantanément', 'cost': 0, 'coach': False, 'center': True},
            {'name': 'Visite Virtuelle 360°', 'type': 'center', 'description': 'Visite virtuelle de votre centre', 'cost': 0, 'coach': False, 'center': True},
            {'name': 'Badge Centre Vérifié', 'type': 'center', 'description': 'Badge "Centre Vérifié" officiel', 'cost': 0, 'coach': False, 'center': True},

            # Communication features
            {'name': 'Chat Direct Élèves', 'type': 'communication', 'description': 'Messagerie directe avec vos élèves', 'cost': 0, 'coach': True, 'user': True},
            {'name': 'Notifications Push', 'type': 'communication', 'description': 'Envoyer des notifications push', 'cost': 0, 'coach': True, 'center': True},
            {'name': 'Forum Privé', 'type': 'communication', 'description': 'Forum privé pour vos formations', 'cost': 0, 'coach': True, 'user': False},
            {'name': 'Sondages et Enquêtes', 'type': 'communication', 'description': 'Créer des sondages pour vos élèves', 'cost': 0, 'coach': True, 'user': False},
            {'name': 'Rappels Automatiques', 'type': 'communication', 'description': 'Rappels automatiques par email/SMS', 'cost': 0, 'coach': True, 'center': True},

            # Content features
            {'name': 'Article de Blog Sponsorisé', 'type': 'content', 'description': 'Publier un article de blog sponsorisé', 'cost': 0, 'coach': True, 'center': True},
            {'name': 'Page Dédiée Formateur', 'type': 'content', 'description': 'Page personnalisée avec votre branding', 'cost': 0, 'coach': True, 'user': False},
            {'name': 'Portfolio en Ligne', 'type': 'content', 'description': 'Créer un portfolio de vos formations', 'cost': 0, 'coach': True, 'user': False},
            {'name': 'Certificats Personnalisés', 'type': 'content', 'description': 'Créer des certificats avec votre logo', 'cost': 0, 'coach': True, 'user': False},
            {'name': 'Ressources Illimitées', 'type': 'content', 'description': 'Héberger des ressources sans limite', 'cost': 0, 'coach': True, 'user': False},
        ]

        for feature_data in features:
            feature, created = Feature.objects.get_or_create(
                name=feature_data['name'],
                defaults={
                    'slug': slugify(feature_data['name']),
                    'description': feature_data['description'],
                    'feature_type': feature_data['type'],
                    'credits_cost': feature_data['cost'],
                    'available_for_coaches': feature_data.get('coach', False),
                    'available_for_centers': feature_data.get('center', False),
                    'available_for_users': feature_data.get('user', True),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ {feature.name} ({feature.get_feature_type_display()}) - {feature.credits_cost} crédits')
