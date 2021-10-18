from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).parent.parent
environ.Env.read_env(str(BASE_DIR / '.env'))

SECRET_KEY = env('KESHA_SECRET_KEY')

DEBUG = env.bool('KESHA_DEBUG', False)

ALLOWED_HOSTS = env.list('KESHA_ALLOWED_HOSTS', default=['127.0.0.1'])

INSTALLED_APPS = [
    'simpleui',
    'django_extensions',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'http_stubs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'kesha.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / Path('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('KESHA_DB_NAME', 'kesha'),
        'USER': env.str('KESHA_DB_USER', 'kesha'),
        'PASSWORD': env.str('KESHA_DB_PASSWORD', 'kesha'),
        'HOST': env.str('KESHA_DB_HOST', 'kesha-database'),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = False
USE_L10N = False
USE_TZ = True

STATICFILES_DIRS = [
    BASE_DIR / Path('static'),
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / Path('static_build')

# Admin UI settings
SIMPLEUI_HOME_INFO = False
SIMPLEUI_STATIC_OFFLINE = True
SIMPLEUI_DEFAULT_THEME = 'layui.css'
SIMPLEUI_ANALYSIS = False
SIMPLEUI_LOGO = STATIC_URL + 'kesha_icon.png'

SIMPLEUI_ICON = {
    'HTTP Stubs': 'fas fa-feather-alt',
    'Request stubs': 'fas fa-feather-alt',
    'Request logs': 'fas fa-layer-group',
    'Proxy stubs': 'fas fa-feather-alt',
    'Proxy logs': 'fas fa-layer-group',
}

INTERNAL_IPS = env.list('KESHA_INTERNAL_HOSTS', default=['127.0.0.1'])

# Celery settings
CELERY_BROKER_URL = env(
    'KESHA_CELERY_BROKER_URL',
    default='redis://kesha-celery-broker',
)
CELERY_TASK_TIME_LIMIT = 20
CELERY_TASK_SOFT_TIME_LIMIT = 10
CELERY_TASK_DEFAULT_RATE_LIMIT = '96/m'
CELERY_MAX_MEMORY_PER_CHILD = 65536
