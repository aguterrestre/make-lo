import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-pi=t!i$zqc_a=h2z2u0n@^jhm-wtnm^c$*@2^(qy%+1zst#z!'

# SECURITY WARNING: don't run with debug turned on in production!
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
    # apps
    'core.login',
    'core.sale',
    'core.stock',
    'core.report',
    'core.setting',
    'core.purchase',
    'core.money',
    # django tweaks
    'widget_tweaks',
    # django afip
    'django_afip',
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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'desarrollo',
        # 'NAME': 'make-lobase',
        'USER': 'postgres',
        'PASSWORD': 'SanLore10$$',
        'HOST': '127.0.0.1',
        'DATABASE_PORT': '5432',
    }
}


# Password validation
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


# Internationalization

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Definimos donde estarán los archivos estaticos para servirlos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

# Definimos donde buscará los archivos estaticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# url que se dirige cuando el login es exitoso
LOGIN_REDIRECT_URL = '/login/dashboard/'

# url que se dirige cuando se hace logout
# No la vamos a usar. De esta manera resuelvo el logout en backends django
#  LOGOUT_REDIRECT_URL = '/login/'

# url que se dirige cuando el usuario no esta logeado y se intenta acceder
# a una url distinta del login
LOGIN_URL = '/login/'

# Donde guardará los archivos image y file.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# URL absoluta de los archivos media.
MEDIA_URL = '/media/'
