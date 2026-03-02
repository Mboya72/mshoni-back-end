import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 1️⃣ PATHS AND ENV
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# 2️⃣ SECURITY
SECRET_KEY = os.getenv(
    'SECRET_KEY', 
    'django-insecure-r2=&)+30s#bgh51ze)8)&1+h&o6d0d2^=94+z@@ft2^c)1&@9='
)
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

# 3️⃣ AUTH & SOCIAL CONFIG
AUTH_USER_MODEL = 'api.User'  # Your CustomUser model
SITE_ID = 1
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

SOCIALACCOUNT_ADAPTER = 'api.adapters.RoleSocialAccountAdapter'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# 4️⃣ INSTALLED APPS
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    # Local apps
    'api',
]

# 5️⃣ MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Required by Allauth
    'allauth.account.middleware.AccountMiddleware',
]

# 6️⃣ DATABASE (SQLite local / PostgreSQL production)
is_migration = 'migrate' in sys.argv or 'makemigrations' in sys.argv
use_postgres = os.getenv('USE_POSTGRES', 'False') == 'True'

if use_postgres:
    import dj_database_url
    db_url = os.getenv('DIRECT_URL') if is_migration else os.getenv('DATABASE_URL')
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            ssl_require=True,
            engine='django.db.backends.postgresql',
        )
    }
    if not is_migration:
        DATABASES['default']['OPTIONS'] = {'prepare_threshold': None}
else:
    # Local SQLite for testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# 7️⃣ TEMPLATES (Allauth needs request context)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Allauth requirement
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 8️⃣ REST FRAMEWORK + JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 10,
}

# 9️⃣ URLS & WSGI
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# 1️⃣0️⃣ PASSWORD VALIDATORS
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 1️⃣1️⃣ INTERNATIONALIZATION & TIMEZONE
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 1️⃣2️⃣ STATIC FILES
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 1️⃣3️⃣ CORS (For mobile apps)
CORS_ALLOW_ALL_ORIGINS = True