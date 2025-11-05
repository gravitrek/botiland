import Navbar from '@/components/Navbar';
import HeroCarousel from '@/components/HeroCarousel';
import { useTranslations } from 'next-intl';
import Link from 'next/link';

export default function Home() {
  const t = useTranslations();

  return (
    <main className="min-h-screen bg-gray-50">
      <Navbar />

      {/* Hero Carousel */}
      <HeroCarousel />

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">{t('features.title')}</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center p-6 bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">🔍</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">{t('features.browse.title')}</h3>
            <p className="text-gray-600">
              {t('features.browse.description')}
            </p>
          </div>
          <div className="text-center p-6 bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">📚</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">{t('features.enroll.title')}</h3>
            <p className="text-gray-600">
              {t('features.enroll.description')}
            </p>
          </div>
          <div className="text-center p-6 bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">🏆</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">{t('features.earn.title')}</h3>
            <p className="text-gray-600">
              {t('features.earn.description')}
            </p>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-800 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div className="text-white">
              <div className="text-5xl font-bold mb-2">1000+</div>
              <div className="text-primary-100 text-lg">{t('nav.formations')}</div>
            </div>
            <div className="text-white">
              <div className="text-5xl font-bold mb-2">500+</div>
              <div className="text-primary-100 text-lg">{t('nav.coaches')}</div>
            </div>
            <div className="text-white">
              <div className="text-5xl font-bold mb-2">50+</div>
              <div className="text-primary-100 text-lg">{t('nav.centers')}</div>
            </div>
            <div className="text-white">
              <div className="text-5xl font-bold mb-2">10000+</div>
              <div className="text-primary-100 text-lg">Apprenants</div>
            </div>
          </div>
        </div>
      </div>

      {/* Popular Categories */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Catégories Populaires</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
          {[
            { name: 'Cuisine', emoji: '👨‍🍳', color: 'from-orange-400 to-red-500' },
            { name: 'Tech', emoji: '💻', color: 'from-blue-500 to-cyan-600' },
            { name: 'Business', emoji: '💼', color: 'from-purple-500 to-pink-600' },
            { name: 'Langues', emoji: '🗣️', color: 'from-green-500 to-teal-600' },
            { name: 'Design', emoji: '🎨', color: 'from-pink-500 to-rose-600' },
            { name: 'Marketing', emoji: '📊', color: 'from-indigo-500 to-purple-600' },
          ].map((category) => (
            <Link
              key={category.name}
              href={`/formations?category=${category.name.toLowerCase()}`}
              className={`bg-gradient-to-br ${category.color} text-white p-6 rounded-xl text-center hover:shadow-xl transition-all transform hover:scale-105`}
            >
              <div className="text-4xl mb-2">{category.emoji}</div>
              <div className="font-semibold">{category.name}</div>
            </Link>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-900 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-4">Prêt à commencer votre aventure d'apprentissage ?</h2>
          <p className="text-xl text-gray-300 mb-8">
            Rejoignez des milliers d'apprenants et formateurs à Casablanca
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/register"
              className="bg-primary-600 text-white px-10 py-4 rounded-xl font-bold text-lg hover:bg-primary-700 transition-all transform hover:scale-105"
            >
              Commencer Gratuitement
            </Link>
            <Link
              href="/formations"
              className="border-2 border-white text-white px-10 py-4 rounded-xl font-bold text-lg hover:bg-white hover:text-gray-900 transition-all"
            >
              Explorer les Formations
            </Link>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-2xl font-bold mb-4 text-primary-400">formations.casa</h3>
              <p className="text-gray-400">Plateforme de formation professionnelle à Casablanca, Maroc</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4 text-lg">Pour les Apprenants</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/formations" className="hover:text-primary-400 transition-colors">Parcourir les Formations</Link></li>
                <li><Link href="/centers" className="hover:text-primary-400 transition-colors">Centres de Formation</Link></li>
                <li><Link href="/coaches" className="hover:text-primary-400 transition-colors">Trouver des Formateurs</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4 text-lg">Pour les Formateurs</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/dashboard" className="hover:text-primary-400 transition-colors">Tableau de Bord</Link></li>
                <li><Link href="/register?role=coach" className="hover:text-primary-400 transition-colors">Devenir Formateur</Link></li>
                <li><Link href="/register?role=center" className="hover:text-primary-400 transition-colors">Inscrire un Centre</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4 text-lg">Entreprise</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-primary-400 transition-colors">À Propos</Link></li>
                <li><Link href="/blog" className="hover:text-primary-400 transition-colors">Blog</Link></li>
                <li><Link href="/contact" className="hover:text-primary-400 transition-colors">Contact</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 formations.casa. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </main>
  )
}
