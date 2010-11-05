# Django settings for webapp project.

import os
import logging

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Begin custom settings
RESOURCES_DEBUG = False
RESULTS_FILE_DEBUG = False
WGET_DEBUG = False

RULESET = '1004-1' # should match wamttest version

try:
    from local_settings import *
except:
    pass

VERSION = '1.1.b1' + VERSION_SUFFIX[PLATFORM]
INSTALLATION = FAE_INSTALL[PLATFORM]
PUBLIC_URL = 'http://fae.cita.illinois.edu/'

TEST_INSTALL = PLATFORM != PRODUCTION
ENABLE_DHTMLGET = TEST_INSTALL
LOGGING = TEST_INSTALL

XML_PATH  = os.path.join(PROJECT_DIR, 'fae/xml')
XSLT_PATH = os.path.join(PROJECT_DIR, 'fae/xslt')

USER_REPORTS_DIR  = os.path.join(FAE_PATH, 'reports/user')
GUEST_REPORTS_DIR = os.path.join(FAE_PATH, 'reports/guest')
SITES_DIR         = os.path.join(FAE_PATH, 'sites')
LOGS_DIR          = os.path.join(FAE_PATH, 'logs')
DOC_ROOT          = os.path.join(FAE_PATH, 'html')

DHTMLGET = os.path.join(FAE_PATH, 'bin/dhtmlget.sh')
WGET = os.path.join(FAE_PATH, 'bin/wget')
WAMT = os.path.join(FAE_PATH, 'bin/wamt')
XSLTPROC = '/usr/bin/xsltproc'

logging.basicConfig(
    level    = logging.DEBUG,
    format   = '%(asctime)s %(levelname)s %(message)s',
    filename = os.path.join(DOC_ROOT, 'logs', 'timing.log')
)

MAX_AGE = 24*60*60*14 # 14 days for cookies
STATS_DAYS_OFFSET = 2 # minimum of 2 days

DEFAULT_QUOTA = 5
ACCT_TYPE_QUOTA = {
    1 : DEFAULT_QUOTA,
    2 : 10,
    3 : 20,
    4 : 50,
    5 : 100
    }

DEFAULT_BUFFER = 5
ACCT_TYPE_BUFFER = {
    1 : DEFAULT_BUFFER,
    2 : DEFAULT_BUFFER,
    3 : 10,
    4 : 10,
    5 : 20
    }

AUDIO_VIDEO_TYPES = u'.aac,.ac3,.avi,.mov,.mp2,.mp3,.mpeg,.mpg,.qt,.wav,.wma'
REJECT_LIST = u'.css,.doc,.ico,.js,.odf,.pdf,.ppt,.xls,' + AUDIO_VIDEO_TYPES
# End custom settings

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = DB_NAME[PLATFORM]
DATABASE_USER = DB_USER[PLATFORM]
DATABASE_PASSWORD = DB_PASSWORD[PLATFORM]
DATABASE_HOST = 'fileserv.dres.illinois.edu'
DATABASE_PORT = ''

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
MEDIA_ROOT = os.path.join(DOC_ROOT, 'media')

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
DEFAULT_FROM_EMAIL = 'do-not-reply@cita.illinois.edu'

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
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
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
