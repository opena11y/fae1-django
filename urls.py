from django.conf.urls.defaults import *
from fae.views import index, report, page_report, archived_reports, about, logout

urlpatterns = patterns('',
    # Default page
    (r'^$', index),
    (r'^multi/$', index, {'multi': True}),
    (r'^evaluate/$', index, {'evaluate': True}),

    # Report pages
    (r'^report/([0-9a-f]{16})/$', report),
    (r'^report/([0-9a-f]{16})/(summary|sitewide|page)/$', report),
    (r'^report/([0-9a-f]{16})/(sitewide)/([a-z]+)/$', report),
    (r'^report/([0-9a-f]{16})/(page)/(\d+)/$', page_report),
    (r'^report/([0-9a-f]{16})/(page)/(\d+)/([a-z]+)/$', page_report),

    # Report archive
    (r'^archive/$', archived_reports),

    # About FAE
    (r'^about/$', about),
    (r'^about/(\w+)/$', about),

    # Authentication
    (r'^logout/$', logout),

    # Next mapping expects login.html in templates/registration
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
