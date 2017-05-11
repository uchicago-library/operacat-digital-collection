
from .base import *

SITE_DIRECTORY = 'data/recitative/sites'

# secret key configuration value
SECRET_KEY = '+!&(+1+5f*lg%^bl_e^ra1efy47ph5=a72)zm8xg0ta4*rkj9c'

# start of database configuration

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'operacat',
        'USER': 'wagtail',
        'PASSWORD': "Kss4DKPtrxTP",
        'HOST': 'localhost'
    }
}

# location to find static files; to change the location of static files modify STATIC_ROOT variable
# location to find media files

MEDIA_ROOT = os.path.join(SITE_DIRECTORY, 'media')

