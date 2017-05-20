Introduction
============

This repo contains the source code for the Operacat website. This is a migration from a php and eXist xml database website to Wagtail and relational database website. 

Quickstart Instructions
=======================

1. create a virtual environment for python3.5
2. activate your virtual environment
3. run pip install wagtail
4. git clone https://github.com/uchicago-library/operacat/
5. create file local.py in operacat/operacat/settings/ directory
6. generate a secret key

TIP: to generate a new secret key open a python interpreter shell and run the code below. You can copy the output generated and paste it as the value of your SECRET_KEY variable.

```
$ python
>>> import os
>>> os.urandom(24)
b'\x03\x9a\x93\xf1\x9c\xeaG\xd0\xff\xdc\xa2\xfb\xe5\x05H\x7f3/rB\t\xbd_\xf7'
>> exit()
```

7. add the followiing configuration definition to new local.py file

```
from .base import * 

# secret key configuration value
SECRET_KEY = your_secret_key

# start of database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'operacat_dabase'),
    }
}
```

8. run python manage.py migrate
9. run python.manage.py createsuperuser

    - fill in the username 'operacatadmin'
    - enter a password for the user of your choice
    - re-enter the password you chose in the previous step

TIP: your dev database is a sqlite3 database file in operacat-digital-collection/operacat/operacat/

10. run python manage.py loaddata testdata/site_data.json
11. run python manage.py runserver
12. click on the wagtailuserbar icon in the bottom righthand corner of the screen
13. enter the username "opercatadmin" and the password you entered in the creatsuperuser step
14. you should see the admin home page of wagtail site declaring there are 5,445 pages in the site

Production Deployment Tips
==========================

1. git clone https://github.com/uchicago-library/operacat to your production server
2. verify that elasticsearch is installed and running on port 9200 on your production server
3. verify that postgres is installed and running on your production server
4. create a database named whatever you want (I recommend naming it after the project so "operacat") and assign all privileges over that database to a specific user. Keep note of the username and password with those privileges over the database.
5. check the version of elasticsearch that is running on your production server
6. create a virtual environment on your production server
7. add the following to your production server instance local.py file

```
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
8. change the database definition in your local.py file to the following

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '[name of the database you created in step four]',
        'USER': '[user with all privileges for the database]',
        'PASSWORD': "[password for the user that has all privileges over the database]",
        'HOST': '[your production server, default is localhost'
    }
}
```
9. set ALLOWED_HOSTS in your local.py file
```
ALLOWED_HOSTS = ['your.production.domain.name']
```

10. pip install the appropriate version of elasticsearch to your virtual environment
    - "elasticsearch>=1.0.0,<2.0.0"  # for Elasticsearch 1.x
    - "elasticsearch>=2.0.0,<3.0.0"  # for Elasticsearch 2.x
    - "elasticsearch>=5.0.0,<6.0.0"  # for Elasticsearch 5.x

11.  run python setup.py install inside the opercat-digital-collection directory
12. add the following configuration to your web server. The examples are for Apache but they are probably similar to NGINX or whatever web server your production server is running

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

Core contributors
=================

- Tyler Danstrom <tdanstrom@uchicago.edu> doing backend development
- Kathy Zadrozny <kzadrozny@uchicago.edu> doing frontend development
