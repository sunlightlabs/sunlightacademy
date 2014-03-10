from django.template.defaultfilters import slugify
import dj_database_url
import os

PWD = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.environ.get('DEBUG') == 'True'
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jeremy Carbaugh', 'jcarbaugh@sunlightfoundation.com'),
)
MANAGERS = ADMINS

SECRET_KEY = os.environ.get('SECRET_KEY')

if not DEBUG:
    ALLOWED_HOSTS = ['training.sunlightfoundation.com']

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

TIME_ZONE = 'America/New_York'
USE_TZ = True

DATABASES = {'default': dj_database_url.config()}

MEDIA_ROOT = os.path.abspath(os.path.join(PWD, '..', 'media_root'))
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.abspath(os.path.join(PWD, '..', 'static_root'))
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_STORAGE = 'sunlightacademy.backends.BetterS3BotoStorage'
DEFAULT_FILE_STORAGE = 'sunlightacademy.backends.BetterS3BotoStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_name_backends',
)

TEMPLATE_DIRS = (
    os.path.join(PWD, 'templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'sunlightacademy.urls'

WSGI_APPLICATION = 'sunlightacademy.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'gunicorn',
    'markup_deprecated',
    'registration',
    'social_auth',
    'sfapp',
    'south',
    'storages',
    'sunlightacademy',
    'training',
)

# email configuration

EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
DEFAULT_FROM_EMAIL = 'contact@sunlightfoundation.com'

# authentication

AUTH_PROFILE_MODULE = 'training.Profile'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/account/error/'

# registration

ACCOUNT_ACTIVATION_DAYS = 7

# social auth

SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/account/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/account/error/'
SOCIAL_AUTH_ERROR_KEY = 'social_errors'
SOCIAL_AUTH_DEFAULT_USERNAME = lambda u: slugify(u)
SOCIAL_AUTH_EXTRA_DATA = False
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'training.pipeline.account_details',
    'training.pipeline.set_account_details',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'training.pipeline.create_profile',
    'training.pipeline.cleanup',
)

# debug toolbar

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

INTERNAL_IPS = ('127.0.0.1',)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#
# social auth
#

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')

FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_API_SECRET = os.environ.get('FACEBOOK_API_SECRET')

GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')


#
# Postmark
#

POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY')
POSTMARK_SENDER = os.environ.get('POSTMARK_SENDER')


#
# AWS
#

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_LOCATION = os.environ.get('AWS_LOCATION')
