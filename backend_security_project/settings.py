from pathlib import Path
from datetime import timedelta # <-- FIX: timedelta must be imported here

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-^qlqv@lytcvfs=@vd)r5eai6be6db$orif9zvpbqutw#bqe!=w'
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom Apps
    'ip_tracking',
    
    # Third-Party Apps
    'django_ip_geolocation',  # Task 2
    'django_celery_results',  # Task 4
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # REQUIRED for Authentication and Sessions (used by ratelimit)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Task 3: Rate Limiting Middleware (Must run before our custom logging/blocking)
    'django_ratelimit.middleware.RatelimitMiddleware', # FIX: Correct, case-sensitive name
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Task 1 & 0: Custom IP Tracking Middleware (Must run after rate limits)
    'ip_tracking.middleware.BlacklistMiddleware',
    'ip_tracking.middleware.IPLoggingMiddleware',
]

ROOT_URLCONF = 'backend_security_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend_security_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CACHE (Used by django-ratelimit and geolocation caching)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Password validation (default)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization (default)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- TASK 3 FIX: DJANGO RATELIMIT CONFIGURATION ---
RATELIMIT_VIEW = 'django.views.defaults.page_not_found' 

# --- TASK 4: CELERY CONFIGURATION ---
# Use the database as the result backend
CELERY_RESULT_BACKEND = 'django-db' 
CELERY_BROKER_URL = 'redis://localhost:6379/0' # Use 'sqla+sqlite:///celerydb.sqlite' if no Redis

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# --- TASK 4: CELERY BEAT SCHEDULE ---
CELERY_BEAT_SCHEDULE = {
    'flag-suspicious-ips-hourly': {
        'task': 'ip_tracking.tasks.flag_suspicious_ips',
        'schedule': timedelta(hours=1), # Run every hour
    },
}