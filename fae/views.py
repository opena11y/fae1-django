from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import datetime
from labels import labels, site_name
from forms import BasicEvalForm, DepthEvalForm, MultiEvalForm

#----------------------------------------------------------------
def index(request):
    """
    Serve the appropriate Run FAE page based on the user's login status.
    """
    if request.user.is_authenticated():
        return index_user(request)
    else:
        return index_guest(request)

#----------------------------------------------------------------
def index_user(request):

    # Create response object for saving cookie values
    response = HttpResponse()

    if request.method == 'POST':
        form = DepthEvalForm(request.POST)
        if form.is_valid():
            response.set_cookie('url', form.cleaned_data['url'])
            response.set_cookie('title', form.cleaned_data['title'])
            response.set_cookie('depth', form.cleaned_data['depth'])
            response.set_cookie('span', form.cleaned_data['span'])
            # TODO: save fields to database...
    else:
        init_values = {}
        if 'url' in request.COOKIES:
            init_values['url'] = request.COOKIES['url']
        if 'title' in request.COOKIES:
            init_values['title'] = request.COOKIES['title']
        if 'depth' in request.COOKIES:
            init_values['depth'] = request.COOKIES['depth']
        if 'span' in request.COOKIES:
            init_values['span'] = request.COOKIES['span']
        form = DepthEvalForm(initial=init_values)

    context = {
        'page_type': 'index',
        'title': labels['index'],
        'form': form,
        }

    # Return response
    t = get_template('index_user.html')
    html = t.render(RequestContext(request, context))
    response.write(html)
    return response

#----------------------------------------------------------------
def index_guest(request):

    if request.method == 'POST':
        form = BasicEvalForm(request.POST)
        if form.is_valid(): pass
    else:
        form = BasicEvalForm()

    context = {
        'page_type': 'index',
        'title': labels['index'],
        'form': form,
        }

    # Return response
    t = get_template('index_guest.html')
    html = t.render(RequestContext(request, context))
    return HttpResponse(html)

#----------------------------------------------------------------
@login_required
def index_multi(request):

    # Create response object for saving cookie values
    response = HttpResponse()

    if request.method == 'POST':
        form = MultiEvalForm(request.POST)
        if form.is_valid():
            response.set_cookie('urls', form.clean_data['urls'])
            response.set_cookie('titles', form.clean_data['titles'])
    else:
        init_values = {}
        if 'urls' in request.COOKIES:
            init_values['urls'] = request.COOKIES['urls']
        if 'titles' in request.COOKIES:
            init_values['titles'] = request.COOKIES['titles']
        form = MultiEvalForm(initial=init_values)

    context = {
        'page_type': 'index',
        'title': labels['index'],
        'form': form,
        }

    # Return response
    t = get_template('index_multi.html')
    html = t.render(RequestContext(request, context))
    response.write(html)
    return response

#----------------------------------------------------------------
@login_required
def archived_reports(request):
    """
    Display a list of the user's currently archived reports.
    """
    context = {
        'page_type': 'archive',
        'title': labels['archive'],
        }

    # Return response
    t = get_template('archive.html')
    html = t.render(RequestContext(request, context))
    return HttpResponse(html)

#----------------------------------------------------------------
def page_report(request, rptid, type, pageid=None, section=None):
    """
    Call the report function, but allow a different ordering of arguments.
    """
    return report(request, rptid, type, section, pageid)

#----------------------------------------------------------------
def report(request, rptid, type=None, section=None, pageid=None):
    """
    Serve the requested report, with defaults for type, section and pageid
    when none are specified.
    """
    # Set default values
    default_type = 'summary'
    default_section = 'nav'
    default_pageid = '1'

    # Get latest report parameters if they exist
    report_info = get_report_info(request, rptid)

    if type:
        report_info['type'] = type
    else:
        if not report_info.has_key('type'):
            report_info['type'] = default_type

    if section:
        report_info['section'] = section
    else:
        if not report_info.has_key('section'):
            report_info['section'] = default_section

    if pageid:
        report_info['pageid'] = pageid
    else:
        if not report_info.has_key('pageid'):
            report_info['pageid'] = default_pageid

    # Store report parameters in session variable
    request.session['report'] = report_info

    # Construct the document title
    title = labels['report'][report_info['type']]
    if report_info['type'] == 'page' and report_info['pgcount'] != '1':
        title += ' ' + report_info['pageid']

    if report_info['type'] == 'sitewide' or report_info['type'] == 'page':
        title += ': ' + labels['section'][report_info['section']]

    # Set up context
    context = {
        'page_type': 'report',
        'title': title,
        }
    if report_info['type'] == 'sitewide' or report_info['type'] == 'page':
        context['display_sections'] = True

    # Return response
    t = get_template('report.html')
    html = t.render(RequestContext(request, context))
    return HttpResponse(html)

#----------------------------------------------------------------
def about(request, content_id='overview'):
    title = labels['about'] + ': ' + labels['subtitle'][content_id]
    content = 'about/' + content_id + '.html'

    context = {
        'page_type': 'about',
        'title': title,
        'subtitle': labels['subtitle'],
        'content': content,
        }

    # Return response
    t = get_template('about/about.html')
    html = t.render(RequestContext(request, context))
    return HttpResponse(html)

#----------------------------------------------------------------
def get_report_info(request, rptid):
    """
    Given a report ID:
        IF rptid matches existing report_info
            return existing report_info
        ELSE
            return a new dictionary with new rptid

    Later, when a new report is requested, this function
    will need to get the report metadata from the database.
    """
    # Get latest report parameters if they exist
    report_info = request.session.get('report', {})

    if report_info.has_key('rptid') and report_info['rptid'] == rptid:
        return report_info
    else:
        return { 'rptid': rptid, 'pgcount': '12' }

#----------------------------------------------------------------
def logout(request):
    from django.contrib.auth.views import logout
    return logout(request, next_page='/')
