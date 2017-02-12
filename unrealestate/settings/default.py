import os

gettext = lambda s: s

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'SPECIFY_IN_LOCAL_PY'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['demo.unrealestate.sg']

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'haystack',
    'unrealestate',
    'allauth',
    'allauth.account',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount',
    'compressor',
    'sorl.thumbnail',
    'ckeditor',
    'ckeditor_uploader',
    'django_comments',
    'django_comments_xtd',
    'django_countries',
    'phonenumber_field',
    'localflavor',
    'django_cleanup',
    'django_extensions',
    'rest_framework',
    'djmoney',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'unrealestate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'unrealestate.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

ACCOUNT_SIGNUP_FORM_CLASS = 'unrealestate.forms.SignupForm'

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', gettext('English')),
)

# TODO: Not a good topic to spend hours on (adding, subtracting, comparing, auto-conversion)
# CURRENCIES = ['SGD', 'USD', 'CNY', 'EUR']
CURRENCIES = ['SGD']

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_ROOT = 'static-cache'

COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.rCSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']

CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 1
COMMENTS_XTD_CONFIRM_EMAIL = False

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = '587'
# EMAIL_HOST_USER = 'laurileet@gmail.com'
# EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'Unreal Estate Demo <info@demo.unrealestate.sg>'

AUTH_USER_MODEL = 'unrealestate.User'

SAMPLE_PROJECTS_ON_HOME_PAGE = 3

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), '../whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

SOCIALACCOUNT_QUERY_EMAIL = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

ADMINS = [
    ('Karl Vään', 'vaankarl@gmail.com'),
    ('Taavi Pettai', 'pettaitaavi@gmail.com'),
    ('Timo Kaus', 'timo.kaus@gmail.com'),
    ('Lauri Elias', 'laurileet@gmail.com')
]

# DJMONEY_AUTO_CONVERT_MONEY = True

# Security hardening
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
#SECURE_HSTS_SECONDS = 3600
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# DJANGO_MONEY_RATES = {
#     'DEFAULT_BACKEND': 'djmoney_rates.backends.OpenExchangeBackend',
#     'OPENEXCHANGE_URL': 'http://openexchangerates.org/api/latest.json',
#     'OPENEXCHANGE_APP_ID': '92a222f841cb42c3b373394db8dfba4f',
#     'OPENEXCHANGE_BASE_CURRENCY': 'EUR',
# }

COMMENTS_XTD_FORM_CLASS = 'unrealestate.forms.MyCommentForm'
