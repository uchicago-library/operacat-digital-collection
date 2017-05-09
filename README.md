Introduction
============

This repo contains the source code for the Operacat website. This is a migration from a php and eXist xml database website to Wagtail and relational database website. 

Quickstart Instructions
=======================

1. git clone https://github.com/uchicago-library/operacat/
2. create file locals.py in operacat/operacat/settings/ directory
3. generate a secret key

TIP: to generate a new secret key open a python interpreter shell and run the code below. You can copy the output generated and paste it as the value of your SECRET_KEY variable.

```
$ python
>>> import os
>>> os.urandom(24)
b'\askdlfjaklsdfjlkasdf\'
>> exit()
```

4. add the followiing configuration definition to new locals.py file

```
from .base import * 

PROJECT_DIR = os.path.dirname([absolute_path_to_top_level_repo_directory])
BASE_DIR = os.path.dirname(PROJECT_DIR)

# secret key configuration value
SECRET_KEY = your_secret_key

# start of database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'operacat_dabase'),
    }
}

# location to find static files; to change the location of static files modify STATIC_ROOT variable

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# location to find media files

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# template configuration; to change the location change the path pointed to in DIRS key

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join('/data/recitative/sites', 'templates'),
        ],
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

# start of locales path configuration
LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, "locale"),
)
```

Core contributors
=================

- Tyler Danstrom <tdanstrom@uchicago.edu> doing backend development
- Kathy Zadrozny <kzadrozny@uchicago.edu> doing frontend development
