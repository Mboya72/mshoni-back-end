import os
import sys
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# 1. PATHS AND ENV
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# 2. SECURITY
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-r2=&)+30s#bgh51ze)8)&1+h&o6d0d2^=94+z@@ft2^c)1&@9=')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = []

# 3. AUTH & SOCIAL CONFIG
AUTH_USER_MODEL = 'api.User' 
SITE_ID = 1
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
SOCIALACCOUNT_ADAPTER = 'api.adapters.RoleSocialAccountAdapter' # Make sure this matches your file name

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# 4. APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third Party
    'rest_framework',
    'rest_framework_simplejwt',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    
    # Local
    'api',
]

# 5. MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # REQUIRED BY ALLAUTH:
    'allauth.account.middleware.AccountMiddleware', 
]

# 6. DATABASE (SUPABASE)
# Automatically switch between Direct (Migrations) and Pooler (App)
is_migration = 'migrate' in sys.argv or 'makemigrations' in sys.argv
db_url = os.getenv('DIRECT_URL') if is_migration else os.getenv('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        default=db_url,
        conn_max_age=600,
        ssl_require=True,
        engine='django.db.backends.postgresql',
    )
}

# Supabase Pooler (6543) fix: Disable prepared statements
if not is_migration:
    DATABASES['default']['OPTIONS'] = {
        'prepare_threshold': None,
    }

# 7. TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Required by Allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 8. REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# ... (Keep Password Validators, Internationalization, Static Files as they were)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'