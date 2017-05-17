from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url, i18n
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

from search import views as search_views
from composerview import views as composer_view
from dealerview import views as dealer_view
from catalogview import views as catalog_view
from placeview import views as place_view
from itemtypeview import views as itemtype_view
from titleview import views as title_view
from recipientview import views as recipient_view
from authorview import views as author_view

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
    url(r'^i18n/', include(i18n)),
]

urlpatterns += i18n_patterns(url(r'^search/$', search_views.search, name='search'),
                             url(r'^advanced_search/', search_views.advanced_search, name="advanced_search"),
                             url('^composerview/(?P<composer_id>[0-9]+)$', composer_view.default, name='composer-browse'),
                             url('^dealerview/(?P<dealer_id>[0-9]+)$', dealer_view.default, name='dealer-view'),
                             url('^catalogview/(?P<catalog_id>[0-9]+)$', catalog_view.default, name='catalog-view'),
                             url('^placeview/(?P<place_id>[0-9]+)$', place_view.default, name='place-view'),
                             url('^itemtypeview/(?P<type_id>[0-9]+)$', itemtype_view.default, name='item-type-view'),
                             url('^titleview/(?P<title_id>[0-9]+)$', title_view.default, name='title_view'),
                             url('^authorview/(?P<author_id>[0-9]+)$', author_view.default, name='author_view'),
                             url('^recipientview/(?P<recipient_id>[0-9]+)$', recipient_view.default, name='recipient_view'),
                             url('^dealerquery/', dealer_view.search_by_keyword, name='dealer-query'),
                             url('^dealerbrowse/', dealer_view.browse, name='dealer-browse'),
                             url(r'', include(wagtail_urls))
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
