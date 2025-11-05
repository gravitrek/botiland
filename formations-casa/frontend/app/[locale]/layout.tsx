import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { locales } from '@/i18n';
import { AuthProvider } from '@/contexts/AuthContext';

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  // Validate that the incoming `locale` parameter is valid
  if (!locales.includes(locale as any)) {
    notFound();
  }

  // Fetch messages for the locale
  const messages = await getMessages();

  return (
    <html lang={locale} dir={locale === 'ar' ? 'rtl' : 'ltr'}>
      <body>
        <NextIntlClientProvider messages={messages}>
          <AuthProvider>
            {children}
          </AuthProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}

export async function generateMetadata({
  params: { locale }
}: {
  params: { locale: string };
}) {
  const titles: Record<string, string> = {
    fr: 'Formations.casa - Plateforme de Formation Professionnelle',
    ar: 'Formations.casa - منصة التكوين المهني',
    en: 'Formations.casa - Professional Training Platform',
    es: 'Formations.casa - Plataforma de Formación Profesional',
  };

  const descriptions: Record<string, string> = {
    fr: 'Trouvez et réservez des formations professionnelles à Casablanca, Maroc',
    ar: 'اكتشف واحجز التكوينات المهنية في الدار البيضاء، المغرب',
    en: 'Find and book professional training courses in Casablanca, Morocco',
    es: 'Encuentra y reserva cursos de formación profesional en Casablanca, Marruecos',
  };

  return {
    title: titles[locale] || titles.fr,
    description: descriptions[locale] || descriptions.fr,
  };
}
