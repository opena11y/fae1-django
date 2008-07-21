from django.contrib.sites.models import Site
from project.settings import VERSION

def app(request):
    context = { 'site': Site.objects.get_current(), 'version': VERSION }
    report_info = request.session.get('report', {})
    if report_info:
        context['report'] = report_info
    return context
