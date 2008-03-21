from django.conf.urls.defaults import *
from fae import views

urlpatterns = patterns('',
    # Default page
    (r'^$', views.index),
    (r'^multi/$', views.index_multi),

    # Report pages
    (r'^report/([0-9a-f]{16})/$', views.report),
    (r'^report/([0-9a-f]{16})/(summary|sitewide|page)/$', views.report),
    (r'^report/([0-9a-f]{16})/(sitewide)/([a-z]+)/$', views.report),
    (r'^report/([0-9a-f]{16})/(page)/(\d+)/$', views.page_report),
    (r'^report/([0-9a-f]{16})/(page)/(\d+)/([a-z]+)/$', views.page_report),

    # Report archive
    (r'^archive/$', views.archived_reports),

    # About FAE
    (r'^about/$', views.about),
    (r'^about/(\w+)/$', views.about),

    # Authentication (The following overrides a mapping in registration.urls)
    (r'^accounts/logout/$', views.logout),

    # Registration app (includes account management)
    (r'^accounts/', include('registration.urls')),

    # Profiles app
    (r'^profiles/', include('profiles.urls')),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
