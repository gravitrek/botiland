'use client';

import { useState, useEffect } from 'react';
import { useLocale } from 'next-intl';
import Link from 'next/link';

interface HeroSlide {
  title: string;
  subtitle: string;
  description: string;
  emoji: string;
  primaryCta: string;
  primaryCtaLink: string;
  secondaryCta: string;
  secondaryCtaLink: string;
  gradient: string;
}

const heroSlides: Record<string, HeroSlide[]> = {
  fr: [
    {
      title: "Vous avez toujours rêvé d'enseigner la pâtisserie marocaine ?",
      subtitle: "Partagez votre passion pour les makrout, cornes de gazelle et msemen",
      description: "Créez votre formation en ligne, fixez votre prix, et enseignez à des centaines d'élèves passionnés",
      emoji: "🥐",
      primaryCta: "Créer ma formation",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "Voir des exemples",
      secondaryCtaLink: "/formations?category=cuisine",
      gradient: "from-orange-500 to-red-600"
    },
    {
      title: "Expert en développement personnel ?",
      subtitle: "Aidez les professionnels marocains à atteindre leurs objectifs",
      description: "Coaching individuel, formations en ligne ou sessions de groupe - vous choisissez votre format",
      emoji: "🚀",
      primaryCta: "Devenir coach",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "Parcourir les formations",
      secondaryCtaLink: "/formations?category=developpement-personnel",
      gradient: "from-purple-600 to-indigo-700"
    },
    {
      title: "Votre équipe a besoin de team building ?",
      subtitle: "Trouvez des activités et formations pour renforcer la cohésion",
      description: "Ateliers créatifs, formations techniques, événements d'entreprise - tout au même endroit",
      emoji: "🤝",
      primaryCta: "Découvrir les options",
      primaryCtaLink: "/formations?type=entreprise",
      secondaryCta: "Créer une demande",
      secondaryCtaLink: "/contact",
      gradient: "from-blue-600 to-cyan-600"
    },
    {
      title: "Maîtrisez l'art du tajine et du couscous authentique",
      subtitle: "Apprenez les secrets des grands-mères marocaines",
      description: "Formations en présentiel à Casablanca avec des chefs expérimentés. Certificat inclus !",
      emoji: "🍲",
      primaryCta: "Explorer les cours",
      primaryCtaLink: "/formations?category=cuisine-marocaine",
      secondaryCta: "En savoir plus",
      secondaryCtaLink: "/about",
      gradient: "from-amber-600 to-orange-700"
    },
    {
      title: "Freelance en web design ?",
      subtitle: "Enseignez Figma, Photoshop et créez un revenu passif",
      description: "Transformez votre expertise en formations en ligne et gagnez jusqu'à 80% des revenus",
      emoji: "🎨",
      primaryCta: "Commencer à enseigner",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "Voir les opportunités",
      secondaryCtaLink: "/formations?category=design",
      gradient: "from-pink-600 to-purple-700"
    },
    {
      title: "Centre de formation à Casablanca ?",
      subtitle: "Louez vos salles pendant les heures creuses",
      description: "Monétisez vos espaces disponibles et connectez avec des formateurs locaux",
      emoji: "🏢",
      primaryCta: "Inscrire mon centre",
      primaryCtaLink: "/register?role=center",
      secondaryCta: "Voir les centres",
      secondaryCtaLink: "/centers",
      gradient: "from-teal-600 to-green-600"
    },
    {
      title: "Apprenez l'arabe dialectal marocain (darija)",
      subtitle: "Cours en ligne avec des natifs casablancais",
      description: "Du niveau débutant à avancé. Sessions individuelles ou en groupe. Commencez quand vous voulez",
      emoji: "🗣️",
      primaryCta: "Découvrir les cours",
      primaryCtaLink: "/formations?category=langues",
      secondaryCta: "Essai gratuit",
      secondaryCtaLink: "/register",
      gradient: "from-emerald-600 to-teal-700"
    },
    {
      title: "Formateur en cybersécurité ou data science ?",
      subtitle: "Le marché marocain a besoin de votre expertise",
      description: "Formations certifiantes, bootcamps intensifs, ou cours en ligne - créez votre programme unique",
      emoji: "💻",
      primaryCta: "Proposer une formation",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "Voir la demande",
      secondaryCtaLink: "/formations?category=tech",
      gradient: "from-slate-700 to-blue-800"
    }
  ],
  ar: [
    {
      title: "هل حلمت دائماً بتعليم الحلويات المغربية؟",
      subtitle: "شارك شغفك بالمقروط، كعب الغزال والمسمن",
      description: "أنشئ دورتك التدريبية عبر الإنترنت، حدد سعرك، وعلّم مئات الطلاب المتحمسين",
      emoji: "🥐",
      primaryCta: "إنشاء دورتي",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "شاهد أمثلة",
      secondaryCtaLink: "/formations?category=cuisine",
      gradient: "from-orange-500 to-red-600"
    },
    {
      title: "خبير في التنمية الشخصية؟",
      subtitle: "ساعد المهنيين المغاربة على تحقيق أهدافهم",
      description: "تدريب فردي، دورات عبر الإنترنت أو جلسات جماعية - أنت تختار الشكل",
      emoji: "🚀",
      primaryCta: "كن مدرباً",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "تصفح الدورات",
      secondaryCtaLink: "/formations?category=developpement-personnel",
      gradient: "from-purple-600 to-indigo-700"
    },
    {
      title: "فريقك بحاجة لبناء الفريق؟",
      subtitle: "ابحث عن أنشطة وتدريبات لتعزيز التماسك",
      description: "ورش إبداعية، تدريبات تقنية، فعاليات شركات - كل شيء في مكان واحد",
      emoji: "🤝",
      primaryCta: "اكتشف الخيارات",
      primaryCtaLink: "/formations?type=entreprise",
      secondaryCta: "إنشاء طلب",
      secondaryCtaLink: "/contact",
      gradient: "from-blue-600 to-cyan-600"
    },
    {
      title: "أتقن فن الطاجين والكسكس الأصيل",
      subtitle: "تعلم أسرار الجدات المغربيات",
      description: "دورات حضورية في الدار البيضاء مع طهاة ذوي خبرة. شهادة مضمنة!",
      emoji: "🍲",
      primaryCta: "استكشف الدورات",
      primaryCtaLink: "/formations?category=cuisine-marocaine",
      secondaryCta: "اعرف المزيد",
      secondaryCtaLink: "/about",
      gradient: "from-amber-600 to-orange-700"
    },
    {
      title: "مستقل في تصميم الويب؟",
      subtitle: "علّم Figma وPhotoshop وأنشئ دخلاً سلبياً",
      description: "حوّل خبرتك إلى دورات عبر الإنترنت واكسب حتى 80٪ من الإيرادات",
      emoji: "🎨",
      primaryCta: "ابدأ التدريس",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "شاهد الفرص",
      secondaryCtaLink: "/formations?category=design",
      gradient: "from-pink-600 to-purple-700"
    },
    {
      title: "مركز تدريب في الدار البيضاء؟",
      subtitle: "أجّر قاعاتك خلال ساعات الذروة",
      description: "استثمر مساحاتك المتاحة وتواصل مع المدربين المحليين",
      emoji: "🏢",
      primaryCta: "سجل مركزي",
      primaryCtaLink: "/register?role=center",
      secondaryCta: "شاهد المراكز",
      secondaryCtaLink: "/centers",
      gradient: "from-teal-600 to-green-600"
    },
    {
      title: "تعلم اللهجة المغربية (الدارجة)",
      subtitle: "دروس عبر الإنترنت مع متحدثين أصليين من كازا",
      description: "من المستوى المبتدئ إلى المتقدم. جلسات فردية أو جماعية. ابدأ متى تريد",
      emoji: "🗣️",
      primaryCta: "اكتشف الدروس",
      primaryCtaLink: "/formations?category=langues",
      secondaryCta: "تجربة مجانية",
      secondaryCtaLink: "/register",
      gradient: "from-emerald-600 to-teal-700"
    },
    {
      title: "مدرب في الأمن السيبراني أو علوم البيانات؟",
      subtitle: "السوق المغربي بحاجة إلى خبرتك",
      description: "دورات معتمدة، معسكرات مكثفة، أو دروس عبر الإنترنت - أنشئ برنامجك الفريد",
      emoji: "💻",
      primaryCta: "اقترح دورة",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "شاهد الطلب",
      secondaryCtaLink: "/formations?category=tech",
      gradient: "from-slate-700 to-blue-800"
    }
  ],
  en: [
    {
      title: "Always wanted to teach others how to make Moroccan pastries?",
      subtitle: "Share your passion for makrout, gazelle horns, and msemen",
      description: "Create your online course, set your price, and teach hundreds of passionate students",
      emoji: "🥐",
      primaryCta: "Create my course",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "See examples",
      secondaryCtaLink: "/formations?category=cuisine",
      gradient: "from-orange-500 to-red-600"
    },
    {
      title: "Expert in personal development?",
      subtitle: "Help Moroccan professionals achieve their goals",
      description: "Individual coaching, online courses, or group sessions - you choose your format",
      emoji: "🚀",
      primaryCta: "Become a coach",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "Browse courses",
      secondaryCtaLink: "/formations?category=developpement-personnel",
      gradient: "from-purple-600 to-indigo-700"
    },
    {
      title: "Your team needs team building services?",
      subtitle: "Find activities and training to strengthen cohesion",
      description: "Creative workshops, technical training, corporate events - all in one place",
      emoji: "🤝",
      primaryCta: "Discover options",
      primaryCtaLink: "/formations?type=entreprise",
      secondaryCta: "Create a request",
      secondaryCtaLink: "/contact",
      gradient: "from-blue-600 to-cyan-600"
    },
    {
      title: "Master the art of authentic tajine and couscous",
      subtitle: "Learn the secrets of Moroccan grandmothers",
      description: "In-person training in Casablanca with experienced chefs. Certificate included!",
      emoji: "🍲",
      primaryCta: "Explore courses",
      primaryCtaLink: "/formations?category=cuisine-marocaine",
      secondaryCta: "Learn more",
      secondaryCtaLink: "/about",
      gradient: "from-amber-600 to-orange-700"
    },
    {
      title: "Freelance web designer?",
      subtitle: "Teach Figma, Photoshop and create passive income",
      description: "Transform your expertise into online courses and earn up to 80% of revenue",
      emoji: "🎨",
      primaryCta: "Start teaching",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "See opportunities",
      secondaryCtaLink: "/formations?category=design",
      gradient: "from-pink-600 to-purple-700"
    },
    {
      title: "Training center in Casablanca?",
      subtitle: "Rent your rooms during off-peak hours",
      description: "Monetize your available spaces and connect with local trainers",
      emoji: "🏢",
      primaryCta: "Register my center",
      primaryCtaLink: "/register?role=center",
      secondaryCta: "See centers",
      secondaryCtaLink: "/centers",
      gradient: "from-teal-600 to-green-600"
    },
    {
      title: "Learn Moroccan Arabic dialect (darija)",
      subtitle: "Online classes with native speakers from Casa",
      description: "From beginner to advanced. Individual or group sessions. Start whenever you want",
      emoji: "🗣️",
      primaryCta: "Discover courses",
      primaryCtaLink: "/formations?category=langues",
      secondaryCta: "Free trial",
      secondaryCtaLink: "/register",
      gradient: "from-emerald-600 to-teal-700"
    },
    {
      title: "Cybersecurity or data science trainer?",
      subtitle: "The Moroccan market needs your expertise",
      description: "Certified training, intensive bootcamps, or online courses - create your unique program",
      emoji: "💻",
      primaryCta: "Propose a course",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "See demand",
      secondaryCtaLink: "/formations?category=tech",
      gradient: "from-slate-700 to-blue-800"
    }
  ],
  es: [
    {
      title: "¿Siempre quisiste enseñar a hacer pasteles marroquíes?",
      subtitle: "Comparte tu pasión por makrout, cuernos de gacela y msemen",
      description: "Crea tu curso en línea, fija tu precio y enseña a cientos de estudiantes apasionados",
      emoji: "🥐",
      primaryCta: "Crear mi curso",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "Ver ejemplos",
      secondaryCtaLink: "/formations?category=cuisine",
      gradient: "from-orange-500 to-red-600"
    },
    {
      title: "¿Experto en desarrollo personal?",
      subtitle: "Ayuda a profesionales marroquíes a alcanzar sus objetivos",
      description: "Coaching individual, cursos en línea o sesiones grupales - tú eliges tu formato",
      emoji: "🚀",
      primaryCta: "Conviértete en coach",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "Explorar cursos",
      secondaryCtaLink: "/formations?category=developpement-personnel",
      gradient: "from-purple-600 to-indigo-700"
    },
    {
      title: "¿Tu equipo necesita team building?",
      subtitle: "Encuentra actividades y formaciones para fortalecer la cohesión",
      description: "Talleres creativos, formación técnica, eventos corporativos - todo en un solo lugar",
      emoji: "🤝",
      primaryCta: "Descubrir opciones",
      primaryCtaLink: "/formations?type=entreprise",
      secondaryCta: "Crear solicitud",
      secondaryCtaLink: "/contact",
      gradient: "from-blue-600 to-cyan-600"
    },
    {
      title: "Domina el arte del tajín y cuscús auténtico",
      subtitle: "Aprende los secretos de las abuelas marroquíes",
      description: "Formación presencial en Casablanca con chefs experimentados. ¡Certificado incluido!",
      emoji: "🍲",
      primaryCta: "Explorar cursos",
      primaryCtaLink: "/formations?category=cuisine-marocaine",
      secondaryCta: "Saber más",
      secondaryCtaLink: "/about",
      gradient: "from-amber-600 to-orange-700"
    },
    {
      title: "¿Diseñador web freelance?",
      subtitle: "Enseña Figma, Photoshop y crea ingresos pasivos",
      description: "Transforma tu experiencia en cursos en línea y gana hasta el 80% de los ingresos",
      emoji: "🎨",
      primaryCta: "Empezar a enseñar",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "Ver oportunidades",
      secondaryCtaLink: "/formations?category=design",
      gradient: "from-pink-600 to-purple-700"
    },
    {
      title: "¿Centro de formación en Casablanca?",
      subtitle: "Alquila tus salas durante horas valle",
      description: "Monetiza tus espacios disponibles y conecta con formadores locales",
      emoji: "🏢",
      primaryCta: "Registrar mi centro",
      primaryCtaLink: "/register?role=center",
      secondaryCta: "Ver centros",
      secondaryCtaLink: "/centers",
      gradient: "from-teal-600 to-green-600"
    },
    {
      title: "Aprende el dialecto árabe marroquí (darija)",
      subtitle: "Clases en línea con hablantes nativos de Casa",
      description: "De principiante a avanzado. Sesiones individuales o grupales. Comienza cuando quieras",
      emoji: "🗣️",
      primaryCta: "Descubrir cursos",
      primaryCtaLink: "/formations?category=langues",
      secondaryCta: "Prueba gratis",
      secondaryCtaLink: "/register",
      gradient: "from-emerald-600 to-teal-700"
    },
    {
      title: "¿Formador en ciberseguridad o ciencia de datos?",
      subtitle: "El mercado marroquí necesita tu experiencia",
      description: "Formación certificada, bootcamps intensivos o cursos en línea - crea tu programa único",
      emoji: "💻",
      primaryCta: "Proponer un curso",
      primaryCtaLink: "/register?role=coach",
      secondaryCta: "Ver demanda",
      secondaryCtaLink: "/formations?category=tech",
      gradient: "from-slate-700 to-blue-800"
    }
  ]
};

