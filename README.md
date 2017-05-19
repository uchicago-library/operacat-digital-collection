Introduction
============

This repo contains the source code for the Operacat website. This is a migration from a php and eXist xml database website to Wagtail and relational database website. 

Quickstart Instructions
=======================

1. git clone https://github.com/uchicago-library/operacat/
2. create file local.py in operacat/operacat/settings/ directory
3. generate a secret key

TIP: to generate a new secret key open a python interpreter shell and run the code below. You can copy the output generated and paste it as the value of your SECRET_KEY variable.

```
$ python
>>> import os
>>> os.urandom(24)
b'\askdlfjaklsdfjlkasdf\'
>> exit()
```

4. add the followiing configuration definition to new local.py file

```
from .base import * 

# secret key configuration value
SECRET_KEY = your_secret_key

# start of database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'operacat_dabase'),
    }
}
```

Core contributors
=================

- Tyler Danstrom <tdanstrom@uchicago.edu> doing backend development
- Kathy Zadrozny <kzadrozny@uchicago.edu> doing frontend development
