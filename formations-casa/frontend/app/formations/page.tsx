'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import { formationsAPI } from '@/lib/api';

interface Formation {
  id: number;
  title: string;
  slug: string;
  short_description: string;
  cover_image: string | null;
  coach: {
    username: string;
    first_name: string;
    last_name: string;
  };
  category: {
    name: string;
    icon: string;
  };
  level: string;
  delivery_mode: string;
  start_date: string;
  price: number;
  currency: string;
  max_participants: number;
  current_participants: number;
  average_rating: number;
  is_featured: boolean;
}

export default function FormationsPage() {
  const [formations, setFormations] = useState<Formation[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [level, setLevel] = useState('');

  useEffect(() => {
    loadFormations();
  }, [category, level]);

  const loadFormations = async () => {
    try {
      const params: any = {};
      if (category) params.category = category;
      if (level) params.level = level;

      const response = await formationsAPI.list(params);
      setFormations(response.results || response);
    } catch (error) {
      console.error('Failed to load formations:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredFormations = formations.filter((f) =>
    f.title.toLowerCase().includes(search.toLowerCase()) ||
    f.short_description.toLowerCase().includes(search.toLowerCase())
  );

  const getDeliveryModeLabel = (mode: string) => {
    switch (mode) {
      case 'in_person': return '🏢 Présentiel';
      case 'remote': return '💻 En ligne';
      case 'hybrid': return '🔀 Hybride';
      default: return mode;
    }
  };

  const getLevelLabel = (level: string) => {
    switch (level) {
      case 'beginner': return 'Débutant';
      case 'intermediate': return 'Intermédiaire';
      case 'advanced': return 'Avancé';
      case 'all': return 'Tous niveaux';
      default: return level;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filters */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Toutes les Formations</h1>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-2">
              <input
                type="text"
                placeholder="Rechercher une formation..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <select
                value={level}
                onChange={(e) => setLevel(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Tous les niveaux</option>
                <option value="beginner">Débutant</option>
                <option value="intermediate">Intermédiaire</option>
                <option value="advanced">Avancé</option>
                <option value="all">Tous niveaux</option>
              </select>
            </div>
            <div>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Toutes les catégories</option>
                {/* Categories will be loaded dynamically */}
              </select>
            </div>
          </div>
        </div>

        {/* Formations Grid */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p className="mt-4 text-gray-600">Chargement des formations...</p>
          </div>
        ) : filteredFormations.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Aucune formation trouvée.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredFormations.map((formation) => (
              <Link
                key={formation.id}
                href={`/formations/${formation.slug}`}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden"
              >
                <div className="relative h-48 bg-gradient-to-br from-primary-400 to-primary-600">
                  {formation.cover_image && (
                    <img
                      src={formation.cover_image}
                      alt={formation.title}
                      className="w-full h-full object-cover"
                    />
                  )}
                  {formation.is_featured && (
                    <span className="absolute top-2 right-2 bg-yellow-400 text-yellow-900 px-3 py-1 rounded-full text-xs font-semibold">
                      ⭐ Populaire
                    </span>
                  )}
                  <div className="absolute top-2 left-2 bg-white px-3 py-1 rounded-full text-sm">
                    {formation.category.icon} {formation.category.name}
                  </div>
                </div>

                <div className="p-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2 line-clamp-2">
                    {formation.title}
                  </h3>

                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {formation.short_description}
                  </p>

                  <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
                    <span>👨‍🏫 {formation.coach.first_name} {formation.coach.last_name}</span>
                  </div>

                  <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
                    <span>{getDeliveryModeLabel(formation.delivery_mode)}</span>
                    <span>📊 {getLevelLabel(formation.level)}</span>
                  </div>

                  <div className="flex items-center gap-2 mb-4">
                    <div className="flex items-center">
                      <span className="text-yellow-400">★</span>
                      <span className="ml-1 text-sm">{formation.average_rating.toFixed(1)}</span>
                    </div>
                    <span className="text-sm text-gray-500">
                      {formation.current_participants}/{formation.max_participants} inscrits
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-2xl font-bold text-primary-600">
                        {formation.price} {formation.currency}
                      </span>
                    </div>
                    <div className="text-sm text-gray-500">
                      {new Date(formation.start_date).toLocaleDateString('fr-MA')}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
