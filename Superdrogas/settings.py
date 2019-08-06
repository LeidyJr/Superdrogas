"""
Django settings for Superdrogas project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bl#5bnnaj_vy2ssr)j2o!mov*-ocl$*@jcz9ls!w%xy_flaq$f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.localhost', '127.0.0.1', ]


AUTH_USER_MODEL = 'usuarios.Usuario'

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'Superdrogas.tenant_urls'
PUBLIC_SCHEMA_URLCONF = 'Superdrogas.public_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'Superdrogas.wsgi.application'

#--------------- APPS -----------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]
THIRD_PARTY_APPS = [
    'bootstrap4',
    'django_select2',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]
PUBLIC_APPS = [
    'django_tenants',
    'apps.empresas',
    'apps.usuarios',
    #'apps.logs',
]
LOCAL_APPS = [
    'apps.medicamentos',
    'apps.usuarios',
    'apps.core',
    'apps.grupos',
]

SHARED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PUBLIC_APPS
TENANT_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_MODEL = "empresas.Empresa"
TENANT_DOMAIN_MODEL = "empresas.Dominio"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'superdrogas',
        'USER': 'superdrogas',
        'PASSWORD': 'superdrogas',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',


)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'

SITE_ID = 1

BOOTSTRAP4 = {
    'include_jquery': True,
}

STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)

LOGIN_REDIRECT_URL = 'usuarios:login'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = 'usuarios:login'
LOGOUT_REDIRECT_URL = 'usuarios:login'

DOMAIN = '.localhost'

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') # 'media' is my media folder
MEDIA_URL = '/media/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'thetownofrock@gmail.com'
EMAIL_HOST_PASSWORD = '22082011'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Leidy <thetownofrock@gmail.com>'

ADMINS = (
    ('Leidy', 'rivera.leidy@correounivalle.edu.co'),
    ('Juan', 'tello.juan@correounivalle.edu.co'),
)
MANAGERS = ADMINS

CORREO_CONTACTO = 'rivera.leidy@correounivalle.edu.co' 