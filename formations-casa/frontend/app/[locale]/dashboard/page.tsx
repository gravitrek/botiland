'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import Navbar from '@/components/Navbar';
import Link from 'next/link';

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading || !user) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-12 text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-lg p-8 mb-8">
          <h1 className="text-3xl font-bold mb-2">
            Bienvenue, {user.first_name || user.username}! 👋
          </h1>
          <p className="text-primary-100">
            {user.role === 'coach' && 'Gérez vos formations et suivez vos étudiants'}
            {user.role === 'center' && 'Gérez votre centre et vos salles de formation'}
            {user.role === 'user' && 'Découvrez de nouvelles formations et développez vos compétences'}
            {user.role === 'admin' && 'Administrez la plateforme et gérez le contenu'}
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Niveau</p>
                <p className="text-3xl font-bold text-primary-600">{user.level}</p>
              </div>
              <span className="text-4xl">🎯</span>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Points Totaux</p>
                <p className="text-3xl font-bold text-yellow-600">{user.total_points}</p>
              </div>
              <span className="text-4xl">⭐</span>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Crédits</p>
                <p className="text-3xl font-bold text-green-600">{user.credits}</p>
              </div>
              <span className="text-4xl">💰</span>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Statut</p>
                <p className="text-sm font-semibold">
                  {user.is_approved ? (
                    <span className="text-green-600">✓ Approuvé</span>
                  ) : (
                    <span className="text-yellow-600">⏳ En attente</span>
                  )}
                </p>
              </div>
              <span className="text-4xl">🎖️</span>
            </div>
          </div>
        </div>

        {!user.is_approved && user.role !== 'user' && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8">
            <div className="flex items-start gap-4">
              <span className="text-3xl">⏳</span>
              <div>
                <h3 className="font-semibold text-yellow-900 mb-2">
                  Compte en attente d'approbation
                </h3>
                <p className="text-yellow-800 text-sm">
                  Votre compte {user.role === 'coach' ? 'formateur' : 'centre de formation'} est en cours de vérification
                  par notre équipe. Vous serez notifié par email dès que votre compte sera approuvé.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {user.role === 'coach' && (
            <>
              <Link
                href="/coach/formations"
                className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-4">📚</div>
                <h3 className="text-lg font-semibold mb-2">Mes Formations</h3>
                <p className="text-gray-600 text-sm">
                  Gérer et créer de nouvelles formations
                </p>
              </Link>

              <Link
                href="/coach/students"
                className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-4">👥</div>
                <h3 className="text-lg font-semibold mb-2">Mes Étudiants</h3>
                <p className="text-gray-600 text-sm">
                  Suivre la progression de vos étudiants
                </p>
              </Link>

              <Link
                href="/coach/payments"
                className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-4">💳</div>
                <h3 className="text-lg font-semibold mb-2">Paiements</h3>
                <p className="text-gray-600 text-sm">
                  Gérer les paiements et la réconciliation
                </p>
              </Link>
            </>
          )}

          {user.role === 'center' && (
            <>
              <Link
                href="/center/rooms"
                className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-4">🏢</div>
                <h3 className="text-lg font-semibold mb-2">Mes Salles</h3>
                <p className="text-gray-600 text-sm">
                  Gérer les salles et la disponibilité
                </p>
              </Link>

              <Link
                href="/center/bookings"
                className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-4">📅</div>
                <h3 className="text-lg font-semibold mb-2">Réservations</h3>
                <p className="text-gray-600 text-sm">
                  Voir toutes les réservations
                </p>
              </Link>

              <Link
                href="/center/stats"
                className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-4">📊</div>
                <h3 className="text-lg font-semibold mb-2">Statistiques</h3>
                <p className="text-gray-600 text-sm">
                  Analyser les performances
                </p>
              </Link>
            </>
          )}

          {user.role === 'user' && (
            <>
              <Link
                href="/formations"
                className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-4">🔍</div>
                <h3 className="text-lg font-semibold mb-2">Explorer</h3>
                <p className="text-gray-600 text-sm">
                  Découvrir de nouvelles formations
                </p>
              </Link>

              <Link
                href="/user/formations"
                className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-4">📖</div>
                <h3 className="text-lg font-semibold mb-2">Mes Formations</h3>
                <p className="text-gray-600 text-sm">
                  Voir mes formations en cours
                </p>
              </Link>

              <Link
                href="/user/badges"
                className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
              >
                <div className="text-4xl mb-4">🏆</div>
                <h3 className="text-lg font-semibold mb-2">Badges & Points</h3>
                <p className="text-gray-600 text-sm">
                  Voir mes accomplissements
                </p>
              </Link>
            </>
          )}

          <Link
            href="/profile"
            className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
          >
            <div className="text-4xl mb-4">⚙️</div>
            <h3 className="text-lg font-semibold mb-2">Mon Profil</h3>
            <p className="text-gray-600 text-sm">
              Gérer vos informations personnelles
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
}
