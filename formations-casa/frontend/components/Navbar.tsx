'use client';

import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { usePathname, useRouter } from 'next/navigation';
import { useLocale, useTranslations } from 'next-intl';
import { useState } from 'react';

export default function Navbar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const locale = useLocale();
  const t = useTranslations('nav');
  const [showLangMenu, setShowLangMenu] = useState(false);

  const isActive = (path: string) => pathname.includes(path);

  const switchLocale = (newLocale: string) => {
    // Get the path without the locale
    const pathWithoutLocale = pathname.replace(`/${locale}`, '');
    router.push(`/${newLocale}${pathWithoutLocale || '/'}`);
    setShowLangMenu(false);
  };

  const languages = [
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'ar', name: 'العربية', flag: '🇲🇦' },
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'es', name: 'Español', flag: '🇪🇸' },
  ];

  const currentLang = languages.find(lang => lang.code === locale);

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <Link href={`/${locale}`} className="text-2xl font-bold text-primary-600">
            formations.casa
          </Link>

          <div className="hidden md:flex space-x-6 items-center">
            <Link
              href={`/${locale}/formations`}
              className={`${
                isActive('/formations') ? 'text-primary-600' : 'text-gray-700'
              } hover:text-primary-600 transition-colors`}
            >
              {t('formations')}
            </Link>
            <Link
              href={`/${locale}/centers`}
              className={`${
                isActive('/centers') ? 'text-primary-600' : 'text-gray-700'
              } hover:text-primary-600 transition-colors`}
            >
              {t('centers')}
            </Link>
            <Link
              href={`/${locale}/coaches`}
              className={`${
                isActive('/coaches') ? 'text-primary-600' : 'text-gray-700'
              } hover:text-primary-600 transition-colors`}
            >
              {t('coaches')}
            </Link>

            {/* Language Switcher */}
            <div className="relative">
              <button
                onClick={() => setShowLangMenu(!showLangMenu)}
                className="flex items-center gap-1 text-gray-700 hover:text-primary-600 transition-colors px-3 py-2 rounded-lg hover:bg-gray-100"
              >
                <span>{currentLang?.flag}</span>
                <span className="text-sm">{currentLang?.code.toUpperCase()}</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {showLangMenu && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
                  {languages.map((lang) => (
                    <button
                      key={lang.code}
                      onClick={() => switchLocale(lang.code)}
                      className={`w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center gap-2 ${
                        locale === lang.code ? 'bg-primary-50 text-primary-600' : 'text-gray-700'
                      }`}
                    >
                      <span>{lang.flag}</span>
                      <span>{lang.name}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {user ? (
              <>
                <Link
                  href={`/${locale}/dashboard`}
                  className={`${
                    isActive('/dashboard') ? 'text-primary-600' : 'text-gray-700'
                  } hover:text-primary-600 transition-colors flex items-center gap-2`}
                >
                  <span className="text-xl">{user.level}</span>
                  <span>{user.username}</span>
                  <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                    {user.total_points} {t('points')}
                  </span>
                </Link>
                <button
                  onClick={logout}
                  className="text-gray-700 hover:text-primary-600 transition-colors"
                >
                  {t('logout')}
                </button>
              </>
            ) : (
              <>
                <Link
                  href={`/${locale}/login`}
                  className="text-primary-600 hover:text-primary-700 transition-colors"
                >
                  {t('login')}
                </Link>
                <Link
                  href={`/${locale}/register`}
                  className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
                >
                  {t('register')}
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
