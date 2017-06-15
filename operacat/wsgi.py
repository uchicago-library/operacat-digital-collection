"""
WSGI config for operacat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

from __future__ import absolute_import, unicode_literals
import os
import sys

sys.path.append("/data/recitative/venvs/operacatENV/lib/python3.5/site-packages")
sys.path.append("/data/recitative/sites/operacat-digital-collection/operacat")

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "operacat.settings.dev")

application = get_wsgi_application()
