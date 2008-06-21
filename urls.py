from django.conf.urls.defaults import *
from fae import views

urlpatterns = patterns(
    '',
    # Default page
    (r'^$', views.index),
    (r'^multi/$', views.index_multi),

    # Report pages
    (r'^report/([0-9a-f]{16})/$', views.report),
    (r'^report/([0-9a-f]{16})/(summary|sitewide|page|menu|urls)/$', views.report),
    (r'^report/([0-9a-f]{16})/(sitewide)/([a-z]+)/$', views.report),
    (r'^report/([0-9a-f]{16})/(page)/(\d+)/$', views.page_report),
    (r'^report/([0-9a-f]{16})/(page)/(\d+)/([a-z]+)/$', views.page_report),

    # Accessibility Extension
    (r'^evaluate/dhtml/$', views.process_dhtml),

    # Direct link to FAE
    (r'^evaluate/link/$', views.process_link),

    # List of page evals for Sitewide Report
    (r'^pgrpteval/$', views.pgrpteval),

    # Report archive
    (r'^reports/archive/$', views.archived_reports),
    (r'^reports/manage/$', views.manage_reports),

    # About FAE
    (r'^about/$', views.about),
    (r'^about/(\w+)/$', views.about),

    # User profile
    (r'^accounts/profile/$', views.my_account),

    # Authentication (The following overrides a mapping in registration.urls)
    (r'^accounts/logout/$', views.logout),

    # Registration app (includes account management)
    (r'^accounts/', include('registration.urls')),

    # Admin
    (r'^admin/', include('django.contrib.admin.urls')),
)
