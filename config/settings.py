import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'core.login',
    'core.sale',
    'core.stock',
    'core.report',
    'core.setting',
    'core.purchase',
    'core.money',
    'core.client_current_account',
    # django tweaks
    'widget_tweaks',
    # django afip
    'django_afip',
    # django_filters
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'config.wsgi.application'


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


LANGUAGE_CODE = 'es-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# url que se dirige cuando el login es exitoso
LOGIN_REDIRECT_URL = '/login/dashboard/'

# url que se dirige cuando se hace logout
# No la vamos a usar. De esta manera resuelvo el logout en backends django
# LOGOUT_REDIRECT_URL = '/login/'

# url que se dirige cuando el usuario no esta logeado y se intenta acceder
# a una url distinta del login
LOGIN_URL = '/login/'

# Donde guardará los archivos image y file.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# URL absoluta de los archivos media.
MEDIA_URL = '/media/'

# Configuración según entorno de trabajo
if os.environ.get('PRODUCTION') is None:
    from .local_settings import *
else:
    from .production_settings import *
