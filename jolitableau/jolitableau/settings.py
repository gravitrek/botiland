"""
Django settings for JoliTableau project.
La galerie d'art en ligne - Online Art Gallery Platform
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',
    "django-insecure-65c@cip)(6f9u70&03gtuwz21++ryn*%2i)wq-6iw@yp6sp*+&")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Application definition
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",

    # Third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_filters",
    "drf_yasg",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "guardian",
    "ckeditor",
    "ckeditor_uploader",
    "channels",

    # JoliTableau apps
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "artworks.apps.ArtworksConfig",
    "galleries.apps.GalleriesConfig",
    "community.apps.CommunityConfig",
    "conseil.apps.ConseilConfig",
    "marketplace.apps.MarketplaceConfig",
    "communications.apps.CommunicationsConfig",
    "payments.apps.PaymentsConfig",
    "verification.apps.VerificationConfig",
    "analytics.apps.AnalyticsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # i18n support
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "core.middleware.MultiTenantMiddleware",  # Custom middleware for multi-tenant
]

ROOT_URLCONF = "jolitableau.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = "jolitableau.wsgi.application"
ASGI_APPLICATION = "jolitableau.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if os.environ.get('USE_POSTGRES', 'False') == 'True':
    # AWS RDS PostgreSQL Configuration
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get('DB_NAME', 'jolitableau'),
            "USER": os.environ.get('DB_USER', 'postgres'),
            "PASSWORD": os.environ.get('DB_PASSWORD', ''),
            "HOST": os.environ.get('DB_HOST', 'localhost'),
            "PORT": os.environ.get('DB_PORT', '5432'),
            "OPTIONS": {
                "sslmode": os.environ.get('DB_SSLMODE', 'prefer'),
            },
        }
    }
else:
    # SQLite for development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Custom User Model
AUTH_USER_MODEL = 'users.UserProfile'

# Internationalization (i18n)
# Default language: French
LANGUAGE_CODE = 'fr'

# Available languages
LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
    ('es', 'Español'),
]

# Time zone
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Locale paths for translations
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# AWS S3 Configuration (for production)
if os.environ.get('USE_S3', 'False') == 'True':
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'jolitableau-media')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'eu-west-3')  # Paris
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = 'public-read'
    AWS_LOCATION = 'media'

    # Static files via CloudFront
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Sites Framework
SITE_ID = 1

# Security Settings (Production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# CORS Settings
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# Django Allauth Configuration
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
]

# Email Configuration
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.sendgrid.net')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@jolitableau.com')

# Celery Configuration (for async tasks)
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Channels (WebSockets)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379/1')],
        },
    },
}

# Stripe Configuration
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

# Mollie Configuration
MOLLIE_API_KEY = os.environ.get('MOLLIE_API_KEY', '')

# Twilio Configuration (WhatsApp)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_WHATSAPP_NUMBER = os.environ.get('TWILIO_WHATSAPP_NUMBER', '')

# OpenAI/Grok API (for AI features)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
GROK_API_KEY = os.environ.get('GROK_API_KEY', '')

# Elasticsearch Configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.environ.get('ELASTICSEARCH_HOST', 'localhost:9200')
    },
}

# CKEditor Configuration
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'jolitableau.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': os.environ.get('LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

# JoliTableau Specific Settings
JOLITABLEAU_DOMAIN_PRICE = float(os.environ.get('JOLITABLEAU_DOMAIN_PRICE', '9.99'))
JOLITABLEAU_BOOST_PRICE = float(os.environ.get('JOLITABLEAU_BOOST_PRICE', '4.99'))
JOLITABLEAU_WHATSAPP_MESSAGE_PRICE = float(os.environ.get('JOLITABLEAU_WHATSAPP_MESSAGE_PRICE', '0.05'))
JOLITABLEAU_FAIR_LISTING_PRICE = float(os.environ.get('JOLITABLEAU_FAIR_LISTING_PRICE', '49.00'))
JOLITABLEAU_COMMISSION_RATE = float(os.environ.get('JOLITABLEAU_COMMISSION_RATE', '0.10'))  # 10%

# Conseil des Sages Settings
CONSEIL_MAX_MEMBERS = int(os.environ.get('CONSEIL_MAX_MEMBERS', '20'))

# Trial Period (in days)
DOMAIN_TRIAL_PERIOD = int(os.environ.get('DOMAIN_TRIAL_PERIOD', '30'))
