This repository was archived on 2024-10-08. The website is no longer active.

Introduction
============

This repo contains the source code for the Operacat website. This is a migration from a php and eXist xml database website to Wagtail and relational database website.

Quickstart Instructions
=======================

1. Install [PostgreSQL](https://www.postgresql.org).
2. Create a development database and user:

```sql
CREATE DATABASE operacat_dev;
CREATE USER operacat WITH PASSWORD '';
GRANT PERMISSIONS ON operacat_dev TO operacat;
```

3. Install [ElasticSearch 6](https://www.elastic.co/products/elasticsearch).
4. Start ElasticSearch:

```console
$ ./bin/elasticsearch
```

5. create and activate a virtual environment for python3.x:

```console
$ python3 -m venv operacat_env
$ cd operacat_env
$ source bin/activate
```

6. git clone https://github.com/uchicago-library/operacat-digital-collection/
7. create file local.py in operacat/operacat/settings/ directory
8. generate a secret key using the Python code below:

```python
import os
os.urandom(24)
b'\x03\x9a\x93\xf1\x9c\xeaG\xd0\xff\xdc\xa2\xfb\xe5\x05H\x7f3/rB\t\xbd_\xf7'
```

9. add the following configuration definition to new local.py file

```
from .base import * 

# secret key configuration value
SECRET_KEY = your_secret_key

# database configuration (add a username and password below)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'NAME': 'operacat_dev',
        'PASSWORD': your_password,
        'PORT': '',
        'USER': 'operacat',
    }
}

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch2',
        'URLS': ['http://localhost:9200'],
        'INDEX': 'wagtail',
        'TIMEOUT': 5,
        'OPTIONS': {},
        'INDEX_SETTINGS': {},
    }
}
```

10. run python manage.py migrate
11. run python.manage.py createsuperuser

    - fill in the username 'operacatadmin'
    - enter a password for the user of your choice
    - re-enter the password you chose in the previous step

12. run python manage.py runserver

Production Deployment Tips
==========================

1. git clone https://github.com/uchicago-library/operacat-digital-collection/ to your production server.
2. verify that elasticsearch >=6 is installed and running on port 9200.
3. verify that postgres is installed and running.
4. create a database named whatever you want (I recommend naming it after the project so "operacat") and assign all privileges over that database to a specific user.
7. add the following to your production server instance local.py file:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'OperaCat <operacat@lib.uchicago.edu>'

ALLOWED_HOSTS = ['your.production.domain.name']
```

8. pip install the appropriate version of elasticsearch to your virtual environment
    - "elasticsearch>=1.0.0,<2.0.0"  # for Elasticsearch 1.x
    - "elasticsearch>=2.0.0,<3.0.0"  # for Elasticsearch 2.x
    - "elasticsearch>=5.0.0,<6.0.0"  # for Elasticsearch 5.x

9.  run python setup.py install inside the opercat-digital-collection directory
10. add the following configuration to your web server. The examples are for Apache but they are probably similar to NGINX or whatever web server your production server is running

```
Alias /static /path/to/static/files/on/your/production/server
Alias /media /path/to/media/files/on/your/production/server

<Directory /path/to/media/files/on/your/production/server>
 Require all granted
</Directory>

<Directory /path/to/static/files/on/your/production/server>
 Require all granted
</Directory>

WSGIScriptAlias / /path/to/wsgi/file/in/your/virtualenv/installation/wsgi.py
WSGIDaemonProcess [unique wsgi domain name] python-path=/path/to/your/operacat/install/directory python-home=/path/to/your/virtualenv/for/operacat user=wsgi group=wsgi threads=15 processes=1 umask=0002
WSGIProcessGroup [unique wsgi process group name]
```

Contributors
=================

- Tyler Danstrom <tdanstrom@uchicago.edu> original backend development
- John Jung <jej@uchicago.edu>
- Kathy Zadrozny <kzadrozny@uchicago.edu> original frontend development
