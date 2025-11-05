'use client';

import { useState, useEffect } from 'react';
import { use } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/Navbar';
import { formationsAPI } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

export default function FormationDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const resolvedParams = use(params);
  const [formation, setFormation] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    loadFormation();
  }, [resolvedParams.slug]);

  const loadFormation = async () => {
    try {
      const data = await formationsAPI.get(resolvedParams.slug);
      setFormation(data);
    } catch (error) {
      console.error('Failed to load formation:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = () => {
    if (!user) {
      router.push('/login');
      return;
    }
    // TODO: Implement enrollment
    alert('Inscription en cours de développement');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-12 text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    );
  }

  if (!formation) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-12 text-center">
          <h1 className="text-2xl font-bold text-gray-900">Formation non trouvée</h1>
          <Link href="/formations" className="text-primary-600 hover:underline mt-4 inline-block">
            Retour aux formations
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-8">
              <div className="mb-6">
                <span className="inline-block bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm mb-4">
                  {formation.category.icon} {formation.category.name}
                </span>
                <h1 className="text-4xl font-bold text-gray-900 mb-4">{formation.title}</h1>
                <p className="text-lg text-gray-600">{formation.short_description}</p>
              </div>

              <div className="flex items-center gap-6 mb-6 pb-6 border-b">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">👨‍🏫</span>
                  <div>
                    <p className="text-sm text-gray-500">Formateur</p>
                    <p className="font-semibold">
                      {formation.coach.first_name} {formation.coach.last_name}
                    </p>
                  </div>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Niveau</p>
                  <p className="font-semibold">{formation.level}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Mode</p>
                  <p className="font-semibold">{formation.delivery_mode}</p>
                </div>
              </div>

              <div className="mb-8">
                <h2 className="text-2xl font-bold mb-4">Description</h2>
                <div
                  className="prose max-w-none"
                  dangerouslySetInnerHTML={{ __html: formation.description }}
                />
              </div>

              {formation.curriculum_items && formation.curriculum_items.length > 0 && (
                <div className="mb-8">
                  <h2 className="text-2xl font-bold mb-4">Programme</h2>
                  <div className="space-y-4">
                    {formation.curriculum_items.map((item: any, index: number) => (
                      <div key={item.id} className="bg-gray-50 p-4 rounded-lg">
                        <div className="flex items-start gap-4">
                          <div className="flex-shrink-0 w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-semibold">
                            {index + 1}
                          </div>
                          <div className="flex-1">
                            <h3 className="font-semibold text-lg mb-2">{item.title}</h3>
                            <div
                              className="text-gray-600 text-sm"
                              dangerouslySetInnerHTML={{ __html: item.description }}
                            />
                            <p className="text-sm text-gray-500 mt-2">
                              ⏱️ {item.duration_minutes} minutes
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {formation.prerequisites && (
                <div className="mb-8">
                  <h2 className="text-2xl font-bold mb-4">Prérequis</h2>
                  <div
                    className="prose max-w-none"
                    dangerouslySetInnerHTML={{ __html: formation.prerequisites }}
                  />
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6 sticky top-4">
              <div className="text-center mb-6">
                <div className="text-4xl font-bold text-primary-600 mb-2">
                  {formation.price} {formation.currency}
                </div>
                <p className="text-sm text-gray-500">Prix de la formation</p>
              </div>

              <button
                onClick={handleEnroll}
                className="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors mb-4"
              >
                S'inscrire maintenant
              </button>

              <div className="space-y-4 text-sm">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">📅</span>
                  <div>
                    <p className="text-gray-500">Date de début</p>
                    <p className="font-semibold">
                      {new Date(formation.start_date).toLocaleDateString('fr-MA')}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-2xl">⏱️</span>
                  <div>
                    <p className="text-gray-500">Durée</p>
                    <p className="font-semibold">{formation.duration_hours}h</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-2xl">👥</span>
                  <div>
                    <p className="text-gray-500">Places disponibles</p>
                    <p className="font-semibold">
                      {formation.max_participants - formation.current_participants} / {formation.max_participants}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-2xl">⭐</span>
                  <div>
                    <p className="text-gray-500">Note moyenne</p>
                    <p className="font-semibold">
                      {formation.average_rating.toFixed(1)} / 5.0
                    </p>
                  </div>
                </div>

                {formation.training_center && (
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">🏢</span>
                    <div>
                      <p className="text-gray-500">Centre</p>
                      <p className="font-semibold">{formation.training_center.name}</p>
                    </div>
                  </div>
                )}
              </div>

              <div className="mt-6 pt-6 border-t">
                <p className="text-xs text-gray-500 text-center">
                  Après inscription, vous recevrez les instructions de paiement par email
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
