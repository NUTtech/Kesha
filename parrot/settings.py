import environ
from pathlib import Path

env = environ.Env()

BASE_DIR = Path(__file__).parent.parent
environ.Env.read_env(str(BASE_DIR / '.env'))

SECRET_KEY = env('PARROT_SECRET_KEY')

DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list('PARROT_ALLOWED_HOSTS', default=['127.0.0.1'])

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

ROOT_URLCONF = 'parrot.urls'

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
        'NAME': env.str('PARROT_DB_NAME', 'parrot'),
        'USER': env.str('PARROT_DB_USER', 'parrot'),
        'PASSWORD': env.str('PARROT_DB_PASSWORD', 'parrot'),
        'HOST': env.str('PARROT_DB_HOST', 'parrot-database'),
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
SIMPLEUI_LOGO = STATIC_URL + 'parrot_icon.png'

SIMPLEUI_ICON = {
    'HTTP Stubs': 'fas fa-feather-alt',
    'Stubs': 'fas fa-feather-alt',
    'Logs': 'fas fa-layer-group',
}