export default function HeroCarousel() {
  const locale = useLocale() as 'fr' | 'ar' | 'en' | 'es';
  const slides = heroSlides[locale] || heroSlides.fr;

  const [currentSlide, setCurrentSlide] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (isPaused) return;

    const interval = setInterval(() => {
      setIsAnimating(true);
      setTimeout(() => {
        setCurrentSlide((prev) => (prev + 1) % slides.length);
        setIsAnimating(false);
      }, 300);
    }, 5000); // Change slide every 5 seconds

    return () => clearInterval(interval);
  }, [isPaused, slides.length]);

  const goToSlide = (index: number) => {
    if (index === currentSlide) return;
    setIsAnimating(true);
    setTimeout(() => {
      setCurrentSlide(index);
      setIsAnimating(false);
    }, 300);
  };

  const nextSlide = () => {
    setIsAnimating(true);
    setTimeout(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
      setIsAnimating(false);
    }, 300);
  };

  const prevSlide = () => {
    setIsAnimating(true);
    setTimeout(() => {
      setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
      setIsAnimating(false);
    }, 300);
  };

  const slide = slides[currentSlide];

  return (
    <div
      className={`relative bg-gradient-to-br ${slide.gradient} text-white py-24 md:py-32 overflow-hidden transition-all duration-500`}
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
    >
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className={`text-center transition-all duration-300 ${isAnimating ? 'opacity-0 transform scale-95' : 'opacity-100 transform scale-100'}`}>
          {/* Emoji */}
          <div className="text-8xl mb-6 animate-bounce-slow">
            {slide.emoji}
          </div>

          {/* Title */}
          <h1 className="text-4xl md:text-6xl font-bold mb-4 leading-tight max-w-5xl mx-auto">
            {slide.title}
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl mb-4 text-white/90 font-medium max-w-3xl mx-auto">
            {slide.subtitle}
          </p>

          {/* Description */}
          <p className="text-lg md:text-xl mb-10 text-white/80 max-w-2xl mx-auto">
            {slide.description}
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              href={`/${locale}${slide.primaryCtaLink}`}
              className="bg-white text-gray-900 px-8 py-4 rounded-xl font-bold text-lg hover:bg-gray-100 transition-all transform hover:scale-105 shadow-xl hover:shadow-2xl"
            >
              {slide.primaryCta} →
            </Link>
            <Link
              href={`/${locale}${slide.secondaryCtaLink}`}
              className="border-2 border-white text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white hover:text-gray-900 transition-all transform hover:scale-105"
            >
              {slide.secondaryCta}
            </Link>
          </div>
        </div>

        {/* Navigation Arrows */}
        <div className="absolute top-1/2 left-4 right-4 -translate-y-1/2 flex justify-between pointer-events-none">
          <button
            onClick={prevSlide}
            className="pointer-events-auto bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-4 rounded-full transition-all transform hover:scale-110 shadow-lg"
            aria-label="Previous slide"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button
            onClick={nextSlide}
            className="pointer-events-auto bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-4 rounded-full transition-all transform hover:scale-110 shadow-lg"
            aria-label="Next slide"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        {/* Dots Indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-3">
          {slides.map((_, index) => (
            <button
              key={index}
              onClick={() => goToSlide(index)}
              className={`transition-all duration-300 rounded-full ${
                index === currentSlide
                  ? 'bg-white w-12 h-3'
                  : 'bg-white/40 hover:bg-white/60 w-3 h-3'
              }`}
              aria-label={`Go to slide ${index + 1}`}
            />
          ))}
        </div>
      </div>

      {/* Slide counter */}
      <div className="absolute top-8 right-8 bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm font-semibold">
        {currentSlide + 1} / {slides.length}
      </div>
    </div>
  );
}
