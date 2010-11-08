from django.contrib.sites.models import Site
from project.settings import RULESET, VERSION, ENABLE_DHTMLGET, TEST_INSTALL, CONTACT_EMAIL

def app(request):
    context = {
        'site': Site.objects.get_current(),
        'ruleset': RULESET,
        'version': VERSION,
        'enable_dhtmlget': ENABLE_DHTMLGET,
        'test_install': TEST_INSTALL,
        'contact_email': CONTACT_EMAIL,
        }
    report_info = request.session.get('report', {})
    if report_info:
        context['report'] = report_info
    return context
