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
b'\x03\x9a\x93\xf1\x9c\xeaG\xd0\xff\xdc\xa2\xfb\xe5\x05H\x7f3/rB\t\xbd_\xf7'
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'operacat_dabase'),
    }
}
```

5. run python manage.py migrate
6. run python.manage.py createsuperuser

    - fill in the username 'operacatadmin'
    - enter a password for the user of your choice
    - re-enter the password you chose in the previous step

7. run python manage.py loaddata site_data.json
8. run python manage.py runserver
9. click on the wagtailuserbar icon in the bottom righthand corner of the screen
10. enter the username "opercatadmin" and the password you entered in the creatsuperuser step
11. you should see the admin home page of wagtail site declaring there are 5,445 pages in the site

Core contributors
=================

- Tyler Danstrom <tdanstrom@uchicago.edu> doing backend development
- Kathy Zadrozny <kzadrozny@uchicago.edu> doing frontend development
