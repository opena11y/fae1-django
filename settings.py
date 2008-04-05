# Django settings for webapp project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Custom settings
PROJECT_ROOT = '/home/nhoyt/src/wamt/project/'
XML_PATH = PROJECT_ROOT + 'fae/xml/'
XSLT_PATH = PROJECT_ROOT + 'fae/xslt/'
MAX_AGE = 24*60*60*14 # 14 days for cookies
USER_REPORTS_DIR = '/var/www/fae/reports/user/'
GUEST_REPORTS_DIR = '/var/www/fae/reports/guest/'
SITES_DIR = '/var/www/fae/sites/'
WGET = '/var/www/html/dev/wget'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'faetest'
DATABASE_USER = 'faetest'
DATABASE_PASSWORD = 'sP3Qr74z'
DATABASE_HOST = 'fileserv'
DATABASE_PORT = ''             # Set to empty string for default.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_ROOT + 'media'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Associate FAE's UserProfile model with the User model in the auth middleware
AUTH_PROFILE_MODULE = 'fae.userprofile'

# Registration application settings:
ACCOUNT_ACTIVATION_DAYS = 14
DEFAULT_FROM_EMAIL = 'do-not-reply@cita.uiuc.edu'

# Overrides
LOGIN_REDIRECT_URL = '/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+&x+wo@t$y24bu5k+d+7z1vzkt33wal#-$)onqjp$_5pss4%3v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
#   'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT + 'templates',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'project.fae',
    'registration',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'project.fae.context_processors.app',
)
