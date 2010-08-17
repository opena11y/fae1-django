from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from fae import views, utils
from registration.forms import RegistrationFormUniqueEmail
from registration.views import register

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Default page
    (r'^$', views.index),
    (r'^multi/$', views.index_multi),

    # Debugging
    (r'^sysinfo/$', utils.sysinfo),
    (r'^urltest/$', utils.urltest),

    # Report pages
    (r'^report/([0-9a-f]{16})/$', views.report),
    (r'^report/([0-9a-f]{16})/(summary|sitewide|page|menu|urls|xml)/$', views.report),
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

    # Admin
    (r'^admin/(.*)', admin.site.root),
)

if settings.ALLOW_REGISTRATION:
    urlpatterns += patterns(
        '',
        # Require unique email address by specifying form_class
        (r'^accounts/register/$', register, {'form_class': RegistrationFormUniqueEmail}, 'registration_register'),
    )
else:
    urlpatterns += patterns(
        '',
        # Override register URL in registration.urls
        (r'^accounts/register/$', views.registration_closed),
    )

urlpatterns += patterns(
    '',
    # Override logout URL in registration.urls
    (r'^accounts/logout/$', views.logout),

    # Registration app (includes account management)
    (r'^accounts/', include('registration.urls')),
)
