'use client';

import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-primary-600">
            formations.casa
          </Link>

          <div className="hidden md:flex space-x-6 items-center">
            <Link
              href="/formations"
              className={`${
                isActive('/formations') ? 'text-primary-600' : 'text-gray-700'
              } hover:text-primary-600 transition-colors`}
            >
              Formations
            </Link>
            <Link
              href="/centers"
              className={`${
                isActive('/centers') ? 'text-primary-600' : 'text-gray-700'
              } hover:text-primary-600 transition-colors`}
            >
              Centres
            </Link>
            <Link
              href="/coaches"
              className={`${
                isActive('/coaches') ? 'text-primary-600' : 'text-gray-700'
              } hover:text-primary-600 transition-colors`}
            >
              Formateurs
            </Link>

            {user ? (
              <>
                <Link
                  href="/dashboard"
                  className={`${
                    isActive('/dashboard') ? 'text-primary-600' : 'text-gray-700'
                  } hover:text-primary-600 transition-colors flex items-center gap-2`}
                >
                  <span className="text-xl">{user.level}</span>
                  <span>{user.username}</span>
                  <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                    {user.total_points} pts
                  </span>
                </Link>
                <button
                  onClick={logout}
                  className="text-gray-700 hover:text-primary-600 transition-colors"
                >
                  Déconnexion
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="text-primary-600 hover:text-primary-700 transition-colors"
                >
                  Connexion
                </Link>
                <Link
                  href="/register"
                  className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Inscription
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button className="md:hidden p-2">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </nav>
  );
}
