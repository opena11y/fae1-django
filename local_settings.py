# Local settings for Django project installation

import os

# Dynamically determine project path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Installation variables
(DEVELOPMENT, STAGING, PRODUCTION) = tuple(range(3))

# Dynamically determine which installation
if   PROJECT_DIR == '/home/nhoyt/src/project':
    PLATFORM = DEVELOPMENT
    FAE_PATH = '/services/faedev'
elif PROJECT_DIR == '/services/faetest/lib/project':
    PLATFORM = STAGING
    FAE_PATH = '/services/faetest'
elif PROJECT_DIR == '/services/faedata/lib/project':
    PLATFORM = PRODUCTION
    FAE_PATH = '/services/faedata'

DB_NAME =     ('faedev',     'faetest',     'faedata')
DB_USER =     ('faedev',     'faetest',     'faedata')
DB_PASSWORD = ('faeDev2oo8', 'faeTest2oo8', 'faeData2oo8')
