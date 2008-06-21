from django.contrib.sites.models import Site

def app(request):
    context = { 'site': Site.objects.get_current() }
    report_info = request.session.get('report', {})
    if report_info:
        context['report'] = report_info
    return context
