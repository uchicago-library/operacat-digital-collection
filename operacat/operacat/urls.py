from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url, i18n, static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf.urls.i18n import i18n_patterns
import os

from .settings import base, local

from search import views as search_views
from dealerview import views as dealer_view

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

import registration

urlpatterns = [

    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^comments/', include('django_comments_xtd.urls')),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url('^accounts/', include('registration.backends.simple.urls'), name='register'),
    url('^login/', auth_views.login, name='login'),
    url('^logout/', auth_views.logout, name='logout'),

]

urlpatterns += i18n_patterns(url(r'^search/$', search_views.search, name='search'),
                             url(r'^advanced_search/', search_views.advanced_search, name="advanced_search"),
                             url('^dealerbrowse/', dealer_view.browse, name='dealer-browse'),
                             url(r'^i18n/', include(i18n)),
                             url(r'', include(wagtail_urls))
)

if local.DEBUG:
    print("hi")
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
    urlpatterns += static(base.MEDIA_URL + 'images/', document_root=os.path.join(base.MEDIA_ROOT, 'images'))
    urlpatterns += [
        url(r'^favicon\.ico$', RedirectView.as_view(url=base.STATIC_URL + 'myapp/images/favicon.ico'))
    ]

print(base.STATIC_ROOT)
print(urlpatterns)
