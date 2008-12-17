# Local settings for Django project installation

import os

# Dynamically determine project path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Installation variables
(DEVELOPMENT, STAGING, PRODUCTION) = tuple(range(3))

# Dynamically determine which installation
if   PROJECT_DIR == '/home/nhoyt/src/project':
    PLATFORM = DEVELOPMENT
    VAR_PATH = '/var/www/faedev'
elif PROJECT_DIR == '/usr/local/faetest/project':
    PLATFORM = STAGING
    VAR_PATH = '/var/www/faetest'
elif PROJECT_DIR == '/usr/local/faedata/project':
    PLATFORM = PRODUCTION
    VAR_PATH = '/var/www/faedata'

DB_NAME =     ('faedev',     'faetest',     'faedata')
DB_USER =     ('faedev',     'faetest',     'faedata')
DB_PASSWORD = ('faeDev2oo8', 'faeTest2oo8', 'faeData2oo8')
