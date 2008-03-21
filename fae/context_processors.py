from labels import site_name

def app(request):
    context = { 'site_name': site_name }
    report_info = request.session.get('report', {})
    if report_info:
        context['report'] = report_info
    return context
