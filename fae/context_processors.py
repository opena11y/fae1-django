from django.contrib.sites.models import Site
from project.settings import RULESET, VERSION, TEST_INSTALL

def app(request):
    context = {
        'site': Site.objects.get_current(),
        'ruleset': RULESET,
        'version': VERSION,
        'test_install': TEST_INSTALL,
        }
    report_info = request.session.get('report', {})
    if report_info:
        context['report'] = report_info
    return context
